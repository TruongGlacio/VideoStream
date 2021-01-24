import socket
import time
import select

class ServerManager:
	def __init__(self, host, port ):
		self.host = host
		self.port = port
		self.connected_list = []
		self.record = {}
		self.buffer = 4096
		self.OpenConnect(self.host,self.port)
		pass

	def OpenConnect(self, host, port):
    		
		self.server_socket = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
		self.server_socket.bind((host, port))

		self.server_socket.listen(10)
		self.connected_list.append(self.server_socket)
		print("\33[32m \t\t\t\tSERVER START WORKING at address: " + str(host)+ ", port: "+ str(port) +"\33[0m")

	def run(self):
		while 1:
			# Get the list sockets which are ready to be read through select
			rList,wList,error_sockets = select.select(self.connected_list,[],[])

			for sock in rList:
				#New connection
				if sock == self.server_socket:
					# Handle the case in which there is a new connection recieved through server_socket
					sockfd, addr = self.server_socket.accept()
					name=sockfd.recv(self.buffer)
					print('Messages from client: ', name)
					self.connected_list.append(sockfd)
					self.record[addr]=""
					#print "record and conn list ",record,connected_list
					
					#if repeated username
					if name in self.record.values():
						sockfd.send(bytes("\r\33[31m\33[1m Username already taken!\n\33[0m", "utf-8"))
						del self.record[addr]
						self.connected_list.remove(sockfd)
						sockfd.close()
						continue
					else:
						#add name and address
						self.record[addr]=name
						print("Client (%s, %s) connected" % addr," [",self.record[addr],"]")
						sockfd.send(bytes( "\33[32m\r\33[1m Welcome to chat room. Enter 'tata' anytime to exit\n\33[0m", "utf-8"))
						#send_to_all(sockfd, "\33[32m\33[1m\r "+name+" joined the conversation \n\33[0m")

				#Some incoming message from a client
				else:
					# Data from client
					try:
						data1 = sock.recv(self.buffer)
						#print "sock is: ",sock
						data=data1[:data1.index("\n")]
						#print "\ndata received: ",data
						
						#get addr of client sending the message
						i,p=sock.getpeername()
						if data == "tata":
							msg="\r\33[1m"+"\33[31m "+self.record[(i,p)]+" left the conversation \33[0m\n"
							self.send_to_all(sock,msg,self.connected_list,self.server_socket)
							print ("Client (%s, %s) is offline" % (i,p)," [",self.record[(i,p)],"]")
							del self.record[(i,p)]
							self.connected_list.remove(sock)
							sock.close()
							continue

						else:
							msg="\r\33[1m"+"\33[35m "+self.record[(i,p)]+": "+"\33[0m"+data+"\n"
							self.send_to_all(sock,msg,self.connected_list,self.server_socket)
				
					#abrupt user exit
					except:
						(i,p)=sock.getpeername()
						#send_to_all(sock, "\r\33[31m \33[1m"+record[(i,p)]+" left the conversation unexpectedly\33[0m\n")
						print ("Client (%s, %s) is offline (error)" % (i,p)," [",self.record[(i,p)],"]\n")
						del self.record[(i,p)]
						self.connected_list.remove(sock)
						sock.close()
						continue
		self.server_socket.close()


	#Function to send message to all connected clients
	def send_to_all(sock, message,connected_list, server_socket):
		#Message not forwarded to server and sender itself
		for socket in connected_list:
			if socket != server_socket and socket != sock :
				try :
					socket.send(message)
				except :
					# if connection not available
					socket.close()
					connected_list.remove(socket)	


if __name__ == '__main__':
	host =  '192.168.1.15'
	port = 8080
	serverManager = ServerManager(host, port)
	serverManager.run()
