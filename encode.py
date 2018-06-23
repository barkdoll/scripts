import sys
import os
from pathlib import Path
from bs4 import UnicodeDammit

try:
	DATA_DIR = '<add-folder-of-files-to-be-reencoded-here>'
	OUTPUT_DIR = '<add-folder-to-send-new-files-to-here>'
except:
	print("There's an issue with your directory path(s)")

# Make output directory if it does not exist
if not Path(OUTPUT_DIR).is_dir():
	os.makedirs(OUTPUT_DIR)

def refineEncoding(data, subs={ '_':'', 'cp':''}):
	for i, j in subs.items():
			data = data.replace(i, j)
	return data


def convert_to_utf8(filename, output_path):
	source_file_path = DATA_DIR + filename
	# decode the file
	try:
		# try to open the file and exit if some IOError occurs
		f = open(source_file_path, 'rb').read()
		
		# Handling the encoding
		e = UnicodeDammit(f)
		enc = refineEncoding(e.original_encoding)

		data = f.decode(enc)
		print('converting {} from {} to utf-8…'.format(file, enc))

		# Construct new file path
		newfile = output_path + filename
		# and at last convert it to utf-8
	
		open(newfile, 'wb').write(data.encode('utf-8'))

	except Exception as ex:
		print('error:', ex)
		pass
	

for file in os.listdir(DATA_DIR):
	if Path(DATA_DIR + file).is_file():
		convert_to_utf8(file, OUTPUT_DIR)
