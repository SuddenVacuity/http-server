'''
This file is subject to the terms and conditions found 
in the file "LICENSE" located in the project base directory.
'''

import http.server
import socket
import socketserver
import urllib
import json
import threading
from cgi import parse_header, parse_multipart

import processRequest

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

	# parses the body of http request
	# RETURNS: (dict) containing the ojects from the requests body
	def _readBodyData(self):
		postvars = {}

		# no centent
		if(self.headers['content-length'] == None):
			return postvars

		clength = int(self.headers['content-length'])
		ctype, pdict = parse_header(self.headers['content-type'])

		# check for supported body data type
		if ctype == 'application/json':
			postvars = json.loads(self.rfile.read(clength))
		# media type not supported
		else:
			# this is handled in preocessRequest.py
			self.path = "415"

		return postvars

	# creates and sends a header + body http request
	#	status - the http request status to be included in the header
	#	data - the data to be the http request body
	#	*attributes - must be tuple(s) containing [attributeName, attributeValue]
	#		the data in these tuple(s) must be standard name/value pairs for a http header
	def respond(self, status, data, attributes):
		self._set_headers(status, attributes)
		self.wfile.write(data)

	# override the base handler's request handlers
	def do_GET(self):
		url = urllib.parse.unquote(self.path)
		parsedUrl = urllib.parse.urlparse(url)
		response = processRequest.do_GET(parsedUrl)
		self.respond(response.status, response.body, response.header)
	def do_HEAD(self):
		url = urllib.parse.unquote(self.path)
		parsedUrl = urllib.parse.urlparse(url)
		response = processRequest.do_HEAD(parsedUrl)
		self.respond(response.status, b'', response.header)
	def do_POST(self):
		postvars = self._readBodyData()
		url = urllib.parse.unquote(self.path)
		parsedUrl = urllib.parse.urlparse(url)
		response = processRequest.do_POST(parsedUrl, postvars)
		self.respond(response.status, response.body, response.header)
	def do_PUT(self):
		response = processRequest.do_PUT()
		self.respond(response.status, response.body, response.header)
	def do_DELETE(self):
		response = processRequest.do_DELETE()
		self.respond(response.status, response.body, response.header)
	def do_CONNECT(self):
		response = processRequest.do_CONNECT()
		self.respond(response.status, response.body, response.header)
	def do_OPTION(self):
		response = processRequest.do_OPTION()
		self.respond(response.status, response.body, response.header)
	def do_TRACE(self):
		response = processRequest.do_TRACE()
		self.respond(response.status, response.body, response.header)
	def do_PATCH(self):
		response = processRequest.do_PATCH()
		self.respond(response.status, response.body, response.header)


class ThreadedServer(threading.Thread):
	def __init__(self, host="127.0.0.1", port=80):
		threading.Thread.__init__(self)
		self.daemon = True
		self.port = port
		self.host = host

	def run(self):
		Handler = server
		with socketserver.TCPServer((self.host, self.port), Handler) as httpd:
			print("HOST: {0}\nPORT: {1}\nListening...".format(self.host, self.port))
			try:
				httpd.serve_forever()
			except KeyboardInterrupt:
				httpd.shutdown()
				httpd.server_close()
				quit()
