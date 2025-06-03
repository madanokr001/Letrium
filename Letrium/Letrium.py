import os
from PIL import Image
from pystyle import Colorate, Colors

def Letrium():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Colorate.Horizontal(Colors.blue_to_purple,r"""
    __         __       _               
   / /   ___  / /______(_)_  ______ ___ 
  / /   / _ \/ __/ ___/ / / / / __ `__ \   [ Author ]   :  cybermad
 / /___/  __/ /_/ /  / / /_/ / / / / / /   [ Version ]  :  1.0
/_____/\___/\__/_/  /_/\__,_/_/ /_/ /_/    [ Letrium ]  :  N/A

 [ Windows Remote Administration Tool ]  
     [ https://github/madanokr001 ]
       [ https://t.me/cybermads ]
          """))

def convert(image_path):
    try:
        img = Image.open(image_path) 
        icon_path = "icon.ico"
        img.save(icon_path, "ICO") 
        return icon_path
    except Exception as e:
        print(Colorate.Horizontal(Colors.red_to_white,"FAILD"))
        return None

def build():
    icon_path = convert(icon)  
    if icon_path is None:
        print(Colorate.Horizontal(Colors.red_to_white,"FAILD"))
        return

    os.system(f'pyinstaller --onefile --clean --name {exe} --icon {icon_path} --noconsole lib/bot.py')

    print(Colorate.Horizontal(Colors.blue_to_cyan,"Done."))
    input()

if __name__ == "__main__":
    Letrium()
    exe = input(Colorate.Horizontal(Colors.blue_to_purple,"""
┌──(root@letrium)-[~]]
└─> Enter the exe file name
                                    
┌──(root@letrium)-[~]
└─# """))

    icon = input(Colorate.Horizontal(Colors.blue_to_purple,"""
┌──(root@letrium)-[~]]
└─> Enter the icon image file path
                                                                 
┌──(root@letrium)-[~]
└─# """))
    
    build()    