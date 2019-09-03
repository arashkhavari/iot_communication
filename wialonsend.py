#!/usr/bin/python3.5
import pymysql.cursors
from socket import *
import ast

'''
cursor mysql ezafe shode ke haman pymysql ast
socket ezafe shode baraye TCP
ast niz convertor data mibashad
port listen dar pain avarde shode ast
socket bind shode data az database gerefte mishavad
va montazer darkhast az wialon baraye 3way handshake mishavad
daryaft shavad data ta zamani ke socket bind ast ersal mishavad
'''

serverPort = 11800
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
cl = '\n'
cb = '\r'
se= '0'
cv = ','
print ('The server is ready to receive')
while True:
    try:
        connectionSocket, addr = serverSocket.accept()
        print('first')
        while True:
            try:
                _connection=pymysql.connect(host='localhost',user='root',password='!QAZ1qaz1qaz',db='t2m',charset='utf8',cursorclass=pymysql.cursors.DictCursor,autocommit=True)
                print('connect to db')
                _cursor = _connection.cursor()
                print('fuckin cursor')
                _cursor.execute('Select unit,adate,lat,lon,speed,astatus,carrier From parsing where astatus="input" limit 1;')
                print('c steps i tired :(')
                _fetchone = _cursor.fetchall()
                _fetchone = str(_fetchone)
                print('fetchone')
                __dataG =ast.literal_eval(_fetchone)
                print('format')
                _connection.close()
                print(__dataG,'1')
                if __dataG!=():
                    ___dataG=__dataG[0]
                    print(___dataG,'2')
                    _unit=___dataG['unit']
                    _unit=str(_unit)
                    print(_unit,'3')
                    _lat=___dataG['lat']
                    print(_lat,'4')
                    _lon=___dataG['lon']
                    print(_lon,'5')
                    _carrier=___dataG['carrier']
                    print(_carrier,'6')
                    _speed=___dataG['speed']
                    print(_speed,'7')
                    _adate=___dataG['adate']
                    print(_adate,'8')
                    ___dataG=str('\n'+'P'+cv+_unit+cv+_adate+cv+_lat+cv+_lon+cv+_speed+cv+se+cv+se+cv+'00Vsi,'+_carrier+'\r')
                    print(___dataG,'9')
                    connectionSocket.send(___dataG.encode())
                    print('GSM data is sent')
                    _connection=pymysql.connect(host='localhost',user='root',password='!QAZ1qaz1qaz',db='t2m',charset='utf8',cursorclass=pymysql.cursors.DictCursor,autocommit=True)
                    _cursor = _connection.cursor()
                    _cursor.execute('update parsing set astatus="pass" where astatus="input" limit 1;')
            #_connection.close()
                else:
                    print('khavari ye tuple list ro rad kardi barikala')
                    break;
            except BrokenPipeError:
                    print('Broken Pipe yaani connection is chokh :)))))')
                    break;
            except TypeError:
                 _connection=pymysql.connect(host='localhost',user='root',password='!QAZ1qaz1qaz',db='t2m',charset='utf8',cursorclass=pymysql.cursors.DictCursor,autocommit=True)
                 _cursor = _connection.cursor()
                 _cursor.execute('update parsing set astatus="faild" where astatus="input" limit 1;')
                 print('faild for Type error excepttion')
                 pass;
            finally:
                pass;
    finally:
        connectionSocket.close()
