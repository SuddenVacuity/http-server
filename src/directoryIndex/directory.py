'''
This file is subject to the terms and conditions found 
in the file "LICENSE" located in the project base 
'''

import os # used to check if directories exist and create them if they don't
import errno # check exceptions thrown

# This method of managing filepaths is temporary

# this should be chaged depending on the operating system the server is run on.
#   linux/mac: "/"
#   windows:   "\\" # needs to be escaped
_SLASH = "/"
if(os.name != "posix"):
	_SLASH = "\\"
	
# the os user permission level of any directories created
_DIRECTORY_PERMISSION_LEVEL = 0o777

# folder names for each part of the directory tree
_www    = "www"
_db     = "db"
_subImages = "images"
_subText   = "text"
_subAudio  = "audio"
_subVideo  = "video"
_subJson   = "jsonText"

# the directory where the www and database folders exist
# this is either loaded from config.json in the projects base directory 
# or set to the relative project base dir (src/main.py/../)
base = "" 

# base folders
www = _SLASH + _www
database = _SLASH + _db

# database subfolders
databaseImages = database + _SLASH + _subImages
databaseText   = database + _SLASH + _subText
databaseAudio  = database + _SLASH + _subAudio
databaseVideo  = database + _SLASH + _subVideo
databaseJson   = database + _SLASH + _subJson

# changes the base directory and updates sub directories to match the change
# also ensures the set directories exist
# this must be run on startup
def setBaseDirectory(path):
	global base
	base = path
	makeDir(base)

	global www
	global database
	www = base +_SLASH +  _www
	database = base +_SLASH +  _db
	makeDir(www)
	makeDir(database)

	global databaseImages
	global databaseText
	global databaseAudio
	global databaseVideo
	global databaseJson
	databaseImages = database + _SLASH + _subImages
	databaseText   = database + _SLASH + _subText
	databaseAudio  = database + _SLASH + _subAudio
	databaseVideo  = database + _SLASH + _subVideo
	databaseJson   = database + _SLASH + _subJson
	makeDir(databaseImages)
	makeDir(databaseText)
	makeDir(databaseAudio)
	makeDir(databaseVideo)
	makeDir(databaseJson)

# make sure all the directories exist
# this runs on startup and should be a fail point
def makeDir(directory):
	# mkdir won't make a folder unless the name ends with a slash
	if(directory.endswith(_SLASH) == False):
		directory = directory + _SLASH

	try:
		os.mkdir(os.path.dirname(directory))
		os.chmod(os.path.dirname(directory), _DIRECTORY_PERMISSION_LEVEL)
	# an exception is raised if the directory already exists
	# this is to be extra confirmation that a directory previously existed
	except OSError as e:
		# make sure the exception is actually because the directory exists
		if e.errno == errno.EEXIST:
			print("filepath already exists: {0}".format(directory))
			return
		else:
			raise

	print("filepath created: {0}".format(directory))

# searches a directory for a target file
# path (str) - 
# target (str) - 
# OPTIONS: caseSensitive (True) - 
#          recursive (True) - 
# RETURNS: [(str), ...] - list of all directories containing the target
def searchDirectory(path, target, caseSensitive=True, recursive=True):
	indexList = []

	if(caseSensitive == False):
		target = target.lower()

	dirs = os.listdir(path)

	for d in dirs:
		if(caseSensitive == False):
			d = d.lower()

		current = path + "/" + d
		if(os.path.isfile(current) == True):
			if(d == target):
				indexList.append(path)
		elif(recursive == True):
			if(os.path.isdir(current) == True):
				subIndexList = searchDirectory(current, target)
				indexList = indexList + subIndexList

	return indexList