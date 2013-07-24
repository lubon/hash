#!/usr/bin/python
import os
import sys
import hashlib
import simplejson
import argparse
#import re
import fnmatch
import difflib
#from Crypto.PublicKey import RSA

version = '1.0'
hash_table = list()
#hist_file = ''
#log_file = ''

def hash_file(fname):
# calculate hash value for a file
	blocksize=4096

	fl = open(fname)
	res = hashlib.sha256()
	buf=fl.read(blocksize)
	while len(buf)>0:
		buf=fl.read(blocksize)
		res.update(buf)
	fl.close()
	return res.hexdigest()

#-------------------------------------------------------
def process_files(dir,patrn):
# generate database with hash values
	global hash_table
	for root, dirs, files in os.walk(dir):
		for folder in dirs:
		   for file in fnmatch.filter(files,patrn):
				ffull=os.path.join(root,file)
				hash_table.append([root,folder,file,hash_file(ffull),os.path.getsize(ffull)])
	return

#-----------------------------------------
def find_hash_dups():
# compare hash values
	global hash_table
	for i in range(len(hash_table)-1):
		for j in range(i+1,len(hash_table)):
			if hash_table[i][3]==hash_table[j][3]:
				print hash_table[i][2], hash_table[j][2],' - ', hash_table[i][3]
	return

#---------------------------------------
def find_name_dups():
# compare file names 
        global hash_table
        for i in range(len(hash_table)-1):
                for j in range(i+1,len(hash_table)):
                        if (hash_table[i][2]==hash_table[j][2]): print hash_table[i][2], ' - ', hash_table[i][1], hash_table[j][1]
        return

#---------------------------------------
def find_name_dups2():
# compare folder names with difflib
	global hash_table
	for i in range(len(hash_table)-1):
		for j in range(i+1,len(hash_table)):
			sss = difflib.SequenceMatcher(None, hash_table[i][2], hash_table[j][2])
			if (sss.quick_ratio()>0.7): print sss.quick_ratio(), hash_table[i][2], hash_table[j][2]
	return

#---------------------------------------
def find_size_dups():
# compare sizes of the files
        global hash_table
        for i in range(len(hash_table)-1):
                for j in range(i+1,len(hash_table)):
                        if (hash_table[i][4]==hash_table[j][4]): print hash_table[i][4], ' - ', hash_table[i][2], hash_table[j][2]
        return

#-------------------------------------------------------

def save_data( fname ):
	global hash_table

#	privatekey = RSA.generate(1024, rng)
#	publickey = privatekey.publickey()
#	enc_data = publickey.encrypt(hash_table)
#	dec_data = privatekey.decrypt(enc_data)
	print fname
	if os.path.isfile(fname):
		fname_new=fname+'.old' 
		os.rename(fname, fname_new)
	file = open (fname, "w")
	simplejson.dump(hash_table,file)
	file.close()
	return

#--------------------------------------------------------

def load_data(fname):
	global hash_table
	
	if os.path.isfile(fname):
		file = open (fname, "r")
		hash_table = simplejson.load(file)
		file.close()
	else:
	     debug_msg("data file nowhere defined")
	

#-----------------------------------------------------------
def debug_msg(dmsg):
	if args.debug:
		print dmsg
	return

parser = argparse.ArgumentParser(prog='fhash',description='File hashing and comparing to the result.', usage='%(prog)s [options]', epilog='''
	Example:
		fhash -i database.db -c1
		fhash -o database.db /directory/''')

parser.add_argument('-i','--input', help='Input file name',type=str)
parser.add_argument('-o','--output',help='Database file name',type=str)
parser.add_argument('-c','--compare',help='Compare the files with database',type=int, choices=[1,2,3,4])
parser.add_argument('-v','--version',action='version', version='%(prog)s '+version)
parser.add_argument('-d','--debug',help='Show debug messages')
parser.add_argument('-s','--directory', help='directory where to look')
args = parser.parse_args()

debug_msg('Arguments: ')
debug_msg(args)

if (args.input is None):
	if (args.directory is None):
	  	sys.exit("Error: No directory is specified to initiate database from.")
	else:
		debug_msg("Generating database from "+args.directory)
		process_files(args.directory , "*")
else:
		debug_msg("Loading database from "+args.input)
		load_data(args.input)
		args.directory=args.input
if args.compare==2:
		debug_msg("Comparing files for same size dups in "+args.directory)
		find_hash_dups()
if args.compare==1:
		debug_msg("Comparing same names duplicates in"+args.directory)
		find_name_dups()
if args.compare==3:
                debug_msg("Comparing size duplicates in"+args.directory)
                find_size_dups()
if args.compare==4:
                debug_msg("Comparing similar names duplicates in"+args.directory)
                find_name_dups2()

if not (args.output is None):
		debug_msg('Saving the data to '+args.output)
		save_data(args.output)

