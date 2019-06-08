from os import remove as delete
from os.path import basename
import re
import subprocess
import sys
import time
from pathlib import Path
from termcolor import colored
from tqdm import tqdm
from chardet import detect

from lib.print_utils import wr
from lib.encode import (
    u8dec,
    u8enc
    )




# Gets the beginning time for script execution
# to later calculate total operation time
start_time = time.time()

# WARNING: ONLY WORKS WITH UNICODE FILES (UTF-8)
# Set this to the directory where all your text files are located
# There must be a slash separator at the end to properly
# parse the file paths when the script is mining sentences.
DATA_DIR = Path('<path-to-your-text-files>')
# Choose whether or not to you want to open the output
# in yout text editor automatically after finishing the search
# Set to False to disable auto-opening output file
EDITOR_PATH = False
# Choose which directory to send output files
OUTPUT_DIR = str(Path.home() / 'Desktop')


def log_skipped(file_list, query_name):

    log_file = f'''
        {OUTPUT_DIR}/SKIPPED_{query_name.replace('txt', 'log')}
        '''.strip()

    with open(log_file, 'wb') as skip_log:

        skip_log.write(u8enc(
            'Files skipped in source directory ' +
            str(DATA_DIR)))

        for idx, fname in enumerate(file_list):
            # Uncomment below to print all skipped files to console
            # print(' ➥', str(idx+1).zfill(len(str(len(file_list)))), fname)
            n = str(idx+1).zfill(len(str(len(file_list))))
            skip_log.write(
                u8enc(f'{n}. {fname}' + '\n'))

        skip_message = '\n'.join((
            'Files were skipped due to their encoding.',
            'Files must be encoded in utf-8 in order to be used.',
            f'Open {basename(skip_log)} in a text editor',
            'to see which files were skipped.'
        ))
        print(colored(skip_message, 'yellow'))


# set() removes duplicates;
# list() turns it back into list (duh)
# for more flexible/iterable functionality
query = list(set(sys.argv[1:]))

# Error handling
no_search_term = any((
    not query,
    (len(query) == 1 and query[0].isdigit()),
    (len(query) > 1 and all(q.isdigit() for q in query))
))

if no_search_term:
    print(wr('I need a search term pal.', '\n'))
    quit()

if sum(1 for i in query if i.isdigit()) > 1:
    print(wr(
        'Only put one character limit number in your query please :)',
        '\n')
    )
    quit()

modes = ('--subs', '--novel')
if any(a in modes for a in query):
    if all(a in modes for a in query):
        mode = 'novel'
    else:
        mode = (next(
            m for m in modes if m in query)
            .replace('--', ''))
else:
    mode = 'novel'

# Initial setup before search
if (len(query) > 1) and any(q.isdigit() for q in query):
    upper_limit = next(n for n in query if n.isdigit())
else:
    upper_limit = '40'

targets = [
    q for q in query
    if q not in (f'--{mode}', upper_limit)
]

print('\n' + f'Sentence character limit: {upper_limit}')

output_basename = f'''{'-'.join(targets)}-{upper_limit}.txt'''
output_file = Path(OUTPUT_DIR) / output_basename

headline = u8enc('\n'.join((
    'Sentences mined for ' + ', '.join(targets),
    '================================'
    '\n\n\n'
)))


(print(f'Overwriting {output_basename}')
    if Path(output_file).is_file()
    else print(f'Creating {output_basename}'))

open(output_file, 'wb').write(headline)

rex_target = (
    '({})'.format('|'.join(targets)) if len(targets) > 1
    else f'({targets[0]})')

rex = {
    'novel': f'((?<=。)[^。]*{rex_target}[^。]*。)',
    'subs': f'(.*{rex_target}.*)'
}[mode]

print(f'''Here's Rexy (regex): {rex}''')
# The range [:-1] removes tailing backslash
print(f'Search target: {str(DATA_DIR)}')
print('Mining for golden Anki nuggets...', end='\n\n')

file_counter, file_match, match_count, unfiltered = 0, 0, 0, 0
skipped = []
# The search and data processing; a.k.a. the heavy lifting

text_formats = ('.txt', '.srt', '.ass')

for file in tqdm(DATA_DIR.glob('**/*')):

    if file.is_dir() or not str(file).endswith(text_formats):
        continue

    # Useful for something?
    # ext = next(
    #     f for f in text_formats
    #     if str(file).endswith(f))

    with open(file, 'rb') as current_file:

        try:
            text = u8dec(current_file.read())
        except Exception as e:
            skipped.append(file)
            continue

        file_counter += 1

        if (re.search(rex, text)):
            file_match += 1
            # Because the regex returns a list of tuples
            # when multiple argument search words are given,
            # the first (zero) index of each tuple is always the full sentence.
            matches = [x[0].strip('\r\n 　') for x in re.findall(rex, text)]
            unfiltered += len(matches)
            # Removes matches larger than the specified character limit
            limited = [
                sentence for sentence in matches
                if len(sentence) <= int(upper_limit)]

            match_count += len(limited)

            # This is only needed because all matches could be
            # thrown out if they are above the character limit
            if not limited:
                continue

            # Additional processing to enumerate
            # if multiple matches are found
            if (len(limited) > 1):
                z_pad = len(str(len(limited)))
                z_pad = 2 if z_pad < 2 else z_pad

                trimmed = [
                    f'{str(i+1).zfill(z_pad)}. {x}'
                    for i, x in enumerate(limited)]
            else:
                trimmed = limited

            file_name = str(file)

            # Special file name format processing
            # name format: TITLE // AUTHOR（著）
            file_name = re.sub(
                r"(?P<author>.+) –– (?P<title>.+)",
                r'\g<title> // \g<author>（著）',
                file_name
            )
            file_name = re.sub(
                r"([^ ])(\(校正)",
                r'\g<1> \g<2>',
                file_name
            )

            blob = ([
                file_name.replace(str(DATA_DIR), ''),
                '----------------'] +
                trimmed +
                ['\n\n'])

            # [item for sublist in l for item in sublist]
            pancake = [i for i in blob]

            content = u8enc('\n'.join(pancake))
            open(output_file, 'ab').write(content)

print('')
print('Files found:\t\t', colored(file_counter, 'cyan'))

skip_print_count = (
    colored(len(skipped), 'red')
    if len(skipped) > 0 else colored('0', 'cyan'))

print('Files skipped:\t\t', skip_print_count)
if len(skipped) > 0:
    log_skipped(skipped, output_basename)

print('Files scanned:\t\t', colored(file_counter - len(skipped), 'cyan'))
print('Files matched:\t\t', colored(file_match, 'cyan'))
print('Matches found:\t\t', colored(unfiltered, 'cyan'))
print('Matches limited:\t', colored(unfiltered - match_count, 'cyan'))
print('Matches kept:\t\t', colored(match_count, 'cyan'))

# Print completion statement with operation time
completed_time = time.time() - start_time
if completed_time < 60:
    print(
        colored('COMPLETED', 'green') + ' extraction in ' +
        colored(f'{completed_time:.1f} seconds', 'green'),
        end='\n\n'
    )
else:
    m = int(completed_time / 60)
    s = int(completed_time % 60)
    print(
        colored('COMPLETED', 'green') + ' extraction in ' +
        colored(f'{m}m {str(s).zfill(2)}s', 'green'),
        end='\n\n'
    )


if match_count is 0:
    delete(output_file)
    print('')
    print(' '.join((
            'Output file was deleted since no matches',
            'were kept for your search.'
        )),
        end='\n\n')

# opens output file in your favorite text editor
# change the path to the editor path on your machine
if EDITOR_PATH:
    subprocess.call([EDITOR_PATH, output_file])
