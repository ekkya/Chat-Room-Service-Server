import socket
import select
import sys
from thread import *

Stu_ID = "13317728"
Connection_List = []
Seq_num = 1
CRN = "room1"
Ser_IP = socket.gethostbyname(socket.gethostname())
print Ser_IP
Room_Ref = "1"
Join_ID = Seq_num
connections = set()

serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serverSocket.bind(('0.0.0.0', 0))
serverSocket.listen(10)
serverPort = serverSocket.getsockname()[1]
print serverPort
print 'The server is ready to receive on Port: ' + str(serverSocket.getsockname()[1])

#Test for basic connection with client - Expecting "Helo" type message
Conn, address = serverSocket.accept()
print Conn
Data = Conn.recv(1024)

print "Data from base connection client: " + Data
response = (Data, "IP: " +Ser_IP, "Port: " + str(serverPort), "Student ID: " + Stu_ID)   #Need to print to separate lines
resp = str(response)
print resp
Conn.send(response)

while data != "KILL_SERVICE":
        conn = serverSocket.accept()
        data = conn.recv(4096)
        print "Connection received. Adding to registry"
        Connection_List.add(conn)
        
        #Need to look at parsing the data coming from the client
        mylist = data.split(" ")
        print mylist
        
        #Condition for joining chat room
        if mylist[0] == "JOIN_CHATROOM:":
                Connection_List.add(serverSocket, CRN, Room_Ref, Join_ID, mylist[8])                
                reply_j = JOIN_single(CRN, SER_IP, serverPort, Room_Ref, Join_ID)
                conn.send(reply_j)
                Seq_num = Seq_num + 1   #Increase Join_ID by 1 for new client
                Join_ID = Seq_num

        #Condition for multiple clients joining the same chat room (room1)
        if mylist[0] == "JOIN_CHATROOM:" and Connection_List[4] > 1:
                Connection_List.add(serverSocket, CRN, Room_Ref, Join_ID, mylist[8])
                reply_j = JOIN_single(CRN, SER_IP, serverPort, Room_Ref, Join_ID)
                conn.send(reply_j)
                
        #Condition for same client joining multiple chat rooms
        if mylist[0] == "JOIN_CHATROOM:" and Connection_List[4] == 1:
                Room_Ref = "2"
                reply_j = JOIN_single(CRN, SER_IP, serverPort, Room_Ref, Join_ID)
                conn.send(reply_j)
        
        #Condition for leaving chat room
        if mylist[0] == "LEAVE_CHATROOM:" and mylist[4] == Connection_List[4]:
                Connection_List.remove(serverSocket, CRN, Room_Ref, Join_ID)
                reply_l = LEAVE_single(CRN, Room_Ref, Join_ID)
                conn.send(reply_l)

        #Condition for same client leaving multiple chat rooms
        if mylist[0] == "LEAVE_CHATROOM:" and mylist[4] == Connection_List[4]:
                if Connection_List[3] == "1":
                        Room_Ref = "1"
                        reply_l = LEAVE_single(CRN, Room_Ref, Join_ID)
                        conn.send(reply_l)
                elif Connection_List[3] == "2":
                        Room_Ref = "2"
                        reply_l = LEAVE_single(CRN, Room_Ref, Join_ID)
                        conn.send(reply_l)
        

        #Start new thread
        #start_new_thread(clientthread, (conn,))

        #Deal with messages and disconnections using Threads
        threading.Thread(target = receive, args = [conn]).start()



#Function for handling connections. Used to create Threads - Attempt 1
def clientthread(connection):
        #Infinite Loop that does not terminate
        while True:
                #Receive data from client
                data = connection.recv(4096)
                mylist = data.split(" ")
                print mylist
        #break
        
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

def receive(conn):
        while True:
                message = conn.recv(1024)
                if not message:
                        print "Closing connection and removing from registry"
                        conn.remove(conn)
                        return
                print "Received %s, sending to all" % message
                send_all(message)
                
