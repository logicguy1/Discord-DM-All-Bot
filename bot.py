from discord.ext import tasks, commands
import discord

from colored import fg, bg, attr
from datetime import datetime
import asyncio
import time
import json
import sys
import os

message = "" # Initialise a few variables to use later
embed = None
cooldown = 0

r = fg(241) # Setup the diffrent color variables
r2 = fg(247)
b = fg(31)
w = fg(15)

intents = discord.Intents.default() # Setup permissions for the bot to be able to see all the members in a server
intents.members = True

bot = commands.Bot( # Setup the bot object
    command_prefix = '>> ',
    intents=intents
) 

def progressbar(it, prefix="", size=60, file=sys.stdout): # Setup the progress bar to be used later
    count = len(it) # Get the lenght of the loop
    def show(i, user): # Define a function to show the current progress bar
        x = int(size * i / count) # Get the lenght of the bar
        
        file.write(f"{r} [{w}?{r}] {b}|{r2}{'#' * x}{'.' * ( size - x )}{b}| {i}{r}/{b}{count} {r}|{b} {str(user):<30}              {r}\r") 
        file.flush() # Print out the bar

    show(0, "None") # Show the bar empty
    for i, item in enumerate(it): # Loop over the iterator
        yield item # Yield the item allowing us to loop over the function later
        show(i+1, item) # Show the progress bar at its current state

    show(len(it), "Done") # Show the progress bar is done

    file.write("\n") # Flush the newline
    file.flush()

@bot.event
async def on_ready(): # Tell the user when the bot comes online
    global cooldown # Globalise variables we need to use later
    global message  # This is needed since if we change them here they will be private variables
    global embed

    with open("data.json", "r") as file: # Open the data.json file 
        data = json.load(file) # Load the data using a json parser

    message = data["message"] # Get the message to send
    cooldown = data["cooldown"] # And the cooldown

    if data["embed"] is not None: # Check if the embed has a value
        dictEmbed = data["embed"]["embed"] # Get the embed
        try: # We want to catch any errors that might come up
            dictEmbed.pop("timestamp") # Remove the timestamp since that wont work properbly
        except: # If we get an error and the provided data does not have a timestamp key
            pass # Do nothing
        embed = discord.Embed.from_dict(dictEmbed) # Create the embed variable from the data

    print(f"{r} [{w}!{r}] Logged in as: {b}{bot.user}{r}") # Say who its logged in as
    print(f" [{w}+{r}] Message: {b}{message}{r}") # Tell the user the message
    print(f" [{w}+{r}] Embed: {b}{'True' if embed is not None else 'False'}{r}") # If it has a embed or not
    print(f" [{w}+{r}] Cooldown: {b}{cooldown}s\n{r}") # Tell the cooldown

@bot.event
async def on_guild_join(guild): # If the bot joins a guild
    print(f"{r} [{w}!{r}] Joined server {b}{guild.name}{r}. Starting Attack.{r}") # Warn the user its about to start an attack
    time.sleep(2) # Wait a bit

    start = time.time() # Start a timer
    successes = 0 # Setup a counter for the successfull attempts
    fails = 0 # And one for the unsuccessfull attempts

    members = guild.members # Get all the members of the guild
    for i in progressbar(guild.members, "", 40): # Loop over the members in the guild
        try: # Try to send the message
            if embed is None: # Check if there is an embed
                await i.send(message) # Send the message without an embed
            else: # Or if there is an embed
                await i.send(message, embed = embed) # Send the message with an embed
            successes += 1 # Increase the successes with one
            time.sleep(cooldown) # Wait for the cooldown
        except Exception as e: # If there happens an error
            # print(e)
            fails += 1 # Increase fails by one

    print(f"{r} [{w}?{r}] {b}{successes}{r} Successes && {b}{fails}{r} Fails && Total time: {b}{( time.time() - start ) / 60}{r} minutes") # Give a report of the results
    time.sleep(2) # Wait 2 seconds
    print(f"{r} [{w}!{r}] Finished attack, leaving server.\n") # Warn the user its about to leave a guild
    await guild.leave() # Leave the guild

if __name__ == '__main__': # If the file is getting ran directly
    bot.run("") # Run the bot
