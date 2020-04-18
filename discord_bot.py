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

######### KNOWN EMOJIS #############
THUMB_UP_EMOJI = "\U0001F44D"
THUMB_DOWN_EMOJI = "\U0001F44E"

#machine = [number, User]
NUM_MACHINES = 16
machines = []
for x in range(1, NUM_MACHINES+1):
	machines.append([x, None])

#init Bot
bot = commands.Bot(command_prefix='!')

######### HELPER FUNCTIONS ############

def get_emoji_from_number(num):
	if num == 1:
		return "1\u20e3"
	elif num == 2:
		return "2\u20e3"
	elif num == 3:
		return "3\u20e3"
	elif num == 4:
		return "4\u20e3"
	elif num == 5:
		return "5\u20e3"
	elif num == 6:
		return "6\u20e3"
	elif num == 7:
		return "7\u20e3"
	elif num == 8:
		return "8\u20e3"
	elif num == 9:
		return "9\u20e3"
	elif num == 10:
		return "\U0001F51F"
	elif num == 11:
		return "<:eleven:701065306856095807>"
	elif num == 12:
		return "<:twelve:701065385851617330>"
	elif num == 13:
		return "<:thirteen:701065447688372355>"
	elif num == 14:
		return "<:fourteen:701065538125692988>"
	elif num == 15:
		return "<:fifteen:701065620430520320>"
	elif num == 16:
		return "<:sixteen:701065696511131809>"
	else:
		return None

######### CHECKS ####################
def board_channel_check():
	def predicate(ctx):
		return ctx.channel.name == "board-reservations"
	return commands.check(predicate)
	
def test_channel_check():
	def predicate(ctx):
		return ctx.channel.name == "bot-testing"
	return commands.check(predicate)
	
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
	message = str(ctx.author) + ' used command \"' + str(ctx.command) + '\" in server ' + str(ctx.guild) + ' at ' + str(ctx.message.created_at) + "\n"
	f.write(message)
	f.close()
	
######### COMMANDS ##################
@bot.command(name='on', help="Reserves a Computer/Board.")
@commands.check_any(board_channel_check(), test_channel_check())
@commands.check(guild_check)
async def reserve_board(ctx, board_num: int):
	await record_usage(ctx)
	if board_num > NUM_MACHINES:
		await ctx.message.add_reaction(THUMB_DOWN_EMOJI)
		return
		
	board = machines[board_num - 1]
	if board[1] == None:
		board[1] = str(ctx.author)
		await ctx.message.add_reaction(THUMB_UP_EMOJI)
		emoji = get_emoji_from_number(board_num)
		if emoji:
			await ctx.message.add_reaction(emoji)
		else:
			await ctx.send("Emoji number not found: " + str(m[0]))
	else:
		await ctx.message.add_reaction(THUMB_DOWN_EMOJI)
		await ctx.send("Failure! Board already taken by " + board[1])

@bot.command(name='off', help="Free one of the Computers/Boards.")
@commands.check_any(board_channel_check(), test_channel_check())
@commands.check(guild_check)
async def free_board(ctx, board_num: int):
	await record_usage(ctx)
	board = machines[board_num - 1]
	if board[1] == None:
		await ctx.message.add_reaction(THUMB_DOWN_EMOJI)
		await ctx.send("Hmmm... Seems that board was already free.")
	else:
		if board[1] == str(ctx.author):
			board[1] = None
			await ctx.message.add_reaction(THUMB_UP_EMOJI)
			emoji = get_emoji_from_number(board_num)
			if emoji:
				await ctx.message.add_reaction(emoji)
			else:
				await ctx.send("Emoji number not found: " + str(m[0]))
		else:
			await ctx.message.add_reaction(THUMB_DOWN_EMOJI)
			await ctx.send("Failure! That's not your board to release!")
	
@bot.command(name="open", help="Bot reacts with which boards are available.")
@commands.check_any(board_channel_check(), test_channel_check())
@commands.check(guild_check)
async def check_open(ctx):
	await record_usage(ctx)
	open_count = 0
	for m in machines:
		if m[1] == None:
			open_count = open_count + 1
			emoji = get_emoji_from_number(int(m[0]))
			if emoji:
				await ctx.message.add_reaction(emoji)
			else:
				await ctx.send("Emoji not found: " + str(m[0]))
	if open_count == 0:
		await ctx.message.add_reaction(THUMB_UP_EMOJI)
	
@bot.command(name="open-v", help="Bot says which boards are available.")
@commands.check_any(board_channel_check(), test_channel_check())
@commands.check(guild_check)
async def check_open_verbose(ctx):
	await record_usage(ctx)
	message = "Available Boards:\n"
	for m in machines:
		if m[1] == None:
			message = message + "\tCO2041-" + str(m[0]) + "\n"
	await ctx.send(message)
	
@bot.command(name="taken", help="See which boards are being used.")
@commands.check_any(board_channel_check(), test_channel_check())
@commands.check(guild_check)
async def check_taken(ctx):
	await record_usage(ctx)
	taken_count = 0
	for m in machines:
		if m[1] != None:
			taken_count = taken_count + 1
			emoji = get_emoji_from_number(int(m[0]))
			if emoji:
				await ctx.message.add_reaction(emoji)
			else:
				await ctx.send("Emoji not found: " + str(m[0]))
	if taken_count == 0:
		await ctx.message.add_reaction(THUMB_UP_EMOJI)

@bot.command(name="taken-who", help="See which boards are being used and by whom.")
@commands.check_any(board_channel_check(), test_channel_check())
@commands.check(guild_check)
async def check_taken_verbose(ctx):
	await record_usage(ctx)
	message = "Taken Boards:\n"
	for m in machines:
		if m[1] != None:
			message = message + "\tCO2041-" + str(m[0]) + " -- Used by: " + str(m[1]) + "\n"
	await ctx.send(message)
	
@bot.command(name="greet")
@commands.check_any(owner_check(), bryan_check())
@commands.check_any(board_channel_check(), test_channel_check())
async def b_cmd(ctx):
	await record_usage(ctx)
	await ctx.send("Hullo Sir!")
		
@bot.command(name="stop", help="Command to kill the bot. Only useable by James or Bryan.")
@commands.check_any(owner_check(), bryan_check())
@commands.check_any(board_channel_check(), test_channel_check())
async def kill(ctx):
	await record_usage(ctx)
	await bot.logout()

#RUN
bot.run(TOKEN)