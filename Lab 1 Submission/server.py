"""
Aleksas Murauskas 260718389
Florence Diep     260727117
ECSE 416
Lab 1: Client/Server
Server Side 
"""
#import statements
import socket
import sys
import pickle
from PIL import Image

#Set server information 
ServerName = '127.0.0.2'
serverPort = 12345

#Create Socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Bind Socket to server name and Port number 
serverSocket.bind((ServerName, serverPort))

#Wait for a Client Request 
serverSocket.listen(1)

#Infinite loop to listen
while True: 
    connectionSocket, addr = serverSocket.accept()
    print("Client Request received.")
    request = connectionSocket.recv(1024).decode()  
    filename = request
    #Use pickle library to serialize content
    try:
        if(filename.endswith(".txt")):
            data = open(filename, "r").read()
            mime_type = "text/html"
            file_content = pickle.dumps(data)
        elif(filename.endswith(".jpg")):
            data = Image.open(filename)
            mime_type = "image/jpg"
            file_content = pickle.dumps(data)
        else:
            print("Invalid File Type")
            resp = "\HTTP/1.1 404 not found"
            connectionSocket.send(resp.encode())
            print("Server Response Sent.")
            connectionSocket.close()
            print("Socket closed and request cannot be completed.")
            continue
    except IOError:
        print("Unknown file, must send failed message")
        resp = "\HTTP/1.1 404 not found"
        connectionSocket.send(resp.encode())
        print("Server Response Sent.")
        connectionSocket.close()
        print("Socket closed and request cannot be completed.")
        continue
    #Send Server Response 
    resp = "HTTP/1.1 200 OK"
    connectionSocket.send(resp.encode())
    print("HTTP Response Sent.")
    #Send Content Type Response
    connectionSocket.send(mime_type.encode("utf-8"))
    print("Content Type Response Sent.")
    #Send File Content Response
    connectionSocket.send(file_content)
    print("File Content Response Sent.")
    #Close Socket
    connectionSocket.close()
    print("Socket closed and request completed.")


    #cd Documents/"Fall 2020"/"ECSE 416"/ECSE-416/"Lab 1"
    #python server.py
    #python client.py 127.0.0.2 12345 test.txt