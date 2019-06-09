import os, sys, re, cmd, random, psutil
from os.path import basename
from pathlib import Path
from mutagen import File as MutaFile
from lib.print_utils import wr

# Source directories for your video files
DATA_DIRS = [ 'put all of your', 'audio file paths', 'in this list' ]
# Path to your media player executable
MEDIA_PLAYER = 'C:\\Program Files\\change\\this\\path\\to\\your\\MediaPlayer.exe'


def is_audio(f, 
	audio_formats=('.mp3', '.m4a', '.ogg', '.wma', '.flac', '.wav')):
	return f.endswith(audio_formats):


def genres(path_list):
	genre_list = []
	for folder in path_list:
		for root, directory, files in os.walk(folder):
			for fname in files:
				fpath = root + '\\' + fname
				if is_audio(fpath):
					# I haven't figured out the most 
					# semantic way to read genre tags so 
					# for now, this works by grabbing it 
					# from the TCON property 
					if MutaFile(fpath) and MutaFile(fpath).tags.get('TCON'):
						genre = str( MutaFile(fpath).tags.get('TCON') ).lower()
						if genre not in genre_list:
							genre_list.append(genre)
	# common construct for removing duplicate list values
	return genre_list


def get_genre(file):
	if MutaFile(file) and MutaFile(file).tags.get('TCON'):
		file_meta_genre = str( MutaFile(file).tags.get('TCON') ).lower()
		return file_meta_genre


def generate_dir_list(data_path_list):
	dir_list = []
	for root_folder in data_path_list:
		dir_list += [
			os.path.join(root_folder, d)
			for d in os.listdir(root_folder)
			if Path(root_folder+d).is_dir()
		]
	return dir_list


def generate_select_list(data_path_list):
	file_list = []
	for root_folder in data_path_list:
		for root, directory, files in os.walk(root_folder):
			for fname in files:
				fpath = root + '\\' + fname
				if is_audio(fpath):
					file_list.append(fpath)

	return file_list

def choose_album(path_list, series_top_dir):
	while True:
		chosen_folder = random.choice(generate_dir_list(path_list))
		if series_top_dir in chosen_folder:
			break

	series_list = []
	for root, directory, files in os.walk(chosen_folder):
		for fname in files:
			fpath = root + '\\' + fname
			if is_audio(fpath):
				series_list.append(fpath)
	return series_list



try:
	# TODO: ADD SUPPORT FOR PLAYING A RANDOM ALBUM
	# if '--album' in sys.argv:
	# 	series = choose_album()
	# 	sname = series[-1].split('\\')
	# 	sname = sname[sname.index('tv_shows') + 1].split('_')
	# 	sname = ' '.join(sname).title()
	# 	print('\nplaying {}\n'.format(sname))
	# 	arg_list = [wr(MEDIA_PLAYER, '"')] + [wr(f, '"') for f in series]
	# 	os.execv(MEDIA_PLAYER, arg_list)

	if any(genre in sys.argv for genre in genres(DATA_DIRS)):
		choice_list = [ 
			song for song in generate_select_list(DATA_DIRS) 
			if get_genre(song) in sys.argv
		]
		s = random.choice(choice_list)
	else:
		# Chooses one random video file
		s = random.choice(generate_select_list(DATA_DIRS))
	
	print('\n' + f'full path: "{s}"')
	
	# TODO: get TITLE and ARTIST from Mutagen
	print(f'playing "{basename(s)}"', end='\n\n')

	# qq() function is needed here because spaces
	# must be escaped in file paths when passed as arguments
	os.execv(MEDIA_PLAYER, [qq(MEDIA_PLAYER), qq(s)])

except Exception as e:
	print(wr(e, '\n'))