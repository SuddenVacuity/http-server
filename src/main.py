'''
This file is subject to the terms and conditions found 
in the file "LICENSE" located in the project base directory.
'''

import sys # used to read command line arguments

import json

import server
import config
from serverLogic import accessFile
from directoryIndex import directory

if __name__ == "__main__":
	config.importConfigFile()

	directory.setBaseDirectory(config.values["baseDirectory"])
	HOST = config.values["ip4host"]
	PORT = config.values["port"]

	# override defaults/config with command line arguments
	if(len(sys.argv) == 2):
		arg = sys.argv[1]
		try:
			arg = int(arg)
			PORT = arg
		except:
			print("Argument for port must be an int")

	server.run(HOST, PORT)
	quit()
