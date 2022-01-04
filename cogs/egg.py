"""
############################################################################################
 Commands
 * search     - Pull a little bit of potentially useful information from a users backup
 * ecalc      - Calculate a hypothetical EB based on input.
 * update     - Force the leaderboard to update right away.
 * addaccount - Add an EID to your account.
############################################################################################
"""

# Imports
import discord
from discord.ext import commands
import tools as t
from discord.commands import Option, permissions
from decimal import Decimal
import ei as e


class Egg(commands.Cog, name="Egg Server Functions"):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="search", guild_ids=[901328556603367446])
    async def search(self, ctx, eid: Option(str, "EID of person to search.")):
        searchChannel = self.bot.get_channel(927716139302268968)
        if searchChannel == ctx.channel:
            #try:
                if eid == "EI5450109629759488":
                    return
                search = e.firstContactRequest(eid)
                username = search['backup']['userName']
                tier1info = f"```{eid} | {username}```"

                boostsUsed = search["backup"]['stats']['boostsUsed']
                goldenEggsSpent = search['backup']['game']['goldenEggsSpent']
                goldenEggsEarned = search['backup']['game']['goldenEggsEarned']
                timeCheats = search['backup']['game']['totalTimeCheatsDetected']

                tier2info = f"```# of Boosts Used: {boostsUsed}\nGolden Eggs Spent: {goldenEggsSpent}\nGolden Eggs Earned: {goldenEggsEarned}\nTime Cheats Detected: {timeCheats}```"
                boostInfo = "```BOOST INFO\n"
                boostList = search["backup"]["game"]["boosts"]
                for boost in boostList:
                    boostInfo += f"{boost['boostId']}: {boost['count']}\n"
                responseMessage = tier1info + tier2info + boostInfo + "```"
                await ctx.respond(responseMessage)
            #except:
            #    await ctx.respond("Something went wrong, double check EID entered")
        else:
            await ctx.respond("That command may not be used in this channel.")

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
        souleggs = t.formatLargeNumber(souleggs)
        results = t.calculateEB(souleggs, prophecyeggs, prophecybonus, soulfood, humanreadable)
        if results == False:
            await ctx.respond(f"Something went wrong when calculating...```Soul Eggs: {souleggs}\nProphecy Eggs: {prophecyeggs}\nProphecy Bonus: {prophecybonus}\nSoul Food: {soulfood}```")
        elif results == "E1":
            await ctx.respond("Must enter 1 or more Soul Eggs.")
        else:
            messageToSend = f"Results:```Soul Eggs: {souleggs}\nProphecy Eggs: {prophecyeggs}\nProphecy Bonus: {prophecybonus}\nSoul Food: {soulfood}\n\nEarnings Bonus: {results}%```"
            await ctx.respond(messageToSend)

    @commands.slash_command(name='addaccount', guild_ids=[901328556603367446])
    async def addAccount(self, ctx, eid: Option(str, "What is your EID")):
        result = t.addAccount(eid, ctx.author.display_name, ctx.author.id)
        if result == True:
            await ctx.respond("Added account.")
        else:
            await ctx.respond("Something went wrong.")

    # Update a user's egg data
    @commands.slash_command(name='update', guild_ids=[901328556603367446], default_permission=False)
    @permissions.has_role(902679876065181708) # 902679876065181708 Is Update Perms
    async def update(self, 
                     ctx):
        """Update the leaderboard"""
        await ctx.respond("Working...", ephemeral=True)
        leaderboardChannel = self.bot.get_channel(901710731848867900) # Get the #leaderboard channel
        sortedLeaderboard = t.updateLeaderboard() # Collect the current leaderboard stats
        countingNumber = 0 # Counting number for place values on leaderboard
        embedLimitCounter = 0 # Limit counter to avoid accidentlly adding too many fields to the embed
        initialLeaderboardEmbed = discord.Embed(title = "Leaderboard", color=0xb3e4f4) # Create the leaderboard embed
        await leaderboardChannel.purge(limit=100) # Clear out any messages currently in #leaderboard
        for x in sortedLeaderboard: # For each group (N,o,S,s,Q,q,t,b,m,other) in the leaderboard
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
   
def setup(bot):
    bot.add_cog(Egg(bot))
