#!/usr/bin/python3
import socket
import sys, cv2, json
import numpy as np
from socketing import recv_variable_length
from socketing import TCP_PORT

if(len(sys.argv) > 1):
  TCP_PORT = int(sys.argv[1])


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', TCP_PORT))
s.listen(True)

img_count = 0
SECS = 30

save = False

def main():
  global img_count
  while True:
    conn, addr = s.accept()
    try:
      while (img_count < SECS*30 or save == False):
        bytedata = recv_variable_length(conn)
        frame = np.frombuffer(bytedata, dtype='uint8')
        frame = cv2.imdecode(frame, 1)
        cv2.imshow('Streaming video', frame)
        cv2.waitKey(1)
        if(save):
          img_count += 1
      return
    except EOFError as err:
      print(err)
      conn.close()
      cv2.destroyAllWindows()


if __name__ == '__main__':
  try:
    main()
  finally:
    s.shutdown(0)
    cv2.destroyAllWindows()