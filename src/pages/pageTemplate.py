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
	# action (str) - The action request to the page. Use this to determine what custom action the page should perform.
	# params ({{"key":"value"}, ...}) - The query arguments extracted from a requests header and requested url
	#           NOTE: This is a dictionary containing three sub dictionaries
	#                 ["query"] (dict) - request query parameters extracted from the url
	#                 ["cookies"] (dict) - cookies extracted from the headers
	#                                      To create a cookie add "Set-Cookie" along with a cookie name followed 
	#                                      by key/value pairs to a responses header.
	#                                         ex. "Set-Cookie": "myCookie=key=value"
	#                                      Multi-value cookies are also supported with each value seperated by &
	#                                         ex. "Set-Cookie": "myCookie=key1=value1&key2=value2"
	#                                      To access a cookies' key's value read query["cookies"]["myCookie"]["key"]
	#                                      NOTE: cookie structure is "cookiename": {"key": "value", ...}
	#                 ["headers"] (dict) - non-cookie http header attributes from the headers
	# data (bytes) - data from the body of an http request
	def performAction(self, action, params, data):
		return None
