import numpy as np
import scipy.interpolate as si

def pointOP(im, lut, origin, increament,warnings):
    X = origin + increament*(np.array(range(0,len(lut))))
    Y = lut

    im2 = im.transpose()
    im2 = im2.flatten()   
    
    intP = si.interp1d(X, Y, bounds_error=False, fill_value='extrapolate')
    interp_vals = intP(im2)

    interp_vals = np.reshape(interp_vals,(im.shape[1],im.shape[0]))
    interp_vals = interp_vals.transpose()
       

    return interp_vals