# Based on Andre Torres' tutorial here:
# https://www.pythoncentral.io/finding-duplicate-files-with-python/

import os
import sys
import hashlib

def findDup(parentFolder):
	# Dups in format {hash:[names]}
	dups = {}
	for dirName, subdirs, fileList in os.walk(parentFolder):
		print('Scanning %s...' % dirName)
		counter = 0
		for filename in fileList:
			counter += 1
			sys.stdout.write('\rfiles scanned: {}'.format(counter))
			sys.stdout.flush()
			# Get the path to the file
			path = os.path.join(dirName, filename)
			# Calculate hash
			file_hash = hashfile(path)
			# Add or append the file path
			if file_hash in dups:
				dups[file_hash].append(path)
			else:
				dups[file_hash] = [path]

	return dups

# Join two dictionaries
def joinDicts(dict1, dict2):
	for key in dict2.keys():
		if key in dict1:
			dict1[key] = dict1[key] + dict2[key]
		else:
			dict1[key] = dict2[key]

def hashfile(path, blocksize = 65536):
	afile = open(path, 'rb')
	hasher = hashlib.md5()
	buf = afile.read(blocksize)
	while len(buf) > 0:
			hasher.update(buf)
			buf = afile.read(blocksize)
	afile.close()
	return hasher.hexdigest()

def printResults(dict1):
	results = list(filter(lambda x: len(x) > 1, dict1.values()))
	if len(results) > 0:
		print('\n\n{} duplicates found:'.format(len(results)))
		print('The following files are identical. The name could differ, but the content is identical')
		print('___________________')
		for result in results:
			for subresult in result:
				print('\t%s' % subresult)
			print('___________________')

	else:
		print('No duplicate files found.')

if __name__ == '__main__':
	if len(sys.argv) > 1:
		dups = {}
		folders = sys.argv[1:]
		for i in folders:
			# Iterate the folders given
			if os.path.exists(i):
				# Find the duplicated files and append them to the dups
				joinDicts(dups, findDup(i))
			else:
				print('{} is not a valid path, please verify'.format(i))
				sys.exit()
		printResults(dups)
	else:
		print(
			'Usage:\t\tOption #1. python {} folder\n'\
				.format(os.path.basename(__file__)) + 
			'\t\tOption #2. python {} folder1 folder2 folder3'\
				.format(os.path.basename(__file__))
		)