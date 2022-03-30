# Imports
import discord, random
from discord.ext import commands, tasks
from discord.utils import get
import tools as t
from decimal import Decimal

# Config Variables
gameList = t.load("displayGame") # List of games to cycle through


bot = commands.Bot(command_prefix=t.botPrefix,
                   description=t.botName,
                   case_insensitive=True)

if __name__ == '__main__':
    bot.remove_command('help')



@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online)
    print("Successfully logged in and booted... Now go fix some bugs!")
    if not changeStatus.is_running():
        changeStatus.start()



@tasks.loop(minutes=5)
async def changeStatus():
    """Update the leaderboard and change the bot game every 7 minutes"""
    t.updateAllUsers()
    guild = bot.get_guild(901328556603367446)
    await bot.change_presence(activity=discord.Game("Updating Board(s)"))
    leaderboardChannel = bot.get_channel(901710731848867900) # Get the #leaderboard channel
    sortedLeaderboard = t.updateLeaderboard() # Collect the current leaderboard stats
    countingNumber = 0 # Counting number for place values on leaderboard
    embedLimitCounter = 0 # Limit counter to avoid accidentlly adding too many fields to the embed
    initialLeaderboardEmbed = discord.Embed(title = "Leaderboard", color=0xb3e4f4) # Create the leaderboard embed
    await leaderboardChannel.purge(limit=100) # Clear out any messages currently in #leaderboard
    for x in sortedLeaderboard: # For person in the leaderboard
        countingNumber += 1 # Add one to the Counting Number
        embedLimitCounter += 1 # Add one to the Embed Limit Number
        if embedLimitCounter == 26: # If there are 25 fields on the embed already
            await leaderboardChannel.send(embed=initialLeaderboardEmbed) # Send the first embed
            embedLimitCounter = 0 # Reset the embed limit
            initialLeaderboardEmbed = discord.Embed(color=0xb3e4f4) # Create a new leaderboard embed
        try: 
            member = await guild.fetch_member(x["discord"])
            
            role = get(guild.roles, name=x['rank'])
            await member.add_roles(role, reason="Leaderboard Update.")
        except:
            print(f"Could not give role '{x['rank']}' to {x['discord']}")
        eb = t.human_format(Decimal(x["eb"]))
        embedTitle = "{}. {}".format(countingNumber, member.display_name) # Set the title of the embed field
        initialLeaderboardEmbed.add_field(name=embedTitle, value=f"{eb}%", inline=False) # add the field to the embed
    await leaderboardChannel.send(embed=initialLeaderboardEmbed) # send any leftover embeds
    



    soulLeaderboardChannel = bot.get_channel(943762108087160842) # Get the #leaderboard channel
    sortedSoulLeaderboard = t.updateSoulLeaderboard() # Collect the current leaderboard stats
    countingNumber = 0 # Counting number for place values on leaderboard
    embedLimitCounter = 0 # Limit counter to avoid accidentlly adding too many fields to the embed
    initialSoulLeaderboardEmbed = discord.Embed(title = "Soul Egg Leaderboard", color=0xb3e4f4) # Create the leaderboard embed
    await soulLeaderboardChannel.purge(limit=100) # Clear out any messages currently in #leaderboard
    for x in sortedSoulLeaderboard: # For person in the leaderboard
        countingNumber += 1 # Add one to the Counting Number
        embedLimitCounter += 1 # Add one to the Embed Limit Number
        if embedLimitCounter == 26: # If there are 25 fields on the embed already
            await soulLeaderboardChannel.send(embed=initialSoulLeaderboardEmbed) # Send the first embed
            embedLimitCounter = 0 # Reset the embed limit
            initialSoulLeaderboardEmbed = discord.Embed(color=0xb3e4f4) # Create a new leaderboard embed
        try: 
            member = await guild.fetch_member(x["discord"])
        except:
            pass
        soulEggs = t.human_format(Decimal(x["soulEggs"]))
        embedTitle = "{}. {}".format(countingNumber, member.display_name) # Set the title of the embed field
        initialSoulLeaderboardEmbed.add_field(name=embedTitle, value=f"{soulEggs} Soul Eggs", inline=False) # add the field to the embed
    await soulLeaderboardChannel.send(embed=initialSoulLeaderboardEmbed) # send any leftover embeds
    
    
    
    
    await bot.change_presence(activity=discord.Game(random.choice(gameList)))




bot.run(t.load("leaderboardToken"))
