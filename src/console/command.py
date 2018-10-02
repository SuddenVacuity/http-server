'''
This file is subject to the terms and conditions found 
in the file "LICENSE" located in the project base directory.
'''

import _thread # used to quit main thread

def process(command):
		# handle input here
		print("You entered:", command)
		if(command == "quit"):
			print("quitting")
			# this was the only simple way I could find to quit that allowed the main thread perform its shutdown process
			# the interrupt is treated as a KeyboardInterrupt exception
			_thread.interrupt_main()
