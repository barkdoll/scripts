import re
import sys
import os
import requests
import shutil
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def slugify(value):
	"""
	https://stackoverflow.com/a/295466/10039085
	
	Originally from the Django framework.
	
	Normalizes string, converts to lowercase, removes non-alpha characters,
	and converts spaces to hyphens.
	"""
	value = re.sub(r'[^\w\s\-\.]', '', value).strip().lower()
	value = re.sub('[-\s]+', '-', value)
	return value

def download_file(url):
	path_segments = url.split('/')[-3:-1]
	fname = slugify(url.split('/')[-1])

	dir_path = os.path.join(
		os.path.expanduser('~'), 
		'Desktop', 'test', 'seisho', *path_segments
	)
		
	if not os.path.exists(dir_path):
		os.makedirs(dir_path)

	fpath = os.path.join(dir_path, fname)
	print(fpath)

	with requests.get(url, stream=True, verify=False) as r:
		with open(fpath, 'wb') as f:
			shutil.copyfileobj(r.raw, f)

			# alternative method
			# for chunk in r.iter_content(chunk_size=1024): 
			# 	if chunk: # filter out keep-alive new chunks
			# 		f.write(chunk)

	return fpath


def main(url, target):

	hostname = urlparse(url).hostname

	sauce = requests.get(url).content
	soup = BeautifulSoup(sauce, 'html.parser')

	batch_list = []

	for a in soup('a'):
		if a['href'].endswith(target):
			link = a['href']
			
			if not a['href'].startswith(url):
				link = url + link			
			batch_list.append(link)
	
	for thing in batch_list:
		# print(thing)
		download_file(thing)
	
	print('done!')
	return


if len(sys.argv) is 3:
	main(sys.argv[1], sys.argv[2]);

else:
	print('pass exactly two arguments')
	print('first argument is the url')
	print('second argument is the file ending that the links should contain (e.g. - ".pdf")')
	
