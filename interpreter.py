import sys
import socket
import time
import subprocess
import threading

from struct import pack
from modules.malicioussocket import mexploit
from modules.exploitsocket import exploit
from modules.inetd_tcp_crash import tcpcrash
from functools import wraps
from weakref import WeakKeyDictionary



payloads = {'rpc_dos', 'zombie', 'default_exploit', 'inetd_tcp_crash'}

canshow = {'payloads', 'settings'}


red = "\033[31m"
blue = "\033[34m"
bold = "\033[1m"
reset = "\033[0m"
green = "\033[32m"
yellow = "\033[33m"

host1 = False
port1 = False
connrefused = False
target = ''
port = int


class DummyFile(object):
   def write(self, x):
      pass



def check_alive(target, port):
   global connrefused
   try:
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      sock.settimeout(1)
      sock.connect((target, port))
      sock.close()
      print(f"{green}[+]{reset} Target is alive")
   except Exception as err:
      print(f"{red}[FATAL_ERROR]{reset} {target} - Failed to connect")
      quit()
      connrefused = True
      return False
   return True



def mute(fn):
   @wraps(fn)
   def wrapper(self, *args, **kwargs):
      thread_output_stream = WeakKeyDictionary()
      thread_output_stream.setdefault(threading.current_thread(), []).append(DummyFile())
      try:
         return fn(self, *args, **kwargs)
      finally:
         thread_output_stream[threading.current_thread()].pop()
   return wrapper




def run(inputshell):
   global host1
   global port1
   global target
   global port
   global payloadshell
   if inputshell == "quit":
      sys.exit()

   elif "set target" in inputshell:
      org1 = inputshell
      spl1 = "target"

      res = org1.split(spl1)[1]
      target = res.translate({ord(' '): None})

      print(f"{green}[+]{reset} " + "{'target':" + f" '{target}'" + "}")
      host1 = True

   elif "set port" in inputshell:
      org3 = inputshell
      spl3 = "port"

      res3 = int(org3.split(spl3)[1])
      port = int(res3)
      int(port)
      port1 = True

      print(f"{green}[+]{reset} " + "{'port':" + f" '{port}'" + "}")


   elif "use" in inputshell:
      org2 = inputshell
      spl2 = "use"
      resl = org2.split(spl2)[1]
      payload = resl
      payload = payload.translate({ord(' '): None})

      while True:
         if payload in {'rpc_dos', 'zombie', 'default_exploit', 'inetd_tcp_crash'}:

            print(f"┌─({blue}lsf@lsf{reset})─[{blue}{red}{payload}{reset}{reset}]")
            payloadshell = input(f"└─────{blue}${reset} ")
            if payloadshell == "back":
               break



            elif payload == "rpc_dos":
               if host1 == False:
                  print(f"{red}[-]{reset} No target acquired")
                  break

               if port1 == False:
                  print(f"{red}[-]{reset} No port acquired!")
                  break


               if "run" in payloadshell:
                  print(f"{blue}[*]{reset} Running module")
                  try:
                     check_alive(target=target, port=port)

                  except False:
                     break


                  print(f"{blue}[*]{reset} Sending RPC DoS packets")
                  time.sleep(0.9)


                  try:
                     exploit(target=target, port=port)
                     print(f"{green}[+]{reset} Module ran successfully")

                  except:
                     break




            elif payload == "default_exploit":
               if host1 == False:
                  print(f"{red}[-]{reset} No target acquired!")
                  break

               if port1 == False:
                  print(f"{red}[-]{reset} No port acquired!")
                  break


               if payloadshell in "run":
                  print(f"{blue}[*]{reset} Running module")
                  try:
                     check_alive(target=target, port=port)
                  except False:
                     break

                  print(f"{blue}[*]{reset} Sending malicious packets")
                  time.sleep(0.9)
                  
                  try:
                     mexploit(target=target, port=port)
                     print(f"{green}[+]{reset} Module ran successfully")
                  except:
                     break

            elif payload == "inetd_tcp_crash":
               if host1 == False:
                  print(f"{red}[-]{reset} No target acquired!")
                  break

               if port1 == False:
                  print(f"{red}[-]{reset} No port acquired!")
                  break

               if "run" in payloadshell:
                  print(f"{blue}[*]{reset} Running module")
                  try:
                     check_alive(target=target, port=port)
                  except Exception:
                     break

                  print(f"{blue}[*]{reset} Sending packets")
                  time.sleep(0.9)

                  try:
                     tcpcrash(target=target, port=port)
                  except Exception as err:
                     print(err)
                     break

                  print(f"{green}[+]{reset} Module ran successfully")

                  




            else:
               print(f"{yellow}[!]{reset} Command not found, try running it in the default lsf input")






         else:
            print(f"{red}[-]{reset} Payload not found")
            break

   elif "show info" == inputshell:
      print(f"""
      Payloads          Exploit requirements      Status
      --------          --------------------      ------
      rpc_dos           target   payload          {green}[ OK ]{reset}

      default_exploit   port                      {green}[ OK ]{reset}

      inetd_tcp_crash                             {green}[ OK ]{reset} 

      
      
      
      """)

   elif "help" == inputshell:
      print("""
      Commands:
         set
         use
         show
         run
         quit
         back


      How to use:
         set target/port
         use rpc_dos/default_exploit/inetd_tcp_crash
         show info
         run *with active payload*
         quit
         back
      
      
      """)
      

   else:
      if '' == inputshell:
         pass
      else:
         print(f"{red}[-]{reset} '{inputshell}' Command not found")