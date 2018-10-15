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
	def performAction(self, urlSplit, query, data):
		response = None

		# check if calling subpage
		if(urlSplit[0] == "subpage"):
			response = pageIndex.pages["subpage"].process(urlSplit, query, data)
			status = response.status
			header = response.header
			body = response.body

		# this page's functions
		# this is a GET request
		elif(urlSplit[0] == "get"):
			filepath = directory.databaseJson + "/" + query + ".txt"
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
		elif(urlSplit[0] == "post"):
			baseDir = None
			if(query == "image"):
				baseDir = directory.databaseImages
				filepath = baseDir + "/" + "test" + ".jpeg"
				writeData = data["value"][0]
			elif(query == "text"):
				baseDir = directory.databaseText
				filepath = baseDir + "/" + "test" + ".txt"
				writeData = data["value"][0]
			elif(query == "audio"):
				baseDir = directory.databaseAudio
				filepath = baseDir + "/" + "test" + ".mp3"
				writeData = data["value"][0]
			elif(query == "video"):
				baseDir = directory.databaseVideo
				filepath = baseDir + "/" + "test" + ".mp4"
				writeData = data["value"][0]
			elif(query == "json"):
				baseDir = directory.databaseJson
				filepath = baseDir + "/" + data['id'] + ".txt"
				writeData = data["value"].encode()
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
		elif(urlSplit[0] == "license"):
			filepath = directory.www + "/LICENSE.html"
			status = HTTPStatus.OK
			header = [("content-type", "text/html")]
			body = accessFile.readFile(filepath, directory.base)
		else:
			return None

		return Response(status, header, body)
