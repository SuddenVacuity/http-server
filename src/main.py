'''
This file is subject to the terms and conditions found 
in the file "LICENSE" located in the project base directory.
'''

import sys # used to read command line arguments

import json

import server
from serverLogic import accessFile
from directoryIndex import directory

if __name__ == "__main__":
	HOST = "127.0.0.1"
	PORT = 80

	# try to load config data
	try:
		configData = accessFile.readFile(directory.base + "/config.json", directory.base)
		configDict = json.loads(configData)

		HOST = configDict['ip4host']
		PORT = configDict['port']
	except:
		print("Import config.json failed.")
		while True:
			userinput = input("Continue using default values? y/n").lower()
			if(userinput == 'y'):
				server.run()
				quit()
			elif(userinput == 'n'):
				quit()
	
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
