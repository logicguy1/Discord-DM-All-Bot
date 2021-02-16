import json
import time
import bot
import os

from colored import fg, bg, attr

r = fg(241) # Setup color variables
r2 = fg(255)
b = fg(31)
w = fg(15)

class DMAllBot: # Initialise the class
    def main(self): # Main function, holds the main code
        os.system('cls' if os.name == 'nt' else 'clear') # Clear the screen
        print(f""" {r2} █████{b}╗{r2} ███{b}╗{r2}   ██{b}╗{r2} ██████{b}╗{r2} ███{b}╗{r2}   ██{b}╗{r2}██{b}╗{r2}██{b}╗{r2}  ██{b}╗{r2}
 ██{b}╔══{r2}██{b}╗{r2}████{b}╗  {r2}██{b}║{r2}██{b}╔═══{r2}██{b}╗{r2}████{b}╗  {r2}██{b}║{r2}██{b}║╚{r2}██{b}╗{r2}██{b}╔╝{r2}
 ███████{b}║{r2}██{b}╔{r2}██{b}╗ {r2}██{b}║{r2}██{b}║   {r2}██{b}║{r2}██{b}╔{r2}██{b}╗ {r2}██{b}║{r2}██{b}║ ╚{r2}███{b}╔╝{r2}
 ██{b}╔══{r2}██{b}║{r2}██{b}║╚{r2}██{b}╗{r2}██{b}║{r2}██{b}║   {r2}██{b}║{r2}██{b}║╚{r2}██{b}╗{r2}██{b}║{r2}██{b}║ {r2}██{b}╔{r2}██{b}╗{r2}
 ██{b}║  {r2}██{b}║{r2}██{b}║ ╚{r2}████{b}║╚{r2}██████{b}╔╝{r2}██{b}║ ╚{r2}████{b}║{r2}██{b}║{r2}██{b}╔╝ {r2}██{b}╗{r2}
 {b}╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝╚═╝  ╚═╝
                                                        """) # Print the title card

        time.sleep(2) # Wait a few seconds
        self.slow_type(f"{r} [{w}+{r}] DMAllBot made by: {b}Drillenissen#4268{r} && {b}Benz#1001", .02) # Print who developed the code
        time.sleep(1) # Wait a little more
        self.slow_type(f"{r} [{w}?{r}] Input the bot Discord token: {b}", .02, newLine = False)
        token = input("").strip() # Get the discord token

        self.slow_type(f"{r} [{w}?{r}] Input the message to post: {b}", .02, newLine = False) # Ask for a message to dm
        message = input("") # Wait for an awnser
        self.slow_type(f"{r} [{w}?{r}] Do you wish yo use embeds? (Y/n): {b}", .02, newLine = False) # Ask for a message to dm
        emb = input("") # Wait for an awnser

        if "y" in emb.lower(): # Check if "y" is in the responce 
            data = self.emb_setup() # Run the embed setup function
        else: # Otherwise
            data = None # Set the embed as None

        self.slow_type(f"{r} [{w}?{r}] Set a cooldown ( Seconds ): {b}", .02, newLine = False) # Ask for a message to dm
        cooldown = int(input("")) # Wait for an awnser


        with open("data.json", "w") as josnFile: # Open the file used to pass data into the bot
            json.dump( # Dump the requed data
                {
                  "message" : f"{message}​",
                  "embed" : data,
                  "cooldown" : cooldown
                },
                josnFile
            )

        print(r) # Reset the color
        self.start(token) # Start the bot using the start code

    def slow_type(self, text, speed, newLine = True): # Function used to print text a little more fancier
        for i in text: # Loop over the message
            print(i, end = "", flush = True) # Print the one charecter, flush is used to force python to print the char
            if i not in f"{r}{r2}{b}{w}":
                time.sleep(speed) # Sleep a little before the next one
        if newLine: # Check if the newLine argument is set to True
            print() # Print a final newline to make it act more like a normal print statement

    def emb_setup(self): # The function to setup embeds
        with open("EMBED.json", "w") as file: # Create the file embed.json
            file.write("") # Write an empty line in it

        self.slow_type(f"{r} [{w}!{r}] Place your embed data in the new file {b}\"EMBED.json\"{r} Press enter when done {b}", .02, newLine = False) # Tell the user to put the embed data in the file
        message = input("") # Wait for an awnser

        with open("EMBED.json", "r") as file: # Open the file agein in read mode
            data = json.load(file) # Read the file using a json parser

        os.remove("EMBED.json") # Remove the file
 
        return data # Return the data as a dict


    def start(self, token): # Function used to start the main bot
        Bot = bot.bot # Initialise the bot object ( This is a discord bot )

        Bot.run( # Run the bot with the token etc
            token
        )

if __name__ == '__main__': # If the file is getting ran directly
    DMClient = DMAllBot() # Create the sniper class
    DMClient.main() # Run the main function
