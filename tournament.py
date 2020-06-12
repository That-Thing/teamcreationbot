import discord
from discord.ext import commands
from discord.ext.commands import Bot
import random
from discord.utils import get
import asyncio
import time


class tournament(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    


    @commands.command(pass_context=True, aliases=['createteam', 'crteam', 'CrTeam','crTeam','CreateTeam']) #pass context and add alternative command names
    @commands.cooldown(rate=1, per=2.0) #command cooldown so it can't be spammed by some loser
    async def createTeam(self, ctx, teammate: discord.User): 
        #ctx.message.guild.roles
        #<:tickYes:315009125694177281>
        cross = self.bot.get_emoji(315009174163685377) #red x emoji
        check = self.bot.get_emoji(315009125694177281) # green checkmark emoji
        guild = ctx.message.guild #current server
        numOfRoles = len(ctx.message.guild.roles) #amount of roles in server
        roles = ctx.message.guild.roles #all roles in server
        #checks is the member is in a role already, if not, the script can continue
        roleCount = 0 #initializes roleCount with a value of 0
        for role in ctx.message.guild.roles: #every role in the server roles
            if role in ctx.message.author.roles: #if the message author has a role
                roleCount += 1 #current roleCount value + 1
        if(roleCount > 1): #the role count will ALWAYS be 1 or greater because @everyone counts as a role
            await ctx.send("You are already in a team.")
            #print(roleCount)

        else:
            randomNumber = str(random.randint(0,100)) #just a random number so channels don't get messed up. 
            
            createdRole = await guild.create_role(name="Team "+randomNumber) #creates a role with the same number as the channel
            #print(createdRole)
            createdChannel = await guild.create_text_channel("create-team"+randomNumber) #creates a text channel
            await createdChannel.set_permissions(ctx.message.author, read_messages=True, send_messages=True, add_reactions=True) #set perms for message author
            await createdChannel.set_permissions(teammate, read_messages=True, send_messages=True, add_reactions=True) #set perms for teammate
            await createdChannel.set_permissions(guild.default_role, read_messages=False, send_messages=False, add_reactions=False) #permissions for @everyone
            #discord embed below
            embed = discord.Embed(name="HvH Tournament Teams", description="HvH Tournament Teams")
            embed.add_field(name="Both users must react to this message within 2 minutes", value=ctx.message.author.mention + " " + teammate.mention)
            message = await createdChannel.send(embed=embed)
            await message.add_reaction(emoji="🟢") #ADD REACTION
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=120.0) #wait for a reaction for 120 seconds
            except asyncio.TimeoutError: #time ends
                embed = discord.Embed(name="User(s) did not react in time", description="Please redo the commmand.", color=0xFF0000)
                embed.add_field(name="User(s) did not react in time", value="Channel will be deleted in 10 seconds")
                message = await createdChannel.send(embed=embed)
                time.sleep(10) #wait for 10 seconds
                await createdChannel.delete() #delete created channel.
                await createdRole.delete()
            else:
                #print("reaction added")
                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=120.0) #waits for 2 minutes(120 seconds) for any of the users to add a reaction
                except asyncio.TimeoutError: #on event of the time ending
                    embed = discord.Embed(name="User(s) did not react in time", description="Please redo the commmand.", color=0xFF0000)
                    embed.add_field(name="User(s) did not react in time", value="Channel will be deleted in 10 seconds")
                    message = await createdChannel.send(embed=embed)
                    time.sleep(10) 
                    await createdChannel.delete() #delete channel
                    await createdRole.delete()
                else:
                    await ctx.message.author.add_roles(createdRole) #add created role to person who initiated the command
                    await ctx.message.author.add_roles(teammate) #add created role to teammate 
                    embed = discord.Embed(name="Team Created Successfully", description="Success!")
                    embed.add_field(name="Team Created Successfully!", value="Channel will be deleted in 10 seconds")
                    message = await createdChannel.send(embed=embed)
                    time.sleep(10) #wait for 10 seconds
                    await createdChannel.delete() #delete channel
               

def setup(bot):
    bot.add_cog(tournament(bot))