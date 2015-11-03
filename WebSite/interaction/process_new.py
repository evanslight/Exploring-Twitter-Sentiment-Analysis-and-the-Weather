###########################################################################
# Author: Hao DUAN<548771> Yu SUN<629341>  
# Date: 30 Oct 2015                        
# File Name: process_new.py
# Description : This program is used to deal with the request from website
##########################################################################

import sys
import time
import threading
import socket
import json

import php_python_new
import Smodel_interaction

class ProcessThread(threading.Thread):
	"""
	preThread
	"""
	def  __init__(self,socket):
		threading.Thread.__init__(self)

		#client socket
		self._socket = socket

	def run(self):

		# recv the message

		try:
			mesage = self._socket.recv(16 * 1024)
			print mesage

			new_mesage = json.loads(mesage)

			print new_mesage

		except Exception, e:
			print 'error:',e
			self._socket.close()
			return

		#call the method
		new_mesage_text = new_mesage['Text']
		result = Smodel_interaction.learn(new_mesage_text)

		# #return value
		# result = json.dumps(result)

		print result

		try:
			self._socket.sendall(result)
			pass
		except Exception, e:
			print 'error',e
		finally:
			self._socket.close()
			pass



