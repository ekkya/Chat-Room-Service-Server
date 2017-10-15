from socket import *
import select
import sys
from thread import *

Connection_List = []
Seq_num = 1
CRN = room1
Ser_IP = socket.gethostbyname(socket.gethostname())
Room_Ref = 1
Join_ID = Seq_num
serverPort = 81

serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(10)
print 'The server is ready to receive on Port' + serverPort

Connection_List.append(serverSocket)
print "Connection List: " + Connection_List

while 1:
        read_sockets, write_sockets, error_sockets = select.select(Connection_List, [], [])

        for sock in read_sockets:
                #For New Connections
                if sock == serverSocket:
                        sockfc, addr = serverSocket.accept()
                        Connection_List.append(sockfc)
                        print "Connection List: " + Connection_List
                        JOIN(CRN, Ser_IP, serverPort, Room_Ref, Join_ID)
                        print "Client (%s, %s) connected" % addr
                        broadcast(sockfc, "[%s:%s] entered chat room\n" % addr)
                #else:
                        #Deal with messages coming from the client - including with "Nonsense" messages





#Join the chat room - Response sent to client after establishing socket connection
def JOIN(CRN, Ser_IP, Port, Room_Ref, Join_ID):        
        response = ("JOINED CHATROOM:"+str(CRN), Ser_IP, Port, Room_Ref, Join_ID)
        print "Response sent to Client on first connection: " + response

        return response

#Function to broadcast chat messages to all connected clients
def broadcast(sock, message):
        for socket in Connection_List:
                if socket != serverSocket and socket != sock:
                        try:
                                socket.send(message)
                        except:
                                socket.close()
                                Connection_List.remove(socket)
