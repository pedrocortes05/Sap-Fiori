import json
import discord
import asyncio
import random
import traceback
import importlib
from discord.ext import commands
from timeit import default_timer as timer

import main
from qr_generator import generate_qr_code
#importlib.reload(qr_generator)


def edit_data(id, username="None", password="None"):
    data = ""
    with open("login.txt" ,'r', encoding="UTF8") as login_file:
        # Retrieve encrypted data
        encrypted_data = login_file.read()

        # Dcrypt data
        decrypted_data = main.decrypt(main.SECRET_KEY, encrypted_data)

        # Turn data into dictionary
        data_dict = json.load(decrypted_data)

        # Edit or add user
        if id in data_dict:
            # Existing User
            new_username = data_dict[id]["user"] if username == "None" else username
            new_password = data_dict[id]["pass"] if password == "None" else password
            data_dict[id] = {"user" : username, "pass" : password}
        else:
            # New User
            data_dict.update({id : {"user" : username, "pass" : password}})

        # Return dictionary into string
        data = json.dumps(data_dict)
    
    with open("login.txt" ,'w', encoding="UTF8") as login_file:
        # Encrypt data and write to file
        encrypted_data = main.encrypt(main.SECRET_KEY, data)
        login_file.write(encrypted_data)

def get_user(id):
    pass


class Test(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def Username(self, ctx, username):
        edit_data(ctx.message.author.id, username)

    @commands.command()
    async def Password(self, ctx, password):
        edit_data(ctx.message.author.id, password)

    @commands.command()
    async def Qr(self, ctx):
        username, password = get_user(ctx.message.author.id)
        generate_qr_code(username, password)


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
