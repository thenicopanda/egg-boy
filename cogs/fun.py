"""
####################################################
 Commands
 * headsOrTails - Return Either Heads or Tails
 * 8ball - Return an Eight Ball Response
 * convert - Convert between various things
####################################################
"""

# Imports
import random
from discord.ext import commands
from discord.commands import Option


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
        responses = { 0: "It is certain.", 1: "It is decidedly so.", 2: "Without a doubt.", 3: "Yes, definitely.", 4: "You may rely on it.", 5: "As I see it, yes.", 6: "Most likely.", 7: "Outlook good.", 8: "Yes.", 9: "Signs point to yes.", 10: "Reply hazy, try again.", 11: "Ask again later.", 12: "Better not tell you now.", 13: "Cannot predict now.", 14: "Concentrate and ask again.", 15: "Don't count on it.", 16: "My reply is no.", 17: "My sources say no.", 18: "Outlook not so good.", 19: "Very doubtful.", 20: "Your funeral." }
        value = random.randint(0, 20)
        await ctx.respond(responses[value])


    @commands.slash_command(name="convert", guild_ids=[901328556603367446])
    async def convert(self, ctx, 
                      number: Option(int, "Number to be converted"),
                      conversion: Option(str, "Convert what to What?", choices=["mph->km/h", "km/h->mph", "F->C", "C->F"])
                      ):
        if conversion == "mph->km/h":
            result = f"{number}mph is equal to {round(number * 1.609344)} km/h."
        elif conversion == "km/h->mph":
            result = f"{number}km/h is equal to {round(number * 0.6213711922)} mph."
        elif conversion == "F->C":
            result = f"{number} Fahrenheit is equal to {round((number-32)/1.8, 1)} Celsius."
        elif conversion == "C->F":
            result = f"{number} Celsius is equal to {round((number * 1.8) + 32)} Fahrenheit"
        else: pass
        await ctx.respond(result)



def setup(bot):
    bot.add_cog(Fun(bot))
