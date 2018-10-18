'''
This file is subject to the terms and conditions found 
in the file "LICENSE" located in the project base directory.
'''

from pages import *

# dictionary containing registered pages
# USE: create a registered page uby adding an oject that inherits the wepbage class
#      Label the inserted class with a unique identifier. This identifier will be used to 
#      reference the class when loading it as a subpage
#      NOTE: sub pages must have a trailing slash on its path
pages = {
	"landingpage": landingpage.Landingpage("", "/"),
	"subpage": subpage.Subpage("subpage", "/subpage/"),
	"subpage2": subpage2.Subpage2("subpage2", "/subpage/subpage2/")
}

def process(urlSplit, query, data):
	# this should call the process function of the website's landing page
	return pages["landingpage"].process(urlSplit, query, data)