'''
This file is subject to the terms and conditions found 
in the file "LICENSE" located in the project base directory.
'''

# data that's passed back to httpServer
class Response():
	# int http status code
	status = 0
	# list of tuples containing http header labels and values to be added to the header
	#     eg. [["Content-Type", "text/html"], ["Content-Length", "1024"], ["Cookie-Set", "test"]]
	header = ""
	# bytes data to send
	body = b''

	def __init__(self, status, header, body=b''):
		self.status = status
		self.header = header
		self.body = body