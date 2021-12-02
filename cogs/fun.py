"""
####################################################
 Commands
 * headsOrTails - Return Either Heads or Tails
 * urban - Search for a Term on Urban Dictionary
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

    @commands.slash_command(name='urban',
                            guild_ids=[901328556603367446]
                            )
    async def urban(self, 
                    ctx, 
                    term: Option(str, "Term to search for.")
                    ):
        """Search for a Term on Urban Dictionary"""
        term = " ".join(term)
        msg = await ctx.respond("Searching...")
        #  The headers required to recieve the information
        headers={
                "X-RapidAPI-Host": "mashape-community-urban-dictionary.p.rapidapi.com",
                "X-RapidAPI-Key": "34176a38aamsh1a3cc0a94ed8bcep1c92b1jsn54239f977d2b"
            }
        #  Get the response
        response = requests.get(f"https://mashape-community-urban-dictionary.p.rapidapi.com/define?term={term}", headers=headers)
        #  Convert the response to a dictionary
        response = json.loads(response.text)
        #  Get the number of definitions
        lenOfResponse = len(response['list'])
        #  If there are results
        if lenOfResponse > 0:
            #  Randomly pick a response, subtract one from the number of
            #  definitions so that it dosen't go past the final term
            responseNum = random.randint(0, lenOfResponse - 1)
            #  Save the definition
            responseDef = response['list'][responseNum]['definition']
            #  Save the author
            responseAuthor = response['list'][responseNum]['author']
            embed = discord.Embed(title = term, description = responseDef)
            embed.set_footer(text=responseAuthor)
            await msg.edit_original_message(embed=embed, content=None)
        #  No results
        else:
            await msg.edit_original_message(content="No results found...")


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