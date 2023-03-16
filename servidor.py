import socket

HOST = 'localhost'
PORT = 8082

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sok:

    sok.bind((HOST, PORT))
    sok.listen()
    conn, adr = sok.accept()

    with conn:

        while True:
            print ("Waiting to receive message from client")

            data = conn.recv(1024)

            if not data:
                break
        

            conn.sendall(b'ACK')
            conn.sendall(b'Error!')


    