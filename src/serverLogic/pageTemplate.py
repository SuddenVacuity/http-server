'''
This file is subject to the terms and conditions found 
in the file "LICENSE" located in the project base directory.
'''

from http import HTTPStatus

from directoryIndex import directory
from directoryIndex import accessFile
from response import Response

from serverLogic import webpage

# webpage are responsible for loading their index.html 
# and performing any actions associated with the page

# this file is a template file to be copied
# performAction() is to be overloaded with all the actions the page is to perform

# This class will attempt to load an index.html if the url part matches its name.
# If not the above it will then attempt to perform actions through the perfromAction function.
# If not the above it will then attempt to load a 404.html
# If not the above it will return a plain text 500 internal server error
# HOW TO USE:
# create this class with: myPage = MyPage(name, path)
# name (str) - the name of the folder containing this page's index.html
# path (str) - the parent path of name
#              NOTE: path + name must lead to the page's index.html
# to call this classes functions during processing call 
# the inherited function: myPage.process(urlSplit, query, data)
class PageTemplate(webpage.Webpage):
	# Create copy of this file and place webpage in this function
	# urlSplit ([(str), ...]) - A list created from a request url path that has had str.split('/') called on it
	#          Example: GET request: "/subpage/read?myData"
	#          Becomes: urlSplit = ["", "subpage", "read"]
	# A      As the urlSplit is passed along to subpages the part that were associated with the previous pages are removed.
 	#          Example: ["", "subpage", "read"]
 	# B          First serverLogic sends this to the page named "" which should always be always the landing page
 	# I          ServerLogic then removes the first element "" from urlSplit
 	# T            The landing page receives urlSplit as ["subpage", "read"]
 	#              Then the landing page check if "subpage" is one of its actions
 	# L            It should find that "subpage" should be sent to a page called "subpage"
 	# O            If "subpage" is a vaild page urlSplit will be passed to subpage
 	# N            The landing page then removes the first element "subpage" from urlSplit
 	# G          The subpage receives urlSplit as ["read"]
 	#              Then the subpage check if "read" is one of its actions
 	#              "read" would be a GET request for data so there should be a query value to determine what to read
	# query (str) - The query arguments extracted from a url
	# data (bytes) - data from the body of an http request
	def performAction(self, urlSplit, query, data):
		return None
