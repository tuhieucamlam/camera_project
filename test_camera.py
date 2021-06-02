import time
FPS = '*rtsp fps value*'
cap = cv2.VideoCapture("rtsp://192.168.1.53/"); 
CALIBRATION = 1.5

def skipFrames(timegap):
   global FPS,cap
   latest = None
   while True :  
      for i in range(timegap*FPS/CALIBRATION) :
        _,latest = cap.read()
        if(not _):
           time.sleep(0.5)#refreshing time
           break
      else:
        break
   return latest

gap = 0.1
while cap.isOpened(): 
   current = skipFrames(gap)
   s = time.time()
   """
   My time hungry task here , may be some object detection stuff
   """
   gap = time.time()-s