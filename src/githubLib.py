from logging import RootLogger, exception
from os import environ
import subprocess
from time import sleep
from pathlib import Path
import signal
import minecraft.rcon as rcon
import json

from discord import channel

ROOT_DIR = Path('/home/snavesutit/minecraft_servers/mapjam/')

SERVER_DIR = Path(ROOT_DIR, 'server/')
GIT_DIR = Path(ROOT_DIR, 'git/')

SERVER_PROPERTIES_PATH = Path(SERVER_DIR, 'server_properties.json')

SERVER_WORLD_DIR = Path(SERVER_DIR, 'world/')
GIT_WORLD_DIR = Path(GIT_DIR, 'world/')

WORLD_FILES_TO_UPDATE = [
	'data/',
	'entities/',
	'region/',
	'level.dat'
]

WORLD_FILES_TO_FORGET = [
	'poi/',
	'DIM1/',
	'DIM-1/',
	'advancements/',
	'level.dat_old'
]


def send_mc_message(msg):
	rc.execute('tellraw @a ["",{"text":"PuffyBoi","color":"aqua"},{"text":" » ","color":"gray"},{"text":"'+msg+'"}]')


with open(SERVER_PROPERTIES_PATH.as_posix(), 'r') as file:
	properties = json.loads(file.read())

rc = rcon.RconHandler(['localhost', properties['rcon']['port'], properties['rcon']['password']])


def execute(cmd):
	return subprocess.call(cmd)


def execute_in_dir(dir, cmd):
	full_cmd = [
		'if', 'cd', dir.as_posix(), ';',
		'then', *cmd, ';',
		'fi'
	]
	return subprocess.call(' '.join(full_cmd), shell=True)


def toBytes(s):
	return bytes(s, encoding='utf-8')


def bump_git():
	# Delete existing git
	execute(['rm', '-rf', GIT_DIR.as_posix()])
	# clone git
	execute_in_dir(ROOT_DIR, ['git', 'clone', 'git@github.com:Puffy-Boi/mapjam-map.git git/'])


def bump_world(top=True):
	if top: bump_git()

	execute_in_dir(SERVER_WORLD_DIR, ['rm', '-r', *WORLD_FILES_TO_UPDATE, *WORLD_FILES_TO_FORGET])

	for file in WORLD_FILES_TO_UPDATE:
		execute_in_dir(ROOT_DIR, ['cp', '-r', f'git/world/{file}', f'server/world/{file}'])


def bump_datapack(top=True):
	if top: bump_git()

	send_mc_message('Bumping Data Pack...')

	execute_in_dir(SERVER_WORLD_DIR, ['rm', '-r', 'datapacks/'])
	execute_in_dir(ROOT_DIR, ['cp', '-r', Path(GIT_WORLD_DIR, 'datapacks/').as_posix(), SERVER_WORLD_DIR.as_posix()])

	send_mc_message('Bumped!')
	send_mc_message('Building Data Pack...')

	out = execute_in_dir(Path(SERVER_WORLD_DIR, 'datapacks/mapjam/'), ['mcb', '-build', '-offline'])

	send_mc_message('Build complete! Reloading...')
	rc.execute('reload')


def bump_resourcepack(top=True):
	send_mc_message('Bumping Resource Pack...')

	if top: bump_git()

	execute_in_dir(SERVER_DIR, ['rm', '-r', 'resources.zip'])
	execute_in_dir(Path(GIT_DIR, 'resource_pack/'), ['7z', 'a', Path(SERVER_DIR, 'resources.zip').as_posix(), '*'])
	execute_in_dir(ROOT_DIR, ['cp', '-r', 'server/resources.zip', 'git/'])

	# Commit changes
	execute_in_dir(GIT_DIR, ['git', 'add', '-A'])
	execute_in_dir(GIT_DIR, ['git', 'commit', '-m', '"Bump Resource Pack"'])

	# Push the changes
	execute_in_dir(GIT_DIR, ['git', 'push'])

	send_mc_message('Bumped! Prepare for restart in 10 seconds')
	sleep(10)
	rc.execute('kick @a Updating Server Resource Pack')
	rc.execute('stop')



def push_world():
	send_mc_message('Pushing world to git...')

	# Remove the world from the git
	execute(['rm', '-rf', GIT_WORLD_DIR.as_posix()])
	execute_in_dir(GIT_DIR, ['git', 'add', '-A'])
	execute_in_dir(GIT_DIR, ['git', 'commit', '-m', '"Push world (step 1/2)"'])

	rc.execute('save-off')

	# Copy the world from the server onto the git
	execute(['cp', '-r', SERVER_WORLD_DIR.as_posix(), GIT_DIR.as_posix()])
	execute_in_dir(GIT_DIR, ['git', 'add', '-A'])
	execute_in_dir(GIT_DIR, ['git', 'commit', '-m', '"Push world (step 2/2)"'])

	rc.execute('save-on')

	# Push the changes
	execute_in_dir(GIT_DIR, ['git', 'push'])

	send_mc_message('World Pushed!')


