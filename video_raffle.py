#  01 Default of maybe picking one video at random?
#  02 Parameter for random entire series
#  03 Parameter for compiled random list
#  04 Maybe a parameter for specifying source
# 		directory on-the-fly for randomized choice
# 		that bypasses DATA_DIRS variable

import os
import random
import psutil
from pathlib import Path

DATA_DIRS = [ 'put all of your', 'video file paths', 'in this list' ]
MEDIA_PLAYER = 'C:\\Program Files\\Change\\This\\Path\\to\\yourMediaPlayer.exe'


def isVideo(f):
	if f.endswith(('.mkv', '.mp4', '.avi', '.mov', '.flv')):
		return True
	else:
		return False


def playerRunning(player):
	player_process = player.split('\\')[-1]
	yes = False
	for pid in psutil.pids():
		if psutil.Process(pid).name() == player_process:
			yes = True
	return yes


def generateDirList(data_path_list):
	dir_list = []
	for root_folder in data_path_list:
		dir_list += [ os.path.join(root_folder, d)
      for d in os.listdir(root_folder)
      if Path(root_folder+d).is_dir()
    ]
	return dir_list


def generateSelectionList(data_path_list):
	file_list = []
	for root_folder in data_path_list:
		for root, directory, files in os.walk(root_folder):
			for fname in files:
				fpath = root + '\\' + fname
				if isVideo(fpath):
					file_list.append(fpath)

	return file_list


def chooseOne(path_list):
	files = generateSelectionList(path_list)
	# Choose random folder to get video from
	chosen_one = random.choice(files)
	# Choose random file from selected folder
	return chosen_one


def chooseSeries(paths):
	# 01 chosen_folder = random.choice(generateDirList())
	# 02 use os.walk() or similar operation to
	# grab all media files within the chosen folder's
	# files and subfolders
	# 03 Generate an alphabetically sorted list
	# of the video files and open them as a playlist in VLC
	pass


# Quick shortcut to wrap strings in quotes
def qquote(s):
	return '"{}"'.format(s)


try:
	# Make the call!
	p = chooseOne(DATA_DIRS)
	print('\nplaying "{}"\n'.format(p))
	# qquote() function is needed here because spaces
	# must be escaped in file paths when passed as arguments
	os.execv(MEDIA_PLAYER, [qquote(MEDIA_PLAYER), qquote(p)])

except Exception as e:
	print('\n{}\n'.format(e))
