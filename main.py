# Imports
import discord, random
from discord.ext import commands, tasks
import tools as t
from decimal import Decimal

# Config Variables
extensions = t.load('cogs') # Which cogs to load
gameList = t.load("displayGame") # List of games to cycle through


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
    await bot.change_presence(status=discord.Status.online)
    print("Successfully logged in and booted... Now go fix some bugs!")
    changeStatus.start()


@tasks.loop(minutes=7)
async def changeStatus():
    """Update the leaderboard and change the bot game every 7 minutes"""
    await bot.change_presence(activity=discord.Game(random.choice(gameList)))
    leaderboardChannel = bot.get_channel(901710731848867900) # Get the #leaderboard channel
    sortedLeaderboard = t.updateLeaderboard() # Collect the current leaderboard stats
    countingNumber = 0 # Counting number for place values on leaderboard
    embedLimitCounter = 0 # Limit counter to avoid accidentlly adding too many fields to the embed
    initialLeaderboardEmbed = discord.Embed(title = "Leaderboard", color=0xb3e4f4) # Create the leaderboard embed
    await leaderboardChannel.purge(limit=100) # Clear out any messages currently in #leaderboard
    for x in sortedLeaderboard: # For person in the leaderboard
        countingNumber += 1 # Add one to the Counting Number
        embedLimitCounter += 1 # Add one to the Embed Limit Number
        if embedLimitCounter == 25: # If there are 25 fields on the embed already
            await leaderboardChannel.send(embed=initialLeaderboardEmbed) # Send the first embed
            embedLimitCounter = 0 # Reset the embed limit
            initialLeaderboardEmbed = discord.Embed(color=0xb3e4f4) # Create a new leaderboard embed

        eb = t.human_format(Decimal(x["eb"]))
        embedTitle = "{}. {}".format(countingNumber, x["nickname"]) # Set the title of the embed field
        initialLeaderboardEmbed.add_field(name=embedTitle, value=eb, inline=False) # add the field to the embed
    await leaderboardChannel.send(embed=initialLeaderboardEmbed) # send any leftover embeds


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
