from configparser import ConfigParser
import codecs

 
def read_file_config(filename='config.ini', section='config_sqlsever',encoding='utf-8'):
    """ Đọc thông tin kết nối từ file config
    subject = An email with attachment from Python
    body = This is an email with attachment sent from Python
    sender_email = member.logging@gmail.com
    password = uchihaitachi
    receiver_email = autobaseshome@gmail.com
    receiver_email_cc = tuhieucamlam@gmail.com,tuhieunonglam@gmail.com
    receiver_email_bcc = bccperson1@gmail.com,bccperson2@yahoo.com
    """
    # Tạo parser và đọc ini configuration file
    parser = ConfigParser()
    parser.read(filename,encoding='utf-8')
 
    # Lấy section, mặc định là mysql
    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))
 
    return db

#string_config = read_file_config()
#print(string_config)
#print(type(string_config))
