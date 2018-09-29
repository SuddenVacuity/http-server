'''
This file is subject to the terms and conditions found 
in the file "LICENSE" located in the project base directory.
'''

from http import HTTPStatus

from directoryIndex import directory
from directoryIndex import accessFile
from response import Response

# webpage are responsible for loading their index.html 
# and performing any actions associated with the page

# this file is a template class made to be inherited by webpages that will be in use
# performAction() is to be overloaded with all the actions the page is to perform

# to call this classes functions during processing use the funciton process()

class Webpage():
	indexPath = '/'
	pageName = None
	def __init__(self, name, path):
		self.indexPath = path
		self.pageName = name

	# do not override
	# this function should only be called internally
	def _loadIndex(self, urlSplit):
		# www.yourdomain.com/page/
		if(urlSplit[0] == ''):
			print("loading Index.html")
			filepath = directory.www + self.indexPath + "index.html"
			status = HTTPStatus.OK
			header = [["content-type", "text/html"]]
			body = accessFile.readFile(filepath, directory.www)

			return Response(status, header, body)

		# www.yourdomain.com/page
		if(urlSplit[0] == self.pageName):
			print("loading Index.html")
			filepath = directory.www + self.indexPath + "/index.html"
			status = HTTPStatus.OK
			header = [["content-type", "text/html"]]
			body = accessFile.readFile(filepath, directory.www)

			return Response(status, header, body)

		return None

	# do not override
	# this function should only be called internally
	def _notFound(self):
		status = HTTPStatus.NOT_FOUND
		header = [["content-type", "text/html"]]
		body = accessFile.readFile(directory.www + "/404.html", directory.www)

		return Response(status, header, body)

	# do not override
	# this function is called externally when the url is being processed
	def process(self, urlSplit, query, data):
		response = self._loadIndex(urlSplit)

		if(response == None):
			response = self.performAction(urlSplit, query, data)
		if(response == None):
			response = self._notFound()

		return response

	# override this function and insert the desired actions
	# this function should only be called by called by process()
	# RETURNS: (Response) http response data
	#                     should return None on failure
	def performAction(self, urlSplit, query, data):
		print("Create copy of this file and override this function to perform actions here")
		return None
