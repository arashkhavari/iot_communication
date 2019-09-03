#!/usr/bin/python3.5

import socket
from threading import Thread
from socketserver import ThreadingMixIn
import pymysql.cursors
from time import localtime , strftime
import binascii
from datetime import datetime

class ClientThread(Thread):
    def __init__(self,ip,port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        with open('importlog.txt', 'a') as out:
            out.write(str(datetime.now())+" 7766tcp "+"[+] New thread started for "+ip+":"+str(port)+'\n')
    def run(self):
        while True:
            data, addr = conn.recvfrom(2048)
            addr = self.ip
            current_time = strftime("%Y-%m-%d %H:%M:%S", localtime())
            commandname=data[4:6]
            cn=data[4:6]
            commandname=binascii.hexlify(commandname)
            commandname=int(str(commandname,'ascii'))
            #commandname=int(commandname,16)
            if commandname==5101:
                print('event data')
                collect=[]
                data0=data[2:4] #length
                data0 = binascii.hexlify(data0)
                data0 = str(data0, 'ascii')
                data0 = int(data0, 16)
                collect.append(data0)
                data1=data[4:6] #command
                data2=data[6:10] #unit number
                data3=data[10:14] #date
                data4=data[14:18] #time
                data5=data[18:22] #longitude
                data6=data[22:26] #latitude
                data71=data[26:27] #4 bit IGN 12 bit Azimuth
                data72=data[27:28]
                data8=data[28:30] #speed
                data9=data[30:32] #RPM
                q=data0-1
                data10=data[q-1:] #type
                data11=data[32:q-6]
                ###########for send ack to dev
                val1=data2.decode('ISO-8859-1')
                val2=cn.decode('ISO-8859-1')
                val3=data10.decode('ISO-8859-1')
                print(val1)
                print(val2)
                print(val3)
                print(data2)
                print(cn)
                print(data10)
                ackk='#T\x01\x05\x99\x01'+val1+val2+'\x01'+val3
                print(ackk)
                ackk=bytes(ackk, 'utf-8')
                print(ackk)
                conn.send(ackk)
                #######for selectable data work with RE or Match
                data1 = binascii.hexlify(data1)
                data1 = int(str(data1, 'ascii'))
                #data1 = int(data1, 16)
                collect.append(data1)
                data2 = binascii.hexlify(data2)
                data2 = str(data2, 'ascii')
                data2 = int(data2, 16)
                collect.append(data2)
                data3 = binascii.hexlify(data3)
                data3 = str(data3, 'ascii')
                data3 = str(int(data3, 16))
                data3 = datetime.strptime(data3, '%Y%m%d').strftime('%Y-%m-%d')
                collect.append(data3)
                data4 = binascii.hexlify(data4)
                data4 = str(data4, 'ascii')
                data4 = str(int(data4, 16))
                data4 = datetime.strptime(data4, '%H%M%S').strftime('%H:%M:%S')
                collect.append(data4)
                data5 = binascii.hexlify(data5)
                data5 = str(data5, 'ascii')
                data5 = int(data5, 16) * 0.000001
                data5 = format(data5, '.6f')
                data5 = str(data5)
                collect.append(data5)
                data6 = binascii.hexlify(data6)
                data6 = str(data6, 'ascii')
                data6 = int(data6, 16) * 0.000001
                data6 = format(data6, '.6f')
                data6 = str(data6)
                collect.append(data6)
                data71 = binascii.hexlify(data71)
                data71 = str(data71, 'ascii')
                data71 = int(data71, 16)
                data71 = '{0:08b}'.format(data71)
                data72 = binascii.hexlify(data72)
                data72 = str(data72, 'ascii')
                data72 = int(data72, 16)
                data72 = '{0:08b}'.format(data72)
                data7 = int(str(data71)+str(data72))
                data7 = [int(i) for i in str(data7)]
                tedad = len(data7)
                kol = 16
                menha = kol - tedad
                data711=data7[:4-menha]
                data712=data7[4-menha:]
                collect.append(data711)
                collect.append(data712)
                data8 = binascii.hexlify(data8)
                data8 = str(data8, 'ascii')
                data8 = int(data8, 16)
                collect.append(data8)
                data9 = binascii.hexlify(data9)
                data9 = str(data9, 'ascii')
                data9 = int(data9, 16)
                collect.append(data9)
                data10 = binascii.hexlify(data10)
                data10 = str(data10, 'ascii')
                data10 = int(data10, 16)
                collect.append(data10)
                data11 = str(data11)
                data11 = data11.split(',')
                print(data11)
                tool = len(data11)
                tool = int(tool-1)
                print(tool)
                while True:
                    if tool>=0:
                        cin=data11[tool]
                        cin=cin.split(':')
                        vali=cin[1]
                        if cin[0]=='A1':
                            collect.extend(['A1',vali])
                        elif cin[0]=='A2':
                            collect.extend(['A2',vali])
                        elif cin[0] == 'A3':
                            collect.extend(['A3',vali])
                        elif cin[0] == 'B1':
                            collect.extend(['B1',vali])
                        elif cin[0] == 'B2':
                            collect.extend(['B2',vali])
                        elif cin[0] == 'B3':
                            collect.extend(['B3',vali])
                        elif cin[0] == 'C1':
                            collect.extend(['C1',vali])
                        elif cin[0] == 'C2':
                            collect.extend(['C2',vali])
                        elif cin[0] == 'C3':
                            collect.extend(['C3',vali])
                        elif cin[0] == "b'A1":
                            collect.extend(['A1', vali])
                        elif cin[0] == "b'A2":
                            collect.extend(['A2', vali])
                        elif cin[0] == "b'A3":
                            collect.extend(['A3', vali])
                        elif cin[0] == "b'B1":
                            collect.extend(['B1', vali])
                        elif cin[0] == "b'B2":
                            collect.extend(['B2', vali])
                        elif cin[0] == "b'B3":
                            collect.extend(['B3', vali])
                        elif cin[0] == "b'C1":
                            collect.extend(['C1', vali])
                        elif cin[0] == "b'C2":
                            collect.extend(['C2', vali])
                        elif cin[0] == "b'C3":
                            collect.extend(['C3', vali])
                        tool=tool-1
                    else:
                        print(collect)
                        break
            else:
                print(data)

TCP_IP = '0.0.0.0'
TCP_PORT = 7766
BUFFER_SIZE = 20  # Normally 1024, but we want fast response
tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((TCP_IP, TCP_PORT))
threads = []

while True:
    tcpsock.listen(4)
    with open('importlog.txt', 'a') as out:
        out.write(str(datetime.now())+" 7766tcp "+"Waiting for incoming connections..."+ '\n')
    (conn, (ip,port)) = tcpsock.accept()
    newthread = ClientThread(ip,port)
    newthread.start()
    threads.append(newthread)
for t in threads:
    t.join()
