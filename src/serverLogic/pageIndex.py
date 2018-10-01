'''
This file is subject to the terms and conditions found 
in the file "LICENSE" located in the project base directory.
'''
from serverLogic import landingpage
from serverLogic import subpage

# registered pages
pages = {
	"landingpage": landingpage.Landingpage("", "/"),
	"subpage": subpage.Subpage("subpage", "/subpage")
}

def process(urlSplit, query, data):
	# this should call the process function of the website's landing page
	return pageIndex.pages["landingpage"].process(urlSplit, query, data)