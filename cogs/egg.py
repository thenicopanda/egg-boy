"""
############################################################################################
 Commands
 * ecalc    - Calculate a hypothetical EB based on input.
 * update   - Update a user's stats in the users.json file (Update Perm Required)
############################################################################################
"""

# Imports
import discord
from discord.ext import commands
import tools as t
from discord.commands import Option, permissions


class Egg(commands.Cog, name="Egg Server Functions"):
    def __init__(self, bot):
        self.bot = bot


    @commands.slash_command(name='ecalc', guild_ids=[901328556603367446])
    async def ecalc(self,
                    ctx,
                    souleggs: Option(str, "How many Soul Eggs?"),
                    prophecyeggs: Option(int, "How many Prophecy Eggs?"),
                    prophecybonus: Option(int, "How many Prophecy Bonus levels? (Ingame max is 5 at the moment)", required = False, default = 5),
                    soulfood: Option(int, "How many Soul Food levels? (Ingame max is 140 at the moment)", required = False, default = 140),
                    humanreadable: Option(bool, "True for preformatted, False for exact numbers", required = False, default = True, options = [True, False])
                    ):
        """Calculate EB based on values you enter."""
        results = t.calculateEB(souleggs, prophecyeggs, prophecybonus, soulfood, humanreadable)
        if results == False:
            await ctx.respond(f"Something went wrong when calculating...```Soul Eggs: {souleggs}\nProphecy Eggs: {prophecyeggs}\nProphecy Bonus: {prophecybonus}\nSoul Food: {soulfood}```")
        elif results == "E1":
            await ctx.respond("Must enter 1 or more Soul Eggs.")
        else:
            messageToSend = f"Results:```Soul Eggs: {souleggs}\nProphecy Eggs: {prophecyeggs}\nProphecy Bonus: {prophecybonus}\nSoul Food: {soulfood}\n\nEarnings Bonus: {results}%```"
            await ctx.respond(messageToSend)


    # Update a user's egg data
    @commands.slash_command(name='update', guild_ids=[901328556603367446], default_permission=False)
    @permissions.has_role(902679876065181708) # 902679876065181708 Is Update Perms
    async def update(self, 
                     ctx, 
                     person: Option(discord.User, "@ of the user you'd like to update" ), 
                     eb: Option(float, "Their EB (ex: 123.456)"), 
                     letter: Option(str, "The letter their EB ends with", choices=["none", "k", "m", "b", "t", "q", "Q", "s", "S", "o", "N", "d"]) 
                     ):
        """Update a users information."""
        t.UpdateEggUser(person.id, person.display_name, eb, letter, 0, 0) # Push the users new stats into the JSON file
        returnChannel = self.bot.get_channel(902674849082773544) # Grab the #update-output channel
        embed=discord.Embed(title="New Stats") # Create the Embed + Add a title to it
        embed.set_author(name=person.display_name, icon_url=person.avatar.url) # Set the author of the embed as the person who got updated
        embed.add_field(name="Earnings Bonus %", value=str(eb) + letter, inline=False) # Add the EB field
        await returnChannel.send(embed=embed) # Send embed in #update-output
            
        leaderboardChannel = self.bot.get_channel(901710731848867900) # Get the #leaderboard channel
        sortedLeaderboard = t.updateLeaderboard() # Collect the current leaderboard stats
        countingNumber = 0 # Counting number for place values on leaderboard
        embedLimitCounter = 0 # Limit counter to avoid accidentlly adding too many fields to the embed
        initialLeaderboardEmbed = discord.Embed(title = "Leaderboard", color=0xb3e4f4) # Create the leaderboard embed
        await leaderboardChannel.purge(limit=100) # Clear out any messages currently in #leaderboard
        for x in sortedLeaderboard: # For each group (N,o,S,s,Q,q,t,b,m,other) in the leaderboard
            for y in x: # For user in group
                countingNumber += 1 # Add one to the Counting Number
                embedLimitCounter += 1 # Add one to the Embed Limit Number
                if embedLimitCounter == 25: # If there are 25 fields on the embed already
                    await leaderboardChannel.send(embed=initialLeaderboardEmbed) # Send the first embed
                    embedLimitCounter = 0 # Reset the embed limit
                    initialLeaderboardEmbed = discord.Embed(color=0xb3e4f4) # Create a new leaderboard embed
                data = y[1] # Open the user like a fish
                eb = data["eb"] # Collect EB
                letter = data["letter"] # Collect Letter
                eb = str(eb) + letter # Combine letter and EB
                nickname = data['nickname'] # Collect Nickname
                embedTitle = "{}. {}".format(countingNumber, nickname) # Set the title of the embed field
                initialLeaderboardEmbed.add_field(name=embedTitle, value=eb, inline=False) # add the field to the embed
        await leaderboardChannel.send(embed=initialLeaderboardEmbed) # send any leftover embeds
        await ctx.respond("Thank you!", ephemeral=True)
   
def setup(bot):
    bot.add_cog(Egg(bot))
