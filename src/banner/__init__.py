
from colorama import Fore, Style

def banner():
  print(f"""\n
        .__                                __          __          
        |__|_____           _______  _____/  |______ _/  |_  ____  
        |  \____ \   ______ \_  __ \/  _ \   __\__  \\   __\/ __ \ 
        |  |  |_> > /_____/  |  | \(  <_> )  |  / __ \|  | \  ___/ 
        |__|   __/           |__|   \____/|__| (____  /__|  \___  >
          |__|                                     \/          \/      
  """)

def info():
  print(f"""
  {Fore.CYAN}
  Autor: Higor Diego
  Website: http://higordiego.com.br
  Email: me@higordiego.com.br
  {Style.RESET_ALL}
  """)

