# Author : cybermad

import os
import shutil
from PIL import Image

def fsociety():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(r"""
    ___________ ____  ________________________  __  _________ 
   / ____/ ___// __ \/ ____/  _/ ____/_  __/\ \/ / / ____/__ \   [Author]   :  cybermad
  / /_   \__ \/ / / / /    / // __/   / /    \  / / /    __/ /   [Version]  :  1.0
 / __/  ___/ / /_/ / /____/ // /___  / /     / / / /___ / __/    [Patched]  :  N/A
/_/    /____/\____/\____/___/_____/ /_/     /_/  \____//____/    [Revolt]   :  https://rvlt.gg/sb4jwq9G
        
            [ Windows Remote Administration Tool ]
              [ https://github.com/madanokr001 ]
                  [ https://t.me/cybermads ]
          """)

def convert(image_path):
    try:
        img = Image.open(image_path) 
        icon_path = "whiterose.ico"
        img.save(icon_path, "ICO") 
        return icon_path
    except Exception as e:
        print("FAILD")
        return None

def build():
    icon_path = convert(icon)  
    if icon_path is None:
        print("FAILD")
        return

    os.system(f'pyinstaller --onefile --clean --name {exe} --icon {icon_path} --noconsole bot.py')

    exepath = f"dist/{exe}.exe"
    lib = "PAYLOAD"

    if not os.path.exists(lib):
        os.makedirs(lib)

    if os.path.exists(exepath):
        shutil.copy(exepath, os.path.join(lib, f"{exe}.exe"))

    if os.path.exists("dist"):
        shutil.rmtree("dist")
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists(f"{exe}.spec"):
        os.remove(f"{exe}.spec")

    if os.path.exists(icon_path):
        os.remove(icon_path)

    print("Done.")
    input()

if __name__ == "__main__":
    fsociety()
    exe = input("""
[FSOCIETY] ENTER THE EXE FILE NAME
                        
┌──(root@FSOCIETY)-[C2]
└─# """)

    icon = input("""
[FSOCIETY] ENTER THE ICON IMAGE FILE PATH (LOCAL FILE PATH)
                 
┌──(root@DARK-4RMY)-[C2]
└─# """)
    
    build()    
