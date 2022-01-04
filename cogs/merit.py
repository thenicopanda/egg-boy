"""
####################################################
 Commands
 * addmerit - Add a merit to a user of your choice
 * merits - get a list of your merits
 * remmerit = Remove a person's merit if needed (Mod Role Required)

 User Command
 * Merits - same as /merits
####################################################
"""

# Imports
import discord
from discord.ext import commands
import tools as t
from discord.commands import Option, permissions


# Set the moderator role
modrole = t.load('modRole')

class Merits(commands.Cog, name="Merits"):
    def __init__(self, bot):
        self.bot = bot


    @commands.slash_command(name="addmerit",
                            guild_ids=[901328556603367446])
    async def addmerit(self,
                       ctx,
                       who: Option(discord.Member, "Who is getting the merit?"),
                       why: Option(str, "Why is this person getting a merit?")):
        """Give another user a merit."""
        if who.id != ctx.author.id:
            t.addMerits(who.id, why)
            await ctx.respond(f"Merit '`{why}`' given to {who.mention} successfully!")
            meritLogChannel = self.bot.get_channel(t.load("meritLogChannel"))
            await meritLogChannel.send(f"{who.mention}: `{why}`")
        else:
            await ctx.respond("Stop it you greedy bastard.")
    
    @commands.slash_command(name="merits",
                            guild_ids=[901328556603367446])
    async def merits(self, ctx,
                     who: Option(discord.Member, "Who are you checking??", required=False, default=None)
                     ):
        """Get a list of your merits."""
        if who == None:
            userid = ctx.author.id
            meritString = f"Current list of Merits for {ctx.author.display_name}:"
        else: 
            userid = who.id
            meritString = f"Current list of Merits for {who.display_name}:"
        merits = t.loadMerits(userid)
        if merits != False:
            meritNumber = 1
            for merit in merits:
                meritString += f"\n{meritNumber}. `{merit}`"
                meritNumber += 1
            await ctx.respond(meritString)
        else:
            await ctx.respond("You do not have any merits quite yet.")
        
    @commands.slash_command(name="remmerit", guild_ids=[901328556603367446])
    @permissions.has_role(modrole)
    async def remmerrit(self, ctx,
                        who: Option(discord.Member, "Who are you removing a merit from?", required=True),
                        which: Option(int, "Which one? (Number)")):
        """Remove a merit from someone."""
        response = t.removeMerit(who.id, which)
        if response == 1:
            await ctx.respond("That is not a valid number.", ephemeral = True)
        elif response == 2:
            await ctx.respond("User currently has no merits.", ephemeral = True)
        elif response == 3:
            await ctx.respond("Merit removed successfully!", ephemeral = True)
            if t.load("modLogChannel"):
                modLogChannel = self.bot.get_channel(t.load("modLogChannel"))
                logEmbed = discord.Embed().set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url).add_field(name="Merit Deleted", value= f"Deleted one of {who.mention}'s merits.", inline=False)
                await modLogChannel.send(embed=logEmbed)
        else: 
            await ctx.respond("Something went wrong...", ephemeral = True)


    @commands.user_command(name="Merits",
                            guild_ids=[901328556603367446])
    async def merits(self, ctx,
                     who: discord.Member
                     ):
        """Get a list of your merits."""
        userid = who.id
        meritString = f"Current list of Merits for {who.display_name}:"
        merits = t.loadMerits(userid)
        if merits != False:
            meritNumber = 1
            for merit in merits:
                meritString += f"\n{meritNumber}. `{merit}`"
                meritNumber += 1
            await ctx.respond(meritString)
        else:
            await ctx.respond("You do not have any merits quite yet.")
        
def setup(bot):
    bot.add_cog(Merits(bot))
