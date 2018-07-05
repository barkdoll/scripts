#  01 Default of maybe picking one video at random?
#  02 Parameter for random entire series
#  03 Parameter for compiled random list
#  04 Maybe a parameter for specifying source
# 		directory on-the-fly for randomized choice
# 		that bypasses DATA_DIRS variable

import os
import random
import subprocess
import psutil
from pathlib import Path

DATA_DIRS = [ 'put all of your', 'video file paths', 'in this list' ]
MEDIA_PLAYER = 'C:\\Program Files\\Change\\This\\Path\\to\\yourMediaPlayer.exe'


def playerRunning(player):
	player_process = player.split('\\')[-1]
	yes = False
	for pid in psutil.pids():
		if psutil.Process(pid).name() == player_process:
			yes = True
	return yes


def generateSelectionList(data_path_list):
	dir_list = []
	for root_folder in data_path_list:
		dir_list += [ os.path.join(root_folder, d) for d in os.listdir(root_folder)
			if Path(root_folder+d).is_dir() ]
	return dir_list


def chooseOne(path_list):
	while True:
		folders = generateSelectionList(path_list)
		# Choose random folder to get video from
		chosen_folder = random.choice(folders)
		# Choose random file from selected folder
		chosen_one = random.choice(os.listdir(chosen_folder))
		# Handles any non-video file choices
		if chosen_one.endswith(('.mp4', '.mkv', '.avi', '.flv')):
			break
	
	chosen_path = chosen_folder + '\\' + chosen_one
	return chosen_path
	

def chooseSeries(paths):
	# Use os.walk() or similar operation to
	# grab all media files within the given folder (or subfolder)
	# and open them in VLC
	pass


try: 
	# Make thecall!
	p = chooseOne(DATA_DIRS)
	while not Path(p).is_file():
		p = chooseOne(DATA_DIRS)

	print('\nplaying {}\n'.format(p))
	# subprocess.Popen([MEDIA_PLAYER, p])
except Exception as e:
	print(e)