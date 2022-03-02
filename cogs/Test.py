import json
import discord
import asyncio
import random
import traceback
import importlib
from discord.ext import commands
from timeit import default_timer as timer

import main
import qr_generator
importlib.reload(qr_generator)


def edit_data(id, username="None", password="None"):
	data = ""
	with open("login.txt" ,'r', encoding="UTF8") as login_file:
		# Retrieve encrypted data
		encrypted_data = login_file.read()

		# Dcrypt data
		if encrypted_data != '':
			decrypted_data = main.decrypt(main.SECRET_KEY, encrypted_data)
		else:
			decrypted_data = "{}"

		# Turn data into dictionary
		data_dict = json.loads(decrypted_data)

		# Edit or add user
		if id in data_dict:
			# Existing User
			new_username = data_dict[id]["user"] if username == "None" else username
			new_password = data_dict[id]["pass"] if password == "None" else password
			data_dict[id] = {"user" : new_username, "pass" : new_password}
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
	with open("login.txt" ,'r', encoding="UTF8") as login_file:
		# Retrieve encrypted data
		encrypted_data = login_file.read()

		# Dcrypt data
		if encrypted_data != '':
			decrypted_data = main.decrypt(main.SECRET_KEY, encrypted_data)
		else:
			decrypted_data = "{}"

		# Turn data into dictionary
		data_dict = json.loads(decrypted_data)

		if str(id) in data_dict:
			username = data_dict[str(id)]["user"]
			password = data_dict[str(id)]["pass"]
			return username, password
		else:
			return False, False


class Test(commands.Cog):

	def __init__(self, client):
		self.client = client
	
	@commands.group(invoke_without_command=True)
	async def help(self, ctx):
		embed = discord.Embed(title="Commands", color=ctx.me.color)
		embed.set_author(name="Sap Fiori", icon_url="https://cdn.discordapp.com/avatars/948216694764109897/4defcaf7e389b38f73717868d21e901d.webp?size=128")
		prefix = main.get_prefix(main.client, ctx)

		commands = f"""**{prefix}help**: - Opens this lmao
								**{prefix}Username**: - Save Username for Sap Fiori
								**{prefix}Password**: - Save Password for Sap Fiori
								**{prefix}QR**: - Generate QR code"""
		
		notice = """This is an __unofficial__ Sap Fiori bot
					All information is safely stored and encrypted
					Please answer the questionare truthfully
					Sap Fiori bot is open-source software available at
					https://github.com/pedrocortes05/Sap-Fiori"""
		
		embed.add_field(name="__Commands__", value=commands, inline=False)
		embed.add_field(name="__Notice__", value=notice, inline=False)
		await ctx.send(embed=embed)

	@commands.command(pass_context=True)
	async def Username(self, ctx, username):
		edit_data(str(ctx.message.author.id), username=username)
		await ctx.send("Username was saved successfully")

	@commands.command()
	async def Password(self, ctx, password):
		edit_data(str(ctx.message.author.id), password=password)
		await ctx.send("Password was saved successfully")

	@commands.command()
	async def Qr(self, ctx):
		username, password = get_user(ctx.message.author.id)
		if username:
			await ctx.send("Gimme a sec bro")
			try:
				await qr_generator.generate_qr_code(ctx, username, password)
			except:
				await ctx.send("Error ocurred from the Sap Fiori website")
				print(traceback.format_exc())
		else:
			await ctx.send("You need to sign up first")


	#Error handling
	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		if isinstance(error, commands.CommandNotFound):
			pass
			# if ctx.message.content.lower() not in ('y', 'n', "yes", "no"):
			# 	await ctx.send("Invalid command")

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
