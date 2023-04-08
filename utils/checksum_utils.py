def calculate_checksum(data):
    return sum(data) % 256


def is_corrupted(recv_data, checksum):
    return calculate_checksum(recv_data) != checksum
