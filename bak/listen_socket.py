import sys
import socket
if __name__ == "__main__":
	#sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	sock.bind(('10.100.206.223',162))
	while True:  
        	data, addr = sock.recvfrom(2048)  
        	if not data:  
            		print "client has exist"  
            		break
		for i in data:
			sys.stdout.write('%#x '% ord(i))
		print("\n\n========\n")
		msg = "received:%s from %s" % (data, addr)
		
		print msg
