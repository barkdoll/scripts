#  01 Parameter for compiled random list
#  02 Maybe a parameter for specifying source
# 		directory on-the-fly for randomized choice
# 		that bypasses DATA_DIRS variable

import os, sys, re, cmd
import random
import psutil
from pathlib import Path

# Source directories for your video files
DATA_DIRS = [ 'put all of your', 'video file paths', 'in this list' ]
# Strings that help identify a high-level folder name 
# to make sure the script knows where your TV/video 
# series live and your movies live
SERIES_DIR_IDENTIFIER = 'series folder name goes here' # example: 'tv_shows'
MOVIE_DIR_IDENTIFIER = 'movie folder name goes here'  # example: 'movies'
# Path to your media player executable
MEDIA_PLAYER = 'C:\\Program Files\\change\\this\\path\\to\\your\\MediaPlayer.exe'


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
		dir_list += [
			os.path.join(root_folder, d)
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


def chooseSeries(path_list, series_top_dir):
	while True:
		chosen_folder = random.choice(generateDirList(path_list))
		if series_top_dir in chosen_folder:
			break

	series_list = []
	for root, directory, files in os.walk(chosen_folder):
		for fname in files:
			fpath = root + '\\' + fname
			if isVideo(fpath):
				series_list.append(fpath)
	return series_list


def chooseMovie(path_list, movie_top_dir):
	while True:
		m = chooseOne(DATA_DIRS)
		if movie_top_dir in m:
			break
	return m


# Quick shortcut to wrap strings in quotes
def qq(s):
	return '"{}"'.format(s)


try:
	if '--series' in sys.argv:
		series = chooseSeries(DATA_DIRS, SERIES_DIR_IDENTIFIER)
		sname = series[-1].split('\\')
		sname = sname[sname.index('tv_shows') + 1].split('_')
		sname = ' '.join(sname).title()
		print('\nplaying {}\n'.format(sname))
		arg_list = [qq(MEDIA_PLAYER)] + [qq(f) for f in series]
		os.execv(MEDIA_PLAYER, arg_list)

	elif '--movie' in sys.argv:
		movie = chooseMovie(DATA_DIRS, MOVIE_DIR_IDENTIFIER)
		os.execv(MEDIA_PLAYER, [qq(MEDIA_PLAYER), qq(movie)])

	else:
		# Chooses one random video file
		p = chooseOne(DATA_DIRS)
		print('\nfull path:', '"{}"'.format(p))
		
		basename = p.split('\\')[-1]
		print('playing "{}"\n'.format(basename))
		# qq() function is needed here because spaces
		# must be escaped in file paths when passed as arguments
		os.execv(MEDIA_PLAYER, [qq(MEDIA_PLAYER), qq(p)])

except Exception as e:
	print('\n{}\n'.format(e))
