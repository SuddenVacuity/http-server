'''
This file is subject to the terms and conditions found 
in the file "LICENSE" located in the project base directory.
'''

import os

__all__ = []

path = os.path.abspath(__file__).rstrip(os.path.basename(__file__))
dirs = os.listdir(path)

for ob in dirs:
	if ob.startswith("_") == True:
		continue

	if ob.endswith(".py") == False:
		continue

	sp = ob.split(".")
	if len(sp) != 2: 
		continue

	__all__.append(sp[0])
