'''
This file is subject to the terms and conditions found 
in the file "LICENSE" located in the project base directory.
'''

# data passed from httpServer
class Request():
	# str the base url requested
	path = None
	# str url query included in the request
	query = None

	# requestUrl [(str), ...] - tuple containing data parsed from a http request
	#    attribute name: [scheme, netloc, path, params, query, fragment, username, password, hostname, port]
	#    default values: ['',     '',     '',   '',     '',    '',       None,     None,     None,     None]
	def __init__(self, requestUrl):
		self.path = requestUrl[2]
		self.query = requestUrl[4]