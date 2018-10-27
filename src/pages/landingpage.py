'''
This file is subject to the terms and conditions found 
in the file "LICENSE" located in the project base directory.
'''

from http import HTTPStatus
import mimetypes

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

class Landingpage(webpage.Webpage):
	def performAction(self, action, params, data):
		response = None

		# this page's functions
		# this is a GET request
		if(action == "get"):
			filepath = directory.databaseJson + "/" + params["query"]["name"] + ".txt"
			status = HTTPStatus.OK
			mimeType = mimetypes.guess_type(filepath)
			header = [("content-type", mimeType[0]), ("content-encoding", mimeType[1])]
			body = accessFile.readFile(filepath, directory.database)
			# if read data is empty
			if(body == b''):
				status = HTTPStatus.NOT_FOUND
				header = [("content-type", "text/plain")]
				body = b'Entry Does Not Exist'
		# this is a POST request
		# there needs to be server side data type validations
		elif(action == "post"):
			baseDir = None
			# the name the data is stored as
			# NOTE: this is set in the client that sends the request
			key = "value"
			# the client-defined type of the data that was sent
			dataType = params['query']['type']
			if(dataType == "image"):
				baseDir = directory.databaseImages
				filepath = baseDir + "/" + "test" + ".jpeg"
				writeData = data[key][0]
			elif(dataType == "text"):
				baseDir = directory.databaseText
				filepath = baseDir + "/" + "test" + ".txt"
				writeData = data[key][0]
			elif(dataType == "audio"):
				baseDir = directory.databaseAudio
				filepath = baseDir + "/" + "test" + ".mp3"
				writeData = data[key][0]
			elif(dataType == "video"):
				baseDir = directory.databaseVideo
				filepath = baseDir + "/" + "test" + ".mp4"
				writeData = data[key][0]
			elif(dataType == "json"):
				baseDir = directory.databaseJson
				filepath = baseDir + "/" + data['id'] + ".txt"
				writeData = data[key].encode()
			else:
				status = HTTPStatus.BAD_REQUEST
				header = [("content-type", "text/plain")]
				body = b'400 - Bad Request'

				return Response(status, header, body)

			# attempt to create the file
			if(accessFile.writeFile(filepath, writeData, baseDir) == True):
				status = HTTPStatus.CREATED
				header = [("content-type", "text/plain")]
				body = b'Successfully Created Entry'
			# unable to write to file
			else:
				status = HTTPStatus.CONFLICT
				header = [("content-type", "text/plain")]
				body = b'Unable to process request'
		# call for the license
		elif(action == "license"):
			filepath = directory.www + "/LICENSE.html"
			status = HTTPStatus.OK
			header = [("content-type", "text/html")]
			body = accessFile.readFile(filepath, directory.base)
		else:
			return None

		return Response(status, header, body)
