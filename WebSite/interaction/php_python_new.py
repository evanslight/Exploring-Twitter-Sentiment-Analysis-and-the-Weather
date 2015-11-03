###########################################################################
# Author: Hao DUAN<548771> Yu SUN<629341>  
# Date: 30 Oct 2015                        
# File Name: php_python_new.py
# Description : This program is used to deal with the request from website
##########################################################################

import time
import socket
import os

import process_new

# set the basic info
LISTEN_PORT = 21230


# main process
if __name__ == '__main__':

	print ("-------------------------------------------")
	print ("- PPython Service")
	print ("- Time: %s" % time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) )
	print ("-------------------------------------------")

	# define the socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #TCP/IP
	sock.bind(('', LISTEN_PORT))  
	sock.listen(5)  

	print ("Listen port: %d" % LISTEN_PORT)
	print ("Server startup...")

	# keep listen a port ,wait the request from website
	while 1:
		connection,address = sock.accept() #get a request
		print ("client's IP:%s, PORT:%d" % address)

		#call thread to process
		try:
			process_new.ProcessThread(connection).start()
		except:
			pass