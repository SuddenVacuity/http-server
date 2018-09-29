'''
This file is subject to the terms and conditions found 
in the file "LICENSE" located in the project base directory.
'''

from http import HTTPStatus

from directoryIndex import directory
from directoryIndex import accessFile
from response import Response

from serverLogic import landingpage
from serverLogic import subpage

# This file is responsible for every action the landing page can perform as well as
# loading direct file requests and directing the request down the tree of subpages

# register pages
# this will be moved to file used to load webpages
pages = {
	"landingpage": landingpage.Landingpage("", "/"),
	"subpage": subpage.Subpage("subpage", "/subpage")
}

# there's definitely a standard lib for this
# get that .. don't expand this function
def _getMimeType(fileExtension):
	result = "text/plain"

	if(fileExtension == "css"):
		result = "content-type", "text/css"
	elif(fileExtension == "js"):
		result = "content-type", "text/javascript"
	elif(fileExtension == "gif"):
		result = "content-type", "image/gif"

	return result

# url (str) - the base url from the request
#             NOTE: url has a leading "/"
#             NOTE: any url ending with '/' calls index.html
#             NOTE: any url with a file extension at the end opens a file
#             NOTE: any other valid url calls an internal server process
# query (str) - url query
#               NOTE: for file operations query does NOT have a leading or trailing "/"
# data (dict) - httprequest body data
#               will be NoneType on GET/HEAD requests
#               NOTE: for file operations data does NOT have a leading or trailing "/"
# returns http [header, body]
def readUrl(url, query, data):
	# default response contents
	status = HTTPStatus.BAD_REQUEST
	header = [["content-type", "text/plain"]]
	body = b'400 - Bad Request'

	urlSplit = url.split("/") # [''. 'path', 'subpath', 'file']

	urlLength = len(urlSplit)
	urlLast = urlLength - 1

	# http request
	if(urlLength > 1):
		# check if attempting to load a file directly
		fileSplit = urlSplit[urlLast].split('.') # [name, extension]

		# if has file extension
		if(len(fileSplit) > 1):
			# check if requesting favicon
			if(fileSplit[0] == "favicon"):
				print("Loading favicon:", fileSplit)
				status = HTTPStatus.OK
				header = [["content-type", "image/gif"]]
				body = accessFile.readFile(directory.www + "/favicon.gif", directory.www)
				if(body == b''):
					status = HTTPStatus.NOT_FOUND
			# get the file by adding the url to the www directory
			else:
				mimeType = _getMimeType(fileSplit[1])
				filepath = directory.www + url
				status = HTTPStatus.OK
				header = [[mimeType[0], mimeType[1]]]
				body = accessFile.readFile(filepath, directory.www)
				if(body == b''):
					status = HTTPStatus.NOT_FOUND
					header = [["content-type", "text/html"]]
					body = accessFile.readFile(directory.www + "/404.html", directory.www)

######### START load webpages (this will be moved to its own file)
		# attempt to perform an action associated with this page
		# NOTE: start at 1 because "/" splites to ['', ''] and removing the leading element when there
		#       are only 2 elements changes the object type to (str)
		elif(urlSplit[1] == "subpage"):
			response = pages["subpage"].process(urlSplit[1:], query, data)
			status = response.status
			header = response.header
			body = response.body
		else:
			response = pages["landingpage"].process(urlSplit[1:], query, data)
			status = response.status
			header = response.header
			body = response.body

######### END load webpages (this will be moved to its own file)

	# internal requests
	else:
		# server requested command
		if(url == "405"):
			status = HTTPStatus.METHOD_NOT_ALLOWED
			header = [["content-type", "text/html"]]
			body = accessFile.readFile(directory.www + "/405.html", directory.www)
		if(url == "415"):
			status = HTTPStatus.UNSUPPORTED_MEDIA_TYPE
			header = [["content-type", "text/html"]]
			body = b'MEDIA TYPE NOT SUPPORTED'
		# if this point is reached the response is the default
		# response created at the top of this function

	return Response(status, header, body)
