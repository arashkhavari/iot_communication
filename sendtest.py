import socket

host = '127.0.0.1'
port = 7766
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
s.sendall(b'#T\x008Q\x01\x00\x01_\x97\x013\xee\x1e\x00\x01#\x83\x03\x10\xda\xce\x02!K\x96\x10\x00\x00\x00\x00\x00B1:1349,B2:0,B3:0\x00\x1054\x00\xf5F')
data = s.recv(1024)
s.close()
print('Received', repr(data))
