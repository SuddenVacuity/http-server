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

# this file is a template class made to be inherited by webpages that will be in use
# performAction() is to be overloaded with all the actions the page is to perform

# to call this classes functions during processing use the funciton process()

class Landingpage(webpage.Webpage):
	def performAction(self, urlSplit, query, data):
		print("Perform Actions Here")
		print("Landingpage >> urlsplit: {}, query: {},  data:{}".format(urlSplit, query, data))

		response = None

		# call for the license
		if(urlSplit[0] == "license"):
			filepath = directory.www + "/LICENSE.html"
			status = HTTPStatus.OK
			header = [["content-type", "text/html"]]
			body = accessFile.readFile(filepath, directory.base)
			# this is a GET request
		elif(urlSplit[0] == "get"):
			filepath = directory.database + "/" + query
			status = HTTPStatus.OK
			header = [["content-type", "text/plain"]]
			body = accessFile.readFile(filepath, directory.database)
			# if read data is empty
			if(body == b''):
				status = HTTPStatus.NOT_FOUND
				header = [["content-type", "text/plain"]]
				body = b'Entry Does Not Exist'
			# this is a POST request
		elif(urlSplit[0] == "post"):
			filepath = directory.database + "/" + data['id']
			# attempt to create the file
			if(accessFile.writeFile(filepath, data["value"], directory.database) == True):
				status = HTTPStatus.CREATED
				header = [["content-type", "text/plain"]]
				body = b'Successfully Created Entry'
			# unable to write to file
			else:
				status = HTTPStatus.CONFLICT
				header = [["content-type", "text/plain"]]
				body = b'Unable to process request'
		else:
			return None

		return Response(status, header, body)
