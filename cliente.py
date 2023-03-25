import socket
import random

def calculate_checksum(data):
    return sum(data) % 256

def main():
    print('CONNECTING TO RATAALADA.COM...')
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.settimeout(1)  # Adicione um timeout ao cliente

    seq_num = 0
    max_retries = 3

    original_message = ''
    while True:
        original_message = input(">> ")
        if original_message.lower() == 'close':
            break

        retries = 0
        while retries < max_retries:
            # Simular erro de integridade
            if random.random() < 0.4:
                message = f"{seq_num}|{original_message}|0"
            else:
                message = f"{seq_num}|{original_message}|{calculate_checksum((str(seq_num) + '|' + original_message).encode('utf-8'))}"
            
            client.sendto(message.encode('utf-8'), ('localhost', 12345))
            try:
                response, _ = client.recvfrom(1024)
                response = response.decode('utf-8').split('|')

                if response[0] == "ACK" and int(response[1]) == seq_num:
                    print('[OK] ACK')
                    seq_num = 1 - seq_num
                    break
                elif response[0] == "NACK":
                    print("[!] NACK - Resending message")
                    retries += 1
            except socket.timeout:
                print("[!] Timeout - Resending message")
                retries += 1

        if retries == max_retries:
            print("[!] Maximum tries reached. Please try again.")
    
    client.close()
    print('>> DISCONNECTED FROM RATAALADA.COM <<')

if __name__ == "__main__":
    main()
