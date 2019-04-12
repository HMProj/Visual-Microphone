import numpy as np
import math
import warnings as w

def SteerToHarmonicMatrix(harmonics, angles, evenorodd):
    
    # print("steer to harm matrx")
    #calculate number of harmonics for the pyramid
    numh = len(harmonics)*2 - int(0 in harmonics) #2
    
    #check even or odd 
    if evenorodd == 'even':
        setval=0 #-->
    else:
        setval=1    

    #create an inverse matrix that maps Fourier Components onto steerable basis
    

    inmtx=np.zeros((numh,len(angles)),int)
    col=0
    for h in harmonics:
        args=h*angles   #[0]
        if h==0:
            inmtx[col] =np.ones(len(angles))
            col+=1
        elif setval:
            inmtx[col] =np.array([math.sin(x) for x in args])
            inmtx[col+1] =(np.array([math.cos(x) for x in args]))*-1
            col+=2
        else: #-->
            inmtx[col] =np.array([math.cos(x) for x in args]) #1
            inmtx[col+1] =(np.array([math.sin(x) for x in args])) #0
 
            col+=2
    inmtx = np.transpose(inmtx)
    r = np.linalg.matrix_rank(inmtx) #1

    if r != numh and r != len(angles):
        w.warn("Matrix is not full rank")
    
    # convert inverse matix to matrix
    mtx = np.linalg.pinv(inmtx) #[[1],[0]]
    return mtx    