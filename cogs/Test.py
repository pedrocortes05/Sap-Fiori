import json
import discord
import asyncio
import traceback
import importlib
from discord.ext import commands
from timeit import default_timer as timer

import main
#import functions
#importlib.reload(functions)

def write_json(id, username="None", password="None"):
    filename="login.json"
    with open(filename,'r+', encoding="UTF8") as file:
        file_data = json.load(file)

        if id in file_data:
            # Existing User
            new_username = file_data[id]["user"] if username == "None" else username
            new_password = file_data[id]["pass"] if password == "None" else password
            file_data[id] = {"user" : username, "pass" : password}
        else:
            # New User
            file_data.update({id : {"user" : username, "pass" : password}})

        # Sets file's current position at offset.
        file.seek(0)
        # Convert back to json.
        json.dump(file_data, file, indent = 4)

class Test(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def Username(self, ctx, username):
        write_json(ctx.message.author.id, username)

    @commands.command()
    async def Password(self, ctx, password):
        write_json(ctx.message.author.id, password)

    @commands.command()
    async def Qr(self, ctx):
        generate_qr_code()


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
