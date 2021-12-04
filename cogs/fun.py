"""
####################################################
 Commands
 * headsOrTails - Return Either Heads or Tails
 * 8ball - Return an Eight Ball Response
####################################################
"""

# Imports
import discord, random, requests, json
from discord.ext import commands
from discord.commands import Option
import tools as t


class Fun(commands.Cog, name="Fun Stuff"):
    #  Initialize the Cog
    def __init__(self, bot):
        self.bot = bot
    


    @commands.slash_command(name='headsortails',
                            guild_ids=[901328556603367446]
                            )
    async def headsOrTails(self, ctx):
        """Return Either Heads or Tails"""
        hOrT = random.randint(0, 1) #  Heads or Tails
        if hOrT == 0:
            await ctx.respond("Heads!")
        else:
            await ctx.respond("Tails!")


    @commands.slash_command(name='8ball',
                            guild_ids=[901328556603367446])
    async def eightball(self, ctx):
        """Return an Eight Ball Response"""
        responses = {
                0: "It is certain.",
                1: "It is decidedly so.",
                2: "Without a doubt.",
                3: "Yes, definitely.",
                4: "You may rely on it.",
                5: "As I see it, yes.",
                6: "Most likely.",
                7: "Outlook good.",
                8: "Yes.",
                9: "Signs point to yes.",
                10: "Reply hazy, try again.",
                11: "Ask again later.",
                12: "Better not tell you now.",
                13: "Cannot predict now.",
                14: "Concentrate and ask again.",
                15: "Don't count on it.",
                16: "My reply is no.",
                17: "My sources say no.",
                18: "Outlook not so good.",
                19: "Very doubtful.",
                20: "Your funeral."
            }
        value = random.randint(0, 20)
        await ctx.respond(responses[value])








def setup(bot):
    bot.add_cog(Fun(bot))
