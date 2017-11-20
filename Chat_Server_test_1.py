import socket
import select
import sys
from thread import *
import threading

#Join the chat room - Response sent to client after establishing socket connection
def JOIN_single(CRN, Ser_IP, Port, Room_Ref, Join_ID):
        response = "JOINED CHATROOM:"+ CRN
	response1 = "SERVER_IP:" + Ser_IP
	response2 = "PORT:" + Port
	response3 = "ROOM_REF:" + Room_Ref
	response4 = "JOIN_ID:" + Join_ID
        #print "Client (%s, %s) connected" % addr
        #print "Response sent to Client on connection: " + response
	resp = str(response + "\n" + response1 + "\n" + response2 + "\n" + response3 + "\n" + response4)
	#print resp
        return resp

def JOIN_multiple(CRN, Ser_IP, Port, Room_Ref, Join_ID):        
        response = ("JOINED CHATROOM:"+str(CRN), Ser_IP, Port, Room_Ref, Join_ID)
        #print "Response sent to Client on connection: " + response

        return response

#Leave the chat room - Response sent to client after requesting to leave
def LEAVE_single(CRN, Room_Ref, JOIN_ID):
        response = "LEFT_CHATROOM:" +CRN
	response3 = "ROOM_REF:" + Room_Ref
	response4 = "JOIN_ID:" + Join_ID
        #print "Response sent to client when leaving: " + response
	resp = str(response + "\n" + response3 + "\n" + response4)
        return resp

#Function to send to all the clients present in the connection list
def send_all(message):
        for connection in connections:
                connection.send(message)
		

def receive(Conn):
        while True:
                message = Conn.recv(1024)
                if not message:
                        print "Closing connection and removing from registry"
                        Conn.remove(Conn)
                        return
                print "Received %s, sending to all" % message
                send_all(message)
                
def datathread(Conn):
	Seq_num = 1
	CRN = "room1"
	Room_Ref = "1"
	Join_ID = Seq_num
	serverPort = serverSocket.getsockname()[1]
	serverIP = socket.gethostbyname(socket.gethostname())
	send_data = (serverPort, CRN, Room_Ref, Join_ID)
	print send_data
	Connection_List = []
	while Data:
		print "Current:" + Data
		print "Connection received. Adding to registry"
		#Connection_List.append(Data)
		
		#Need to look at parsing the data coming from the client
		mylist = Data.split("\n")
		print mylist
		Connection_List.append(mylist)
		mylist1 = [i.split(' ', 1)[0] for i in mylist]
		print mylist1
		#Condition for joining chat room
		if mylist1[0] == "JOIN_CHATROOM:":
			#Connection_List.append(serverSocket, CRN, Room_Ref, Join_ID)                
			reply_j = JOIN_single(CRN, ServerIP, serverPort, Room_Ref, Join_ID)
			Conn.sendall(reply_j)
			response1 = "CHAT:" + Join_ID		
			response = "client" + Join_ID + "has joined this chatroom"
			resp = (response1 + "\n" + response)
			Conn.sendall(resp)	
			#Seq_num = Seq_num + 1   #Increase Join_ID by 1 for new client
			#Join_ID = Seq_num	
			if mylist1[0] == "JOIN_CHATROOM:" and mylist1[2] == "room2":
				Room_Ref = "2"
				reply_j = JOIN_single(CRN, ServerIP, serverPort, Room_Ref, Join_ID)
				Conn.sendall(reply_j)
				response1 = "CHAT:" + Join_ID		
				response = "client" + Join_ID + "has joined this chatroom"
				resp = (response1 + "\n" + response)
				Conn.sendall(resp)		 		
		#Condition for multiple clients joining the same chat room (room1)
		if mylist1[0] == "JOIN_CHATROOM:" and mylist1[1] == "room1":
			#Connection_List.append(serverSocket, CRN, Room_Ref, Join_ID)
			reply_j = JOIN_single(CRN, SER_IP, serverPort, Room_Ref, Join_ID)
			Conn.send(reply_j)
		#Condition for leaving chat room
		if mylist1[0] == "LEAVE_CHATROOM:" and mylist[2] == Connection_List[6]:
			Connection_List.remove()
			reply_l = LEAVE_single(CRN, Room_Ref, Join_ID)
			Conn.sendall(reply_l)
			response1 = "CHAT:" + Join_ID
			response = "client" + Join_ID + "has left this chatroom"
			resp = (response1 + "\n" + response)
			Conn.sendall(resp)
		#Condition for same client leaving multiple chat rooms
		if mylist1[0] == "LEAVE_CHATROOM:" and mylist1[4] == Connection_List[4]:
			if Connection_List[3] == "1":
				Room_Ref = "1"
				reply_l = LEAVE_single(CRN, Room_Ref, Join_ID)
				Conn.send(reply_l)
			elif Connection_List[3] == "2":
				Room_Ref = "2"
				reply_l = LEAVE_single(CRN, Room_Ref, Join_ID)
				Conn.send(reply_l)
					
		Data = Conn.recv(1024)		
	print "END!!!"
	return


Stu_ID = "13317728"
#Connection_List = []
Seq_num = 1
CRN = "room1"
Ser_IP = socket.gethostbyname(socket.gethostname())
#Ser_IP = socket.gethostbyname('www.google.com')
print Ser_IP
Room_Ref = "1"
Join_ID = Seq_num
connections = set()

serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serverSocket.bind(('0.0.0.0', 0))
serverSocket.listen(10)
serverPort = serverSocket.getsockname()[1]
print serverPort
print 'The server is ready to receive on Port: ' + str(serverPort)

#Test for basic connection with client - Expecting "Helo" type message
Conn, address = serverSocket.accept()
Data = Conn.recv(1024)

print "Data from base connection client:" + Data
response = Data.rstrip()
response1 = "IP:"+Ser_IP
response2 = "Port:"+str(serverPort)
response3 = "StudentID:"+Stu_ID

resp = str(response + "\n" + response1 + "\n" + response2 + "\n" + response3)
print resp
Conn.sendall(resp)

#Test for Unknown message
Data = Conn.recv(1024)
print "Data: " + Data
print "Rubbish"
Conn.close()

Conn, address = serverSocket.accept()
Data = Conn.recv(1024)
print "Data after unknown message: " + Data

##Start thread and kill thread when Data == "KILL_SERVICE"
while Data:
	#threading.Thread(target=datathread, args=(Conn,)).start()
	#Data = Conn.recv(1024)
	#print "Current Data: " + Data
	if Data == "KILL_SERVICE":
		print "Goodbye"
		Conn.close()
	else:
		datathread(Conn)
		print "END!!!"
	




	#print "END"
	#Conn.close()
	
	
