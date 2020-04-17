# bot.py
# base code copied from: https://realpython.com/how-to-make-a-discord-bot-python/
# Secondary author = Bryan Friestad
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
BRYAN_ID = int(os.getenv('BRYAN_ID'))

#machine = [number, User]
machines = []
for x in range(1, 16+1):
	machines.append([x, None])

#init Bot
bot = commands.Bot(command_prefix='!')

######### CHECKS ####################
def channel_check(ctx):
	return ctx.channel.name == "board-reservations"
	
def owner_check():
	def predicate(ctx):
		return ctx.guild is not None and ctx.guild.owner_id == ctx.author.id
	return commands.check(predicate)

def bryan_check():
	def predicate(ctx):
		return ctx.guild is not None and BRYAN_ID == ctx.author.id
	return commands.check(predicate)
	
def guild_check(ctx):
	return ctx.guild.name == GUILD
	
async def record_usage(ctx):
	f = open("usage_log.txt", 'a+')
	message = str(ctx.author) + ' used command \"' + str(ctx.command) + '\" at ' + str(ctx.message.created_at) + "\n"
	f.write(message)
	f.close()
	
######### COMMANDS ##################
@bot.command(name='on', help="Reserves a Computer/Board.")
@commands.check(channel_check)
@commands.check(guild_check)
async def reserve_board(ctx, board_num: int):
	await record_usage(ctx)
	board = machines[board_num - 1]
	if board[1] == None:
		board[1] = str(ctx.author)
		await ctx.send("Success! Board " + str(board_num) + " is now reserved by " + str(ctx.author))
	else:
		await ctx.send("Failure! Board already taken by " + board[1])

@bot.command(name='off', help="Free one of the Computers/Boards.")
@commands.check(channel_check)
@commands.check(guild_check)
async def free_board(ctx, board_num: int):
	await record_usage(ctx)
	board = machines[board_num - 1]
	if board[1] == None:
		await ctx.send("Hmmm... Seems that board was already free.")
	else:
		if board[1] == str(ctx.author):
			board[1] = None
			await ctx.send("Success! Board " + str(board_num) + " is now FREE.")
		else:
			await ctx.send("Failure! That's not your board to release!")
	
		
@bot.command(name="open", help="See which boards are available.")
@commands.check(channel_check)
@commands.check(guild_check)
async def check_open(ctx):
	await record_usage(ctx)
	message = "Available Boards:\n"
	for m in machines:
		if m[1] == None:
			message = message + "\tCO2041-" + str(m[0]) + "\n"
	await ctx.send(message)
	
@bot.command(name="taken", help="See which boards are being used and by whom.")
@commands.check(channel_check)
@commands.check(guild_check)
async def check_taken(ctx):
	await record_usage(ctx)
	message = "Taken Boards:\n"
	for m in machines:
		if m[1] != None:
			message = message + "\tCO2041-" + str(m[0]) + " -- Used by: " + str(m[1]) + "\n"
	await ctx.send(message)

@bot.command(name="greet")
@commands.check(channel_check)
@commands.check_any(owner_check(), bryan_check())
async def b_cmd(ctx):
	await record_usage(ctx)
	await ctx.send("Hullo Sir!")
		
@bot.command(name="stop", help="Command to kill the bot. Only useable by James or Bryan.")
@commands.check_any(owner_check(), bryan_check())
async def kill(ctx):
	await record_usage(ctx)
	await bot.logout()

#RUN
bot.run(TOKEN)