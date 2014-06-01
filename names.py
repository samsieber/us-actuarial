#!/usr/bin/env python

import os
from os import listdir
from os.path import isfile, join

#http://stackoverflow.com/questions/3207219/how-to-list-all-files-of-a-directory-in-python
def getfiles(mypath):
	return [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]

def getFileList():
	my_dir = os.getcwd() + "/names"
	return [my_dir + "/" + fname for fname in getfiles(my_dir)]

def get_name_set(file_name, mf):
	with open(file_name) as f:
		return set([line.split(',')[0] for line in f.readlines() if line.split(",")[1] == mf])
		
#http://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks-in-python	
from itertools import izip, chain, repeat
def grouper(n, iterable, padvalue=None):
    "grouper(3, 'abcdefg', 'x') --> ('a','b','c'), ('d','e','f'), ('g','x','x')"
    return izip(*[chain(iterable, repeat(padvalue, n-1))]*n)

def chunk_it(seq, size):
	return [seq[i:i+size] for i  in range(0, len(seq), size)]

import csv
def write_chunk(sorted_keys, data_source, folder):
	dest_file = folder + "/" + sorted_keys[0].replace(" ","_").lower() + ".csv"
	rows = [[name] + data_source[name] for name in sorted_keys]
	with open(dest_file, 'wb') as csvfile:
		filewriter = csv.writer(csvfile, delimiter=' ',
			quotechar='|', quoting=csv.QUOTE_MINIMAL)
		for row in rows:
			filewriter.writerow(row)

def get_data(directory, mf):
	# get target directory
	my_dir = os.getcwd() + directory
	# list all of the file names
	fnames = getfiles(my_dir)
	# sort them
	inorder = sorted(fnames)
	# get the full path to them
	filelist = [my_dir + "/" + fname for fname in inorder]
	# get a set of names from each file
	sets = [get_name_set(fname,mf) for fname in filelist]
	# union them
	unioned = set.union(*sets)
	# init the name lookup
	names = {}
	# provide a empty list for each name
	for name in unioned:
		names[name] = []
	# we'll iterate over the files (sorted in chronological order
	for full_name in filelist:
		with open(full_name) as f:
			# give each name a default of 0 (in case it's not in there)
			for name in names:
				names[name].append(0)
			for line in f:
				name, gender, number = line.split(",")
				# if it's the correct gender
				if gender == mf:
					# overwrite the last value in the list
					names[name][-1] = int(number.strip())
	# sort all the names we have in our master list
	alpha_names = sorted(names.keys())
	# put it into a bunch of chunks
	chunked = chunk_it(alpha_names,199)
	# the file names of the output are based on the first name in each chunk
	chunk_1_names = [l[0] for l in chunked]
	# write each chunk
	for chunk in chunked:
		write_chunk(chunk, names, "files/"+mf)
	# write the index
	import json
	with open("files/"+mf+"/index.txt", 'w') as outfile:
		json.dump({"first_names":chunk_1_names, "first_year":1880}, outfile)
		

if __name__ == "__main__":
	get_data("/names","M")
	get_data("/names","F")
