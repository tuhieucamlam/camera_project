import cv2 #pip install opencv-python
import numpy as np
from time import sleep
from threading import Thread, Lock
from pyModbusTCP.client import ModbusClient #pip install pyModbusTCP
from pymodbus.client.sync import ModbusSerialClient #https://github.com/riptideio/pymodbus
from datetime import datetime, timedelta

#C:\Users\ATB-HIEU\AppData\Local\Programs\Python\Python37\Lib\site-packages
import pyodbc
from python_config_infomation import read_file_config
from check_connect_string import check_connect_sql_sever
from delete_file import select_file_delete

#camera = cv2.VideoCapture(0) #rtsp://192.168.1.2:8080/out.h264
#camera = cv2.VideoCapture(0) #rtsp://192.168.1.2:8080/out.h264/
#rtsp://192.168.1.53/

def check_connect_database(connect_string):
    check_connect = False
    i_check = 0
    is_date_st = datetime.now() + timedelta(days=0, hours=0)
    is_date_string_run = is_date_st.strftime('%Y-%m-%d %H:%M:%S')
    data_log_error = 'data_log/data_log_error_'+is_date_st.strftime('%Y_%m_%d_%H_%M_%S')+ '.txt'
    # Kiểm tra kết nối lần đầu tiên
    while check_connect == False:
        i_check = i_check + 1
        try:
            #global check_connet
            check_connect = check_connect_sql_sever(connect_string)
            if check_connect:
                print('Connect String Kết Nối thành công ... (' + str(i_check) +')')
                cnxn = pyodbc.connect(connect_string)
                #lưu vào file log 
                is_date_string_connected = is_date_st.strftime('%Y-%m-%d %H:%M:%S')
                data_log = 'data_log/data_log_begin_'+is_date_st.strftime('%Y_%m_%d_%H_%M_%S')+ '.txt'
                f = open(data_log,'w')
                f.write("Nguyen Tu Hieu : 097.987.3414 [2021/05/06-HYOSUNG-Camera] Time Program Connect OK " + is_date_string_run +" (-) "+ is_date_string_connected + "\n")
                f.close()

            else:
                print('Connect String Kết Nối không thành công ... (' + str(i_check) +')')
                #lưu vào file log 
                is_date_string_connected = is_date_st.strftime('%Y-%m-%d %H:%M:%S')
                f = open(data_log_error,'a')
                f.write("Nguyen Tu Hieu : 097.987.3414 [2021/05/06-HYOSUNG-Camera] Time Program Connect Not " + is_date_string_run +" (-) "+ is_date_string_connected + "\n")
                f.close()
                sleep(10)
        except:
            sleep(10)
        finally:
            sleep(3)


def Db_Command(query_string):
    try:
        
        cursor = cnxn.cursor()
        cursor = cnxn.execute(str(query_string))
        cursor.commit()
        cursor.close() 
        return True
    except:
        return False


def save_data_camera_online(str_date,str_time):
    
    msg = "INSERT INTO `hyosung_camera`.`data_camera_online`(`YMD`, `HMS`) VALUES ('%s','%s')"  % (str_date,str_time)
    print(msg)
    check = Db_Command(str(msg))
    if check == False:
        check_connect = check_connect_sql_sever(connect_string)
        #print('//.......(1).......//')
        try:
            if check_connect == True:
                global cnxn
                cnxn = pyodbc.connect(connect_string)
                Db_Command(str(msg))
                print('//.......(ODBC_Re_connect).......//')
        except:
            pass
    print('//.......(ODBC).......//' + str(check))

def save_image(str_name,str_date,str_time):
    
    msg = "INSERT INTO `hyosung_camera`.`data_image_file`(`Image_File`, `YMD`, `HMS`) VALUES ('%s','%s','%s')"  % (str_name,str_date,str_time)
    print(msg)
    check = Db_Command(str(msg))
    if check == False:
        check_connect = check_connect_sql_sever(connect_string)
        #print('//.......(1).......//')
        try:
            if check_connect == True:
                global cnxn
                cnxn = pyodbc.connect(connect_string)
                Db_Command(str(msg))
                print('//.......(ODBC_Re_connect).......//')
        except:
            pass
    print('//.......(ODBC).......//' + str(check))


def Camera_RunTime(id_camera):
    camera = cv2.VideoCapture(id_camera) #rtsp://192.168.1.2:8080/out.h264
    global this_value_read
    global connect_check
    chup_anh_old = 0
    currentFrame = 0

    is_date = datetime.now() + timedelta(days=0, hours=0)
    str_Time_Camerea = is_date.strftime('%m%d%H%M')
    str_date = is_date.strftime('%Y%m%d')
    str_time = is_date.strftime('%H%M%S')
    save_data_camera_online(str(str_date),str(str_time))

    while True:
        try:
            return_value = camera.grab()
            return_value,image = camera.retrieve()
            #return_value,image = camera.read()
            #tín hiệu kiểm tra kết nối
            connect_check= 1
            #gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
            #cv2.imshow('image',gray)
            #image = cv2.resize(image, (1024, 768))
            
            chup_anh = this_value_read[0][0]
            #khi no bang

            #cv2.imshow('image',image)
            #cv2.waitKey(1)
            is_date = datetime.now() + timedelta(days=0, hours=0)
            #print("-- ANH ---")
            

            #===xu ly chup khac===#
            if cv2.waitKey(1)& 0xFF == ord('s'):
                data_image = '../log_image/image_test/image_'+is_date.strftime('%Y%m%d_%H_%M_%S')+ '.jpg'
                cv2.imwrite(data_image,image)
                print(data_image)
            elif cv2.waitKey(1)& 0xFF == ord('e'):
                break
            #====xu ly chup anh===#
            elif chup_anh == 1 and chup_anh_old == 0:

                
                data_image = '../log_image/'+str(hex(int(str_Time_Camerea)))+'_'+is_date.strftime('%Y%m%d_%H%M%S')+ '.jpg'
                
                cv2.imwrite(data_image,image)
                str_image = str(hex(int(str_Time_Camerea))) +'_'+is_date.strftime('%Y%m%d_%H%M%S')
                str_date = is_date.strftime('%Y%m%d')
                str_time = is_date.strftime('%H%M%S')
                save_image(str(str_image),str(str_date),str(str_time))
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
            #sleep(10)
            is_date = datetime.now() + timedelta(days=0, hours=0)
            str_Time_Camerea = is_date.strftime('%m%d%H%M')
            try:
                camera = cv2.VideoCapture(id_camera) #rtsp://192.168.1.2:8080/out.h264
            except:
                pass

    camera.release()
    cv2.destroyAllWindows()

##========== Chương Trình Đọc Dữ Liệu Modbus TCP/IP ==========##


def ModbusSerialClient_RTU(PORT,memory_communication):
    #PORT = 'COM7'
    global this_value_read
    global connect_check
    while True:
        try:
            client = ModbusSerialClient(method='rtu', port=PORT, timeout=1,stopbits = 1, bytesize = 8, parity = 'N', baudrate= 115200)
            client.connect()
            while True:
                try:
                    regs = client.read_holding_registers(memory_communication,10,unit=0x01).registers
                    #client.write_register(1, 10, unit=0x01)

                    if(this_value_read[0][1] != connect_check):
                        #c.write_single_register(memory_communication + 1,int(connect_check))
                        client.write_register(memory_communication + 1, int(connect_check), unit=0x01)
                        print("Write.......")
                        print(this_value_read[0][1])
                    #print(regs)
                    sleep(0.700)
                    if regs:
                        #gán giá trị vào biến 
                        this_value_read[0] = regs
                except:
                    print('Error ModbusSerialClient_RTU 1...')
                    sleep(10)
                sleep(0.100)
                print('RTU-'+ str(this_value_read[0]))
        except:
            print('Error ModbusSerialClient_RTU 2...')
            sleep(10)


            

def ModbusSerialClient_TCP(SERVER_HOST,SERVER_PORT,memory_communication):
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
            sleep(0.700)
            
            if(this_value_read[0][1] != connect_check):
                c.write_single_register(memory_communication + 1,int(connect_check))
                print("Write.......")
                print(this_value_read[0][1])

            if regs:
                #print("reg ad #0 to 9: "+str(regs) +" " + str(type(regs)))
                this_value_read[0] = regs
        sleep(0.100)
        print('TCP-'+ str(this_value_read[0]))
        

if __name__ == "__main__":
    this_value_read = {}
    this_value_read[0] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    
    connect_check = 3

    connect_string = ""
    try:
        string_config = read_file_config("config.ini","config_connect_string")
        connect_string = string_config["connect_string"]
        connect_string = connect_string.replace("'", '')
        print('Connect String :'+ str(connect_string))
    except:
        print('Connect String Error:'+ str(connect_string))

    #kiếm tra kết nối lần đầu tiên
    check_connect_database(connect_string)
    select_file_delete(connect_string)

    #====== thong so can cau hinh======#
    Connect = 'TCP'
    IP_Connect = '127.0.0.1'
    Port_Connect = 510
    #or
    PORT = 'COM7'
    memory_communication = 0
    #id_camera = 'rtsp://192.168.1.53'
    id_camera = 0
     #====== thong so can cau hinh======#

    try:
        string_config = read_file_config("config.ini","config_info")
        Connect = string_config["connect"]
        IP_Connect = string_config["ip"]
        Port_Connect = int(string_config["port"])
        PORT = string_config["com"]
        memory_communication = int(string_config["memory_communication"])
        id_camera = string_config["id_camera"]

        print('config_info : ' + str(Connect) + '-' + str(IP_Connect) + '-'+ str(Port_Connect) + '-'+ str(memory_communication) + '-'+ str(memory_communication))
    except:
        print('config_info String Error:')


    try:
        ##========== Gọi Chương Trình Đọc Dữ Liệu Modbus TCP/IP ==========##
        
        threads = list()
        if(Connect == 'TCP'):
            x = Thread(target=ModbusSerialClient_TCP, args=(IP_Connect,int(Port_Connect),int(memory_communication)))
            print('CONNECT PLC PROTOCOL MODBUS TCP/IP')

        else:
            x = Thread(target=ModbusSerialClient_RTU, args=(PORT,int(memory_communication)))
            print('CONNECT PLC PROTOCOL MODBUS RTU')
        x.daemon = True
        x.start()
        ##========== Gọi Chương Trình Đọc Dữ Liệu Modbus TCP/IP ==========##
        while True:
            Camera_RunTime(id_camera)
    except:
        print('error ...')
