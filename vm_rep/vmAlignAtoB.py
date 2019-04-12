import numpy as np

def vmAlignAtoB(Ax, Bx):
    #print("vmalignAtoB")
   
    acorb = np.convolve(Ax, Bx[::-1])
    maxval = np.max(acorb)
    maxind=maxval
    shiftamp = Bx.shape[0] - maxind
    
    Axout = np.roll(Ax , int(shiftamp) , axis=0)
    return [Axout, shiftamp] 