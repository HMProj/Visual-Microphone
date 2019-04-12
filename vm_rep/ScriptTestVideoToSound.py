import sys
import cv2
from scipy.io.wavfile import write
import VmSoundFromVideo as vsv

def main(VideoName):
    #no of scales
    nscales=1

    #no of orientations
    norients=2

    #framerate of the input video
    samplingrate=2200

    #down sample the video by
    dsamplefactor=0.1

    #read the input video
    cap=cv2.VideoCapture(VideoName)

    #Extract Sound From Video
    [S_samplingrate, S_average, S_averageNoAlignment, S_x]=vsv.VmSoundFromVideo(cap,nscales,norients,samplingrate,dsamplefactor)
    
    S_filename = VideoName

    write("mary_abe.wav",S_samplingrate,S_x.flatten())
    

if __name__ == '__main__':
    main(sys.argv[1])