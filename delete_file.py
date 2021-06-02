import pyodbc 
from time import sleep

def delete_file(file_name):
    import os
    file_name = '../log_image/' + file_name +'.jpg'
    try:
        os.remove(file_name)
        print("Remove file: " + file_name)
    except:
        print("The file does not exist : " + file_name)



def select_file_delete(connect_string):
    try:
        cnxn = pyodbc.connect(connect_string)
        cursor = cnxn.cursor()
        cursor.execute("SELECT  `Image_File` FROM `hyosung_camera`.`data_image_file` WHERE Date_Created <= DATE_ADD(NOW(), INTERVAL -180 DAY) and Is_Check ='0'")
        for row in cursor.fetchall():
            print(row[0])
            delete_file(str(row[0]))
        print(True)
        #cursor.close()
        cursor = cnxn.cursor()
        cursor = cnxn.execute("UPDATE `hyosung_camera`.`data_image_file` SET `Is_Check`='1'  WHERE Date_Created <= DATE_ADD(NOW(), INTERVAL -180 DAY) and Is_Check ='0'")
        cursor.commit()
        cursor.close() 
    except:
        #sleep(10)
        print(False)

#connect_string = 'Driver={MySQL ODBC 3.51 Driver};Server=LOCALHOST;Port=3306;Database=test;User=root;Password=15903570;Option=3;'
#select_file(connect_string)

