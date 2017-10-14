from socket import *
import select
import sys
from thread import *

serverPort = 81
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print 'The server is ready to receive'

try:
        while True:
                connectionSocket, addr = serverSocket.accept()
                print addr
                sentence = connectionSocket.recv(1024)
                capitalizedSentence = sentence.upper()
                connectionSocket.send(capitalizedSentence)
finally:        
        connectionSocket.close()

#Join the chat room
def JOIN(CRN, Ser_IP, Port, Room_Ref, Join_ID):        
        Seq_num = 1               #Unique Identifier for Join
        socket.gethostname() 
        Ser_IP = socket.gethostbyname(socket.gethostname())  #Server IP
        Port = 81
        Join_ID = Seq_num
        
