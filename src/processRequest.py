'''
This file is subject to the terms and conditions found 
in the file "LICENSE" located in the project base directory.
'''

import http.cookies

import checkStatus

from directoryIndex import accessFile
from serverLogic import processUrl
from response import Response
from request import Request

# helper function that creates an http response for a 405 method not allowed page
# RETURNS: (response) 405 method not allowed page
def _method_not_allowed():
	print("Method Not Allowed")
	data = accessFile.readFile("/405", self.query, None)
	response = Response(
		405, 
		[("content-type", "text/html")],
		data)
	return response

# this is out of date
# leaving as a reference for when cookies are added
def buildCookie():
	c = [("Set-Cookie", "myData=1234#myData2=5555; Path=/; Max-Age=30")]
	#self.response.header = [self.response.header, c]

def do_GET(requestUrl):
	request = Request(requestUrl)
	response = processUrl.readUrl(request.path, request.query, None)
	return checkStatus.getResponse(response.status, response.header, response.body)

def do_HEAD(requestUrl):
	request = Request(requestUrl)
	response = processUrl.readUrl(request.path, request.query, None)
	return checkStatus.getResponse(response.status, response.header, response.body)

# path - url path
# data - dictionary containing key/value pairs of data sent
def do_POST(requestUrl, data):
	request = Request(requestUrl)
	response = processUrl.readUrl(request.path, request.query, data)
	return checkStatus.getResponse(response.status, response.header, response.body)

def do_PUT():
	return _method_not_allowed()

def do_DELETE():
	return _method_not_allowed()

def do_CONNECT():
	return _method_not_allowed()

def do_OPTION():
	return _method_not_allowed()

def do_TRACE():
	return _method_not_allowed()

def do_PATCH():
	return _method_not_allowed()


''' Sample Http Header
	[
0	'GET /192.168.1.xxx:80 HTTP/1.1\r', 
1	'Host: xx.xxx.xxx.xxx\r', 
2	'Connection: keep-alive\r', 
3	'Cache-Control: max-age=0\r', 
4	'Upgrade-Insecure-Requests: 1\r', 
5	'User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36\r', 
6	'DNT: 1\r', 
7	'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8\r', 
8	'Accept-Encoding: gzip, deflate\r', 
9	'Accept-Language: en-US,en;q=0.9\r', 
10	'Cookie: test\r', 
11	'\r', 
12	'']
'''