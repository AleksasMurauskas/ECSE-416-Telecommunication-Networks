"""
Aleksas Murauskas 260718389
Florence Diep     260727117
ECSE 416
Lab 1: Client/Server
Client Side 
"""
#import statements
import socket
import sys
import pickle
from PIL import Image
import time


#Standard Server Name and Port Numbers and timeout 
serverName = '127.0.0.2'
serverPort = 12345
timeout= 5
#Parse command line inputs
#In case of 5 aruments 0. client.py 1. [-host] 2. [-port] 3. [-filename] 4. [-timeout]
if(len(sys.argv)==5): 
	serverName= str(sys.argv[1])
	serverPort = int(sys.argv[2])
	filename = str(sys.argv[3])
	timeout = int(sys.argv[4])

#In case of 4 aruments 0. client.py 1. [-host] 2. [-port] 3. [-filename]
elif (len(sys.argv)==4): 
	serverName= str(sys.argv[1])
	serverPort = int(sys.argv[2])
	filename = str(sys.argv[3])
#Incorrect Number of arguments
else: 
	print("Incorrect number of arguments, exiting program")
	sys.exit(1)

#Create Socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Set Timeout 
clientSocket.settimeout(timeout)
#Connect Socket
try:
	clientSocket.connect((serverName, serverPort))

except socket.error:
	print("Client Socket could not connect to server")
	sys.exit(1)
print("Connection OK.")
#Create File request
fileRequest = filename
clientSocket.send(fileRequest.encode())
print("Request Message Sent")

#receive server response
serverResponse = clientSocket.recv(1024)
print('Server HTTP Response: ', serverResponse.decode())
if(serverResponse.decode()=="\HTTP/1.1 404 not found"):
	print("404 Not Found")
	clientSocket.close()
	sys.exit(1)

#receive content type
mimetypeResponse = clientSocket.recv(1024).decode("utf-8")
print("Content-type: ", mimetypeResponse)

#receive file content
data = []
#Infinite loop to listen
start_time = time.time()
l=0
while True:
	#Since pickled data is bgt than 4096, pickle data once all parts received 
	packet = clientSocket.recv(1024)
	if not packet: 
		break
	data.append(packet)
	l=l+1
#Pickle complete data
file_content = pickle.loads(b"".join(data))
#Display depending on file format
print("--- %s seconds ---" % (time.time() - start_time))
print("--- %s Packets" % l)
if(mimetypeResponse=="text/html"):
	print(file_content)
elif(mimetypeResponse=="image/jpg"):
	file_content.show()
#Close connection
clientSocket.close()
print("Socket Closed")
sys.exit(0)