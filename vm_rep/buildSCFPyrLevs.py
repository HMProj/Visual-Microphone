import numpy as np
import math
import pointOP as p0p

def buildSCFPyrLevs(lodft, log_rad, xrcos, yrcos, angle, ht, nbands):
    if ht <= 0:
        lo0 = np.fft.ifft2((np.fft.ifftshift(lodft)))
        pyr = np.real((lo0.transpose()).flatten())
        pind = lo0.shape
    
        return [pyr,pind]

    else: 
        bands = np.zeros((lodft.shape[0]*lodft.shape[1] , nbands)) #1400,2
        bands = bands.astype(complex)
        bind = np.zeros((nbands, 2)) #2,2
        xrcos = xrcos - math.log2(2)
        lutsize = 1024
        xcosn = (math.pi * np.array(range(-(2*lutsize+1), (lutsize+2))))/lutsize #3075 size
        order = nbands-1 #1
        
        const = math.pow(2*order,2) * math.pow(math.factorial(order),2) / (nbands*math.factorial(2*order)) #1
        alpha =np.mod(math.pi + xcosn,2*math.pi) - math.pi
        ycosn = 2 * math.sqrt(const) * np.power(np.cos(xcosn),order) * np.ndarray.astype((abs(alpha) < math.pi/2),int)   

        himask = p0p.pointOP(log_rad, yrcos, xrcos[0], xrcos[1]-xrcos[0], 0)
        bands = np.transpose(bands) #2,1400
        '''
        print("-----------------------------before---------------------------------")
        print("log_rad")
        for x in log_rad.transpose():
            print(x)

        print("xrcos")
        for x in xrcos.transpose():
            print(x)

        print("yrcos")
        for x in yrcos.transpose():
            print(x)

        print("angle")
        for x in angle.transpose():
            print(x)            
        
        print("ht",ht)

        print("nbands",nbands)

        print("xcosn")
        for x in xcosn.transpose():
            print(x)

        print("alpha")
        for x in alpha.transpose():
            print(x)
        
        print("ycosn")
        for x in ycosn.transpose():
            print(x)
        
        print("himask")
        for x in himask.transpose():
            print(x)

        print("const",const)
        '''     
        for b in range(0, nbands):
            anglemask = p0p.pointOP(angle, ycosn, xcosn[0]+math.pi*(b)/nbands, xcosn[1]-xcosn[0], 0) 
            banddft = complex(np.power(-(0+1j),(nbands-1))) * lodft * anglemask * himask
            band = np.fft.ifft2(np.fft.ifftshift(banddft))
            band1=band.transpose()
            bands[b] = band1.flatten() 
            bind[b] = band.shape
            
                    
        bands = np.transpose(bands) #1400,2
        
        dims=[0,0]
        dims[0],dims[1] = lodft.shape
        dims[1]+=1
        ctr_r = math.ceil((dims[0]+0.5)/2)
        ctr_c = math.ceil((dims[1]+0.5)/2)
        lodims_r = math.ceil((dims[0]-0.5)/2)
        lodims_c = math.ceil((dims[1]-0.5)/2)
        loctr_r = math.ceil((lodims_r+0.5)/2)
        loctr_c = math.ceil((lodims_c+0.5)/2)
        lostart_r = ctr_r - loctr_r+1
        lostart_c = ctr_c - loctr_c+1
        loend_r = lostart_r + lodims_r-1
        loend_c = lostart_c + lodims_c-1
        '''
        print("------------------------------------------------after-----------------------------------------------")

        print("angle mask")
        for x in anglemask.transpose():
            print(x)

        print("dims",dims[0],dims[1])
        print("ctr",ctr_r,ctr_c)
        print("lodims",lodims_r,lodims_c)
        print("loctr",loctr_r,loctr_c)
        print("lostart",lostart_r,lostart_c)
        print("loend",loend_r,loend_c)


        '''
        log_rad = log_rad [lostart_r-1 : loend_r, lostart_c-1:loend_c]
        angle = angle [lostart_r-1 : loend_r, lostart_c-1:loend_c] 
        lodft = lodft [lostart_r-1 : loend_r, lostart_c-1:loend_c]
        YIrcos = abs(np.sqrt((1.0 - np.power(yrcos,2))))
        lomask = p0p.pointOP(log_rad, YIrcos, xrcos[0], xrcos[1]-xrcos[0], 0)
        lodft = lomask * lodft

        
        [npyr ,nind] = buildSCFPyrLevs(lodft, log_rad, xrcos, yrcos, angle, ht-1, nbands)
        bb = (bands.transpose()).flatten()
       
        pyr = np.append((bands.transpose()).flatten(), npyr)
        pind =  np.vstack((bind, nind))
        return [pyr,pind]


        





