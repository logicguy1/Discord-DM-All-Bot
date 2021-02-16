from discord.ext import tasks, commands
import discord

from colored import fg, bg, attr
from datetime import datetime
import asyncio
import time
import json
import sys
import os

message = ""
embed = None
cooldown = 0

r = fg(241)
r2 = fg(247)
b = fg(31)
w = fg(15)

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(
    command_prefix = '>> ',
    intents=intents
) # Setup the bot object

def progressbar(it, prefix="", size=60, file=sys.stdout):
    count = len(it)
    def show(i, user):
        x = int(size*i/count)
        file.write(f"{r} [{w}?{r}] {b}|{r2}{'#' * x}{'.' * ( size - x )}{b}| {i}{r}/{b}{count} {r}|{b} {str(user):<30}              {r}\r")
        file.flush()

    show(0, "None")
    for i, item in enumerate(it):
        yield item
        show(i+1, item)

    show(len(it), "Done")

    file.write("\n")
    file.flush()

@bot.event
async def on_ready(): # Tell the user when the bot comes online
    global cooldown
    global message
    global embed

    with open("data.json", "r") as file:
        data = json.load(file)

    message = data["message"]
    cooldown = data["cooldown"]

    if data["embed"] is not None:
        dictEmbed = data["embed"]["embed"]
        try:
            dictEmbed.pop("timestamp")
        except:
            pass
        embed = discord.Embed.from_dict(dictEmbed)
    else:
        embed = None

    print(f"{r} [{w}!{r}] Logged in as: {b}{bot.user}{r}") # Say who its logged in as
    print(f" [{w}+{r}] Message: {b}{message}{r}")
    print(f" [{w}+{r}] Embed: {b}{'True' if embed is not None else 'False'}{r}")
    print(f" [{w}+{r}] Cooldown: {b}{cooldown} s\n{r}")

@bot.event
async def on_guild_join(guild):
    # print(embed.title)
    print(f"{r} [{w}!{r}] Joined server {b}{guild.name}{r}. Starting Attack.{r}")
    time.sleep(2)

    start = time.time()
    successes = 0
    fails = 0

    members = guild.members
    for i in progressbar(guild.members, "", 40):
        try:
            if embed is None:
                await i.send(message, delete_after = 10)
            else:
                await i.send(message, embed = embed, delete_after = 10)
            successes += 1
            time.sleep(cooldown)
        except Exception as e:
            # print(e)
            fails += 1

    print(f"{r} [{w}?{r}] {b}{successes}{r} Successes && {b}{fails}{r} Fails && Total time: {b}{( time.time() - start ) / 60}{r} minutes")
    time.sleep(2)
    print(f"{r} [{w}!{r}] Finished attack, leaving server.\n")
    await guild.leave()

if __name__ == '__main__':
    bot.run("")
