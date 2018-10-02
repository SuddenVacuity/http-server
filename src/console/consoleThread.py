'''
This file is subject to the terms and conditions found 
in the file "LICENSE" located in the project base directory.
'''

import threading

from console import command

userInput = ""
inputLock = threading.Event()

class TakeInputThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		global userInput
		message = input("Enter a command: >> ")
		inputLock.set()
		userInput = message

class ProcessInputThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		inputLock.wait()
		message = userInput
		inputLock.clear()

		command.process(message)

def start():
	takeInput = TakeInputThread()
	processInput = ProcessInputThread()

	takeInput.start()
	processInput.start()