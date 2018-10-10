'''
This file is subject to the terms and conditions found 
in the file "LICENSE" located in the project base directory.
'''

import os # used to get project base directory
import sys # used to get project base directory
import json

from directoryIndex import accessFile

# This loads key/value pairs form file config.json and makes the values
# available to the server during runtime

# dictionary containing the key/value pairs
_values = {}

# sets the config values to default
def _setDefault():
	# default project base directory
	# NOTE: do not add trailing slash
	# NOTE: this must lead to the folder containing folders www, db and file config.json
	abspath = os.path.abspath(sys.argv[0])
	path, file = os.path.split(abspath)
	_values["baseDirectory"] = os.path.realpath(path + "/..")

	# ip config
	_values["ip4host"] = "127.0.0.1"
	_values["port"] = 80

def help():
	return "Use this command to access configuration options \
		\r  Commands:\
		\r  @config.read.key\
		\r     Get the value of [key] from the current configuration\
		\r  @config.set.key=value\
		\r     Set the current configuration option [key] to [value]"

# loads the config.json file and imports all key/value pairs to memory
# RETURNS: (bool) succcess
def importConfigFile():
	_setDefault()

	# try to load config data
	try:
		# this must lead to where config.json exists
		fileDirectory = _values["baseDirectory"]
		configData = accessFile.readFile(fileDirectory + "/config.json", fileDirectory)

		configDict = json.loads(configData)
		loadedKeys = configDict.keys()

		for key in loadedKeys:
			_values[key] = configDict[key]

	except:
		print("Import config.json failed.")
		_setDefault()
		return False

	return True

# Takes a key/value pair and converts the type of value based on what data the key requires
# key (str) - the key associanted with the value to be stored
# value (str) - the value to be stored associated with the key
def setKeyValue(key, value):
	# convert the type of all values that should not be stored as (str)
	# NOTE: This was decided to prevent a value of the wrong type to be stored nd prevent a value of the 
	#       incorrect type to be called causing errors/exception,
	# Exceptions will occur as soon as the value is set giving a warning that the type was incorrect
	if(key == "port"):
		try:
			value = int(value)
			_values[key] = value
		except:
			print("WARNING: config.py >> \"{0}\": Argument must be an int".format(key))
	else:
		_values[key] = value


# Gets the value associated with a key
# RETURNS: () value stored in dictionary for key
#          NOTE: the data type depends on what type the data stored in the dictionary is.
#                Find the key in setKeyValue() to see the type it is stored as
#          returns None if the value does not exist
def getKeyValue(key):
	if not key in _values:
		return None
	return _values[key]
