'''
This file is subject to the terms and conditions found 
in the file "LICENSE" located in the project base directory.
'''

import os # used to check for filepath backwards traversal attempts
import sys # used to check for filepath backwards traversal attempts

from directoryIndex import directory # used to check for filepath backwards traversal attempts

# confirm the requested directory is within the input base directory
# RETURNS: (bool) isContained
def isDirectoryContained(targetpath, basepath, follow_symlinks=True):
	if(follow_symlinks == True):
		return os.path.realpath(targetpath).startswith(basepath)

	return os.path.abspath(targetpath).startswith(basepath)

# filepath (str) - local filepath to the file to read
# RETURNS: (bytes)data read from file
def readFile(filepath, basepath):
	data = b''

	# confirm the requested directory is within the intended accessable area
	if (isDirectoryContained(filepath, basepath) == False):
		print("Illegal Read attempted on file:", filepath)
		return b'Can\'t let you do that Starfox.'

	print("Read File:", filepath)
	try:
		with open(filepath, 'rb') as f:
			data = f.read()
	except FileNotFoundError:
		print("ERROR: accessFile.py >> readFile(): File Does Not Exist.")
		print("Error File:", filepath)
		data = b''
	except:
		print("ERROR: accessFile.py >> readFile(): Unable to Read File.")
		print("Error File:", filepath)
		data = b''

	return data

# creates a new file overwriting any existing file at the same path
# filepath (str) - local filepath to the file to write to
# data (str) - data to be written
# RETURNS: (bool) success
def writeFile(filepath, data, basepath):
	# confirm the requested directory is within the intended accessable area
	if (isDirectoryContained(filepath, basepath) == False):
		print("Illegal Write attempted on file:", filepath)
		return False

	print("Write File:", filepath)
	try:
		with open(filepath, 'wb') as f:
			f.write(data)
	except:
		print("ERROR: accessFile.py >> writeFile(): Unable to Write to File")
		print("Error File:", filepath)
		return False

	return True