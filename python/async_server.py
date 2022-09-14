import asyncio
import struct
import sys, cv2
import numpy as np
from socketing import TCP_PORT

if(len(sys.argv) > 1):
  TCP_PORT = int(sys.argv[1])


@asyncio.coroutine
def handle_echo(reader, writer):
    data = yield from reader.read(100)
    try:
      (msg,) = struct.unpack("i", data)

      print(data)
      frame = np.frombuffer(data, dtype='uint8')
      frame = cv2.imdecode(frame, 1)
     
      #cv2.imshow('Streaming video', frame)
      #cv2.waitKey(1)
    except EOFError as err:
      print(err)
      cv2.destroyAllWindows()
    #addr = writer.get_extra_info('peername')
    #print("Received %r from %r" % (data, addr))
    #print("Send: success")
    #writer.write("success".encode())
    #yield from writer.drain()
    writer.close()

loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_echo, '0.0.0.0', TCP_PORT, loop=loop)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
