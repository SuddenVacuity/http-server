'''
This file is subject to the terms and conditions found 
in the file "LICENSE" located in the project base directory.
'''

# This metohod of managing filepaths is temporary

from dir import directory

class Image:
	# the full pathname to an image
	favicon = directory.imageShared + "favicon.gif"

class Html:
	class Error:
		methodNotAllowed = directory.wwwBase + "405.html"
		notFound = directory.wwwBase + "404.html"

	index = directory.wwwBase + "index.html"
	license = directory.wwwBase + "LICENSE.html"

class Style:
	css = directory.wwwBase + "style.css"

class Script:
	js = directory.wwwBase + "script.js"
