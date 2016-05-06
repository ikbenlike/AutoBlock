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

blockFile = open("blocklist.txt", "r")
blocked = blockFile.read().replace('\n', '')
blockFile.close()

payload = {"type": 2}
async def block(userToBlock, userToBlockName, server, channel):
	global blocked
	headers = {"Content-Type": "application/json", "Authorization": client.token, "Origin": "https://discordapp.com", "Accept": "*/*", "Referer": "https://discordapp.com/channels/" + server + "/" + channel}
	try:
		if userToBlock not in blocked:
			with aiohttp.ClientSession() as session:
				await asyncio.sleep(5)
				async with session.put("https://discordapp.com/api/users/@me/relationships/" + userToBlock, data=json.dumps(payload), headers=headers) as response:
					print("blocked " + userToBlock + " - " + userToBlockName)
					await session.close()
					blockFile = open("blocklist.txt", "a")
					blockFile.write(userToBlock)
					blockFile.close()
					blockFile = open("blocklist.txt", "r")
					blocked = blockFile.read().replace('\n', '')
					blockFile.close()
	except aiohttp.errors.ServerDisconnectedError:
		pass


client = discord.Client()

@client.event
async def on_ready():
	print("logged in as " + client.user.name + " - " + client.user.id)

init = False
allowedChars = "aàãáäâbcdeèẽéëêfghiìĩíïîjklmḿnǹñńoòõóöôpqrsśtuùũúüûvǜṽǘwxẍyỳỹýÿŷzAÀÃÁÄBCDEÈẼËÉFGHIÌĨÍÏJKLMḾNǸÑŃOÒÕÓÖPQRSŚTUÙŨÚÜVǛṼǗWXẌYỲỸÝŸZ 1234567890 !@#$%*()_+`~[]}{\|;´\";:,./<>?'"
@client.event
async def on_message(message):
	count = 0
	tok = ""
	global init
	if message.content.startswith("acc") and message.author.id == client.user.id:
		tempMsg = message.content.split(" ")
		try:
			if tempMsg[1] == "init":
				init = True
			elif tempMsg[1] == "exit":
				await client.logout()
		except IndexError:
			pass
	if init == True:
		tempAuthor = list(message.author.name)
		for char in tempAuthor:
			if char not in allowedChars:
				count += 1
			if count > 2:
				await block(message.author.id, message.author.name, message.server.id, message.channel.id)
				break

client.run(inEmail, inPassword)
