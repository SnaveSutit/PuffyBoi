import discord
from discord.ext import commands
from os import environ
import src.githubLib as git

command_prefix = ">"
def get_prefix(bot, message): return command_prefix
bot = commands.Bot(command_prefix=get_prefix,case_insensitive=True,status=discord.Status('online'),activity=discord.Activity())


@bot.event
async def on_ready():
	print('{0.user.name} {0.user.id} online!'.format(bot))


@bot.command(name='push')
async def push(ctx):
	message:discord.Message = ctx.message
	channel:discord.TextChannel = message.channel

	try:
		command, arg = message.content[1:].split(' ')

		if arg == 'all':
			msg = await channel.send('Pushing git to server <a:spinner:867932823590412308>')
			git.push_all(ctx)
			await msg.edit(content='Server synced with git <:Yes:723386284277497907>')


	except Exception as e:
		await channel.send(f'```\n{e}\n```')

@bot.command(name='pull')
async def pull(ctx):
	message:discord.Message = ctx.message
	channel:discord.TextChannel = message.channel
	try:
		command, arg = message.content[1:].split(' ')

		if arg == 'world':

			msg = await channel.send(embed=discord.Embed(
				title='>pull world',
				description='Taking the world from the server and putting it on the github repo',
				thumbnail=''
				),
			)

			git.pull_world()

			await msg.edit(embed=discord.Embed(
				title='>pull world <:Yes:723386284277497907>',
				description='World synced to git')
			)

	except Exception as e:
		await channel.send(f'```\n{e}\n```')





if token := environ.get('PUFFYBOY_TOKEN'):
	bot.run(token)

else:
	print('Bot token not found...')
