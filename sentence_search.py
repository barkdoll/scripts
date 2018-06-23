import os
import re
import subprocess
import sys
import time
from pathlib import Path
from termcolor import colored
from tqdm import tqdm

# Gets the beginning time for script execution
# to later calculate total operation time
start_time = time.time()

# WARNING: ONLY WORKS WITH UNICODE FILES (UTF-8)
# Set this to the directory where all your text files are located
# There must be a slash separator at the end to properly
# parse the file paths when the script is mining sentences.
DATA_DIR = '<insert-directory-to-be-searched-here>'
# Choose whether or not to you want to open the output
# in yout text editor automatically after finishing the search
EDITOR_PATH = '<insert-path-to-your-text-editor-or-set-below-variable-to-False>'
# Set to False to disable auto-opening output file
i_want_to_open_the_output_file_in_my_text_editor = True
# Choose which directory to send output files
OUTPUT_DIR = os.path.expanduser('~') + '\\Desktop\\'


def isNumber(s):
	try:
		int(s)
		return True
	except ValueError:
		return False


def logSkipped(file_list, query_name):
	with open(OUTPUT_DIR + 'SKIPPED_'
           + query_name.replace('txt', 'log'), 'wb') as skip_log:
		skip_log.write('Files skipped in source directory {}\n'
                 .format(DATA_DIR).encode())
		for idx, fname in enumerate(file_list):
			# Uncomment below to print all skipped files to console
			# print(' ➥', str(idx+1).zfill(len(str(len(file_list)))), fname)
			skip_log.write((
				'{0}. {1}\n'.format(str(idx+1).zfill(len(str(len(file_list)))), fname)
			).encode())

		skip_message = (
			'Files were skipped due to their encoding.\n'
			+ 'Files must be encoded in utf-8 in order to be used.\n'
			+ 'Open {} in a text editor\n'
			+ 'to see which files were skipped.'
		).format(skip_log.name.split('\\')[-1])
		print(colored(skip_message, 'yellow'))


# set() removes duplicates;
# list() turns it back into list (duh)
# for more flexible/iterable functionality
query = list(set(sys.argv[1:]))

# Error handling
if not query or (len(query) == 1 and isNumber(query[0])) or \
	(len(query) > 1 and all(isNumber(q) for q in query)):
	print('\nI need a search term pal.\n')
	sys.exit(1)

if sum(1 for i in query if isNumber(i)) > 1:
	print('\nOnly put one character limit number in your query please :)\n')
	sys.exit(1)


# Initial setup before search
if (len(query) > 1) and any(isNumber(q) for q in query):
	upper_limit = next(n for n in query if isNumber(n))
	query = [q for q in query if not isNumber(q)]
else:
	upper_limit = '40'

print('\nSentence character limit:', upper_limit)

output_basename = '{}-{}.txt'.format('-'.join(query), upper_limit)
output_file = OUTPUT_DIR + output_basename

headline = (
	'Sentences mined for ' + ', '.join(query) +
	'\n================================\n\n'
).encode('utf-8')


if Path(output_file).is_file():
	print('Overwriting {}'.format(output_basename))
else:
	print('Creating {}'.format(output_basename))

open(output_file, 'wb').write(headline)


if len(query) > 1:
	query = '({})'.format('|'.join(query))
else:
	query = '({})'.format(query[0])

rex = '((?<=。)[^。]*' + query + '[^。]*。)'

print('Here\'s Rexy-boy (regex pattern):', rex)
print('Search target:', DATA_DIR)
print('Mining for golden Anki nuggets...\n')

file_counter, match_counter, file_match, dir_counter = 0, 0, 0, 0
skipped = []
# The search and data processing; a.k.a. the heavy lifting
for file in tqdm(os.listdir(DATA_DIR)):
	if Path(DATA_DIR + file).is_file():
		file_counter += 1

		with open(DATA_DIR + file, 'rb') as currentFile:
			try:
				text = currentFile.read().decode('utf-8')
			except Exception as e:
				skipped.append(file)
				continue

			if (re.search(rex, text)):
				file_match += 1
				# Because the regex returns a list of tuples
				# when multiple argument search words are given,
				# the first (zero) index of each tuple is always the full sentence.
				matches = [x[0].strip('\r\n 　') for x in re.findall(rex, text)]
				# Removes matches larger than the specified character limit
				trimmed = [sentence for sentence in matches
                                    if len(sentence) <= int(upper_limit)]

				for s in trimmed:
					match_counter += 1

				# Additional processing to enumerate
				# if multiple matches are found
				if (len(trimmed) > 1):
					trimmed = ['{}. {}'.format(str(i+1).zfill(2), x)
                                            for i, x in enumerate(trimmed)]

				# This is only needed because all matches could be
				# thrown out if they are above the character limit
				if not trimmed:
					pass
				else:
					file_name = file.split('.txt')[0]

					# Special file name format processing
					# for the 3000+ book repo
					# name format: TITLE // AUTHOR（著）
					# ==== uncomment below to activate ====
					file_name = re.sub(
						r"(?P<author>.+)[－-](?P<title>.+)",
						r'\g<title> // \g<author>（著）',
						file_name
					)
					file_name = re.sub(
						r"([^ ])(\(校正)",
						r'\g<1> \g<2>',
						file_name
					)

					blob = [file_name, '----------------'] + \
						trimmed + ['\n\n']

					content = '\n'.join(blob).encode('utf-8')
					open(output_file, 'ab').write(content)
	elif Path(DATA_DIR + file).is_dir():
		dir_counter += 1


print('')
if dir_counter > 0:
	print('Directories ignored:', dir_counter)

print('Files found:', colored(file_counter, 'cyan'))

skip_print_count = colored(len(skipped), 'red') \
	if len(skipped) > 0 else colored('0', 'cyan')
print('Files skipped:', skip_print_count)
if len(skipped) > 0:
	logSkipped(skipped, output_basename)

print('Files scanned:', colored(file_counter - len(skipped), 'cyan'))
print('Files matched:', colored(file_match, 'cyan'))
print('Matches found:', colored(match_counter, 'cyan'))

# Print completion statement with operation time
completed_time = time.time() - start_time
if completed_time < 60:
	print(colored('COMPLETED', 'green') + ' extraction in '
            + colored('{0:.1f} seconds'.format(completed_time), 'green'))
else:
	m = int(completed_time / 60)
	s = int(completed_time % 60)
	print(colored('COMPLETED', 'green') + ' extraction in '
            + colored('{}m {}s'.format(m, str(s).zfill(2)), 'green'))

print('')

# opens output file in your favorite text editor
# change the path to the editor path on your machine
if i_want_to_open_the_output_file_in_my_text_editor:
	subprocess.call([EDITOR_PATH, output_file])
