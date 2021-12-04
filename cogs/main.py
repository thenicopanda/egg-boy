"""
####################################################
 Commands
 * info  - Give some basic info about the bot
 * ping  - Give basic information about the bot
 * purge - Purge up to 100 messages at a time                        (Mod Role Required)
 * say   - Makes the bot say something in a channel of your choosing (Mod Role Required)
 * pchannel - Create a private channel for up to 5 users             (Mod Role Required)
 * addmerit - Add a merit to a user of your choice
 * merits - get a list of your merits
 * cleardms - clear the bots dms to you
####################################################
"""

# Imports
import discord
from discord.ext import commands
import tools as t
from discord.commands import Option, permissions

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


    # Purge messages
    @commands.slash_command(name='purge', 
                            guild_ids=[901328556603367446], 
                            default_permission=False
                            )
    @permissions.has_role(modrole)
    async def purge(self, 
                    ctx, 
                    numberofmessages: Option(int, "Number of messages you'd like to delete." )
                    ):
        """Purge up to 100 messages."""
        if numberofmessages < 101: # If number is less than 101
            await ctx.channel.purge(limit=numberofmessages, check=lambda msg: not msg.pinned) # Delete the last 100 non pinned messages
            await ctx.respond(f"{numberofmessages} messages purged successfully", ephemeral=True) # Let the person running the command know that it was successful
            modLogChannel = self.bot.get_channel(t.load("modLogChannel"))
            logEmbed = discord.Embed().set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url).add_field(name="Purge", value= f"{numberofmessages} messages were purged in {ctx.channel.mention}.", inline=False)
            await modLogChannel.send(embed=logEmbed)
        else: # Too many messages
            await ctx.respond("I'm sorry, I can only purge up to 100 messages at a time!", ephemeral=True) # Let the user know it's too many messages
   

    # Make the bot say something
    @commands.slash_command(name='say', 
                            guild_ids=[901328556603367446], 
                            default_permission=False
                            )
    @permissions.has_role(modrole)
    async def say(self, 
                  ctx, 
                  channelname: Option(discord.TextChannel, "Which channel to send message in." ), 
                  message: Option(str, "Message to send.")
                  ):
        """Makes the bot say something in a channel of your choosing"""
        await channelname.send(message)
        await ctx.respond("Message Sent.", ephemeral=True)


    # Private Channel Maker
    @commands.slash_command(name='pchannel', guild_ids=[901328556603367446], default_permission=False)
    @permissions.has_role(modrole)
    async def pchannel(self,
                       ctx,
                       channelname: Option(str, "Name of channel"),
                       person1: Option(discord.Member, "@ of the user you'd like to add to the channel."),
                       person2: Option(discord.Member, "@ of the user you'd like to add to the channel.", required=False, default=None),
                       person3: Option(discord.Member, "@ of the user you'd like to add to the channel.", required=False, default=None),
                       person4: Option(discord.Member, "@ of the user you'd like to add to the channel.", required=False, default=None),
                       person5: Option(discord.Member, "@ of the user you'd like to add to the channel.", required=False, default=None)
                       ):
        """Creates a private channel for up to 5 members."""
        privateCategory = self.bot.get_channel(903482862811111454) # Get the category that private channels go in
        newChannel = await privateCategory.create_text_channel(name=channelname) # Create the channel
        await newChannel.edit(sync_permissions = True) # Sync the channel permissions with the Category permissions (@everyone = False)
        await newChannel.set_permissions(person1, read_messages=True, send_messages=True) # Give the first person permission to access the channel
    
        if person2 != None: # If a second person was added
            await newChannel.set_permissions(person2, read_messages=True, send_messages=True) # Give second person perms
        if person3 != None: # If a third person was added
            await newChannel.set_permissions(person3, read_messages=True, send_messages=True) # Give third person perms
        if person4 != None: # If a fourth person was added
            await newChannel.set_permissions(person4, read_messages=True, send_messages=True) # Give fourth person perms
        if person5 != None: # If a fifth person was added
            await newChannel.set_permissions(person5, read_messages=True, send_messages=True) # Give fifth person perms
        
        await ctx.respond("Private channel created successfully.", ephemeral=True) # Let the command user know that the command was successful


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
    async def merits(self, ctx):
        """Get a list of your merits."""
        userid = ctx.author.id
        merits = t.loadMerits(userid)
        if merits != False:
            meritString = "Current list of Merits:"
            meritNumber = 1
            for merit in merits:
                meritString += f"\n{meritNumber}. `{merit}`"
                meritNumber += 1
            await ctx.respond(meritString)
        else:
            await ctx.respond("You do not have any merits quite yet.")

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
