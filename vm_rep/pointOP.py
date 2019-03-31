import numpy as np
import scipy.interpolate as si

def pointOP(im, lut, origin, increament,warnings):
    #print("pointop")
    X = origin + increament*(np.array(range(0,len(lut))))
    Y = lut
    #print("X,Y: ",X.shape,Y.shape)
    intP = si.interp1d(X, Y, bounds_error=False, fill_value='extrapolate')
    interp_vals = intP(im) 
    #print("shapes: ",interp_vals.shape,im.shape)
    return interp_vals