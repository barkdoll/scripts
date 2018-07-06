import os, sys, re, cmd, random, psutil
from pathlib import Path
from mutagen import File as mutaFile

# Source directories for your video files
DATA_DIRS = [ 'put all of your', 'video file paths', 'in this list' ]
# Path to your media player executable
MEDIA_PLAYER = 'C:\\Program Files\\change\\this\\path\\to\\your\\MediaPlayer.exe'


def isAudio(f):
	if f.endswith(('.mp3', '.m4a', '.ogg', '.wma', '.flac', '.wav')):
		return True
	else:
		return False


def genres(path_list):
	genre_list = []
	for folder in path_list:
		for root, directory, files in os.walk(folder):
			for fname in files:
				fpath = root + '\\' + fname
				if isAudio(fpath):
					# I haven't figured out the most 
					# semantic way to read genre tags so 
					# for now, this works by grabbing it 
					# from the TCON property 
					if mutaFile(fpath) and mutaFile(fpath).tags.get('TCON'):
						genre = str( mutaFile(fpath).tags.get('TCON') ).lower()
						if genre not in genre_list:
							genre_list.append(genre)
	# common construct for removing duplicate list values
	return genre_list


def getGenre(file):
	if mutaFile(file) and mutaFile(file).tags.get('TCON'):
		file_meta_genre = str( mutaFile(file).tags.get('TCON') ).lower()
		return file_meta_genre


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
				if isAudio(fpath):
					file_list.append(fpath)

	return file_list

def chooseAlbum(path_list, series_top_dir):
	while True:
		chosen_folder = random.choice(generateDirList(path_list))
		if series_top_dir in chosen_folder:
			break

	series_list = []
	for root, directory, files in os.walk(chosen_folder):
		for fname in files:
			fpath = root + '\\' + fname
			if isAudio(fpath):
				series_list.append(fpath)
	return series_list


# Quick shortcut to wrap strings in quotes
def qq(s):
	return '"{}"'.format(s)

try:
	# TODO: ADD SUPPORT FOR PLAYING A RANDOM ALBUM
	# if '--album' in sys.argv:
	# 	series = chooseAlbum()
	# 	sname = series[-1].split('\\')
	# 	sname = sname[sname.index('tv_shows') + 1].split('_')
	# 	sname = ' '.join(sname).title()
	# 	print('\nplaying {}\n'.format(sname))
	# 	arg_list = [qq(MEDIA_PLAYER)] + [qq(f) for f in series]
	# 	os.execv(MEDIA_PLAYER, arg_list)

	if any(genre in sys.argv for genre in genres(DATA_DIRS)):
		choice_list = [ 
			song for song in generateSelectionList(DATA_DIRS) 
			if getGenre(song) in sys.argv
		]
		s = random.choice(choice_list)
	else:
		# Chooses one random video file
		s = random.choice(generateSelectionList(DATA_DIRS))
	
	print('\nfull path:', '"{}"'.format(s))
	basename = s.split('\\')[-1]
	print('playing "{}"\n'.format(basename))

	# qq() function is needed here because spaces
	# must be escaped in file paths when passed as arguments
	os.execv(MEDIA_PLAYER, [qq(MEDIA_PLAYER), qq(s)])

except Exception as e:
	print('\n{}\n'.format(e))