import pyodbc 
from time import sleep

def check_connect_sql_sever(connect_string):
    while True:
        try:
            pyodbc.connect(connect_string)
            #sleep(1)
            return True
        except:
            #sleep(10)
            return False

