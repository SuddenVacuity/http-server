'''
This file is subject to the terms and conditions found 
in the file "LICENSE" located in the project base 
'''

# This metohod of managing filepaths is temporary

# private directories
base = "" # this is loaded from config.json in the projects base directory
database = base + "/db"

# public directories
www = base + "/www"
image = www + "/image"
imageShared = image + "/shared"

# changes the base directory and updates sub directories to match the change
def setBaseDirectory(path):
	global base
	base = path

	global database
	database = base + "/db"

	global www
	www = base + "/www"

	global image
	image = www + "/image"

	global imageShared
	imageShared = image + "/shared"
