import socket
import select
import sys
from thread import *
import threading

#Join the chat room - Response sent to client after establishing socket connection
def JOIN_single(CRN, Ser_IP, Port, Room_Ref, Join_ID):
        response = ("JOINED CHATROOM: "+ CRN, "SERVER_IP: " + Ser_IP, "PORT: " + Port, "ROOM_REF: " + Room_Ref, "JOIN_ID: " + Join_ID)
        print "Client (%s, %s) connected" % addr
        print "Response sent to Client on connection: " + response

        return response

def JOIN_multiple(CRN, Ser_IP, Port, Room_Ref, Join_ID):        
        response = ("JOINED CHATROOM:"+str(CRN), Ser_IP, Port, Room_Ref, Join_ID)
        #print "Response sent to Client on connection: " + response

        return response

#Leave the chat room - Response sent to client after requesting to leave
def LEAVE_single(CRN, Room_Ref, JOIN_ID):
        response = ("LEFT CHATROOM: " +str(CRN), "ROOM_REF: " + Room_Ref, "JOIN_ID: " + JOIN_ID)
        print "Response sent to client when leaving: " + response

        return response

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
	while Data != "KILL_SERVICE":
		Data = Conn.recv(1024)
		print "Current:" + Data
		#if Data != "JOIN_CHATROOM" and Data != "LEAVE_CHATROOM" and Data != "KILL_SERVICE":
		print "This is Rubbish"
		#continue
	if Data == "KILL_SERVICE":
		print "Goodbye!"
		Conn.close()
		return
	else:
		return

#Function for handling connections. Used to create Threads - Attempt 1
def clientthread(Conn):
        Data = Conn.recv(1024)
	print "Current:" + Data
	print "Connection received. Adding to registry"
        Connection_List.append(Conn)
        
        #Need to look at parsing the data coming from the client
        mylist = data.split(" ")
        print mylist
        
	#Condition for joining chat room
	if mylist[0] == "JOIN_CHATROOM:":
		Connection_List.append(serverSocket, CRN, Room_Ref, Join_ID, mylist[8])                
		reply_j = JOIN_single(CRN, SER_IP, serverPort, Room_Ref, Join_ID)
		Conn.send(reply_j)
		Seq_num = Seq_num + 1   #Increase Join_ID by 1 for new client
		Join_ID = Seq_num

	#Condition for multiple clients joining the same chat room (room1)
	if mylist[0] == "JOIN_CHATROOM:" and Connection_List[4] > 1:
		Connection_List.append(serverSocket, CRN, Room_Ref, Join_ID, mylist[8])
		reply_j = JOIN_single(CRN, SER_IP, serverPort, Room_Ref, Join_ID)
		Conn.send(reply_j)
		        
	#Condition for same client joining multiple chat rooms
	if mylist[0] == "JOIN_CHATROOM:" and Connection_List[4] == 1:
		Room_Ref = "2"
		reply_j = JOIN_single(CRN, SER_IP, serverPort, Room_Ref, Join_ID)
		Conn.send(reply_j)
		
	#Condition for leaving chat room
	if mylist[0] == "LEAVE_CHATROOM:" and mylist[4] == Connection_List[4]:
		Connection_List.remove(serverSocket, CRN, Room_Ref, Join_ID)
		reply_l = LEAVE_single(CRN, Room_Ref, Join_ID)
		Conn.send(reply_l)

	#Condition for same client leaving multiple chat rooms
	if mylist[0] == "LEAVE_CHATROOM:" and mylist[4] == Connection_List[4]:
		if Connection_List[3] == "1":
			Room_Ref = "1"
		        reply_l = LEAVE_single(CRN, Room_Ref, Join_ID)
		        Conn.send(reply_l)
		elif Connection_List[3] == "2":
		        Room_Ref = "2"
		        reply_l = LEAVE_single(CRN, Room_Ref, Join_ID)
		        Conn.send(reply_l)
	print "END!!!"
	return
	   
Stu_ID = "13317728"
Connection_List = []
Seq_num = 1
CRN = "room1"
#Ser_IP = socket.gethostbyname(socket.gethostname())
Ser_IP = socket.gethostbyname('www.google.com')
print Ser_IP
Room_Ref = "1"
Join_ID = Seq_num
connections = set()

serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serverSocket.bind(('', 33333))
serverSocket.listen(10)
serverPort = 33333
print serverPort
print 'The server is ready to receive on Port: ' + str(serverPort)

#Test for basic connection with client - Expecting "Helo" type message
Conn, address = serverSocket.accept()
print Conn
Data = Conn.recv(1024)

print "Data from base connection client: " + Data
response = Data.rstrip()
response1 = "IP:"+Ser_IP
response2 = "Port:"+str(serverPort)
response3 = "StudentID:"+Stu_ID

resp = str(response + "\n" + response1 + "\n" + response2 + "\n" + response3)
print resp
Conn.sendall(resp)

##Start thread and kill thread when Data == "KILL_SERVICE"
while True:
	threading.Thread(target=datathread, args=(Conn,)).start()
	threading.Thread(target=clientthread, args=(Conn,)).start()
	
