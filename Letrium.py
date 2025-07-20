import os
from PIL import Image

let = "\033[38;5;183m"
clear = "\033[0m"
ler = "\033[38;5;54m"
leu = "\033[35m"

def Letrium():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""{let}
 _          _        _                 
| |        | |      (_)                
| |     ___| |_ _ __ _ _   _ _ __ ___  
| |    / _ \ __| '__| | | | | '_ ` _ \ 
| |___|  __/ |_| |  | | |_| | | | | | |
\_____/\___|\__|_|  |_|\__,_|_| |_| |_|
{clear}

    [{let}+{clear}] Letrium {let}RAT{clear} {let}|{clear} V2
    [{let}+{clear}] Author      {let}|{clear} cybermad
    [{let}*{clear}] Github      {let}|{clear} https://github.com/madanokr001
    [{let}*{clear}] Discord     {let}|{clear} https://discord.gg/RUc432Nc
          """)

def convert(path):
    try:
        img = Image.open(path) 
        paths = "icon.ico"
        img.save("icon.ico", "ICO") 
        return paths
    except Exception as e:
        print(f"{e}")
        return None

def build():
    paths = convert(icon)  
    if paths is None:
        print(f"{ler}FAILD{clear}")
        return
    
    if not os.path.exists("PAYLOAD"):
        os.makedirs("PAYLOAD")

    os.system(f'pyinstaller --onefile --clean --name {exe} --icon {paths} --noconsole --distpath PAYLOAD lib/bot.py')

    print(f"{let}Done.{clear}")
    input()

if __name__ == "__main__":
    Letrium()
    exe = input(f""" 
┌──{let}({clear}{ler}root{clear}@{let}letrium{clear}{let}){clear}-[{ler}~{clear}]
└─{let}>{clear} Enter the exe file name
                                      
┌──{let}({clear}{ler}root{clear}@{let}letrium{clear}{let}){clear}-[{ler}~{clear}]
└─{let}>{clear} """)
    
    icon = input(f""" 
┌──{let}({clear}{ler}root{clear}@{let}letrium{clear}{let}){clear}-[{ler}~{clear}]
└─{let}>{clear} Enter the image icon local file path
                                      
┌──{let}({clear}{ler}root{clear}@{let}letrium{clear}{let}){clear}-[{ler}~{clear}]
└─{let}>{clear} """)
    
    build()