import os
import sys
import json
from dotenv import load_dotenv
import discord

load_dotenv()

if len(sys.argv) > 1:
    os.chdir(sys.argv[1])

intents = discord.Intents().all()
bot = discord.Bot(intents=intents)
config = json.loads(open("config/config.json", "r").read())
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    for box in config["boxes"]:
        user = await bot.fetch_user(box["discord_uid"])
        url = "http://boxes.dunhack.me:"+str(box["port"])
        pwd = box["novnc_password"]
        msg = f"Your box is available at {url}\nYour password is: {pwd}"
        await user.send(msg)
        print(f"sent message to {user}")
    await bot.logout()

bot.run(token=os.getenv("TOKEN"))
        


