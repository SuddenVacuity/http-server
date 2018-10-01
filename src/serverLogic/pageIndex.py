'''
This file is subject to the terms and conditions found 
in the file "LICENSE" located in the project base directory.
'''
from serverLogic import landingpage
from serverLogic import subpage

# dictionary containing registered pages
# USE: create a registered page uby adding an oject that inherits the wepbage class
#      Label the inserted class with a unique identifier. This identifier will be used to 
#      reference the class when loading it as a subpage
pages = {
	"landingpage": landingpage.Landingpage("", "/"),
	"subpage": subpage.Subpage("subpage", "/")
}

def process(urlSplit, query, data):
	# this should call the process function of the website's landing page
	return pages["landingpage"].process(urlSplit, query, data)