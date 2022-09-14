import struct

TCP_PORT = 5001

def recv_variable_length(socket):
    data = socket.recv(4)
    if(data == b''):
        raise EOFError('Connection closed by client')
    
    (msg,) = struct.unpack("i", data)

    data = b""
    remaining = int(msg)
    while remaining > 0:
        recieved = socket.recv(remaining)
        remaining = remaining - len(recieved)
        data += recieved

    return data


def send_variable_length(socket, message):
    msg_len = len(message)
    socket.send(struct.pack("i", msg_len))
    socket.send(message)