FHASH
=========

Project for  searching and identifying duplicate files within a directory.


Requirements
------------

Python 2.x


Usage
-----

initiate the file database
fhash.py -s /directory/ -o database.db

run a filename comparison
fhash.py -i database.db -c 1

run a filesize comparison
fhash.py -i database.db -c 2

run a hash comparison
fhash.py -i database.db -c 3

run a similar name comparison
fhash.py -i database.db -c 4

clone a database (not useful yet)
fhash.py -i database.db -o database2.db



Changelog
---------



License
-------
The fhash is licensed under GPL V3.

