from http import client
import discord
import asyncio
import traceback
import importlib
from discord.ext import commands
from timeit import default_timer as timer

import main
import functions
importlib.reload(functions)

class Test(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.group(invoke_without_command=True)
	async def help(self, ctx):
		embed = discord.Embed(title="Mapgame Commands", color=ctx.me.color)
		embed.set_author(name="Mapgame", icon_url="https://cdn.discordapp.com/avatars/908858108246384721/9f90605cce51952bd639bd88ac807bff.webp?size=128")
		prefix = main.get_prefix(main.client, ctx)

		player_commands = f"""**{prefix}Stockpile**: - Inspect a nations stockpile
								**{prefix}Remind**: - Set a reminder for the next X turns"""

		mapgame_commands = f"""**{prefix}BuildCity**: - Constructing buildings in your city
								**{prefix}RuralTax**: - Change the taxes on your rural population"""

		admin_commands = f"""**{prefix}NewTurn**
							**{prefix}SumMoney**"""

		embed.add_field(name="__Player__", value=player_commands, inline=False)
		embed.add_field(name="__Mapgame__", value=mapgame_commands, inline=False)
		embed.add_field(name="__Moderation__", value=admin_commands, inline=False)
		await ctx.send(embed=embed)

	@commands.commnad()
    async def Username(self, ctx, username):
        print(username)

    @commands.commnad()
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
