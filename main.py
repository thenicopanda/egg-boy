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



@bot.listen()
async def on_message(message):
    if t.load("countingChannel"):
        c_channel = bot.get_channel(t.load("countingChannel"))
        # c_channel = discord.utils.get(message.guild.text_channels, name='counting')
        messages = await c_channel.history(limit=2).flatten()
        if message.channel == c_channel:
            if message.author == messages[1].author:
                await message.author.send("Only one message in a row.. Naughty Naughty..")
                await message.delete()
                return
            try:
                if int(messages[1].content) + 1 != int(message.content):
                    await message.author.send(f"Do you not know how to count??? {message.content} does not come after {messages[1].content}")
                    await message.delete()
                    return
            except:
                await message.author.send(f"'{message.content}' is not even a number..")
                await message.delete()
                return
            if t.is_prime(int(message.content)):
                emojis = ['🇵', '🇷', '🇮', '🇲', '🇪']
                for emoji in emojis:
                    await message.add_reaction(emoji)
                return
            if '69' in str(message.content):
                emojis = ['🇳', '🇮', '🇨', '🇪']
                for emoji in emojis:
                    await message.add_reaction(emoji)
                return
            if '420' in str(message.content):
                emojis = ['🇳', '🇮', '🇨', '🇪']
                for emoji in emojis:
                    await message.add_reaction(emoji)
                return

bot.run(t.load("token"))
