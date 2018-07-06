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
		dir_list += [os.path.join(root_folder, d)
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
	# Choose a  random folder and select
	# random video file from within said folder
	return random.choice(generateSelectionList(path_list))


def chooseSeries(path_list):
	chosen_folder = random.choice(generateDirList(path_list))
	series_list = []
	for root, directory, files in os.walk(chosen_folder):
		for fname in files:
			fpath = root + '\\' + fname
			if isVideo(fpath):
				series_list.append(fpath)
	return series_list


# Quick shortcut to wrap strings in quotes
def qquote(s):
	return '"{}"'.format(s)


try:
	if '--series' in sys.argv:
		series = chooseSeries(DATA_DIRS)
		sname = series[-1].split('\\')
		sname = sname[sname.index('tv_shows') + 1].split('_')
		sname = ' '.join(sname).title()
		print('\nplaying series {}\n'.format(sname))
		arg_list = [qquote(MEDIA_PLAYER)] + [qquote(f) for f in series]
		os.execv(MEDIA_PLAYER, arg_list)
	else:
		# Make the call!
		p = chooseOne(DATA_DIRS)
		print('\nfull path:', '"{}"'.format(p))
		
		basename = p.split('\\')[-1]
		print('playing "{}"\n'.format(basename))
		# qquote() function is needed here because spaces
		# must be escaped in file paths when passed as arguments
		os.execv(MEDIA_PLAYER, [qquote(MEDIA_PLAYER), qquote(p)])

except Exception as e:
	print('\n{}\n'.format(e))
