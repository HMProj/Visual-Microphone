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
      
    firstframe = firstframe.astype('float32')
    
    if dsamplefactor !=1:
        dim = firstframe.shape
        d1,d2=int((dim[0]*dsamplefactor)/2),int(dim[1]*dsamplefactor)
        firstframe = cv2.resize(firstframe,(d2,d1),interpolation=cv2.INTER_AREA)
        #BluePlane = cv2.resize(BluePlane,(d1,d2),interpolation=cv2.INTER_AREA)
        #GreenPlane = cv2.resize(GreenPlane,(d1,d2),interpolation=cv2.INTER_AREA)
        #RedPlane = cv2.resize(RedPlane,(d1,d2),interpolation=cv2.INTER_AREA)
        #dim=firstframe.shape    
    
    firstframe = cv2.cvtColor(firstframe, cv2.COLOR_BGR2GRAY)
    #get the colour planes to calculate average across them
    '''BluePlane = firstframe[:,:,0]
    GreenPlane =firstframe[:,:,1]
    RedPlane =firstframe[:,:,2]

    
    # average calculation
    fullframe = (BluePlane+GreenPlane+RedPlane)/3
    '''
    
    #construct Complex Steerable Pyramid
    [PyrRef, Pind, steerMatrix, harmonics] = bsp.BuildSCFPyr(firstframe,nscales,norients-1)

    totalSigns = nscales * norients #2
    signalFFS = np.zeros((nF, nscales, norients))
    ampsigs = np.zeros((nF, nscales, norients))

    for i in range(1,nF+1):
        print("------------------------------------------------loop ",i," ------------------------------------------------------")
        if (i % math.floor(nF/100)) ==1 :
            progress = i /nF
            currentTime = datetime.datetime.now() 
            print("Progress: ", (progress*100), " done after " ,str(currentTime))    
        frame = cap.read()
              

        if frame[0] == True:
            frame=frame[1]
                
            
            if dsamplefactor !=1:
                dim = frame.shape
                d1,d2=int((dim[0]*dsamplefactor)/2),int(dim[1]*dsamplefactor)
                frame = cv2.resize(frame,(d2,d1),interpolation=cv2.INTER_AREA)
                
                '''dim = BluePlane.shape
                d1,d2=int((dim[0]*dsamplefactor)/2),int(dim[1]*dsamplefactor)
                BluePlane =cv2.resize(BluePlane,(d1,d2),interpolation=cv2.INTER_AREA)
                GreenPlane = cv2.resize(GreenPlane,(d1,d2),interpolation=cv2.INTER_AREA)
                RedPlane = cv2.resize(RedPlane,(d1,d2),interpolation=cv2.INTER_AREA)
                dim=RedPlane.shape    
                
            BluePlane = frame[:,:,0]
            GreenPlane = frame[:,:,1]
            RedPlane = frame[:,:,2]

            # average calculation
            fullframe = (BluePlane+GreenPlane+RedPlane)/3
            
            #normalizing the fullframe
            #fullframe = fullframe /np.max(fullframe)
            '''
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = frame.astype('float32')
            [pyr, pind, steermtx, harmo]  =  bsp.BuildSCFPyr(frame, nscales, norients-1)

            pyramp = abs(pyr)
            '''
            print("Refpyr:")
            ans = PyrRef[99:120]
            for x in ans.transpose():
                print(x)
            

            
            print("pyr:")
            ans=pyr[99:120]
            for x in ans.transpose():
                print(x)
            
            ans = (math.pi + np.angle(pyr) - np.angle(PyrRef))
            
            print("Diff:")
            ans = pyr[99:120]
            ans2 = PyrRef[99:120]
            for x in range(0,20):
                print(ans2[x]-ans[x])
                
            
            pyrDeltaPhase = ((math.pi + np.angle(pyr) - np.angle(PyrRef)) % (2 * math.pi)) - math.pi
            i=1
            print("----------------------------------------------------------------") #--> diff 
            for x in pyrDeltaPhase.transpose():
                print(i,":",x)
                i+=1
            '''
            pyrDeltaPhase = ((math.pi + np.angle(pyr) - np.angle(PyrRef)) % (2 * math.pi)) - math.pi
            for j in range(0,nscales):
                bandIdx = 1 + (j)*norients + 1 #2
                curH = Pind[bandIdx-1][0] 
                curW = Pind[bandIdx-1][1]
                for k in range(0,norients):  
                    bandIdx = 1 + j * norients + k
                    amp = pb.pyrBand(pyramp, Pind, bandIdx)
                    phase = pb.pyrBand(pyrDeltaPhase, Pind, bandIdx)
                    phasew = phase * np.power(abs(amp), 2)
                    sumamp = np.sum(abs(amp))
                    ampsigs[i-1][j][k] = sumamp
                    signalFFS[i-1][j][k] = np.mean(phasew)/sumamp
                #    print("signal ffs",signalFFS[i-1][j][k])
            ''' print("pyrdelta")
            for x in pyrDeltaPhase.transpose():
                print(x)
            print("curH",curH)
            print("curW",curW)
            print("amp")
            for x in amp.transpose():
                print(x)
            print("phase")
            for x in phase.transpose():
                print(x)
            print("phasew")
            for x in phasew.transpose():
                print(x)
            print("sumamp:",sumamp)
            '''
            
            #print("ampsigs",ampsigs[i-1][j][k])
            #print("signalffs",signalFFS[i-1][j][k])
            
   


        else:
            break    
    S_samplingrate = samplingrate

    sigOut = np.zeros((1, nF))

    for q in range(0, nscales):
        for p in range(0, norients):
            [sigaligned, shiftamp] = atb.vmAlignAtoB(np.squeeze(signalFFS[:, q, p]), np.squeeze(signalFFS[:, 0, 0]))
            sigOut = sigOut + sigaligned

    S_aligned = sigOut
    S_averageNoAlignment = np.transpose(np.mean(np.reshape(np.ndarray.astype(signalFFS,float), (nscales * norients, nF)),axis=0))
    highpassfc = 0.05
    [b, a] = sp.butter(3, highpassfc, 'high', output='ba')
    S_x = sp.lfilter(b, a, S_aligned, axis = 0)
    S_x[0:10] = np.mean(S_x,axis=0)
    
    maxSx = np.max(S_x)
    minSx = np.min(S_x)
    if (maxSx !=1.0 or minSx != -1.0):
        range_x = maxSx - minSx
        if (range_x !=0 ):
            S_x = 2 * S_x / range_x
        newmx = np.max(S_x)
        offset = newmx - 1.0
        S_x = S_x - offset

    return [S_samplingrate, S_aligned, S_averageNoAlignment, S_x]