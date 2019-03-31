import cv2
import numpy as np
import datetime
import math
import scipy.signal as sp
import BuildSCFPyramid as bsp
import pyrBand as pb
import vmAlignAtoB as atb

def VmSoundFromVideo(cap,nscales,norients,samplingrate,dsamplefactor):
    
    #check if sampling rate is provided as input
    if samplingrate < 0:
        samplingrate=cap.get(cv2.cv.CV_CAP_PROP_FPS)

    nF = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    #read the first frame from the video
    firstFrame=cap.read()    
    #check whether to down sample or not
    firstframe = firstFrame[1]
    print("first frame shape:",firstframe.shape)
    firstframe = firstframe.astype('float32')

    
    #get the colour planes to calculate average across them
    BluePlane = firstframe[:,:,0]
    GreenPlane =firstframe[:,:,1]
    RedPlane =firstframe[:,:,2]

    
    
    if dsamplefactor !=1:
        dim = BluePlane.shape
        d1,d2=int((dim[0]*dsamplefactor)/2),int(dim[1]*dsamplefactor)
        BluePlane = np.resize(BluePlane,(d1,d2))
        GreenPlane = np.resize(GreenPlane,(d1,d2))
        RedPlane = np.resize(RedPlane,(d1,d2))
        dim=RedPlane.shape    
    

    # average calculation
    fullframe = (BluePlane+GreenPlane+RedPlane)/3
    print("fullframe shape:",fullframe.shape)
    arr = fullframe[0:10,0:10]
    print(arr)
    #construct Complex Steerable Pyramid
    [PyrRef, Pind, steerMatrix, harmonics] = bsp.BuildSCFPyr(fullframe,nscales,norients-1)


    
    totalSigns = nscales * norients #2
    signalFFS = np.zeros((nF, nscales, norients))
    ampsigs = np.zeros((nF, nscales, norients))

    for i in range(1,nF+1):
        print("loop",i)
        if (i % math.floor(nF/100)) ==1 :
            progress = i /nF
            currentTime = datetime.datetime.now() 
            print("Progress: ", (progress*100), " done after " ,str(currentTime))    
        if i==1:
            frame = firstFrame
        else:
            frame = cap.read()
        

        if frame[0]==True:
            frame=frame[1]
            frame = frame.astype('float32')    
            BluePlane = frame[:,:,0]
            GreenPlane = frame[:,:,1]
            RedPlane = frame[:,:,2]

            if dsamplefactor !=1:
                dim = BluePlane.shape
                d1,d2=int((dim[0]*dsamplefactor)/2),int(dim[1]*dsamplefactor)
                BluePlane = np.resize(BluePlane,(d1,d2))
                GreenPlane = np.resize(GreenPlane,(d1,d2))
                RedPlane = np.resize(RedPlane,(d1,d2))
                dim=RedPlane.shape    
                

            # average calculation
            fullframe = (BluePlane+GreenPlane+RedPlane)/3
            
            #normalizing the fullframe
            #fullframe = fullframe /np.max(fullframe)

            [pyr, pind, steermtx, harmo]  =  bsp.BuildSCFPyr(fullframe, nscales, norients-1)
            pyramp = abs(pyr)
            pyrDeltaPhase = ((math.pi + np.angle(pyr) - np.angle(PyrRef)) % (2 * math.pi)) - math.pi
            #print("pyrD",pyrDeltaPhase)
            for j in range(0,nscales):
                bandIdx = 1 + (j)*norients + 1 #2
                curH = Pind[bandIdx-1][0]
                curW = Pind[bandIdx-1][1]
                for k in range(0,norients):  
                    bandIdx = 1 + j * norients + k
                    amp = pb.pyrBand(pyramp, Pind, bandIdx)
                    #print(amp.shape,"amp")
                    phase = pb.pyrBand(pyrDeltaPhase, Pind, bandIdx)
                    #print("phase shape",phase.shape)
                    #print("pind.shape",Pind.shape)
                    phasew = phase * np.power(abs(amp), 2)
                    #print(phase.shape,"phase")
                    sumamp = np.sum(abs(amp))
                    ampsigs[i-1][j][k] = sumamp
                    signalFFS[i-1][j][k] = np.mean(phasew)/sumamp
        else:
            break    
    S_samplingrate = samplingrate

    sigOut = np.zeros((1, nF))

    for q in range(0, nscales):
        for p in range(0, norients):
            [sigaligned, shiftamp] = atb.vmAlignAtoB(np.squeeze(signalFFS[:, q, p]), np.squeeze(signalFFS[:, 0, 0]))
            #print("shape1 and shape2",sigaligned.shape,sigOut.shape)
            sigOut = sigOut + sigaligned

    S_aligned = sigOut
    #print("S_aligned:\n",S_aligned)
    S_averageNoAlignment = np.transpose(np.mean(np.reshape(np.ndarray.astype(signalFFS,float), (nscales * norients, nF)),axis=0))
    highpassfc = 0.05
    [b, a] = sp.butter(3, highpassfc, 'high', output='ba')
    S_x = sp.lfilter(b, a, S_aligned, axis = 0)
    #print(S_x.shape,"S_X shape")
    S_x[0:10] = np.mean(S_x,axis=0)
    #print("s_x:\n",S_x)

    maxSx = np.max(S_x)
    minSx = np.min(S_x)
    #print("max and minsx:",maxSx,minSx)
    if (maxSx !=1.0 or minSx != -1.0):
        range_x = maxSx - minSx
        if (range_x !=0 ):
            S_x = 2 * S_x / range_x
        newmx = np.max(S_x)
        offset = newmx - 1.0
        S_x = S_x - offset

    return [S_samplingrate, S_aligned, S_averageNoAlignment, S_x]