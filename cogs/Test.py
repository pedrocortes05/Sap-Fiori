import discord
import asyncio
import traceback
import importlib
from discord.ext import commands
from timeit import default_timer as timer

import main
#import functions
#importlib.reload(functions)

class Test(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def Username(self, ctx, username):
        print(username)

    @commands.command()
    async def Password(self, ctx, password):
        print(password)


    #Error handling
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Invalid command")

    @Username.error
    async def Username_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Syntax: **{main.get_prefix(main.client, ctx)}Username <Username>**")
        else:
            await ctx.send(f"**Error ocurred**")
            print(traceback.format_exc())
        
        print(error)

    @Password.error
    async def Password_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Syntax: **{main.get_prefix(main.client, ctx)}Password <Password>**")
        else:
            await ctx.send(f"**Error ocurred**")
            print(traceback.format_exc())
        
        print(error)


def setup(client):
	client.add_cog(Test(client))
