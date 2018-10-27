'''
This file is subject to the terms and conditions found 
in the file "LICENSE" located in the project base directory.
'''

from http import HTTPStatus

from directoryIndex import directory
from directoryIndex import accessFile
from response import Response

from serverLogic import pageIndex

# webpage are responsible for loading their index.html 
# and performing any actions associated with the page

# this file is a template class made to be inherited by webpages that will be in use
# performAction() is to be overloaded with all the actions the page is to perform

# to call this classes functions during processing use the funciton process()

class Webpage():
	pagePath = None

	# set the name and path of the page
	# name (str) - the name that will be added to the url to request this page
	# path (str) - path to the folder containing the page's index.html
	def __init__(self, path):
		# ending with a slash here simplifies adding files to the path later
		if(path.endswith("/") == False):
			path = path + "/"
		self.pagePath = path

	def _internalError(self):
		print("ERROR: 500 - Internal Server Error: {} no action taken and neither index.html nor 404.html found".format(self.pagePath))
		return Response(HTTPStatus.INTERNAL_SERVER_ERROR, [("content-type", "text/plain")], b'500 - Internal Server Error')

	# do not override
	# this function should only be called internally
	def _notFound(self):
		try:
			status = HTTPStatus.NOT_FOUND
			header = [("content-type", "text/html")]
			body = accessFile.readFile(directory.www + "/404.html", directory.www)
		except:
			return self._internalError()

		return Response(status, header, body)

	# do not override
	# this function should only be called internally
	def loadIndex(self):
		try:
			filepath = directory.www + self.pagePath + "index.html"
			status = HTTPStatus.OK
			header = [("content-type", "text/html")]
			body = accessFile.readFile(filepath, directory.www)
		except:
			return None

		return Response(status, header, body)

	# do not override
	# this function is called externally when the url is being processed
	def process(self, url, params, data):
		requestArgument = url.rstrip(self.pagePath)
		response = self.performAction(requestArgument, params, data)

		if(response == None):
			response = self._notFound()
		if(response == None):
			response = self._internalError()

		return response

	# override this function and insert the desired actions
	# this function should only be called by called by process()
	# RETURNS: (Response) http response data
	#                     returns None when no action taken
	def performAction(self, action, params, data):
		return None
