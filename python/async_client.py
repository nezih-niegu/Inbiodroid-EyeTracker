import sys, struct
import asyncio
from socketing import send_variable_length
from socketing import TCP_PORT

from encoder_stream import EncoderStream

TCP_IP = 'localhost'
if(len(sys.argv) > 1):
  TCP_IP = sys.argv[1]  


if(len(sys.argv) > 2):
  TCP_PORT = int(sys.argv[2])

@asyncio.coroutine
def tcp_echo_client(encoderStream: EncoderStream, loop):
    reader, writer = yield from asyncio.open_connection(TCP_IP, TCP_PORT,
                                                        loop=loop)
    encoded_frame = encoderStream.current_frame
    msg_len = len(encoded_frame)
    writer.write(encoded_frame)

loop = asyncio.get_event_loop()
encoderStream = EncoderStream().start()
while encoderStream.current_frame is None:
    pass

print('Started streaming...')
while encoderStream.running():
    loop.run_until_complete(tcp_echo_client(encoderStream, loop))
    loop.run_until_complete(asyncio.sleep(.001))
    
loop.close()
