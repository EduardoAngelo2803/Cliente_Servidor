import socket


host = 'localhost'
port = 8082

#Create a TCP/IP SOCKET
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Connect the socket to server
server_adress = (host, port)

sock.connect (server_adress)

try:

    message = 'Test message'
    print("Sending...\n")

    sock.sendall(message.endcode('UTF-8'))
    
    received = 0
    expected = len(message)


    while expected < received:

        data = sock.recv(16)
        received += len(data)

except socket.error as erro:

    print("Error in Socket %s!\n", str(erro))

finally:

    print("Closing connection with Server\n")
    sock.close()

