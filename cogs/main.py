"""
####################################################
 Commands
 * info  - Give some basic info about the bot
 * ping  - Give basic information about the bot
 * cleardms - clear the bots dms to you
####################################################
"""

# Imports
import discord
from discord.ext import commands
import tools as t

# Set the moderator role
modrole = t.load('modRole')

class Main(commands.Cog, name="Core Functions"):
    def __init__(self, bot):
        self.bot = bot
    

    # Get some basic info about the bot
    @commands.slash_command(name='info', 
                            guild_ids=[901328556603367446]
                            )
    async def information(self, ctx):
        """Give basic information about the bot"""
        embed = discord.Embed(title = t.botName, description = "Made by Alex(aka: TheNicoPanda)", color=0xffffff)
        embed.add_field(name='Github: ', value='Will be available when bot is finished.')
        await ctx.respond(embed=embed, ephemeral=True)


    # Check the bot's ping
    @commands.slash_command(name='ping', 
                            guild_ids=[901328556603367446]
                            )
    async def ping(self, ctx):
        """Return the bot's latency"""
        newLatency = self.bot.latency * 1000
        await ctx.respond(f"Pong! {round(newLatency)} ms", ephemeral=True)


    @commands.slash_command(name="cleardms", guild_ids=[901328556603367446])
    async def cleardms(self, ctx):
        """Clear up to the past 100 dms I've sent you."""
        dmchannel = await ctx.author.create_dm()
        async for message in dmchannel.history(limit=100):
            if message.author == self.bot.user:
                await message.delete()
        await ctx.respond("Done.", ephemeral=True)

def setup(bot):
    bot.add_cog(Main(bot))
