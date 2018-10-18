'''
This file is subject to the terms and conditions found 
in the file "LICENSE" located in the project base directory.
'''

import os

__all__ = []

path = os.path.abspath(__file__).rstrip(os.path.basename(__file__))
dirs = os.listdir(path)

for ob in dirs:
	sp = ob.split(".")
	print(sp)
	if len(sp) != 2: 
		continue

	if sp[1] == "py":
		if sp[1] == "__init__":
			continue
			
		print("added:", sp[0])
		__all__.append(sp[0])

print(__all__)
