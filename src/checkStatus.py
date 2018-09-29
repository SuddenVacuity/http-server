'''
This file is subject to the terms and conditions found 
in the file "LICENSE" located in the project base directory.
'''

# a list of all statuses can be found here: 
#     https://docs.python.org/3/library/http.html
from http import HTTPStatus

# error html files are stored in the websites base directory
from directoryIndex import directory
from directoryIndex import accessFile
from response import Response

# The final line before data gets sent to the output buffer
# Any global changes to the header/body due to the http return status happen here
# creates a status/body/header to send
# statusCode (int) - 
# header [[(str)name, (str)value], ...] -
# body (bytes) data- 
# RETURNS: [
#              [[(str)name, (str)value], ...] header, 
#              (bytes) body
#          ]
def getResponse(statusCode, header, body):

	# 100 - If the client has a large amount of data to send it may be split into seperate header-only 
	# 100 -   andcomplete http requests.
	# 100 - The requester adds "Expects: 100-continue" to an http request header with a header and no body.
	# 100 - Then the receiver either sends status error (403/405) or continue (100).
	# 100 - If the requesters gets the response status error (403/404) it does not send the the full request.
	# 100 - If the requesters gets the response status continue (100) it follows up with the full request.
#	elif(statusCode == HTTPStatus.CONTINUE):
#		pass
#	# 102 - This status means the request will take some time and the requester should not time out
#	elif(statusCode == HTTPStatus.PROCESSING):
#		pass
	# 200 - the request was successfully processed and the response contains information or the result 
	# 200 -   of the process
	if(statusCode == HTTPStatus.OK):
		pass
	# 201 - A new resource was successfully created
	elif(statusCode == HTTPStatus.CREATED):
		pass
#	# 202 - The request is being processed and it may take some time to finish.
#	# 202 - Processing may or may not result in action being taken and may result in an error status
#	elif(statusCode == HTTPStatus.ACCEPTED):
#		pass
#	# 203 - The receiver is acting as a gateway to another server and has received an OK 200 status
#	# 203 -   from a server farther into the system and is sending a modified version of the internal
#	# 203 -   server's response
#	elif(statusCode == HTTPStatus.NON_AUTHORITATIVE_INFORMATION):
#		pass
#	# 204 - The request was successfully processed and the response body should be empty
	elif(statusCode == HTTPStatus.NO_CONTENT):
		body = b''
#	# 205 - The request was successfully processed, the response is empty and the requester must reload
#	# 205 -   page to see the result
#	elif(statusCode == HTTPStatus.RESET_CONTENT):
#		pass
#	# 206 - Indicates the response is part of a multi request data transfer where progess through the
#	# 206 -   transfer is stored until the transfer is complete or the requester times out.
#	# 206 - Add the the response header "Range: [range within the transfer]" to specify the start and stop
#	# 206 -   points within the file to read
#	elif(statusCode == HTTPStatus.PARTIAL_CONTENT):
#		pass
#	# 304 - This status is the response to a request for a resource that has not been modified since the
#	# 304 -   requester last requested it
#	elif(statusCode == HTTPStatus.NOT_MODIFIED):
#		pass
	# 400 - the request is not valid
	elif(statusCode == HTTPStatus.BAD_REQUEST):
		pass
#	# 401 - the request requires authentication that was not provided
#	elif(statusCode == HTTPStatus.UNAUTHORIZED):
#		pass
#	# 403 - the request is refused before processing
#	elif(statusCode == HTTPStatus.FORBIDDEN):
#		pass
	# 404 - The request was valid but called for a resource that does not exist
	elif(statusCode == HTTPStatus.NOT_FOUND):
		pass
	# 405 - The requests method (GET, POST, ...) is not supproted for the requested resource
	elif(statusCode == HTTPStatus.METHOD_NOT_ALLOWED):
		pass
#	# 408 - Too much time before a requester sent a request and the receiver has unloaded related information
#	elif(statusCode == HTTPStatus.REQUEST_TIMEOUT):
#		pass
	# 409 - The requested process could not be performed on the requested resouce due to the current state 
	# 409 -   of the resource preventing the requested actions of being performed
	elif(statusCode == HTTPStatus.CONFLICT):
		pass
#	# 411 - The requester did not specifiy a content length when the receiver required it
#	elif(statusCode == HTTPStatus.LENGTH_REQUIRED):
#		pass
#	# 413 - The request is larger than ther receiver allows
#	elif(statusCode == HTTPStatus.REQUEST_ENTITY_TOO_LARGE):
#		pass
#	# 414 - The request URI is longer than 255 characters
#	elif(statusCode == HTTPStatus.REQUEST_URI_TOO_LONG):
#		pass
	# 415 - The media contained in a request is a type the server does not support
	elif(statusCode == HTTPStatus.UNSUPPORTED_MEDIA_TYPE):
		pass
#	# 416 - The requster requested a data range outside the range of the file requested
#	elif(statusCode == HTTPStatus.REQUEST_RANGE_NOT_SATISFIABLE):
#		pass
#	# 422 - The request properly formed but could not be processed due to incorrect semantics
#	elif(statusCode == HTTPStatus.UNPROCESSABLE_ENTITY):
#		pass
#	# 429 - The requester has reached their request limit
#	elif(statusCode == HTTPStatus.TOO_MANY_REQUESTS):
#		pass
	# 500 - Vague server error
	elif(statusCode == HTTPStatus.INTERNAL_SERVER_ERROR):
		pass
#	# 501 - Method that has not been added yet.
#	# 501 - The server either does not recognize the method or is unable to fulfil the request
#	elif(statusCode == HTTPStatus.NOT_IMPLEMENTED):
#		pass
#	# 502 - The receiver is acting as a gateway to another server and received a negative response from
#	# 502 -   a server farther into the system
#	elif(statusCode == HTTPStatus.BAD_GATEWAY):
#		pass
#	# 503 - The requested service is currently not available
#	# 503 - This is usually temporary and usually due to heavy load
#	elif(statusCode == HTTPStatus.SERVICE_UNAVAILABLE):
#		pass
#	# 504 - The receiver is acting as a gateway to another server and has timed out from a server farther
#	# 504 - into the system
#	elif(statusCode == HTTPStatus.GATEWAY_TIMEOUT):
#		pass
	else:
		header = [['Content-Type', 'text/plain']]
		body = b'REQUEST STATUS NOT IMPLEMENTED'

	return Response(statusCode, header, body)
