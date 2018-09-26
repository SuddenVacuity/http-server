'''
This file is subject to the terms and conditions found 
in the file "LICENSE" located in the project base directory.
'''

import hashlib # used for basic hashes
import secrets # used to generate a salt
import base64 # used in secureHash() to shorten long password length
import hmac # used to compare blake2b hashes

try:
	from cryptography.fernet import Fernet # used for non-password data encyption
except:
	print("ImportError: encrypt.py >> This module requires cryptography to be installed")
	quit()

try:
	import bcrypt # used for password hashes
except ImportError:
	print("ImportError: encrypt.py >> This module requires python3-bcrypt to be installed")
	quit()

# set to false to skip tests
# SET FALSE FOR DEVELOPEMENT ONLY
# ALWAYS LEAVE TRUE IN PRODUCTION
__DEBUG_SHOULD_RUN_TESTS = False

# the size of the output of weakHash() and saltedHash()
BLAKE2B_DIGEST_SIZE = 64
# the size of the salt values to be used in saltedHash()
BLAKE2B_SALT_LENGTH = hashlib.blake2b.SALT_SIZE

# the maximum length password bcrypt can take as input
BCRYPT_MAX_PASSWORD_LENGTH = 72
# this controls how long the hash takes to complete
# 	Higher = More Secure
# aim for 0.20~0.50 seconds per hash
BCRPYT_COST = 12

# length of didgital signiture used for message authentication
AUTH_SIZE = 16

#	generates a salt for hashing
#	intended for use with saltedHash()
#	size (int) - the length in bytes of the returned token
#	RETURNS: (bytes)data
def generateSalt(size=BLAKE2B_SALT_LENGTH):
	return secrets.token_bytes(size)

#	generates a key for encryption/decryption
#	intended for use with encyption() and decryption()
#	RETURNS: (bytes)data
def generateKey():
	return Fernet.generate_key()

#	creats a non-reversable hash
#	data (str) - data to be hashed
#	RETURNS: (str)hexdigest
def weakHash(data):
	if(data == None):
		return None

	h1 = hashlib.blake2b(digest_size=BLAKE2B_DIGEST_SIZE)
	h1.update(data.encode())

	return h1.hexdigest()

#	creates a non-reversable salted hash
#	data (str) - data to be hashed
#	sodium (bytes) - salt to be used in the hash
#	NOTE: sodium must be BLAKE2B_SALT_LENGTH bytes in length
#	NOTE: ITS RECOMMENED TO ALWAYS CREATE A SALT USING generateSalt()
#	RETURNS: (str)hexdigest
def saltedHash(data, sodium):
	if(data == None):
		return None
	if(sodium == None):
		return None
	if(len(sodium) != BLAKE2B_SALT_LENGTH):
		return None

	h1 = hashlib.blake2b(salt=sodium, digest_size=BLAKE2B_DIGEST_SIZE)
	h1.update(data.encode())

	return h1.hexdigest()

#	creates a slow and non-reversable hash
#	data (str) - data to be hashed
#	RETURNS: [(bytes)data, (bytes)salt]
def secureHash(data, sodium=None):
	if(data == None):
		return None
	if(sodium == None):
		sodium =  bcrypt.gensalt(BCRPYT_COST)

	if(len(data) <= BCRYPT_MAX_PASSWORD_LENGTH):
		pw = data.encode()
	else: # shorten the password so bcrypt can work with it
		pw = base64.b64encode(hashlib.sha256(data.encode()).digest())

	return [bcrypt.hashpw(pw,sodium), sodium]

#	newHash (str) - hexdigest of data hashed using weakHash()
#	storedHash (str) - stored hexdigest of data hashed by weakHash()
#	RETURNS: (bool)isMatch
def compareWeakHash(newHash, storedHash):
	if(newHash == None):
		return False

	return hmac.compare_digest(newHash, storedHash)

#	newHash (str) - hexdigest of data hashed using saltedHash()
#	storedHash (str) - stored hexdigest of data hashed by saltedHash()
#	salt - the salt used to create the hash
#	RETURNS: (bool)isMatch
def compareSaltedHash(newHash, salt, storedHash):
	if(newHash == None):
		return False

	return hmac.compare_digest(newHash, storedHash)

#	newHash (str) - hexdigest of data hashed using secureHash()
#	storedHash (bytes) - stored bytes digest containing data hashed by sercureHash()
#	RETURNS: (bool)isMatch
def compareSecureHash(plainText, storedHash):
	if(plainText == None):
		return False

	return bcrypt.checkpw(plainText.encode(), storedHash)

#	encrypts data
#	data (bytes) - data to encode
#	RETURNS: [(bytes)data, (bytes)key]
def encrypt(data, key=None):
	if(data == None):
		return [None, None]

	if(key == None):
		key = generateKey()

	f = Fernet(key)
	token = f.encrypt(data)

	return [token, key]

#	return the original value of data encrypted by encrypt()
#	data (bytes) - data to decrypt
#	key (bytes) - encryption key
#	RETURNS: (bytes)data
def decrypt(data, key):
	if(data == None):
		return None
	if(key == None):
		return None

	f = Fernet(key)
	return f.decrypt(data)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # #                                         # # # # #
# # # # #                                         # # # # #
# # # # #               TEST AREA                 # # # # #
# # # # #                                         # # # # #
# # # # #                                         # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#
#	These tests check that hashing and encryption are
#	functioning properly.
#
#	__DEBUG_runOnceOnStart() is called once on import
#	and runs all tests automatically.
#
#	check variable __DEBUG_SHOULD_RUN_TESTS at the top
#	of this file to toggle tests
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

from timeit import default_timer
from string import ascii_uppercase # used to test case sensitivity
from string import ascii_lowercase # used to test case sensitivity


#	the minimum and target times in seconds it must take for secureHash() 
#	to hash a password. Longer time means more secure.
__DEBUG_MIN_TIME_REQ_SECURE_HASH = 0.15
__DEBUG_TARGET_TIME_REQ_SECURE_HASH = 0.30

#	does some basic inpt testing to check for runtime exceptions
#	ON FAILURE: the application will crash plain and simple
def __DEBUG_findExceptions():
	# run each function at least once to confirm needed modules are available
	# and try to cause exceptions with input types
	nacl = generateSalt()
	key = Fernet.generate_key()

	# Test a single hash using each hashing function
	data = "Hash test GO!"
	weakHash(data)
	saltedHash(data, nacl)
	secureHash(data)
	e1 = encrypt(data.encode())
	decrypt(e1[0], e1[1])


	# Test hashing using long input
	longData = "asdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdf"
	weakHash(longData)
	saltedHash(longData, nacl)
	secureHash(longData)
	e2 = encrypt(longData.encode())
	decrypt(e2[0], e2[1])

	# Test a single hash using empty string input
	weakHash("")
	saltedHash("", "")
	secureHash("")
	e3 = encrypt("".encode())
	decrypt(e3[0], e3[1])

	# Test a single hash using None input
	weakHash(None)
	saltedHash(None, None)
	secureHash(None)
	e4 = encrypt(None)
	decrypt(e4[0], e4[1])

# 	checks hashing the same input returns the same result as previously made hashes
#	checks that hashing algorithms handle None/empty input
#	ON FAILURE: the hashing algorithm will not be able to compare new inputs 
#               to old inputs saved as hashes and hashes saved in a database
#               will not match new hashes.
#	RETURNS: True if all tests are passed
def __DEBUG_checkHashConsistant():
	testsPassed = True

	# saved hashes are made with the text "debugTest"
	plainText = "debugTest"
	# weak hash
	storedWeakHash = "886e8ad2a7915ecbd49fc5aeba39e85db52180d6575c3221b1d0c7031d63c128419217b46cba6b6a25129df78239115277da22b45b4a5ffdd423521231bac1a0"
	# salted hash
	storedSaltedHash = "4863c06b5a9f2490e8ebdad2f5b2ecef62f78db97e6b79bacbe576d1777a365a6a65dc04fd9f361947a6044e1a8a76ef6041152be61018227c123d4ceb419f36"
	# secure hash
	storedSecureHash = b'$2b$12$RUdvZl.LO4aQ.LIccP4V6uJuKNeG2eVWSiSg8UJKN4GJSZNhwRf5W'

	# stored salt
	wHashSalt = b'i\x91\xb1y\xeb0aK\x17v\x15Q.9\xff\xe3'
	sHashSalt = b'$2b$12$RUdvZl.LO4aQ.LIccP4V6u'

	# test with proper input
	# should be true
	hWeak = weakHash(plainText)
	hSalted = saltedHash(plainText, wHashSalt)
	hSecure = secureHash(plainText, sHashSalt)

	if(compareWeakHash(hWeak, storedWeakHash) == False):
		print("FAILURE: encrypt.py >> _DEBUG_checkHashConsistant() >> compareWeakHash() is not functioning properly")
		testsPassed = False
	if(compareSaltedHash(hSalted, wHashSalt, storedSaltedHash) == False):
		print("FAILURE: encrypt.py >> _DEBUG_checkHashConsistant() >> compareSaltedHash() is not functioning properly")
		testsPassed = False
	if(compareSecureHash(plainText, storedSecureHash) == False):
		print("FAILURE: encrypt.py >> _DEBUG_checkHashConsistant() >> compareSecureHash() is not functioning properly")
		testsPassed = False

	# test with none type input
	# should be false
	if(compareWeakHash(None, storedWeakHash) == True):
		print("FAILURE: encrypt.py >> _DEBUG_checkHashConsistant() >> compareWeakHash(None) is not functioning properly")
		testsPassed = False
	if(compareSaltedHash(None, wHashSalt, storedSaltedHash) == True):
		print("FAILURE: encrypt.py >> _DEBUG_checkHashConsistant() >> compareSaltedHash(None) is not functioning properly")
		testsPassed = False
	if(compareSecureHash(None, storedSecureHash) == True):
		print("FAILURE: encrypt.py >> _DEBUG_checkHashConsistant() >> compareSecureHash(None) is not functioning properly")
		testsPassed = False

	# test with empty type input
	# should be false
	if(compareWeakHash("", storedWeakHash) == True):
		print("FAILURE: encrypt.py >> _DEBUG_checkHashConsistant() >> compareWeakHash("") is not functioning properly")
		testsPassed = False
	if(compareSaltedHash("", wHashSalt, storedSaltedHash) == True):
		print("FAILURE: encrypt.py >> _DEBUG_checkHashConsistant() >> compareSaltedHash("") is not functioning properly")
		testsPassed = False
	if(compareSecureHash("", storedSecureHash) == True):
		print("FAILURE: encrypt.py >> _DEBUG_checkHashConsistant() >> compareSecureHash("") is not functioning properly")
		testsPassed = False

	return testsPassed

#	confirms encryption and decryption give the expected results
#	ON FAILURE: Encrypted data from messages and the database can not be read
#	RETURNS: True if all tests are passed
def __DEBUG_checkEncryptionConsistant():
	testsPassed = True

	data = b'Encryption test GO!'
	savedEncrypted = b'gAAAAABbpQ1nYZjqnOQ8rQ9OGd1i3oufGXqR5MaVs8Q4WMhew4WHlBSOe8PlWm5j_uxOzbhUTl9q_K6XIRyaXVtlh-4LwxNl-dn_n8sKU89C7Hz_xeHcurI='
	savedKey = b'smuBYAoyPj9EDT6f6R9CyZxpwUO9h5R-pV899oa7VhY='

	# decrypt old data and compare the result to the original data
	decryptSaved = decrypt(savedEncrypted, savedKey)
	if(decryptSaved != data):
		print("FAILURE: encrypt.py >> __DEBUG_checkEncryptionConsistant() >> Decryptions of previous data do not match encrytion+decryptions of new data")
		testsPassed = False

	# encrypted and decrypt new data
	encrypted = encrypt(data)
	decrypted = decrypt(encrypted[0], encrypted[1])
	if(data != decrypted):
		print("FAILURE: encrypt.py >> __DEBUG_checkEncryptionConsistant() >> Decrypted message does not match the original message that was encrypted")
		testsPassed = False

	return testsPassed

#	Ensure that giving an inputs, with the only difference being casing, will produce different output.
#	ON WARNING: hashes will accept both lowercase and uppercase as the same value.
#               This makes it easier to find a match password since it reduces the number
#               of effectively unique inputs
def __DEBUG_testCaseSensitivity():
	testsPassed = True

	# salt to be used in the test hashes
	wHashSalt = b'i\x91\xb1y\xeb0aK\x17v\x15Q.9\xff\xe3'

	print("STARTUP: encrypt.py >> >> lower to upper: ", end='',)
	# LOWERCASE to UPPERCASE
	# get from standard to account for regional settings
	LOWERCASE_ALPHABET = list(ascii_lowercase)
	for letter in LOWERCASE_ALPHABET:
		h1u = weakHash(letter.upper())
		h2u = saltedHash(letter.upper(), wHashSalt)
		h3u = secureHash(letter.upper())
		h1l = weakHash(letter)
		h2l = saltedHash(letter, wHashSalt)
		# h3l = secureHash(letter) # compareSecureHash() takes plain-text

		# The results should NOT match
		if(compareWeakHash(h1l, h1u) == True):
			testsPassed = False
		if(compareSaltedHash(h2l, wHashSalt, h2u) == True):
			testsPassed = False
		if(compareSecureHash(letter, h3u[0]) == True): # compareSecureHash() takes plain-text
			testsPassed = False

		if(testsPassed == False):
			print("->", end='', flush=True)
		print(letter, end='', flush=True)

	print("") # manual new line
	print("STARTUP: encrypt.py >> >> upper to lower: ", end='',)
	# UPPERCASE to LOWERCASE
	# get from standard to account for regional settings
	UPPERCASE_ALPHABET = list(ascii_uppercase)
	for letter in UPPERCASE_ALPHABET:
		h1u = weakHash(letter)
		h2u = saltedHash(letter, wHashSalt)
		# h3u = secureHash(letter) # compareSecureHash() takes plain-text
		h1l = weakHash(letter.lower())
		h2l = saltedHash(letter.lower(), wHashSalt)
		h3l = secureHash(letter.lower())

		# The results should NOT match
		if(compareWeakHash(h1u, h1l) == True):
			testsPassed = False
		if(compareSaltedHash(h2u, wHashSalt, h2l) == True):
			testsPassed = False
		if(compareSecureHash(letter, h3l[0]) == True): # compareSecureHash() takes plain-text
			testsPassed = False

		if(testsPassed == False):
			print("->", end='', flush=True)
		print(letter, end='', flush=True)

	print("") # manual new line

	if(testsPassed == False):
		print("WARNING: encrypt.py >> __DEBUG_testCaseSensitivity() >> regional settings allow letter-case based hash collisions")

#	checks that using secureHash() takes long enough to slow down password crackers
#	ON FAILURE: If sensitve data is hashed too easily a password cracker can more easily
#               perform brute force attacks to discover a hash's original text
#               This could mean passwords, names or other sensitive information is 
#               vulnerable.
def __DEBUG_timeSecureHash():
	testsPassed = True
	iterations = 30
	i = 0
	start = default_timer()
	while i < iterations:
		secureHash("password*123")
		i = i + 1
	stop = default_timer()

	secureHashResult = stop - start
	secureHashAvgTime = secureHashResult / iterations

	print("STARTUP: encrypt.py >> __DEBUG_timeSecureHash() >> Total time is:", secureHashResult, "seconds for", iterations, "hashes")
	print("STARTUP: encrypt.py >> __DEBUG_timeSecureHash() >> Average time per hash is:", secureHashAvgTime, "seconds")
	print("STARTUP: encrypt.py >> __DEBUG_timeSecureHash() >> Target time per hash is:", __DEBUG_TARGET_TIME_REQ_SECURE_HASH, "seconds")
	print("STARTUP: encrypt.py >> __DEBUG_timeSecureHash() >> Minumum time per hash is:", __DEBUG_MIN_TIME_REQ_SECURE_HASH, "seconds")

	if(secureHashAvgTime < __DEBUG_MIN_TIME_REQ_SECURE_HASH):
		print("FAILURE: encrypt.py >> __DEBUG_timeSecureHash() >> Secure hash times are too low")
		print("FAILURE: encrypt.py >> __DEBUG_timeSecureHash() >> Increase the value of BCRPYT_COST until the minumum time is reached")
		testsPassed = False
	elif(secureHashAvgTime < __DEBUG_TARGET_TIME_REQ_SECURE_HASH):
		print("WARNING: encrypt.py >> __DEBUG_timeSecureHash() >> Secure hash times are low")
		print("WARNING: encrypt.py >> __DEBUG_timeSecureHash() >> Its reccommended to increase BCRPYT_COST until the target time is reached")

	return testsPassed

#	this tests all implementations of functions and
#	should be run every time the program is started
#	ON FAILURE: Sensitive data is not safe.
#               The program will automatically close on failure to prevent damages
#               DO NOT use try/except to stop any crash. 
#               DO NOT skip/ignore this test in any way
#               Allowing the hash to function improperly could(will) affect features in 
#               the program and/or affect a user/admin ability to access any data and/or 
#               allow sensitive data to be available to anyone and/or corrupt data stored 
#               in a database.
def __DEBUG_runOnceOnStart(shouldRun=__DEBUG_SHOULD_RUN_TESTS):
	if(shouldRun == False):
		print("STARTUP: encrypt.py >> WARNING: SKIPPING IMPORTANT ENVIRONMENT TESTING")
		print("STARTUP: encrypt.py >> WARNING: TESTS SHOULD ONLY BE SKIPPED IN DEVELOPEMENT")
		return

	print("STARTUP: encrypt.py >> Testing hashing algorithms")

	# # # # # # # # # # # 
	# exception on fail
	# do not suppress
	print("STARTUP: encrypt.py >> Checking installation")
	__DEBUG_findExceptions()
	print("STARTUP: encrypt.py >> Done")

	# remains true if all tests are passed
	testsPassed = True

	# # # # # # # # # # # 
	# quit if failed
	print("STARTUP: encrypt.py >> Confirming hashes are consistant")
	if(__DEBUG_checkHashConsistant() == False):
		testsPassed = False
	print("STARTUP: encrypt.py >> Done")

	print("STARTUP: encrypt.py >> Timing secure hashes")
	print("STARTUP: encrypt.py >> This can take a minute")
	print("STARTUP: encrypt.py >> working...")
	if(__DEBUG_timeSecureHash() == False):
		testsPassed = False
	print("STARTUP: encrypt.py >> Done")

	print("STARTUP: encrypt.py >> Confirming encryption and decryption are consistant")
	if(__DEBUG_checkEncryptionConsistant() == False):
		testsPassed = False
	print("STARTUP: encrypt.py >> Done")

	# # # # # # # # # # # 
	# warning on fail
	print("STARTUP: encrypt.py >> Checking case sensitivity")
	print("STARTUP: encrypt.py >> This can take a few minutes")
	print("STARTUP: encrypt.py >> working...")
	__DEBUG_testCaseSensitivity()
	print("STARTUP: encrypt.py >> Done")

	# # # # # # # # # # # 
	# tests complete
	if(testsPassed):
		print("STARTUP: encrypt.py >> SUCCESS")
	else:
		print("\nSTARTUP: encrypt.py >> FAILURE: Hashing/Encrypting functions are not working properly. The program can not run until they are or the database may be leaked/corrupted.")
		quit()

__DEBUG_runOnceOnStart(__DEBUG_SHOULD_RUN_TESTS)