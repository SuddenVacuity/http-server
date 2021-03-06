'''
This file is subject to the terms and conditions found 
in the file "LICENSE" located in the project base directory.
'''

from http import HTTPStatus
import mimetypes

from directoryIndex import directory
from directoryIndex import accessFile
from response import Response

from serverLogic import pageIndex

# This file is responsible for every action the landing page can perform as well as
# loading direct file requests and directing the request down the tree of subpages

# wrapper function: guesses the file's mimetype based on its file extension
# fileExtension (str) - the part after the last . in a filename
# RETURNS: (mimetype, encoding) 
def _getMimeType(fileExtension):
	return mimetypes.guess_type(fileExtension)

# sorts url queries, cookies and non-cookie header attributes into a dictionary
# RETURNS: (dict)
def _extractToDictionary(headers, query):
	params = {}
	# example query is "myData1=123&myData2=456"
	params["query"] = {}
	# ["myData1=123", "myData2=456"]
	queryArgs = query.split("&")
	for arg in queryArgs:
		keypair = arg.split("=")
		if(len(keypair) == 2):
			# params["query"]["myData"] = 123
			params["query"][keypair[0]] = keypair[1]

	# split apart the headers
	headers = headers.split("\n")

	# get the cookies from the headers
	params["cookies"] = {}
	for entry in headers:
		# first find the cookies in the headers
		# example: "Cookie: login=username=admin&password=password123"
		if entry.startswith("Cookie"):
			# "login=username=admin&password=password123"
			entry = entry.lstrip("Cookie:")
			entry = entry.strip(" ")
			cookie = {}

			# ["login", "login=username=admin&password=password123"]
			cookieSplit = entry.split("=", maxsplit=1)

			# ["username=admin", "password=password123"]
			values = cookieSplit[1].split("&")

			for val in values:
				keypair = val.split("=")
				if len(keypair) == 2:
					# cookie["username"] = "admin"
					cookie[keypair[0]] = keypair[1]

			# add the cookie to the params dictionary
			# params["cookies"]["login"] = cookie
			params["cookies"][cookieSplit[0]] = cookie
			
			# blank the value so it doens't get searched again
			entry = ''

	print("COOKIES:", params["cookies"])

	params["headers"] = {}
	# "Host: 127.0.0.1"
	for entry in headers:
		# ["Host", " 127.0.0.1"]
		hdv = entry.split(":")

		if len(hdv) == 2:
			hdv[1] = hdv[1].strip(" ")
			# params["headers"]["Host"] = "127.0.0.1"
			params["headers"][hdv[0]] = hdv[1]

	return params

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
def readUrl(headers, url, query, data):
	# default response contents
	status = HTTPStatus.BAD_REQUEST
	header = [("content-type", "text/plain")]
	body = b'400 - Bad Request'

	# remove trailing / whlie leaving leading slash
	# NOTE: the leading slash is used to check for internal server errors
	#       that were passed along: no leading / means there was an error
	if(len(url) > 1):
		url = url.rstrip('/')

	urlSplit = url.split('/') # [''. 'path', 'subpath', 'file']

	urlLength = len(urlSplit)
	urlLast = urlLength - 1

	# add all query arguments to a dictionary
	params = _extractToDictionary(headers, query)

	# http request
	if(urlLength > 1):
		# check if attempting to load a file directly

		lastArg = urlSplit[urlLast]
		# if has file extension
		if "." in lastArg:
			# check if requesting favicon
			if(lastArg == "favicon.ico"):
				status = HTTPStatus.OK
				header = [("content-type", "image/gif")]
				body = accessFile.readFile(directory.www + "/favicon.gif", directory.www)
				if(body == b''):
					status = HTTPStatus.NOT_FOUND
			# get the file by adding the url to the www directory
			else:
				mimeType = _getMimeType(lastArg)
				filepath = directory.www + url
				status = HTTPStatus.OK
				header = [("content-type", mimeType[0]), ("content-encoding", mimeType[1])]
				body = accessFile.readFile(filepath, directory.www)
				if(body == b''):
					status = HTTPStatus.NOT_FOUND
					header = [("content-type", "text/html")]
					body = accessFile.readFile(directory.www + "/404.html", directory.www)

		# if not loading a file the loading a page
		# NOTE: remove first element because "/page" splits to ['', 'page']
		else:
			response = pageIndex.process(url, params, data)
			if(response != None):
				status = response.status
				header = response.header
				body = response.body

	# internal requests
	else:
		# server requested errors
		print("Internal Error:", url)
		if(url == "405"):
			status = HTTPStatus.METHOD_NOT_ALLOWED
			header = [("content-type", "text/html")]
			body = accessFile.readFile(directory.www + "/405.html", directory.www)
		elif(url == "415"):
			status = HTTPStatus.UNSUPPORTED_MEDIA_TYPE
			header = [("content-type", "text/html")]
			body = b'MEDIA TYPE NOT SUPPORTED'
		else:
			status = HTTPStatus.INTERNAL_SERVER_ERROR
			header = [("content-type", "text/plain")]
			body = b'500 - Internal Server Error'
		# if this point is reached the response is the default
		# response created at the top of this function

	return Response(status, header, body)
