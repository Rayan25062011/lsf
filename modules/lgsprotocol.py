import subprocess

def runc(host, cmd):
   red = "\033[31m"
   blue = "\033[34m"
   bold = "\033[1m"
   reset = "\033[0m"
   green = "\033[32m"
   yellow = "\033[33m"

   ssh = subprocess.Popen(["ssh", "%s" % host, cmd],
   	shell=False,
   	stdout=subprocess.PIPE,
   	stderr=subprocess.PIPE)
      
   result = ssh.stdout.readlines()
   if result != []:
      print(result)
      print("\n")
   else:
      print(f"{red}[-]{reset} Command execution failed")
