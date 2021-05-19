#Import socket
from socket import *

#Prepare a server socket at this address
serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 1234
serverSocket.bind(('',serverPort))

#Queue up to a maximum of 1 request
serverSocket.listen(1)

while True:
    try:
        #Print that the server is ready to service requests
        print("Ready to serve...")

        #Accept any requests and decode them
        connectionSocket, addr = serverSocket.accept()
        msg = connectionSocket.recv(1024).decode()
        fileName = msg.split()[1]

        #Slice '/' from filename and attempt to open
        f  = open(fileName[1:])
        outputData = f.readlines()

        #File was found... send OK response with content type header
        connectionSocket.send('HTTP/1.1 200 OK\n'.encode())
        connectionSocket.send('Content-Type: text/html\n\n'.encode())

        #Feed file into socket
        for line in range (0, len(outputData)):
            connectionSocket.send(outputData[line].encode())

        #Close the file
        f.close()

    #The server couldn't find the file, send a 404
    except IOError:
        print(fileName + " not found")
        connectionSocket.send('HTTP/1.1 404 NOT FOUND\n'.encode())

    #If server failed to parse the message
    except IndexError:
        print("Failed to index msg: " + msg)

    #Close the connection
    connectionSocket.close()