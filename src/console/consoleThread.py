'''
This file is subject to the terms and conditions found 
in the file "LICENSE" located in the project base directory.
'''

import threading
import _thread # used to quit main thread

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

		# handle input here
		print("You entered:", message)
		if(userInput == "quit"):
			print("quitting")
			# this was the only simple way I could find to quit that allowed the main thread perform its shutdown process
			# the interrupt is treated as a KeyboardInterrupt exception
			_thread.interrupt_main()

def start():
	takeInput = TakeInputThread()
	processInput = ProcessInputThread()

	takeInput.start()
	processInput.start()