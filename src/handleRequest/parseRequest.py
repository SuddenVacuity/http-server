'''
This file is subject to the terms and conditions found 
in the file "LICENSE" located in the project base directory.
'''

import http.cookies

from dir import directory
from dir import file

class requestHandler(object):
	status = 200
	url = None
	parameters = None
	readFile = None
	writeFile = None
	header = None
	data = None

	# Returns - [url, parameters]
	def _splitUrl(self, requestUrl):
		baseUrl = requestUrl.split("?")

		if(len(baseUrl) == 1):
			baseUrl.append('')

		return baseUrl

	def _readUrl(self, requestUrl):

		self.urlPath = requestUrl[2]
		self.parameters = requestUrl[4]

	def _ok(self):
		self.status = 200
		self.header = ["Content-Type", "text/plain"]
		self.data = ''

	def _method_not_allowed(self):
		self.status = 405
		self.readFile = file.Html.Error.methodNotAllowed
		self.header = ["Content-Type", "text/html"]
		with open(self.readFile, 'r') as f:
			self.data = f.read()


	def _file_not_found(self):
		self.status = 404
		self.readFile = file.Html.Error.notFound
		self.header = ["Content-Type", "text/html"]
		with open(self.readFile, 'r') as f:
			self.data = f.read()

	def _buildData(self):
		if(self.readFile == None):
			self.data =  ''
			return

		if(self.readFile == directory.dbBase):
			self.readFile = self.readFile + self.parameters

		self._readFile()
		'''
		insertStr = "stuff you got"
		substr = "<p id=\"entry\">---</p>"
		newstr = "<p id=\"entry\">" + insertStr + "</p>"
		pos = self.data.find(substr)
		self.data = self.data[:pos] + newstr + self.data[pos + len(substr):]
		'''

	def _getFilepath(self):
		if(self.urlPath == "/"):
			self.readFile = file.Html.index
		elif(self.urlPath == "/style.css"):
			self.readFile = file.Style.css
		elif(self.urlPath == "/script.js"):
			self.readFile = file.Script.js
		elif(self.urlPath == "/favicon.ico"):
			self.readFile = file.Image.favicon

		elif(self.urlPath == "/post"):
			self.readFile = directory.dbBase
			self.writeFile = directory.dbBase

		elif(self.urlPath == "/license"):
			self.readFile = file.Html.license

		else:
			self._file_not_found()

	def _buildCookie(self, data):
		c = ["Set-Cookie", "myData=1234#myData2=5555; Path=/; Max-Age=30"]
		self.header = [self.header, c]

	def _buildHeader(self):
		if(self.urlPath == "/"):
			self.header = ["Content-Type", "text/html"]
			self._buildCookie("")
		elif(self.urlPath == "/style.css"):
			self.header = ["Content-Type", "text/css"]
		elif(self.urlPath == "/script.js"):
			self.header = ["Content-Type", "text/javascript"].
		elif(self.urlPath == "/favicon.ico"):
			self.header = ["Content-Type", "image/gif"]

		elif(self.urlPath == "/post"):
			self.header = ["Content-Type", "text/plain"]

		elif(self.urlPath == "/license"):
			self.header = ["Content-Type", "text/html"]
			
		else:
			self._file_not_found()
		# COOKIE

	def _readFile(self):
		try:
			with open(self.readFile, 'r') as f:
				self.data = f.read()
		except:
			self._file_not_found()
	
	def _writeData(self, data):
		self.writeFile = self.writeFile + data["id"]
		with open(self.writeFile, 'w') as f:
			f.write(data["value"])

	def do_GET(self, requestUrl):
		self._readUrl(requestUrl)

		self._getFilepath()
		self._buildData()
		self._buildHeader()

	def do_HEAD(self, requestUrl):
		self._readUrl(requestUrl)
		self._buildHeader()

	# path - url path
	# data - dictionary containing key/value pairs of data sent
	def do_POST(self, requestUrl, data):
		self._readUrl(requestUrl)
		self._getFilepath()
		self._writeData(data)

		self._ok()

	def do_PUT(self):
		self._method_not_allowed()

	def do_DELETE(self):
		self._method_not_allowed()

	def do_CONNECT(self):
		self._method_not_allowed()

	def do_OPTION(self):
		self._method_not_allowed()

	def do_TRACE(self):
		self._method_not_allowed()

	def do_PATCH(self):
		self._method_not_allowed()


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