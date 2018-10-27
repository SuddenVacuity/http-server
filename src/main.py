'''
This file is subject to the terms and conditions found 
in the file "LICENSE" located in the project base directory.
'''

import sys # used to read command line arguments

import json

import server
import config
import threading

from window import frames
from serverLogic import pageIndex
from directoryIndex import directory

# initialization function to be run on a seperate thread
# in order to allow the gui to be run as the rest of the program is starting up
def init():
	# load the config file from storage
	if(config.importConfigFile() != True):
		frame.displayText("Import config.json failed.", begin="\nWARNING > ")

		while True:
			frame.displayText("Continue using default values? y/n")
			
			userInput = frame.awaitInput().lower()
			frame.displayText(userInput, begin="\n<< ")

			if(userInput.lower() == 'y'):
				break
			elif(userInput.lower() == 'n'):
				quit()
			else:
				frame.displayText("Invalid input")

	# override defaults/config with command line arguments
	if(len(sys.argv) > 1):
		args = sys.argv[1:]
		for arg in args:
			keyValue = arg.split("=")
			if(len(keyValue) != 2):
				frame.displayText("WARNING: Invalid argument {0}".format(arg))
				continue
			config.setKeyValue(keyValue[0], keyValue[1])
			frame.displayText("Set config from argument: {0}".format(arg))

	# apply config values to the server
	directory.setBaseDirectory(config.getKeyValue("baseDirectory"))
	HOST = config.getKeyValue("ip4host")
	PORT = config.getKeyValue("port")

	# search for unregistered index.html files
	pageIndex.findIndexes()

	# run server
	_server = server.ThreadedServer(HOST, PORT)
	_server.start()

	frame.setStatus("STATUS: Listening")
	frame.displayText("Service Started on: {0}:{1}".format(HOST, PORT))

if __name__ == "__main__":
	frames.init("HTTP Server", "STATUS: Startup - HOST: None")
	frame = frames.mainFrame

	# start thread dhere
	app = threading.Thread(target=init, daemon=True)
	app.start()

	# open gui and start taking operator input
	frames.mainloop()

	quit()
