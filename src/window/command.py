'''
This file is subject to the terms and conditions found 
in the file "LICENSE" located in the project base directory.
'''

import config
from window import frames

# This module is responsible for collecting user commands from the gui
# and calling the apropriate actions

# this is the text given when "help" is called
_helpText = "For any @command you can call .help for more information.\
	\r  Commands:\
	\r  @config\
	\r     Access configuration options\
	\r  help\
	\r     Display help text\
	\r  quit\
	\r     Close the program"


# the config help text shown in the gui
_configHelpText = "Use this command to access configuration options \
	\r  Commands:\
	\r  @config.read.key\
	\r     Get the value of [key] from the current configuration\
	\r  @config.set.key=value\
	\r     Set the current configuration option [key] to [value]"

# wrapper function so the output method is only referenced once
def _displayText(text, begin="\n>> ", end=""):
	frames.mainFrame.displayText(text, begin, end)

# wrapper function so the quit method is only referenced once
def _quit():
	frames.mainFrame.quit()

def process(command):
	# handle input here
	_displayText(command, begin="\n<< ")
	if(command == None):
		return

	if(command.startswith("@") == True):
		command = command.lstrip("@")
		command = command.strip(".")
		commandSplit = command.split(".")

		splitLength = len(commandSplit)
		if(commandSplit[0] == "config"):
			_processConfig(commandSplit[1:])

	elif(command == "help"):
		_displayText(_helpText)
	elif(command == "quit"):
			# do shutdown operations here
		print("Exit Program")
		_quit()
	else:
		_displayText("You Entered:" + command)

def _processConfig(commandSplit):
	if(commandSplit[0] == "set"):
		keyValue = ""
		if(len(commandSplit) == 2):
			keyValue = commandSplit[1].split("=")
			config.setKeyValue(keyValue[0], keyValue[1])
			_displayText("Set Config: {0}={1}".format(keyValue[0], keyValue[1]))
		else:
			_displayText("Invalid key/value pair. use: @config.set.key=value")
	elif(commandSplit[0] == "read"):
		value = config.getKeyValue(commandSplit[1])
		_displayText("Read Config: {0}={1}".format(commandSplit[1], value))
	elif(commandSplit[0] == "help"):
		_displayText(_configHelpText)
	else:
		_displayText("invalid @config command; call \"@config.help\" for more information")
