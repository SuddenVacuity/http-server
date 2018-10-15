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
	#	*attributes - must be tuple(s) containing (attributeName, attributeValue)
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
		if ctype == 'multipart/form-data':
			pdict["boundary"] = bytes(pdict['boundary'], "utf-8")
			postvars = parse_multipart(self.rfile, pdict)
		elif ctype == 'application/json':
			postvars = json.loads(self.rfile.read(clength))
		# media type not supported
		else:
			# this is handled in preocessRequest.py
			self.path = "415"

		return postvars

	# creates and sends a header + body http request
	#	status - the http request status to be included in the header
	#	data - the data to be the http request body
	#	*attributes - must be tuple(s) containing (attributeName, attributeValue)
	#		the data in these tuple(s) must be standard name/value pairs for a http header
	def respond(self, status, data, attributes):
		self._set_headers(status, attributes)
		# there's been an uncommon BrokenPipeError occuring here
		# I've added a data dump to try and find out the cause
		try:
			self.wfile.write(data)
		except BrokenPipeError as e:
			print("==========================================")
			print("Data Dump: server.py >> respond()")
			print("Status:", status)
			print("Headers:", attributes)
			print("Body:", data)
			print(e)

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
		# support for threading requests
		# https://stackoverflow.com/a/46224191
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.bind((host, port))
		self.sock.listen(5)

	def run(self):
		Handler = server
		with socketserver.TCPServer((self.host, self.port), Handler, False) as httpd:
			try:
				# Prevent the HTTP server from re-binding every handler.
        		# https://stackoverflow.com/questions/46210672/
				httpd.socket = self.sock
				httpd.server_bind = self.server_close = lambda self: None

				httpd.serve_forever()
			except KeyboardInterrupt:
				httpd.shutdown()
				httpd.server_close()
				quit()
