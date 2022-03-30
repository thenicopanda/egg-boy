# Imports
import discord, random, logging
from discord.ext import commands, tasks
from discord.utils import get
import tools as t
from decimal import Decimal
from math import trunc

# Config Variables
extensions = t.load('cogs') # Which cogs to load
gameList = t.load("displayGame") # List of games to cycle through

logging.basicConfig(filename="logs.txt", filemode="w", level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

bot = commands.Bot(command_prefix=t.botPrefix,
                   description=t.botName,
                   case_insensitive=True)

if __name__ == '__main__':
    bot.remove_command('help')
    for x in extensions:
        x = f"cogs.{x}"
        bot.load_extension(x)


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.dnd)
    logging.info('Sucessfully logged in.')
    print("Successfully logged in and booted... Now go fix some bugs!")
    if not changeStatus.is_running():
        changeStatus.start()

@tasks.loop(minutes=2)
async def changeStatus():
    await bot.change_presence(activity=discord.Game(random.choice(gameList)))

@bot.event
async def on_error(event, *args, **kwargs):
    message = args[0]
    logging.warning(event + message)


@bot.listen()
async def on_message(message):
    
    if t.load("countingChannel"):
        c_channel = bot.get_channel(t.load("countingChannel"))
        messages = await c_channel.history(limit=2).flatten()
        if message.channel == c_channel:
            if message.author == messages[1].author:
                await message.author.send("Only one message in a row.. Naughty Naughty..")
                await message.delete()
                return
            try:
                if int(messages[1].content) + 1 != int(message.content):
                    await message.author.send(f"Do you not know how to count??? {message.content} does not come after {messages[1].content} https://cdn.discordapp.com/attachments/901328556603367449/934295874299912192/unknown.png")
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
            if t.is_square(int(message.content)):
                emojis = ['🇸', '🇶', '🇺', '🇦', '🇷', '🇪', '🇩']
                numbers = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']
                squareRoot = trunc(t.is_square(int(message.content)))
                usedDigits = []
                for digit in str(squareRoot):
                    if numbers[int(digit)] in usedDigits:
                        if "🔁" in usedDigits:
                            await message.add_reaction("🔂")
                            usedDigits.append("🔂")
                        else:
                            await message.add_reaction("🔁")
                            usedDigits.append("🔁")
                    else:
                        await message.add_reaction(numbers[int(digit)])
                        usedDigits.append(numbers[int(digit)])

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
            if str(message.content).endswith('00'):
                await message.add_reaction("💯")
                return
    if message.content == "chaos":
        await message.reply("Chaos?! I love chaos!")

bot.run(t.load("token"))
