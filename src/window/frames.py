'''
This file is subject to the terms and conditions found 
in the file "LICENSE" located in the project base directory.
'''
try:
	import tkinter as tk
	from tkinter import font
except:
	print("WARNING: module \"tkinter\" not found. Trying to load older version \"Tkinter\"")
	try:
		import Tkinter as tk
		from Tkinter import font
		print("WARNING: using old version Tkinter; the application may not function properly")
	except:
		print("ERROR: No version of module tkinter is available")
		quit()

import threading

from window import command

# This class must me initailized using a tk.Tk() object
# The window this creates has 3 main frames
#   Status Frame: This should contain status about the process the 
#                 window is an interface for.
#   Display Frame: This should contain active feedback from the process 
#                  the window is an interface for.
#   Command Frame: This collects input where it can be received by the 
#                  process the window is an interface for.
#
# Functions intended to be called externally:
#    startGUI()
#    setStatus(str)
#    displayText(str)
#    getCommand()
#    clearDisplay()
#    quit()

mainFrame = None

class Frames(tk.Frame):
	# the maximum number of character that  can be displayed
	# this is to prevent the buffer from taking all RAM when the program
	#   is left runnign for long periods of time
	DISPLAY_BUFFER_SIZE = 1024
	statusLock = threading.Event()
	displayLock = threading.Event()
	commandLock = threading.Event()

	# parent (tk.Tk()) - the tk object to contain the frames
	# title (str) - the text that will be displayed in the title bar
	def __init__(self, parent, title="Window"):
		# initialize the main window
		# the name option allows for this class and its functions to be called
		#   from outside the class
		tk.Frame.__init__(self, parent, background="gray", name="main")
		self.winfo_toplevel().title(title)

		# configure the rows and columns for the main window
		self.grid(sticky="nswe")
		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=0)
		self.rowconfigure(1, weight=1)
		self.rowconfigure(2, weight=0)

		#
		# create and configure the status bar then add it to the main window
		self.status = tk.Frame(self, background="red", borderwidth=4)
		self.status.rowconfigure(0, weight=0)
		self.status.columnconfigure(0, weight=1)
		self.status.text = tk.Label(self.status, text="Status Bar", anchor="nw", justify="left")
		self.status.text.grid(row=0, column=0, sticky="we")

		#
		# create and configure the display window then add it to the main window
		self.display = tk.Frame(self, width=500, height=300, background="blue", borderwidth=4)
		self.display.rowconfigure(0, weight=1)
		self.display.columnconfigure(0, weight=1)
		self.display.columnconfigure(1, weight=0)
		self.display.grid(row=1, column=0, sticky="nswe")
		self.display.grid_propagate(0)

		# start the process of adding a scrollbar and scrolling region
		# create a canvas as child of the frame that will parent the scrolling region
		# the canvas controls what part of the area you see
		self.display.canvas = tk.Canvas(self.display)
		# create a frame that will be scrolled and set the canvas its parent
		# the frame contains everything that can be shown
		self.display.innerFrame = tk.Frame(self.display.canvas)
		# create a scrollbar that will control the scrolling region
		# NOTE: any frame can be the scrollbars parent but its reccommended to add 
		#       it to the same frame the srolling region will be in
		# OPTIONS: orient (str) - determine which direction the scrollbar will control
		#          command () - set as the xview/yview of the canvas that is the scrollable area
		self.display.scrollbar = tk.Scrollbar(self.display, orient="vertical", command=self.display.canvas.yview)
		# associate the canvas of the scrolling area with the scrollbar
		self.display.canvas.configure(yscrollcommand=self.display.scrollbar.set)
		# start with the view at the top of the scrolling area
		self.display.canvas.xview_moveto(0)

		# add the canvas and scrollbar to the display window
		self.display.canvas.grid(row=0, column=0, sticky="nswe")
		self.display.scrollbar.grid(row=0, column=1, sticky="ns")
		# create and get a refernce to a window inside the scrolling area canvas
		# this actually creates the scrolling region in the canvas
		# OPTION: window (tk.FRAME()) - the frame that will be displayed
		innerFrameId = self.display.canvas.create_window(0, 0, window=self.display.innerFrame, anchor="nw")
		# create some content to be shows in the scrolling frame
		self.display.text = tk.Label(self.display.innerFrame, font="Helvetica 8 bold", text="", justify="left")
		self.display.text.grid(row=0, column=0, sticky="nswe")

		#
		# create and configure the command bar then add it to the main window
		self.command = tk.Frame(self, background="green", borderwidth=4)
		self.command.rowconfigure(0, weight=0)
		self.command.columnconfigure(1, weight=1)
		self.command.text = tk.Label(self.command, text="Enter a Command:", anchor="nw", justify="left")
		self.command.entry = tk.Entry(self.command, justify="left")
		self.command.text.grid(row=0, column=0)
		self.command.entry.grid(row=0, column=1, sticky="we")

		# set focus to the command entry on startup
		self.command.entry.focus()

		# add the subframes to the main window
		self.status.grid(row=0, column=0, sticky="we")
		self.display.grid(row=1, column=0, sticky="nswe")
		self.command.grid(row=2, column=0, sticky = "we")

		# # # # # # # # # # # # #
		#    INLINE FUNCTIONS   #
		# # # # # # # # # # # # #

		# set the scrollable area size to the size of its content frame
		def _updateScrollArea(self):
			# get the size of the content
			width = self.display.innerFrame.winfo_reqwidth()
			height = self.display.innerFrame.winfo_reqheight()

			# set the scroll area to the match the size of the content
			self.display.canvas.config(scrollregion="0 0 {} {}".format(width, height))
			#self.display.canvas.xview_moveto(0)

			# make sure the view area is at the bottom of the resized scroll area
			if(height > self.display.canvas.winfo_reqheight()):
				self.display.canvas.yview_moveto(1)

		# update scroll area on start
		_updateScrollArea(self)

		# # # # # # # # # # # #
		#    EVENT BINDINGS   #
		# # # # # # # # # # # #

		# add the text in the command entry to the display window
		# test function for developement
		# in a project commands should be received by getCmmand() and 
		# text should be added to the display frame with displayText()
		def _inputCommand(event):
			message = self.getCommand()
			command.process(message)

		self.command.entry.bind_all("<Return>", _inputCommand)

		# update the configuration of the scroll area's content 
		# this runs on startup and whenever text is added to display.text
		def _configure_displayText(event):
			# get the size of the display canvas
			width = self.display.canvas.winfo_width()
			# set the wraplength of the display label
			self.display.text.config(wraplength=width)

		self.display.text.bind("<Configure>", _configure_displayText)

		# update the configuration of the display canvas when its content changes size
		# this runs on startup and whenever text is added to display.text
		def _configure_interior(event):
			# get the size of the content
			width = self.display.innerFrame.winfo_reqwidth()
			height = self.display.innerFrame.winfo_reqheight()

			# if the size of the content has canged update the scroll area
			if(self.display.innerFrame.winfo_reqwidth() != self.display.canvas.winfo_width()):
				_updateScrollArea(self)

			# update the display contents to match the size change
			_configure_displayText(event)

		self.display.innerFrame.bind("<Configure>", _configure_interior)

		# update the configuration of the display canvas when it changes size
		# this runs on startup and when the main window is resized
		def _configure_canvas(event):
			# update the display window size in the canvas
			if(self.display.innerFrame.winfo_reqwidth() != self.display.canvas.winfo_width()):
				self.display.canvas.itemconfigure(innerFrameId, width=self.display.canvas.winfo_width())

		self.display.canvas.bind("<Configure>", _configure_canvas)

	# # # # # # # # # # # #
	#   CLASS FUNCTIONS   #
	# # # # # # # # # # # #

	# set the text displayed in the status bar
	def setStatus(self, info):
		if(self.statusLock.is_set() == True):
			self.statusLock.wait()

		self.statusLock.set()
		self.status.text["text"] = info
		self.statusLock.clear()

	# get the text currently entered in the text entry then clear the netry
	# RETURNS: (str) command
	def getCommand(self):
		if(self.commandLock.is_set() == True):
			self.commandLock.wait()

		self.commandLock.set()
		cmd = self.command.entry.get()
		self.command.entry.delete(0, tk.END)
		self.commandLock.clear()

		return cmd

	# add text to the end the text currently stored in the display frame
	# addText (str) - the text that will be added
	# begin (str) - a string that gets placed at the beginning of addText
	# end (str) - a string that gets placed at the end of addText
	def displayText(self, addText, begin='\n> ', end=''):
		if(self.displayLock.is_set() == True):
			self.displayLock.wait()

		# get the old text and add the new text
		self.displayLock.set()
		currentText = self.display.text["text"]
		currentText = currentText + begin + addText + end

		# trim text if its too long
		size = len(currentText)
		if(size > self.DISPLAY_BUFFER_SIZE):
			# find the place where the text must be trimmed to fit within the buffer
			startSearchPos = size - self.DISPLAY_BUFFER_SIZE
			# start searching for the next newline to determine where the text will be trimmed
			trimIndex = currentText.find('\n', startSearchPos, size)

			# check that a newline was found
			if(trimIndex != -1):
				# include the found '\n'
				trimIndex = trimIndex + 1
				# trim the text
				currentText = currentText[trimIndex:]
			else:
				print("frames.displayText() >> Single Entry Too Long")
				currentText = ""

		# apply the new text to the display text
		self.display.text["text"] = currentText
		self.displayLock.clear()

	# clears all text from the display window
	def clearDisplay(self):
		if(self.displayLock.is_set() == True):
			self.displayLock.wait()

		self.displayLock.set()
		self.display.text["text"] = ""
		self.displayLock.clear()

	def quit(self):
		quit()

def startGUI(title, statusText="", displayText="Start up"):
	global mainFrame

	if(mainFrame != None):
		return

	root = tk.Tk()

	root.rowconfigure(0, weight=1, minsize=0)
	root.columnconfigure(0, weight=1, minsize=0)

	Frames(root, title).grid(row=0, column=0)

	# get a reference to the main Frames() object
	# change the name="" in Frame().__init__() to use a different name
	mainFrame = root.nametowidget("main")
	mainFrame.displayText(displayText, begin="")
	mainFrame.setStatus(statusText)

	root.mainloop()

if __name__ == "__main__":
	startGUI("Example Window", "Status: Testing", "Text From __main__()")
