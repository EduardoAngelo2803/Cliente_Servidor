from utils.checksum_utils import calculate_checksum


def build_msg(id, data, checksum):
    return f"{id}|{data}|{str(checksum)}"


def define_msg_batch(message, corrupt_index):
    new_message = []
    for i in range(len(message)):
        if i == corrupt_index:
            new_message.append(build_msg(i, message[i], 0))
        else:
            new_message.append(build_msg(i, message[i], calculate_checksum((str(i) + '|' + message[i]).encode('utf-8'))))
    return new_message


def define_msg_single(seq_num, original_message, is_corrupt):
    if is_corrupt == 'y':
        message = build_msg(seq_num, original_message, 0)
    else:
        message = build_msg(seq_num, original_message, calculate_checksum((str(seq_num) + '|' + original_message).encode('utf-8')))
    return message


def resend_msg(message, corrupt_index, client):
    message = define_msg_batch(message, 'n')
    message = '&'.join(message[corrupt_index:])
    client.sendto(message.encode('utf-8'), ('localhost', 12345))
    response, _ = client.recvfrom(1024)
    response = response.decode('utf-8').split('|')
    return response


def resend_msg_individual_batch(message, index, client):
    message = define_msg_batch(message, 'n')
    for msg in message[index:]:
        client.sendto(msg.encode('utf-8'), ('localhost', 12345))
    for msg in message[index:]: # receives all the messages 
        response, _ = client.recvfrom(1024)
        response = response.decode('utf-8').split('|')
        print(f'{response[0]} {response[1]}')
    return response
