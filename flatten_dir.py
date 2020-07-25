import os
import sys
import shutil
import argparse
from pathlib import Path

def flatten_dir(target_dir, destination, options):
    for child in target_dir.iterdir():
        if child.is_dir():
            flatten_dir(child, destination, options)
        else:
            if child.parent != destination:
                transport = Path(destination, child.name)
                if not options.dry_run:
                    if options.delete:
                        child.rename(transport)
                    else:
                        shutil.copy(child, transport)
                if options.log:
                    action_log_symbol = '-->' if options.delete else '<->'
                    print(f'{child} {action_log_symbol} {transport}')

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Flatten a directory tree.')
    
    parser.add_argument(
        'target', 
        type=Path, 
        metavar='<target-directory>',
        help='the directory to flatten (defaults to current environment directory)')
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='do a test run of the file operations without modifying any files')
    
    parser.add_argument(
        '--no-log',
        action='store_false',
        dest='log',
        help='supress output of file operations')
    
    parser.add_argument(
        '--no-delete',
        dest='delete',
        action='store_false',
        help='prevent the original tree subfolders from being deleted')

    args = parser.parse_args()
    absolute_target = args.target.resolve()
    flatten_dir(absolute_target, absolute_target, args)
    
