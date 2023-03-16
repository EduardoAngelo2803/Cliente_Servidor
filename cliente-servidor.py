import socket

HOST = 'localhost'
PORT = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sok:

    sok.bind((HOST, PORT))
    sok.listen()
    conn, adr = sok.accept()

    with conn:

        while True:

            data = conn.recv(1024)

            if not data:
                break
        

            conn.sendall(b'ACK')
            conn.sendall(b'Error!')


    