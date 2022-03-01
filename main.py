import os
import discord
import asyncio
from discord.ext import commands, tasks


token = "OTQ4MjE2Njk0NzY0MTA5ODk3.Yh4lnQ.kZEqV_UDBM6fsmIrh-bVdTLd6p0"
client = commands.Bot(case_insensitive=True)
client.remove_command("help")

@client.event
async def on_ready():
	await client.change_presence(status=discord.Status.online, activity=discord.Game("Google Sheets"))
	print(f"Logged in as {client.user}")

@client.command()
@commands.has_permissions(administrator=True)
async def load(ctx, extension):
	client.load_extension(f"cogs.{extension}")
	await ctx.send(f"{extension} loaded successfully")

@client.command()
@commands.has_permissions(administrator=True)
async def unload(ctx, extension):
	client.unload_extension(f"cogs.{extension}")
	await ctx.send(f"{extension} unloaded successfully")

@client.command()
@commands.has_permissions(administrator=True)
async def reload(ctx, extension):
	client.unload_extension(f"cogs.{extension}")
	client.load_extension(f"cogs.{extension}")
	await ctx.send(f"{extension} unloaded successfully")
	await ctx.send(f"{extension} loaded successfully")

for filename in os.listdir("./cogs"):
	if filename.endswith(".py"):
		client.load_extension(f"cogs.{filename[:-3]}")

client.run(token)
