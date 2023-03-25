import socket
import time

def calculate_checksum(data):
    return sum(data) % 256

def is_corrupted(recv_data, checksum):
    return calculate_checksum(recv_data) != checksum

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(('localhost', 12345))

    print("RATAALADA ONLINE")

    expected_seq_num = 0

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
            if int(seq_num) == expected_seq_num:
                
                print(f"{addr[0]}:{addr[1]} >> {msg}")
                expected_seq_num = 1 - expected_seq_num

            response = f"ACK|{seq_num}"

        time.sleep(0.1)  # Adicione um atraso na resposta do servidor
        server.sendto(response.encode('utf-8'), addr)

if __name__ == "__main__":
    main()
