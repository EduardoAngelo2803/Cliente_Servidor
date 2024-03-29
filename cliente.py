import socket
from utils.msg_utils import define_msg_batch, define_msg_single, resend_msg, resend_msg_individual_batch

DEFAULT_TIMEOUT = 1
MAX_RETRIES = 3


def check_close(client):
    close = input('Close? (y/n) >> ')
    if close == 'y':
        print('>> DISCONNECTED FROM RATAALADA <<')
        client.close()
        exit()



def define_comm(is_batch = False):
    if is_batch == False:
        corrupt = input('Corrupt? (y/n) >> ')
    else:
        corrupt = input('Corrupt? (index/n) >> ')
        corrupt = int(corrupt) if corrupt != 'n' else 'n'
    timeout = input('Timeout? (value/n) >> ')
    timeout = DEFAULT_TIMEOUT if timeout == 'n' else float(timeout)
    return corrupt, timeout


def connect():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.settimeout(DEFAULT_TIMEOUT)  # Adicione um timeout ao cliente
    return client


def single(client):
    seq_num = 0

    original_message = ''
    counter = 0
    while True:
        original_message = f'message_{counter}'
        check_close(client)


        retries = 0
        while retries < MAX_RETRIES:
            corrupt, timeout = define_comm()
            client.settimeout(timeout)
            message = define_msg_single(seq_num, original_message, corrupt)

            client.sendto(message.encode('utf-8'), ('localhost', 12345))
            try:
                response, _ = client.recvfrom(1024)
                response = response.decode('utf-8').split('|')

                if response[0] == "ACK" and int(response[1]) == seq_num:
                    print('[OK] ACK')
                    seq_num = 1 - seq_num
                    break
                else:
                    print("[!] NACK - Resending message")
                    retries += 1
            except socket.timeout:
                print("[!] Timeout - Resending message")
                client.settimeout(timeout*10)
                try:
                    response, _ = client.recvfrom(1024)
                    response = response.decode('utf-8').split('|')
                except:
                    print('[!] Connection was lost')
                    exit()
                retries += 1

        if retries == MAX_RETRIES:
            print("[!] Maximum tries reached. Please try again.")
        else:
            counter += 1


def batch(client):
    while True:
        original_message = ['msg0', 'msg1', 'msg2', 'msg3', 'msg4']
        check_close(client)


        retries = 0
        successful = False
        while retries < MAX_RETRIES and successful == False:
            corrupt_index, timeout = define_comm(True)
            client.settimeout(timeout)
            message = define_msg_batch(original_message, corrupt_index)
            message = '&'.join(message)
            client.sendto(message.encode('utf-8'), ('localhost', 12345))
            successful = True

            try:
                response, _ = client.recvfrom(1024)
                response = response.decode('utf-8').split('|')
                
                tries = 0
                done = 0
                if response[0] == 'ACK' and int(response[1]) == (len(original_message)):
                    print(f'[OK] {response[0]} {response[1]}')
                else:
                    while tries < 3 and done == 0:
                        resend_index = int(response[1])
                        print(f'[!] NACK {resend_index}, resending...')
                        response = resend_msg(original_message, resend_index, client)
                        if response[0] == 'ACK' and int(response[1]) == (len(original_message)):
                            print(f'[OK] {response[0]} {response[1]}')
                            done = 1
                        elif tries < 2:
                            tries += 1
                        else:
                            print('[!] Maximum tries reached, try again later')
            except socket.timeout:
                print("[!] Timeout - Resending message")

def individual_batch(client):
    while True:
        original_message = ['msg0', 'msg1', 'msg2', 'msg3', 'msg4']
        check_close(client)

        retries = 0
        successful = False
        while retries < MAX_RETRIES and successful == False:
            corrupt_index, timeout = define_comm(True)
            client.settimeout(timeout)
            message = define_msg_batch(original_message, corrupt_index)
            for msg in message:
                client.sendto(msg.encode('utf-8'), ('localhost', 12345))
            successful = True

            try:
                all_ok = True
                resend_index = 0
                for msg in message: # receives all the messages 
                    response, _ = client.recvfrom(1024)
                    response = response.decode('utf-8').split('|')
                    print(f'{response[0]} {response[1]}')
                    if all_ok == True and response[0] == 'NACK':
                        all_ok = False
                        resend_index = int(response[1])

                if all_ok == True:
                    print(f'[OK] ACK {response[1]}')
                    break
                else:
                    print(f"[!] NACK - Resending message from {resend_index}")
                    response = resend_msg_individual_batch(original_message, resend_index, client)
                    print(f'[OK] ACK {response[1]}')
            except socket.timeout:
                print("[!] Timeout - Resending message")
                retries += 1



def main():
    client = connect()
    mode = input('single = 0 | batch = 1 | individual confirmation batch = 2 >> ')
    print('CONNECTING TO RATAALADA.COM...')
    if (int(mode) == 0):
        single(client)
    elif (int(mode) == 1):
        batch(client)
    elif (int(mode) == 2):
        individual_batch(client)


if __name__ == "__main__":
    main()
