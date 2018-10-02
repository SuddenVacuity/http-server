'''
This file is subject to the terms and conditions found 
in the file "LICENSE" located in the project base directory.
'''

import sys # used to read command line arguments

import json

import server
import config
from console import consoleThread
from directoryIndex import accessFile
from directoryIndex import directory

if __name__ == "__main__":
	# load the config file from storage
	if(config.importConfigFile() != True):
		while True:
			userinput = input("Continue using default values? y/n >> ").lower()
			if(userinput.lower() == 'y'):
				break
			elif(userinput.lower() == 'n'):
				quit()
			else:
				print("Invalid input")

	# override defaults/config with command line arguments
	if(len(sys.argv) > 1):
		args = sys.argv[1:]
		for arg in args:
			keyValue = arg.split("=")
			if(len(keyValue) != 2):
				print("WARNING: Invalid argument {0}".format(arg))
				continue
			config.setKeyValue(keyValue[0], keyValue[1])
			print("Set config from argument: {0}".format(arg))

	# apply config values to the server
	directory.setBaseDirectory(config.getKeyValue("baseDirectory"))
	HOST = config.getKeyValue("ip4host")
	PORT = config.getKeyValue("port")

	# start waiting for console input
	consoleThread.start()

	# run server
	server.run(HOST, PORT)
	quit()
