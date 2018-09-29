'''
This file is subject to the terms and conditions found 
in the file "LICENSE" located in the project base directory.
'''

# webpage are responsible for loading their index.html 
# and performing any actions associated with the page

# this file is a template class made to be inherited by webpages that will be in use
# performAction() is to be overloaded with all the actions the page is to perform

class Webpage():
	def _loadIndex():

	def _notFound():

	def performAction():

	def process():
		response = _loadIndex()
		if(response == None):
			response = performAction()
		if(response == None):
			response = _notFound()

	return response
