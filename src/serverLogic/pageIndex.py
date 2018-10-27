'''
This file is subject to the terms and conditions found 
in the file "LICENSE" located in the project base directory.
'''

from directoryIndex import directory
from serverLogic import webpage
from pages import *

# dictionary containing registered pages
# USE: create a registered page by adding an oject that inherits the wepbage class
#      Label the inserted class with a unique identifier. This identifier will be used to 
#      reference the class when loading it as a subpage
#      NOTE: sub pages must have a trailing slash on its path
pages = {}

# register pages here
pages["/"] = landingpage.Landingpage("/")
pages["/subpage"] = subpage.Subpage("/subpage")
pages["/subpage/subpage2"] = subpage2.Subpage2("/subpage/subpage2")

# checks the request url against the page registry then performs the apropriate action
# url (str) - the request base url
# params (dict) - data related to the request to be sent to weblogic
# data (bytes) - data sent along with the request
def process(url, params, data):
	response = None

	# requesting index
	if url in pages:
		response = pages[url].loadIndex()

	# requesting action
	if(response == None):
		# get the action argument to be used in the page
		action = url[url.rfind("/") + 1:]

		# get the url path to the page the argument will go to
		pathLength = len(url) - len(action)
		path = url[:pathLength]

		# check if the created path exists in pages
		if path in pages:
			response = pages[path].process(action, params, data)

	return response

# runs once on startup
# searches for existing index.html files in the www folder then registers any that are not already registered
def findIndexes():
	indexPaths = directory.searchDirectory(directory.www, "index.html")

	# go through each found path with an index.html
	for path in indexPaths:
		# convert full path to url request path
		urlFromPath = path[len(directory.www):]

		# flip the slashes from the directory if using windows
		if(os.name != "posix"):
			urlFromPath = urlFromPath.replace("\\", "/")

		# add all pages that weren't manually registered to the dictionary
		if urlFromPath not in pages:
			pages[urlFromPath] = webpage.Webpage(urlFromPath)
