'''
This file is subject to the terms and conditions found 
in the file "LICENSE" located in the project base directory.
'''

from http import HTTPStatus

from directoryIndex import directory
from directoryIndex import accessFile
from response import Response

from serverLogic import webpage
from serverLogic import pageIndex

# webpage are responsible for loading their index.html 
# and performing any actions associated with the page

# this file is a template class made to be inherited by webpages that will be in use
# performAction() is to be overloaded with all the actions the page is to perform

# to call this classes functions during processing use the funciton process()

class Subpage(webpage.Webpage):
	def performAction(self, urlSplit, params, data):
		# check if calling subpage
		if(urlSplit[0] == "subpage2"):
			response = pageIndex.pages["subpage2"].process(urlSplit, params, data)
			status = response.status
			header = response.header
			body = response.body
		else:
			return None

		return Response(status, header, body)
