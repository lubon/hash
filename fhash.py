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

hash_table = list()
hist_file = ''
log_file = ''

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
# compare name and hash value
	global hash_table
	for i in range(len(hash_table)):
		for j in range(len(hash_table)):
			if i<>j and hash_table[i][3]==hash_table[j][3] and hash_table[i][4]==hash_table[j][4]:
				print hash_table[i][2], hash_table[i][4], hash_table[i][3]
	return

#---------------------------------------
def find_name_dups():
# compare folder names
	global hash_table
	i=1
	for i in range(len(hash_table)):
		for j in range(len(hash_table)):
			sss = difflib.SequenceMatcher(None, hash_table[i][2], hash_table[j][2]);
			if sss.quick_ratio()>0.1 and i<>j: print sss.quick_ratio(), hash_table[i][2], hash_table[j][2]
	return


#-------------------------------------------------------

def save_data(fname):
	global hash_table

#	privatekey = RSA.generate(1024, rng)
#	publickey = privatekey.publickey()
#	enc_data = publickey.encrypt(hash_table)
#	dec_data = privatekey.decrypt(enc_data)
	if os.path.isfile(fname): os.rename(fname, fname+'.old')
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
		fhash -i database.db -c1 /tmp/*.txt
		fhash -o database.db /tmp/*.txt''')

parser.add_argument('-i','--input', help='Input file name',type=str)
parser.add_argument('-o','--output',help='Database file name',type=str)
parser.add_argument('-c','--compare',help='Compare the files with database',type=int, choices=[1,2])
parser.add_argument('-v','--version',action='version', version='%(prog)s 1.0')
parser.add_argument('-d','--debug',help='Show debug messages',type=int)
#parser.add_argument('-g','--generate',help='Generate the file database')
parser.add_argument('directory', help='directory where to look')
args = parser.parse_args()
debug_msg(args.source)

#cmd_prompt=sys.argv

if (args.input=='')and(args.compare==0):
		debug_msg("generating database",args.input)
		process_files(args.directory , "*")
if (args.input<>'')and(args.compare>0):
		debug_msg("loading database")
		load(args.input)
if args.compare==2:
		debug_msg("phase2a - same size dups")
		find_hash_dups()
if args.compare==1:
		debug_msg("phase2b - similar names")
		#find_name_dups()
if args.output<>'':
	save_data(args.output)

