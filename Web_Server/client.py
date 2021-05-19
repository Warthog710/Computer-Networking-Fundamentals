from socket import *
import sys

#Read command line arguments, make sure 4 were sent
if (len(sys.argv) != 4):
    print("Usage: client.py server_host server_port filename")
    exit()

try:
    #Create socket
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((sys.argv[1], int(sys.argv[2])))

    #Send an HTTP GET request
    clientSocket.send('GET /' + sys.argv[3] + ' HTTP/1.1\n'.encode())

    #Keep receiving until an empty string
    while True:   
        modifiedSentence = clientSocket.recv(1024)
        print(modifiedSentence)
        if not modifiedSentence:
            break;

    #Close the connection
    clientSocket.close()

except Exception:
    print("An error occured... Does the server exist?")