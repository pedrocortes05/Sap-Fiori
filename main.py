import os
import discord
import asyncio
import random
from discord_token import TOKEN
from discord.ext import commands, tasks

def generate_secret_key():
	# Generate new random SECRET KEY
	secret_key_length = int((random.random() + 50) * 49)
	new_secret_key = ""
	for x in range(secret_key_length):
		new_secret_key += str(int(random.randint(0, 9)))

	# Decrypt data with old key
	with open("secret_key.txt",'r', encoding="UTF8") as secret_f:
		current_secret_key = secret_f.read()
		if current_secret_key == '': current_secret_key = "0"
		with open("login.txt" , 'r', encoding="UTF8") as dB:
			data = decrypt(current_secret_key, dB.read())

	# Encrypt data with new key
	with open("secret_key.txt",'w', encoding="UTF8") as secret_f:
		with open("login.txt" , 'w', encoding="UTF8") as dB:
			data = encrypt(new_secret_key, data)
			dB.write(data)

		secret_f.write(new_secret_key)
	
	return new_secret_key

def encrypt(secret_key, msg):
    encrypted_msg = ""
    counter = 0
    for char in str(msg):
        index = (counter + len(secret_key)) % len(secret_key)
        encrypted_msg += str(chr(ord(char) + int(secret_key[index])))
        counter += 1

    return encrypted_msg

def decrypt(secret_key, encrypted_msg):
    decrypted_msg = ""
    counter = 0
    for char in str(encrypted_msg):
        index = (counter + len(secret_key)) % len(secret_key)
        decrypted_msg += str(chr(ord(char) - int(secret_key[index])))
        counter += 1

    return decrypted_msg

def get_prefix(client, message):
	prefix = "sap!"
	return prefix

SECRET_KEY = generate_secret_key()


client = commands.Bot(command_prefix = get_prefix, case_insensitive=True)
client.remove_command("help")

@client.event
async def on_ready():
	await client.change_presence(status=discord.Status.online, activity=discord.Game("QR codes | sap!"))
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

client.run(TOKEN)
