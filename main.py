# Imports
import discord
from discord.ext import commands
import tools as t

# Config Variables
extensions = t.load('cogs') # Which cogs to load


bot = commands.Bot(command_prefix=t.botPrefix,
                   description=t.botName,
                   case_insensitive=True)

if __name__ == '__main__':
    bot.remove_command('help')
    for x in extensions:
        bot.load_extension(x)

@bot.event
async def on_ready():
    botStatus = discord.Status.online
    botActivity = discord.Game(name=t.load('displayGame'))
    await bot.change_presence(status=botStatus, activity=botActivity)
    print("Successfully logged in and booted... Now go fix some bugs!")

bot.run(t.load("token"))
