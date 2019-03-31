import numpy as np
import math 
import warnings
import SteerToHarmMtx as sth
import rcosFn as rcf
import pointOP as p0p
import buildSCFPyrLevs as bspl


def BuildSCFPyr(frame,nscales,norients):
    #print("build scf")
    # 1] -------Checking and intializing the variables--------

    #calculate max height for the pyramid construction
    max_ht = math.floor(math.log2(min(frame.shape)))-2
    
    #check and initialize scales
    if nscales > max_ht:
        warnings.warn("Scales greater then max possible height!!\n>>'scales reinitialized to max height'<<")
        nscales =max_ht

    #check and initialize orientations
    if (norients < 0 or norients > 15):
        warnings.warn("Orientation not in range [0 ,15] \n >>'orientations reinitialized to value in this range'<<")
        norients =min(max(norients,0),15)
    else:
        norients =int(norients)        
    
    
    nbands=norients+1 #2   

    twidth=1

    # 2] ---------Steering Stuff---------------

    #calculate harmonics for the pyramid
    if nbands%2 == 0:
        harmonics = (np.array(range(0,int(nbands/2)))*2+1) #-->[1]
        
    else:
        harmonics = (np.array(range(0,int((nbands-1)/2)))*2)
        
    #print("harmonics:",harmonics)    
    

    print("haronics: ",harmonics)
    #calculate the angle
    angles = (math.pi*(np.array(range(0,(nbands)))))/nbands #[0]
    print("angles:",angles)
    #get steer Matrix 
    SteerMatrix = sth.SteerToHarmonicMatrix(harmonics, angles,'even') #[[1],[0]]
    print("steer mat:",SteerMatrix)
#---------------------------------------------------

    #get dimensions of frame
    r,c =frame.shape #40,70
    
    #calculate the center point of frame
    ctr_r=math.ceil(((r+0.5)/2)) #21
    ctr_c=math.ceil(((c+0.5)/2)) #36



    x = ((np.array(range(1,c+1)))-ctr_c)/(c/2)
    y = ((np.array(range(1,r+1)))-ctr_r)/(r/2)

    #calculate a meshgrid of x and y
    [xramp, yramp]=np.meshgrid(x,y)
    
    #get the angles using each point in input matrices
    angle = np.arctan2(yramp,xramp)
    log_rad = np.sqrt(np.square(xramp)+np.square(yramp))
    log_rad[ctr_r-1][ctr_c-1]=log_rad[ctr_r-1][ctr_c-2]
    log_rad=np.log2(log_rad)
    [xrcos,yrcos] =rcf.rcosFn(twidth,(-twidth/2),[0,1])  #259 size
    yrcos = np.sqrt(yrcos)
    YIrcos = np.sqrt(1.0-np.square(yrcos))

    lo0mask = p0p.pointOP(log_rad, YIrcos, xrcos[0], xrcos[1]-xrcos[0], 0)
    imdft = np.fft.fftshift(np.fft.fft2(frame))
    lo0dft = imdft * lo0mask 
    #print("Shapes>>",lo0dft.shape,imdft.shape)
    print(nscales,"nscales")
    [pyr, pind] = bspl.buildSCFPyrLevs(lo0dft, log_rad, xrcos, yrcos, angle, nscales, nbands)
    
    print(pind.shape,"pind.shape")

    #for i in pyr:
     #   print(i.shape)
    
    hi0mask = p0p.pointOP(log_rad, yrcos, xrcos[0], xrcos[1]-xrcos[0], 0)
    hi0dft = imdft * hi0mask
    hi0 = np.fft.ifft2(np.fft.ifftshift(hi0dft))
    pyr = np.append((np.real(hi0)).flatten(),pyr)
    pind = np.vstack((hi0.shape, pind))

    return [pyr, pind, SteerMatrix, harmonics]
