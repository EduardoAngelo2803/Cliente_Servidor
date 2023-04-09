import socket
import time
from utils.checksum_utils import is_corrupted

SERVER_DELAY = 0.4


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(('localhost', 12345))

    print("RATAALADA ONLINE")

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

if __name__ == "__main__":
    main()
