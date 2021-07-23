from os import environ
import subprocess
from time import sleep
from pathlib import Path
import signal

from discord import channel

ROOT_DIR = Path('/home/snavesutit/minecraft_servers/mapjam/')

SERVER_DIR = Path(ROOT_DIR, 'server/')
GIT_DIR = Path(ROOT_DIR, 'git/')

SERVER_WORLD_DIR = Path(SERVER_DIR, 'world/')
GIT_WORLD_DIR = Path(GIT_DIR, 'world/')

def execute(cmd):
	subprocess.call(cmd)


def execute_in_dir(dir, cmd):
	full_cmd = [
		'if', 'cd', dir.as_posix(), ';',
		'then', *cmd, ';',
		'fi'
	]
	subprocess.call(' '.join(full_cmd), shell=True)


def toBytes(s):
	return bytes(s, encoding='utf-8')


def push_all():
	# Delete existing git
	execute(['rm', '-rf', GIT_DIR.as_posix()])

	# clone git
	execute_in_dir(ROOT_DIR, ['git', 'clone', 'git@github.com:Puffy-Boi/mapjam-map.git git/'])


def pull_world():

	# Remove the world from the git
	execute(['rm', '-rf', GIT_WORLD_DIR.as_posix()])
	execute_in_dir(GIT_DIR, ['git', 'add', '-A'])
	execute_in_dir(GIT_DIR, ['git', 'commit', '-m', '"Push world (step 1/2)"'])

	# Copy the world from the server onto the git
	execute(['cp', '-r', SERVER_WORLD_DIR.as_posix(), GIT_DIR.as_posix()])
	execute_in_dir(GIT_DIR, ['git', 'add', '-A'])
	execute_in_dir(GIT_DIR, ['git', 'commit', '-m', '"Push world (step 2/2)"'])

	# Push the changes
	execute_in_dir(GIT_DIR, ['git', 'push'])


