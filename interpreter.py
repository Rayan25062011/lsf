import sys
import socket
import time
import subprocess
import threading

from struct import pack
from modules.malicioussocket import mexploit
from modules.exploitsocket import exploit
from modules.inetd_tcp_crash import tcpcrash
from modules.lgsprotocol import runc
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
command = ''


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
   except Exception as err:
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
   global command
   if inputshell == "quit":
      sys.exit()

   elif "set target" in inputshell:
      org1 = inputshell
      spl1 = "target"

      res = org1.split(spl1)[1]
      target = res.translate({ord(' '): None})

      print(f"{green}[+]{reset} {target}")
      host1 = True

   
   elif "set command" in inputshell:
      orgc = inputshell
      splc = "command"

      resc = orgc.split(splc)[1]
      command = resc.translate({ord(' '): None})

      print(f"{green}[+]{reset} {command}")
      host1 = True

   elif "set port" in inputshell:
      org3 = inputshell
      spl3 = "port"

      res3 = int(org3.split(spl3)[1])
      port = int(res3)
      int(port)
      port1 = True

      print(f"{green}[+]{reset} {port}")


   elif "use" in inputshell:
      org2 = inputshell
      spl2 = "use"
      resl = org2.split(spl2)[1]
      payload = resl
      payload = payload.translate({ord(' '): None})

      while True:
         if payload in {'rpc_dos', 'default_exploit', 'inetd_tcp_crash', 'run_cmd_init_ssh'}:

            print(f"┌─({blue}lsf@lsf{reset})─[{blue}~{blue}/modules/{payload}{reset}{reset}]")
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
                  if check_alive(target=target, port=port):

                     if not check_alive(target=target, port=port):
                        print(f"{green}[+]{reset} Target is down")

                     else:
                        print(f"{red}[-]{reset} Target is not vulnerable")
                        break


                     print(f"{blue}[*]{reset} Sending RPC DoS packets")
                     time.sleep(0.9)


                     try:
                        exploit(target=target, port=port)
                        print(f"{green}[+]{reset} Module ran successfully")

                     except:
                        break

                  else:
                     print(f"{red}[-]{reset} Target is not vulnerable")
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
                  if check_alive(target=target, port=port):
                     print(f"{green}[+]{reset} Target is alive")

                  else:
                     print(f"{red}[-]{reset} Target is down")


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
                  if check_alive(target=target, port=port):
                     print(f"{green}[+]{reset} Target is alive")
                  else:
                     print(f"{red}[-]{reset} Target is down")

                     break

                  print(f"{blue}[*]{reset} Sending packets")
                  time.sleep(0.9)

                  try:
                     tcpcrash(target=target, port=port)
                  except Exception as err:
                     print(err)
                     break

                  print(f"{green}[+]{reset} Module ran successfully")



            elif "run_cmd_init_ssh" == payload:
               if command == '':
                  print(f"{red}[-]{reset} Command not specified")
                  break

               print(f"{blue}[*]{reset} Running module")
               if check_alive(target=target, port=port):
                  print(f"{green}[+]{reset} Target is alive")
               else:
                  print(f"{red}[-]{reset} Target is down")

                  break

               print(f"{blue}[*]{reset} Starting an SSH connection with command")
               if runc(target=target, cmd=command):
                  print(f"{green}[+]{reset} Command ran succesfully on SSH connection")
               else:
                  print(f"{red}[-]{reset} Error accured on the SSH connection.")
                  break



            else:
               print(f"{yellow}[!]{reset} Command not found, try running it in the default lsf input")






         else:
            print(f"{red}[-]{reset} Payload not found")
            break

   elif "show payloads" == inputshell:
      print(f"""
      All payloads      Description
      {red}────────────{reset}{red}─────────────────{reset}
      rpc_dos           {red}|{reset}  Remote Procedure Call DoS

      default_exploit   {red}|{reset}  Send malicious packets that may slow down the device or crash it

      inetd_tcp_crash   {red}|{reset}  Crash a the TCP system using inetd

      run_cmd_init_ssh  {red}|{reset}  Run a command over SSH
      
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
         use 'payload'
         show info
         run *with active payload*
         quit
         back
      
      
      """)

   elif "check" == inputshell:
      pass
      

   else:
      if '' == inputshell:
         pass
      else:
         print(f"{red}[-]{reset} '{inputshell}' Command not found")