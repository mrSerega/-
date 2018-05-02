import numpy as np

uiMAX_REG_X = 16;	  #/* max. amount contextual regions in x-direction */
uiMAX_REG_Y = 16;	  #/* max. amount contextual regions in y-direction */

def clh(
    pImage,
    uiXRes,
    uiYRes,
    Min,
    Max,
    uiNrX,
    uiNrY,
    uiNrBins,
    fClipLimit,
    ):

    # unsigned int      uiX, uiY;		                        /* counters */
    # unsigned int      uiXSize, uiYSize, uiSubX, uiSubY;       /* size of context. reg. and subimages */
    # unsigned int      uiXL, uiXR, uiYU, uiYB;                 /* auxiliary variables interpolation routine */
    # unsigned long     ulClipLimit, ulNrPixels;                /* clip limit and region pixel count */
    # kz_pixel_t*       pImPointer;		                        /* pointer to image */
    # kz_pixel_t        aLUT[uiNR_OF_GREY];	                    /* lookup table used for scaling of input image */
    # unsigned long*    pulHist, *pulMapArray;                  /* pointer to histogram and mappings*/
    # unsigned long*    pulLU, *pulLB, *pulRU, *pulRB;          /* auxiliary pointers interpolation */

    if uiNrX > uiMAX_REG_X: return -1	    # amount of regions x-direction too large
    if uiNrY > uiMAX_REG_Y: return -2	    # amount of regions y-direction too large
    if uiXRes % uiNrX: return -3	        # x-resolution no multiple of uiNrX
    if uiYRes % uiNrY: return -4	        # y-resolution no multiple of uiNrY 
    if Max >= uiNR_OF_GREY: return -5	    # maximum too large 
    if Min >= Max: return -6		        # minimum equal or larger than maximum 
    if uiNrX < 2 or uiNrY < 2: return -7    # at least 4 contextual regions required 
    if fCliplimit == 1.0: return 0	        # is OK, immediately returns original image. 
    if uiNrBins == 0: uiNrBins = 128	    # default value when not specified

    pulMapArray = np.zeros(uiNrX*uiNrY*uiNrBins)
    # if (pulMapArray == 0) return -8;	  /* Not enough memory! (try reducing uiNrBins) */ 

    uiXSize = uiXRes / uiNrX
    uiYSize = uiYRes / uiNrY                # Actual size of contextual regions
    ulNrPixels = uiXSize * uiYSize

    if fCliplimit > 0.0: 		            # Calculate actual cliplimit
        ulClipLimit = fCliplimit * (uiXSize * uiYSize) / uiNrBins
        ulClipLimit = 1 if ulClipLimit < 1 else ulClipLimit
    else: 
        ulClipLimit = 2**14;		        # Large value, do not clip (AHE)
    aLUT = MakeLut(Min, Max, uiNrBins);	    # Make lookup table for mapping of greyvalues

    # Calculate greylevel mappings for each contextual region
    for (uiY = 0, pImPointer = pImage; uiY < uiNrY; uiY++) {
	for (uiX = 0; uiX < uiNrX; uiX++, pImPointer += uiXSize) {
	    pulHist = &pulMapArray[uiNrBins * (uiY * uiNrX + uiX)];
	    MakeHistogram(pImPointer,uiXRes,uiXSize,uiYSize,pulHist,uiNrBins,aLUT);
	    ClipHistogram(pulHist, uiNrBins, ulClipLimit);
	    MapHistogram(pulHist, Min, Max, uiNrBins, ulNrPixels);
	}
	pImPointer += (uiYSize - 1) * uiXRes;		  /* skip lines, set pointer */
    }

    # To speed up histogram clipping, the input image [Min,Max] is scaled down to
    # [0,uiNrBins-1]. This function calculates the LUT.
    def MakeLut (pLUT, Min, Max, uiNrBins):
        BinSize = 1 + (Max - Min) / uiNrBins
        for i in range (Min,Max+1): pLUT.append( (i - Min) / BinSize )
        return pLUT

    def ClipHistogram (
        pulHistogram,
        int
		uiNrGreylevels,
        ulClipLimit):
# /* This function performs clipping of the histogram and redistribution of bins.
#  * The histogram is clipped and the number of excess pixels is counted. Afterwards
#  * the excess pixels are equally redistributed across the whole histogram (providing
#  * the bin count is smaller than the cliplimit).
#  */
    pulBinPointer, *pulEndPointer, *pulHisto
    ulNrExcess, ulUpper, ulBinIncr, ulStepSize, i
    lBinExcess

    ulNrExcess = 0;  pulBinPointer = pulHistogram
    for (i = 0; i < uiNrGreylevels; i++) { /* calculate total number of excess pixels */
	lBinExcess = (long) pulBinPointer[i] - (long) ulClipLimit;
	if (lBinExcess > 0) ulNrExcess += lBinExcess;	  /* excess in current bin */
    };

    /* Second part: clip histogram and redistribute excess pixels in each bin */
    ulBinIncr = ulNrExcess / uiNrGreylevels;		  /* average binincrement */
    ulUpper =  ulClipLimit - ulBinIncr;	 /* Bins larger than ulUpper set to cliplimit */

    for (i = 0; i < uiNrGreylevels; i++) {
      if (pulHistogram[i] > ulClipLimit) pulHistogram[i] = ulClipLimit; /* clip bin */
      else {
	  if (pulHistogram[i] > ulUpper) {		/* high bin count */
	      ulNrExcess -= pulHistogram[i] - ulUpper; pulHistogram[i]=ulClipLimit;
	  }
	  else {					/* low bin count */
	      ulNrExcess -= ulBinIncr; pulHistogram[i] += ulBinIncr;
	  }
       }
    }

    while (ulNrExcess) {   /* Redistribute remaining excess  */
	pulEndPointer = &pulHistogram[uiNrGreylevels]; pulHisto = pulHistogram;

	while (ulNrExcess && pulHisto < pulEndPointer) {
	    ulStepSize = uiNrGreylevels / ulNrExcess;
	    if (ulStepSize < 1) ulStepSize = 1;		  /* stepsize at least 1 */
	    for (pulBinPointer=pulHisto; pulBinPointer < pulEndPointer && ulNrExcess;
		 pulBinPointer += ulStepSize) {
		if (*pulBinPointer < ulClipLimit) {
		    (*pulBinPointer)++;	 ulNrExcess--;	  /* reduce excess */
		}
	    }
	    pulHisto++;		  /* restart redistributing on other bin location */
	}
    }
}