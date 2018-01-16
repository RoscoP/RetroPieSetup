#!/usr/bin/python
import os
import argparse
import glob
import re
import fnmatch

# shopt -s nocaseglob

def do_cmd(cmd, showonly=False):
	if showonly:
		print(cmd)
		return 0
	else:
		ret = os.system(cmd)
		if ret != 0:
			print("Command: {} failed : {}".format(cmd, ret))
		return ret

parser = argparse.ArgumentParser(description='List to process')
parser.add_argument('--list', '-l', default='_TOP_NES_.lst', type=str, help='ROM list')
parser.add_argument('--ext' , '-e', default='.zip', type=str, help='Extension')
parser.add_argument('--all' , '-a', default='+ALL+', type=str, help='All folder')
parser.add_argument('--show' , '-s', action='store_true', help='Only show')
args = parser.parse_args()

data = open(args.list, 'r').readlines()
data = [a.rstrip() for a in data]
all_files = os.listdir(args.all)
# Make a mapping of filenames without (xxx) to full names
all_files = {re.sub("\s?\(.*\)\s?",'',f):f for f in all_files}
#print all_files

for r in data:
	file = '{}/{}{}'.format(args.all, r, args.ext)
	if os.path.exists(file):
		do_cmd('ln -s "{}" .'.format(file), args.show)
	else:
		pattern = '{}{}'.format(r, args.ext)
		regex = re.compile(fnmatch.translate(pattern), re.IGNORECASE)
		file_matches = [f for f in all_files.keys() if regex.match(f)]
		# file_match = glob.glob('{}/{}*{}'.format(args.all, r, args.ext))
		if file_matches:
			cmd = 'ln -s "{}/{}" "{}"'.format(args.all, all_files[file_matches[0]], all_files[file_matches[0]])
			ret = do_cmd(cmd, args.show)
		else:
			print("File doesn't exist: {}".format(file))
# find and delete broken links
os.system("find -L ./ -type l -delete")