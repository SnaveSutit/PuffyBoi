import discord
from pathlib import Path
from discord import embeds
from discord.ext import commands
from os import environ
import src.githubLib as git
from src.status_boxes import StatusBox
from time import sleep
import json
import minecraft.rcon as rcon

SERVER_PROPERTIES_PATH = Path('/home/snavesutit//minecraft_servers/mapjam/server/server_properties.json')

command_prefix = ">"
def get_prefix(bot, message): return command_prefix
bot = commands.Bot(command_prefix=get_prefix,case_insensitive=True,status=discord.Status('online'),activity=discord.Activity())

with open(SERVER_PROPERTIES_PATH.as_posix(), 'r') as file:
	properties = json.loads(file.read())

rc = rcon.RconHandler(['localhost', properties['rcon']['port'], properties['rcon']['password']])

@bot.event
async def on_ready():
	print('{0.user.name} {0.user.id} online!'.format(bot))


@bot.command(name='rebootserver')
async def rebootmc(ctx):

	if ctx.guild.id != 867481364538327050: return

	box = StatusBox(
		title='>rebootserver',
		description='Server',
		thumbnail='https://raw.githubusercontent.com/SnaveSutit/PuffyBoi/main/src/assets/loading.gif',
		footer='Action in progress...',
		author=ctx.message.author
	)
	msg = await ctx.channel.send(embed=box)

	rc.execute('stop')

	box.set_footer('Action Complete!')
	box.set_thumbnail('https://raw.githubusercontent.com/SnaveSutit/PuffyBoi/main/src/assets/checkmark.gif')
	await msg.edit(embed=box)



@bot.command(name='bump')
async def bump(ctx):

	if ctx.guild.id != 867481364538327050: return

	message:discord.Message = ctx.message
	channel:discord.TextChannel = message.channel

	try:
		command, arg = message.content[1:].split(' ')

		if arg == 'world':

			await ctx.channel.send('I said don\'t use this one >:I')
			return

			box = StatusBox(
				title='>bump world',
				description='Github -> Server',
				thumbnail='https://raw.githubusercontent.com/SnaveSutit/PuffyBoi/main/src/assets/loading.gif',
				footer='Action in progress...',
				author=ctx.message.author
			)
			msg = await channel.send(embed=box)

			await ctx.message.delete()

			sleep(2.5)
			git.bump_world()

			box.set_footer('Action complete!')
			box.set_thumbnail('https://raw.githubusercontent.com/SnaveSutit/PuffyBoi/main/src/assets/checkmark.gif')
			await msg.edit(embed=box)


		elif arg == 'resourcepack':
			box = StatusBox(
				title='>bump resourcepack',
				description='Github -> Server',
				thumbnail='https://raw.githubusercontent.com/SnaveSutit/PuffyBoi/main/src/assets/loading.gif',
				footer='Action in progress...',
				author=ctx.message.author
			)
			msg = await channel.send(embed=box)

			await ctx.message.delete()

			sleep(2.5)
			git.bump_resourcepack()

			box.set_footer('Action complete!')
			box.set_thumbnail('https://raw.githubusercontent.com/SnaveSutit/PuffyBoi/main/src/assets/checkmark.gif')
			await msg.edit(embed=box)


		elif arg == 'datapack':
			box = StatusBox(
				title='>bump datapack',
				description='Github -> Server',
				thumbnail='https://raw.githubusercontent.com/SnaveSutit/PuffyBoi/main/src/assets/loading.gif',
				footer='Action in progress...',
				author=ctx.message.author
			)
			msg = await channel.send(embed=box)

			await ctx.message.delete()

			sleep(2.5)
			git.bump_datapack()
			sleep(2.5)

			box.set_footer('Action complete!')
			box.set_thumbnail('https://raw.githubusercontent.com/SnaveSutit/PuffyBoi/main/src/assets/checkmark.gif')
			await msg.edit(embed=box)


	except Exception as e:
		await channel.send(f'```\n{e}\n```')


bot.remove_command('help')

@bot.command(name='push')
async def push(ctx):

	if ctx.guild.id != 867481364538327050: return

	message:discord.Message = ctx.message
	channel:discord.TextChannel = message.channel
	try:
		command, arg = message.content[1:].split(' ')

		if arg == 'world':
			box = StatusBox(
				title='>push world',
				description='Server -> Github',
				thumbnail='https://raw.githubusercontent.com/SnaveSutit/PuffyBoi/main/src/assets/loading.gif',
				footer='Action in progress...',
				author=ctx.message.author
			)
			msg = await channel.send(embed=box)

			await ctx.message.delete()

			sleep(2.5)
			git.push_world()

			box.set_footer('Action Complete!')
			box.set_thumbnail('https://raw.githubusercontent.com/SnaveSutit/PuffyBoi/main/src/assets/checkmark.gif')
			await msg.edit(embed=box)

	except Exception as e:
		await channel.send(f'```\n{e}\n```')





if token := environ.get('PUFFYBOY_TOKEN'):
	bot.run(token)

else:
	print('Bot token not found...')
