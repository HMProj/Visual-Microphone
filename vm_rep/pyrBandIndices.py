import warnings as w
import numpy as np
def pyrBandIndices(pind, band):
    #print("pyrbandindices")
    if (band  > pind.shape[0] or (band < 0)):
        w.warn("Band no should be > 1 and no of pyrbands")
    if (pind.shape[1] != 2) :
        w.warn("Indices must be an n/2 MATRIX")
    ind = 1 
    for l in range(0,band):
        ind = ind + np.prod(pind[l])
    indices = np.array(range(int(ind),int(ind + np.prod(pind[band]))))            
    return indices