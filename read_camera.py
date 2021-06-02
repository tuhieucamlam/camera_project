import cv2
from time import sleep

#camera = cv2.VideoCapture(0) #rtsp://192.168.1.2:8080/out.h264
#camera = cv2.VideoCapture(0) #rtsp://192.168.1.2:8080/out.h264/
#rtsp://192.168.1.53/

def Camera_RunTime(id_camera):
    camera = cv2.VideoCapture(id_camera) #rtsp://192.168.1.2:8080/out.h264
    i = 0
    while True:
        try:
            return_value,image = camera.read()
            #gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
            #cv2.imshow('image',gray)
            image = cv2.resize(image, (1024, 768))
        
            cv2.imshow('image',image)
            if cv2.waitKey(2)& 0xFF == ord('s'):
                i =i + 1
                name = 'log/test'+str(i)+ '.jpg'
                cv2.imwrite(name,image)
                print(name)
            if cv2.waitKey(2)& 0xFF == ord('e'):
                break
        except:
            print('mất kết nối cammera ...')
            sleep(10)
            try:
                camera = cv2.VideoCapture(id_camera) #rtsp://192.168.1.2:8080/out.h264
            except:
                pass

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    try:
        while True:
            id_camera = 'rtsp://192.168.1.53/media/video2'
            Camera_RunTime(id_camera)
    except:
        pass
