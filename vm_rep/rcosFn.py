import math
import numpy as np

def rcosFn(width,position,values):
    sz = 256
    X = math.pi*(np.array(range(-sz-1 ,2)))/(2*sz)
    
    Y = values[0]+(values[1]-values[0]) * np.square(np.cos(X))
    Y[0] = Y[1]
    
    Y[sz+2] = Y[sz+1]
    
    X = position + (2*width/math.pi) * (X+math.pi/4)
    return [X,Y]; 