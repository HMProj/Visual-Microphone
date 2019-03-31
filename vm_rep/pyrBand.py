import numpy as np
import pyrBandIndices as pbi

def pyrBand(pyr, pind, band):
    #print("pyr band")
    ind = pbi.pyrBandIndices(pind, band)
    pyrI = [pyr[i-1] for i in ind]
    res = np.transpose(np.reshape(pyrI,(int(pind[band][1]), int(pind[band][0]))))
    return res