import cv2
from time import sleep
from threading import Thread, Lock
from pyModbusTCP.client import ModbusClient
from datetime import datetime, timedelta
#camera = cv2.VideoCapture(0) #rtsp://192.168.1.2:8080/out.h264
#camera = cv2.VideoCapture(0) #rtsp://192.168.1.2:8080/out.h264/
#rtsp://192.168.1.53/

def Camera_RunTime(id_camera):
    camera = cv2.VideoCapture(id_camera) #rtsp://192.168.1.2:8080/out.h264
    global this_value_read
    global connect_check
    chup_anh_old = 0
    while True:
        try:
            return_value,image = camera.read()
            #tín hiệu kiểm tra kết nối
            connect_check= 1
            #gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
            #cv2.imshow('image',gray)
            image = cv2.resize(image, (1024, 768))
            
            chup_anh = this_value_read[0][0]
            #khi no bang

            cv2.imshow('image',image)
            is_date = datetime.now() + timedelta(days=0, hours=0)

            

            #===xu ly chup khac===#
            if cv2.waitKey(2)& 0xFF == ord('s'):
                data_image = 'log/image_test/image_'+is_date.strftime('%Y_%m_%d_%H_%M_%S')+ '.jpg'
                cv2.imwrite(data_image,image)
                print(data_image)
            elif cv2.waitKey(2)& 0xFF == ord('e'):
                break
            #====xu ly chup anh===#
            elif chup_anh == 1 and chup_anh_old == 0:
                data_image = 'log/image_'+is_date.strftime('%Y_%m_%d_%H_%M_%S')+ '.jpg'
                cv2.imwrite(data_image,image)
                print("Save Image .... " + data_image)
                #luu vao mysql nua
                chup_anh_old = 1
            elif chup_anh == 0:
                chup_anh_old = 0

            #===xu ly chup anh===#
            #===xu ly chup khac===#
        except:
            print('mất kết nối cammera ...')
            connect_check= 2
            sleep(10)
            try:
                camera = cv2.VideoCapture(id_camera) #rtsp://192.168.1.2:8080/out.h264
            except:
                pass

    camera.release()
    cv2.destroyAllWindows()

##========== Chương Trình Đọc Dữ Liệu Modbus TCP/IP ==========##
def thread_modbus_tcp(SERVER_HOST,SERVER_PORT,memory_communication):
    c = ModbusClient()
    c.host(SERVER_HOST)
    c.port(SERVER_PORT)
    global this_value_read
    global connect_check
    while True:
        if not c.is_open():
            if not c.open():
                print("unable to connect to "+SERVER_HOST+":"+str(SERVER_PORT))
        if c.is_open():
            # đọc từ thanh ghi 0 tới thanh ghi 10
            regs = c.read_holding_registers(memory_communication, 10)
            sleep(0.100)
            
            if(this_value_read[0][1] != connect_check):
                c.write_single_register(memory_communication + 1,int(connect_check))
                print("Write.......")
                print(this_value_read[0][1])

            if regs:
                #print("reg ad #0 to 9: "+str(regs) +" " + str(type(regs)))
                this_value_read[0] = regs
        sleep(0.100)
        print(this_value_read[0])
        

if __name__ == "__main__":
    this_value_read = {}
    this_value_read[0] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    
    connect_check = 0

    #====== thong so can cau hinh======#
    IP_Connect = '127.0.0.1'
    Port_Connect = 510
    id_camera = 'rtsp://192.168.1.53'
    memory_communication = 0
     #====== thong so can cau hinh======#


    try:
        ##========== Gọi Chương Trình Đọc Dữ Liệu Modbus TCP/IP ==========##
        
        threads = list()
        x = Thread(target=thread_modbus_tcp, args=(IP_Connect,int(Port_Connect),int(memory_communication)))
        x.daemon = True
        x.start()
        ##========== Gọi Chương Trình Đọc Dữ Liệu Modbus TCP/IP ==========##
        while True:
            
            Camera_RunTime(id_camera)
    except:
        print('error ...')
