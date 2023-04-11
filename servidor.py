import socket
import time
from utils.checksum_utils import is_corrupted

SERVER_DELAY = 0.4

def connect():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(('localhost', 12345))
    return server


def single(server):
    while True:
        data, addr = server.recvfrom(1024)
        split_data = data.decode('utf-8').split('|')
        
        if len(split_data) != 3:
            print("[!] INVALID MESSAGE:", data)
            continue

        seq_num, msg, checksum = split_data

        if is_corrupted((str(seq_num) + '|' + msg).encode('utf-8'), int(checksum)):
            response = f"NACK|{seq_num}"
        else:
            print(f"{addr[0]}:{addr[1]} >> {msg}")
            response = f"ACK|{seq_num}"

        time.sleep(SERVER_DELAY)
        print(response)
        server.sendto(response.encode('utf-8'), addr)


def batch(server):
    while True:
        data, addr = server.recvfrom(1024)
        data = data.decode('utf-8').split('&')

        response = ''
        for split_data in data:
            seq_num, msg, checksum = split_data.split('|')
            if not is_corrupted((str(seq_num) + '|' + msg).encode('utf-8'), int(checksum)):
                print(f"{addr[0]}:{addr[1]} >> {msg}")
                seq_num = int(seq_num) + 1
                response = f"ACK|{str(seq_num)}"
            else:
                response = f'NACK|{str(seq_num)}'
                break
        if response == '':
            response = 'ACK|0'

        time.sleep(SERVER_DELAY)
        print(response)
        server.sendto(response.encode('utf-8'), addr)


def main():
    server = connect()
    mode = input('single = 0 | batch = 1 >> ')
    print("RATAALADA ONLINE")
    if (int(mode) == 0):
        single(server)
    else:
        batch(server)


if __name__ == "__main__":
    main()
