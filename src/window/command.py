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

# The first layer of processing an entered command. This determines the 
#   target of a command. Once the target has been determined the command 
#   arguments relevant to the target are passed to the relevant function
# command (str) - the command string to be processed
def process(command):
	# handle input here
	_displayText(command, begin="\n<< ")
	if(command == None):
		return

	# check if the command is targeted
	if(command.startswith("@") == True):
		# remove the target token
		command = command.lstrip("@")
		# remove and leading/trailing argument tokens
		command = command.strip(".")
		# split the arguments into a list
		commandSplit = command.split(".")
		# get the number of elements in the list
		splitLength = len(commandSplit)

		# if config is targeted
		if(commandSplit[0] == "config"):
			_processConfig(commandSplit[1:])

	# non-targeted commands
	elif(command == "help"):
		_displayText(_helpText)
	elif(command == "quit"):
		# do shutdown operations here
		_quit()
	else:
		_displayText("Invalid command; call \"help\" for more information")

# The layer of processing that handles commands that target config
# commandSplit ([(str), ...]) - a list of strings that are the result of command.split()
#                               NOTE: list elements that were processed by the previous layer are removed
def _processConfig(commandSplit):
	# start checking if command is valid
	if(len(commandSplit) == 2):
		if(commandSplit[0] == "set"):
			keyValue = commandSplit[1].split("=")
			if(len(keyValue) == 2):
				config.setKeyValue(keyValue[0], keyValue[1])
				_displayText("Set Config: {0}={1}".format(keyValue[0], keyValue[1]))
			else:
				_displayText("Invalid key/value pair. use: @config.set.key=value")
		if(commandSplit[0] == "read"):
			value = config.getKeyValue(commandSplit[1])
			_displayText("Read Config: {0}={1}".format(commandSplit[1], value))
	elif(commandSplit[0] == "help"):
		_displayText(_configHelpText)
	else:
		_displayText("Invalid @config command; call \"@config.help\" for more information")
