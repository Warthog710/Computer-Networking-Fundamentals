from socket import *
import base64
import ssl
import json

#Password and email information are stored in a config json
#This file is in .gitignore
with open('config.json', 'r') as config:
    config = config.read()
    config = json.loads(config)

email = config['SMTP_EMAIL']
rcvEmail = config['SMTP_RCV_EMAIL']
pswd = config['SMTP_PSWD']

#Mail server info
mailServer = ('smtp.gmail.com', 587)

try:
    #Creating a TCP socket to connect to the mail server
    mailSocket = socket(AF_INET, SOCK_STREAM)
    mailSocket.bind(('', 1234))
    mailSocket.connect(mailServer)
    recv = mailSocket.recv(1024).decode()
    print(recv)

    if '220' not in recv:
        raise Exception ('220 reply not received from server.')

    #Sending HELO msg to server
    helloCmd = 'EHLO ' + mailServer[0] + '\r\n'
    mailSocket.send(helloCmd.encode())
    recv = mailSocket.recv(1024).decode()
    print(recv)

    if '250' not in recv:
        raise Exception ('250 reply not received from server.')

    #Sending a STARTTLS command
    mailSocket.send('STARTTLS\r\n'.encode())
    recv = mailSocket.recv(1024).decode()
    print(recv)

    #Authenticate
    sMailSocket = ssl.wrap_socket(mailSocket, ssl_version=ssl.PROTOCOL_SSLv23)
    sMailSocket.send('AUTH LOGIN\r\n'.encode())
    recv = sMailSocket.recv(1024).decode()
    print(recv)

    if '334' not in recv:
        raise Exception ('334 reply not received from server.')

    #Send username
    sMailSocket.send(base64.b64encode(email.encode()) + '\r\n'.encode())
    recv = sMailSocket.recv(1024).decode()
    print(recv)

    if '334' not in recv:
        raise Exception ('334 reply not received from server.')

    #Send password
    sMailSocket.send(base64.b64encode(pswd.encode()) + '\r\n'.encode())
    recv = sMailSocket.recv(1024).decode()
    print(recv)

    if '235' not in recv:
        raise Exception ('235 reply not received from server.')

    #Send mail from cmd
    sMailSocket.send('MAIL FROM:<'.encode() + email.encode() + '>\r\n'.encode())
    recv = sMailSocket.recv(1024).decode()
    print(recv)

    if '250' not in recv:
        raise Exception ('250 reply not received from server.')

    #Send rcpt to cmd
    sMailSocket.send('RCPT TO:<'.encode() + rcvEmail.encode() + '>\r\n'.encode())
    recv = sMailSocket.recv(1024).decode()
    print(recv)

    if '250' not in recv:
        raise Exception ('250 reply not received from server.')

    #Send data cmd
    sMailSocket.send('DATA\r\n'.encode())
    recv = sMailSocket.recv(1024).decode()
    print(recv)

    if '354' not in recv:
        raise Exception ('354 reply not received from server.')

    #Send msg
    sMailSocket.send('Subject: CSC138-03 Personal SMTP Client\n\n'.encode())
    sMailSocket.send('Hi Quinn,\n\nThis message was sent from your personal SMTP client in Python.\n\nSincerely,\nYour Python SMTP Client'.encode())
    sMailSocket.send('\r\n.\r\n'.encode())
    recv = sMailSocket.recv(1024).decode()
    print(recv)

    if '250' not in recv:
        raise Exception ('250 reply not received from server.')

    #Send quit cmd
    sMailSocket.send('QUIT\r\n'.encode())
    recv = sMailSocket.recv(1024).decode()
    print(recv)

    if '221' not in recv:
        raise Exception ('221 reply not received from server.')

    mailSocket.close()
    sMailSocket.close()
    print('\nExchange finished, email sent.')

except Exception as e:
    print(e)
    exit()