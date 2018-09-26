'''
This file is subject to the terms and conditions found 
in the file "LICENSE" located in the project base directory.
'''

import http.server
import socket
import socketserver
import urllib
import json
from cgi import parse_header, parse_multipart

import time

from handleRequest import parseRequest

HOST = "xxx.xxx.xxx.xxx"
PORT = 80

class server(http.server.BaseHTTPRequestHandler):
	# create http response header
	#	status - the http request status to be included in the header
	#	*attributes - must be tuple(s) containing [attributeName, attributeValue]
	#		the data in these tuple(s) must be standard name/value pairs for a http header
	def _set_headers(self, status, attributes):
		self.send_response(status)

		for pair in attributes:
			self.send_header(pair[0], pair[1])

		# end header adds the blank line to the http request
		# that marks the end of the header
		self.end_headers()

	# creates and sends a header + body http request
	#	status - the http request status to be included in the header
	#	data - the data to be the http request body
	#	*attributes - must be tuple(s) containing [attributeName, attributeValue]
	#		the data in these tuple(s) must be standard name/value pairs for a http header
	def respond(self, status, data, attributes):
		self._set_headers(status, attributes)
		self.wfile.write(data.encode("utf-8"))

	# override the base handler's request handlers
	def do_GET(self):

		print(self.headers)
		
		url = urllib.parse.unquote(self.path)
		handler = parseRequest.requestHandler()
		handler.do_GET(urllib.parse.urlparse(url))
		self.respond(handler.status, handler.data, handler.header)
	def do_HEAD(self):
		url = urllib.parse.unquote(self.path)
		handler = parseRequest.requestHandler()
		handler.do_HEAD(urllib.parse.urlparse(url))
		self.respond(handler.status, b'', handler.header)
	def do_POST(self):
		ctype, pdict = parse_header(self.headers['content-type'])
		if ctype == 'multipart/form-data':
			postvars = parse_multipart(self.rfile, pdict)
		elif ctype == 'application/json':
			length = int(self.headers['content-length'])
			postvars = json.loads(self.rfile.read(length))
		elif ctype == 'application/x-www-form-urlencoded':
			length = int(self.headers['content-length'])
			postvars = urllib.parse.parse_qs(
				self.rfile.read(length).decode("utf-8"), 
				keep_blank_values=1)
		else:
			postvars = {}

		url = urllib.parse.unquote(self.path)
		handler = parseRequest.requestHandler()
		handler.do_POST(urllib.parse.urlparse(url), postvars)
		self.respond(handler.status, handler.data, handler.header)
	def do_PUT(self):
		handler = parseRequest.requestHandler()
		handler.do_PUT()
		self.respond(handler.status, handler.data, handler.header)
	def do_DELETE(self):
		handler = parseRequest.requestHandler()
		handler.do_DELETE()
		self.respond(handler.status, handler.data, handler.header)
	def do_CONNECT(self):
		handler = parseRequest.requestHandler()
		handler.do_CONNECT()
		self.respond(handler.status, handler.data, handler.header)
	def do_OPTION(self):
		handler = parseRequest.requestHandler()
		handler.do_OPTION()
		self.respond(handler.status, handler.data, handler.header)
	def do_TRACE(self):
		handler = parseRequest.requestHandler()
		handler.do_TRACE()
		self.respond(handler.status, handler.data, handler.header)
	def do_PATCH(self):
		handler = parseRequest.requestHandler()
		handler.do_PATCH()
		self.respond(handler.status, handler.data, handler.header)

Handler = server
with socketserver.TCPServer((HOST, PORT), Handler) as httpd:
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		httpd.shutdown()
		httpd.server_close()

