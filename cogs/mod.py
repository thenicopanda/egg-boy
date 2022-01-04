"""
#############################################################################################
Commands 
 * purge - Purge up to 100 messages at a time                        (Mod Role Required)
 * say   - Makes the bot say something in a channel of your choosing (Mod Role Required)
 * pchannel - Create a private channel for up to 5 users             (Mod Role Required)
 * senddm - Reply to a dm sent to the bot                            (Mod Role Required)

Listener
 * modmail - Take any DM sent to the bot and relay it to a channel.
############################################################################################
"""

# Imports
import discord
from discord.ext import commands
import tools as t
from discord.commands import Option, permissions

modrole = t.load('modRole')

class Mod(commands.Cog, name="Moderation Commands"):
    def __init__(self, bot):
        self.bot = bot


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
            if t.load("modLogChannel"):
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
        privateCategory = self.bot.get_channel(t.load("privateChannelCategory")) # Get the category that private channels go in
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
        if t.load("modLogChannel"):
            modLogChannel = self.bot.get_channel(t.load("modLogChannel"))
            logEmbed = discord.Embed().set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url).add_field(name="Private Channel", value= f"Private Channel {newChannel.mention} created.", inline=False)
            await modLogChannel.send(embed=logEmbed)


    @commands.Cog.listener()
    async def on_message(self, message):
        if t.load("modMailChannel"):
            channel = self.bot.get_channel(t.load("modMailChannel"))
            if message.guild is None and message.author != self.bot.user:
                embed=discord.Embed(title="New Message") # Create the Embed + Add a title to it
                embed.set_author(name=message.author.display_name, icon_url=message.author.avatar.url) # Set the author of the embed as the person who got updated
                embed.add_field(name="Message", value=message.content, inline=False) # Add the EB field
            
                await channel.send(embed=embed)
                await channel.send(f"Author ID: {message.author.id}\nMessage ID: {message.id}")

    @commands.slash_command(name='senddm', 
                            guild_ids=[901328556603367446], 
                            default_permission=False
                            )
    @permissions.has_role(modrole)
    async def senddm(self, 
                  ctx, 
                  person: Option(discord.User, "User ID of the person to DM." ), 
                  messageid: Option(str, "Message ID to respond to."),
                  message: Option(str, "Message to send.")
                  ):
        """Makes the bot send a DM to a person."""
        dmChannel = await self.bot.create_dm(person)
        msg = await dmChannel.fetch_message(int(messageid))
        await msg.reply(message)
        embed = discord.Embed(title="Response")
        embed.add_field(name="Original Message:", value=msg.content, inline=False)
        embed.add_field(name="Original Message Author:", value = f"{person.mention}", inline=False)
        embed.add_field(name="Response:", value = message, inline=False)
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(Mod(bot))
