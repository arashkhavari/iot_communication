#!/usr/bin/python3.5

import socket
from threading import Thread
from socketserver import ThreadingMixIn
import pymysql.cursors
from time import localtime , strftime
import binascii
from datetime import datetime

'''
socket baraye kar bar ruye TCP UDP ast
threading baraye pardazesh movazi mibashad
socketserver shamel in do mishavad class haye pichide tar
pymysql.cursors baraye vasl shodan be DB mysql ast
time ke baraye dastrasi be time server ast
binascii class format ascii va binary mibashad
datetime ham noi class manand time mibashad ba function haye bishtar

dar class pain yek thread neveshte shode ast ta socket hamishe dar hale shenidan bar ruye port bashad
chon dar python listen kardan bar ruye port bar asase tedad data mibashad na zaman
sepas data bar asase formati ke dayaft mikonim pardazesh mishavad va item ha har kodam
dara shomare mishavand
dar inja yadavari mikonam bar asase device t2m tanzim shode
harkoja ke mikhahid data ra bebinid zire an khat print($VALUE) ra bezanid

'''
class ClientThread(Thread):
    def __init__(self,ip,port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        print ("[+] New thread started for "+ip+":"+str(port))
    def run(self):
        while True:
            data, addr = conn.recvfrom(2048)
            addr = self.ip
            current_time = strftime("%Y-%m-%d %H:%M:%S", localtime())
            data0=data[2:4]
            data0=binascii.hexlify(data0)
            data0=str(data0,'ascii')
            data0=int(data0,16)
            if data0==137:
                print(data)
                data1=data[6:10]
                data2=data[11:15]
                data3=data[15:19]
                data4=data[19:23]
                data5=data[23:27]
                data6=data[29:31]
                data1=binascii.hexlify(data1)
                data1=str(data1,'ascii')
                data1=int(data1,16)
                data2=binascii.hexlify(data2)
                data2=str(data2,'ascii')
                data2=str(int(data2,16))
                data2=datetime.strptime(data2, '%Y%m%d').strftime('%Y-%m-%d')
                data3=binascii.hexlify(data3)
                data3=str(data3,'ascii')
                data3=str(int(data3,16))
                data3=datetime.strptime(data3, '%H%M%S').strftime('%H:%M:%S')
                data4=binascii.hexlify(data4)
                data4=str(data4,'ascii')
                data4=int(data4,16) * 0.000001
                data4=format(data4, '.6f')
                data4=str(data4)
                print(data4)
                data5=binascii.hexlify(data5)
                data5=str(data5,'ascii')
                print(data5)
                data5=int(data5,16) * 0.000001
                print(data5)
                data5=format(data5, '.6f')
                print(data5)
                data5=str(data5)
                print(data5)
                data6=binascii.hexlify(data6)
                data6=str(data6,'ascii')
                data6=str(int(data6,16))
                data=data1,data2+' '+data3,data4,data5,data6
                sql = "INSERT INTO `parsing`(`service`, `length`, `unit`, `adate`, `lat`, `lon`, `speed`, `currentTime`, `IP`, `astatus`, `carrier`) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                _cursor.execute(sql, ('T#', data0, data1, data2+' '+data3, data5, data4, data6, current_time, addr, 'input', 'G'))
            elif 60<data0<90:
                print(data)
                data1=data[6:10]
                data2=data[10:14]
                data3=data[14:18]
                data4=data[18:22]
                data5=data[22:26]
                data6=data[28:30]
                data1=binascii.hexlify(data1)
                data1=str(data1,'ascii')
                data1=int(data1,16)
                data2=binascii.hexlify(data2)
                data2=str(data2,'ascii')
                data2=str(int(data2,16))
                data2=datetime.strptime(data2, '%Y%m%d').strftime('%Y-%m-%d')
                data3=binascii.hexlify(data3)
                data3=str(data3,'ascii')
                data3=str(int(data3,16))
                data3=datetime.strptime(data3, '%H%M%S').strftime('%H:%M:%S')
                data4=binascii.hexlify(data4)
                print(data4)
                data4=str(data4,'ascii')
                print(data4)
                pisa=int(data4,16)
                print(pisa)
                data4=int(data4,16) * 0.000001
                print(data4)
                data4=format(data4, '.6f')
                data4=str(data4)
                data5=binascii.hexlify(data5)
                data5=str(data5,'ascii')
                data5=int(data5,16) * 0.000001
                data5=format(data5, '.6f')
                data5=str(data5)
                data6=binascii.hexlify(data6)
                data6=str(data6,'ascii')
                data6=str(int(data6,16))
                data=data1,data2+' '+data3,data4,data5,data6
                sql = "INSERT INTO `parsing`(`service`, `length`, `unit`, `adate`, `lat`, `lon`, `speed`, `currentTime`, `IP`, `astatus`, `carrier`) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                _cursor.execute(sql, ('T#', data0, data1, data2+' '+data3, data5, data4, data6, current_time, addr, 'input', 'g'))

            else:
                print(data0, 'not 137 or 78', data)
            if not data: break
#            print ("received data:", bytearray.fromhex(data).decode())
           # conn.send(data)  # echo
TCP_IP = '0.0.0.0'
TCP_PORT = 7766
BUFFER_SIZE = 20  # Normally 1024, but we want fast response
tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((TCP_IP, TCP_PORT))
threads = []
connection = pymysql.connect(host='localhost',user='root',password='!QAZ1qaz1qaz',db='t2m',charset='utf8',cursorclass=pymysql.cursors.DictCursor,autocommit=True)
_cursor = connection.cursor()

'''
dar inja address va port mored nazar ra dadeim va miguim protocol TCP ast
hamchenin username va password DB save shode
'''

while True:
    tcpsock.listen(4)
    print ("Waiting for incoming connections...")
    (conn, (ip,port)) = tcpsock.accept()
    newthread = ClientThread(ip,port)
    newthread.start()
    threads.append(newthread)
for t in threads:
    t.join()
'''
halqei ke listen kardan data niz injast
'''
