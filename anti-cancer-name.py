import discord
import requests
import subprocess
import sys
import os
import asyncio
import aiohttp
import json
import time

logInFromFile = False

if logInFromFile == False:
	inEmail = input("email: ")
	inPassword = input("password: ")
	if os.name == "nt":
		os.system("cls")
	elif os.name == "posix":
		os.system("clear")
elif logInFromFile == True:
	with open("inmail.txt") as inmail:
		inEmail = intoken.read().replace("\n", "")
	with open("inpassword.txt") as inpassword:
		inPassword = intoken.read().replace("\n", "")

payload = {"type": 2}
async def block(userToBlock, server, channel):
	headers = {"Content-Type": "application/json", "Authorization": client.token, "Origin": "https://discordapp.com", "Accept": "*/*", "Referer": "https://discordapp.com/channels/" + server + "/" + channel}
	with aiohttp.ClientSession() as session:
		await session.put("https://discordapp.com/api/users/@me/relationships/" + userToBlock, data=json.dumps(payload), headers=headers)
		await session.close()
		time.sleep(5)

client = discord.Client()

@client.event
async def on_ready():
	print("logged in as " + client.user.name + " - " + client.user.id)
	print(client.token)

init = False
allowedChars = "aàãáäbcdeèẽéëfghiìĩíïjklmnoòõóöpqvǜṽǘwyỳỹýÿzAÀÃÁÄBCDEÈẼËÉFGHIÌĨÍÏJKLMNOÒÕÓÖPQVǛṼǗWXYỲỸÝŸZ 1234567890 !@#$%*()_+`~[]}{\|;´\";:,./<>?'"
@client.event
async def on_message(message):
	count = 0
	tok = ""
	global init
	if message.content.startswith("acc"):
		tempMsg = message.content.split(" ")
		try:
			if tempMsg[1] == "init":
				init = True
		except IndexError:
			pass
	if init == True:
		print("true")
		tempAuthor = list(message.author.name)
		for char in tempAuthor:
			if char not in allowedChars:
				count += 1
			if count > 2:
				await block(message.author.id, message.server.id, message.channel.id)

client.run(inEmail, inPassword)
