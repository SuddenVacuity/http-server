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
		print("WARNING: using old version Tkinter; the application may not function properly")
	except:
		print("ERROR: No version of module tkinter is available")
		quit()

class Frames(tk.Frame):
	DISPLAY_BUFFER_SIZE = 1024

	def __init__(self, parent, title):
		tk.Frame.__init__(self, parent, background="gray", name="main")
		self.winfo_toplevel().title(title)

		self.grid(sticky="nswe")
		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=0)
		self.rowconfigure(1, weight=1)
		self.rowconfigure(2, weight=0)

		# status bar
		self.status = tk.Frame(self, background="red", borderwidth=4)
		self.status.rowconfigure(0, weight=0)
		self.status.columnconfigure(0, weight=1)
		self.status.text = tk.Label(self.status, text="Status Bar", anchor="nw", justify="left")

		# grid
		self.status.text.grid(row=0, column=0, sticky="we")

		# display window
		self.display = tk.Frame(self, width=500, height=300, background="blue", borderwidth=4)
		self.display.rowconfigure(0, weight=1)
		self.display.columnconfigure(0, weight=1)
		self.display.columnconfigure(1, weight=0)
		self.display.grid(row=1, column=0, sticky="nswe")
		self.display.grid_propagate(0)

		self.display.canvas = tk.Canvas(self.display)
		self.display.innerFrame = tk.Frame(self.display.canvas)
		self.display.scrollbar = tk.Scrollbar(self.display, orient="vertical", command=self.display.canvas.yview)
		self.display.canvas.configure(yscrollcommand=self.display.scrollbar.set)

		self.display.canvas.grid(row=0, column=0, sticky="nswe")
		self.display.scrollbar.grid(row=0, column=1, sticky="ns")
		innerFrameId = self.display.canvas.create_window(0, 0, window=self.display.innerFrame, anchor="nw")
		self.display.text = tk.Label(self.display.innerFrame, font="Helvetica 18 bold", text="Display Window", justify="left")
		self.display.text.grid(row=0, column=0, sticky="nswe")

		# command line
		self.command = tk.Frame(self, background="green", borderwidth=4)
		self.command.rowconfigure(0, weight=0)
		self.command.columnconfigure(1, weight=1)
		self.command.text = tk.Label(self.command, text="Enter some text:", anchor="nw", justify="left")
		self.command.entry = tk.Entry(self.command, justify="left")
		self.command.text.grid(row=0, column=0)
		self.command.entry.grid(row=0, column=1, sticky="we")

		self.command.entry.focus()

		# grid
		self.status.grid(row=0, column=0, sticky="we")
		self.display.grid(row=1, column=0, sticky="nswe")
		self.command.grid(row=2, column=0, sticky = "we")

		# # # # # # # # # # # # #
		#    INLINE FUNCTIONS   #
		# # # # # # # # # # # # #

		def _updateScrollArea(self):
			width = self.display.innerFrame.winfo_reqwidth()
			height = self.display.innerFrame.winfo_reqheight()

			self.display.canvas.config(scrollregion="0 0 {} {}".format(width, height))
			self.display.canvas.xview_moveto(0)
			if(height > self.display.canvas.winfo_reqheight()):
				self.display.canvas.yview_moveto(1)

		_updateScrollArea(self)

		# # # # # # # # # # # #
		#    EVENT BINDINGS   #
		# # # # # # # # # # # #

		# test function for developement
		# in a project commands should be received by getCmmand() and 
		# text should be added to the display frame with displayText()
		def _inputCommand(event):
			txt = self.getCommand()
			self.displayText(txt)

		self.command.entry.bind_all("<Return>", _inputCommand)

		# this runs on startup and whenever text is added to display.text
		def _configure_displayText(event):
			width = self.display.canvas.winfo_width()
			self.display.text.config(wraplength=width)

		self.display.text.bind("<Configure>", _configure_displayText)

		# this runs on startup and whenever text is added to display.text
		def _configure_interior(event):
			width = self.display.innerFrame.winfo_reqwidth()
			height = self.display.innerFrame.winfo_reqheight()
			self.display.canvas.config(scrollregion="0 0 {} {}".format(width, height))

			if(self.display.innerFrame.winfo_reqwidth() != self.display.canvas.winfo_width()):
				self.display.canvas.config(width=self.display.innerFrame.winfo_reqwidth())
				_updateScrollArea(self)

			_configure_displayText(event)

		self.display.innerFrame.bind("<Configure>", _configure_interior)

		# this runs on startup and when the main window is resized
		def _configure_canvas(event):
			if(self.display.innerFrame.winfo_reqwidth() != self.display.canvas.winfo_width()):
				self.display.canvas.itemconfigure(innerFrameId, width=self.display.canvas.winfo_width())

		self.display.canvas.bind("<Configure>", _configure_canvas)

	# # # # # # # # # # # #
	#   CLASS FUNCTIONS   #
	# # # # # # # # # # # #

	def setStatus(self, info):
		self.status.configure(text=info)

	def getCommand(self):
		cmd = self.command.entry.get()

		# clear the command entry box
		self.command.entry.delete(0, tk.END)
		return cmd

	def displayText(self, addText, begin='\n >', end=''):
		print("You Entered:", addText)
		# remove newline from pressing enter in a command prompt
		currentText = self.display.text["text"]
		currentText = currentText + begin + addText + end

		# trim text if its too long
		size = len(currentText)
		if(size > self.DISPLAY_BUFFER_SIZE):
			# find next new line and trim it and all before it
			startSearchPos = size - self.DISPLAY_BUFFER_SIZE
			trimIndex = currentText.find('\n', startSearchPos, size)
			if(trimIndex != -1):
				# include the found '\n'
				trimIndex = trimIndex + 1
				currentText = currentText[(trimIndex):]
			else:
				print("frames.displayText() >> Single Entry Too Long")
				currentText = ""

		self.display.text["text"] = currentText

	def clearDisplay(self):
		self.display.text["text"] = ""

if __name__ == "__main__":
	root = tk.Tk()

	root.rowconfigure(0, weight=1, minsize=0)
	root.columnconfigure(0, weight=1, minsize=0)

	Frames(root, "Example Window").grid(row=0, column=0)

	# get a reference to the main Frames() object
	# change the name="" in Frame().__init__() to use a different name
	frame = root.nametowidget("main")
	frame.displayText("Text From __main__()", begin="\n###  ", end="  ###")

	root.mainloop()
