#Im too lazy to do full comments now

from math import floor 
from math import ceil 
#Called in sumHandleFloat, pascalString, pascalCypher, fibonacciString, fibonacciCypher, wordLengthCypher

def isAlphaNum(char, cyphNums=True):
	"""
	Checks if character is letter or number, returns bool
	char: single character
	cyphNums: if true, numbers return true, otherwise false
	"""
	#Equivalent string method str.isalnum()
	if (char >= 'A' and char <= 'Z') or (char >= 'a' and char <='z') or (cyphNums and char >= '0' and char <= '9'):
		return True
	return False

def filterString(text, incNums=True):
	"""
	filters out spaces, punctuation, and optionally number from string
		as well as capitalizing.
	text: string
	incNums: bool, True includes number in result
	returns filtered string
	"""
	#Requires: isAlphaNum
	newString=''
	#iterate through string
	for char in text:
		if isAlphaNum(char, incNums):
			#appending next char,
			newString = newString + char.upper()
	return newString

def shift(char, factor):
	"""
	Takes a character and its shift factor. character will not be shifted outside
		of its given set: uppercase letters, lowerecase letters, or 0-9. it will cycle.
	char: single alphanumeric to be shifted, not meant for other symbols
	factor: signle char or int used to shift char. char examples: 'a' =1, 'A' = 1, '3'= 3
		int factors are not transformed.
	returns shifted character
	"""
	#Convert to Unicode
	char = ord(char)
	#Checking if factor is valid string
	if ( type(factor)==str and len(factor)==1 ):
		#to unicode
		factor = ord(factor)
		#unicode to correct value, 'a' = 1 instead of 97
		if(factor >= 48 and factor <= 57):
			factor = factor - 48
		elif(factor >= 65 and factor <=90):
			factor = factor - 64
		else:
			factor = factor -96
	#applying shift and cycling if needed
	if (char >= 48 and char <= 57):
		char = char + factor
		while char < 48:
			char = char + 10
		while char > 57:
			char = char - 10
		return chr(char)
	elif (char >= 65 and char <= 90):
		char = char + factor
		while char < 65:
			char = char + 26
		while char > 90:
			char = char - 26
		return chr(char)
	else:
		char = char + factor
		while char < 97:
			char = char + 26
		while char > 122:
			char = char - 26
		return chr(char)

def caesar(text, factor, cyphNums=True, standardFormat=True, incNums=True):
	"""
	Simple Caesar cypher, all text shifted by the same value
	text: string to be encrypted
	factor: number to shift text by
	cyphNums: determines if the numbers are also shifted
	standardFormat: all caps, not spaces or punctuation,
		false keeps capitalization, spacing, and punctuation
	incNums: wether numbers are included or removed in standard format
	returns encrypted text
	"""
	#Requires: filterString, isAlphaNum
	#Can be treated as special case of vigenere
	if standardFormat:
		text = filterString(text, incNums)

	cypherText = ''
	for char in text:
		if isAlphaNum(char, cyphNums):
			cypherText = cypherText + shift(char, factor)
		else:
			cypherText = cypherText + char

	return cypherText

def vigenere(text, keyword, cyphNums=True, standardFormat=True, incNums=True):
	"""
	Encrypts text by using an overlayed keyword to determine each chatacter's shift
	text: string to be encrypted
	keyword: world that will be used to encrypt
	cyphNums: whether or not numbers get shifted
	standardFormat: whether all caps, not spaces, no punctuation format it used
	incNums: Whether numbers get taken out of text
	returns encrypted text
	"""
	#Requires: filterString, isAlphaNum, shift
	if standardFormat:
		text = filterString(text, incNums)

	keylength = len(keyword)
	cypherText = ''
	n = 0
	for char in text:
		if isAlphaNum(char, cyphNums):
			#get and shift by correct letter of keyword
			cypherText = cypherText + shift(char, keyword[n % keylength] )
			#incrementing index
			n = n + 1
		else:
			cypherText = cypherText + char
	return cypherText


def keyAlphabet(generator, original= 'abcdefghijklmnopqrstuvwxyz'):
	"""
	Generates a keyalphabet using a given word. Fallout76's method. removes letter in given word from alphabet
		then appending said alphabet to given word

	generator: the word used to make the keyalphabet. A word with repeat letters will shrink the set space making
		decryption more difficult to impossible.
	original: defaults to the alphabet; however maybe changed to anything to include other characters.
	returns the new alphabet
	"""
	if len(generator) > len(original):
		generator = generator[:len(original)]
	#idk if i actually need this part ^^^
	#Im pretty sure I dont but I dont feel like testing it

	#loop goes through letters in generator and removes from alphabet
	for char in generator:
		#str.index(substr) gives error if substring not found. try except handles it
		try:
			i = original.index(char)
			#replace with .find(char)?
		except:
			#continue to next iteration of loop
			continue
		#if index found in original, use it to split into two substrings and
		#	combine wihtout the letter
		#	also pretty sure there a string method for this
		#	str.replace(old, new)
		original = original[:i] + original[i+1:]
	return generator + original

def alphaToKey(char, keyAlpha, basicAlpha):
	"""
	Uses keyalphabet and basicAlphabet (original) to encrypt the char. Goes from basic to key
	char: single char to be changed
	keyAlpha: new letters
	basicAlpha: old letters
	returns new char
	"""
	#find the location of char in normal alphabet and gets char at that index 
	#	in the key alphabet
	return keyAlpha[basicAlpha.index(char)]

def oneToOneAlpha(text, generator, standardFormat=True, incNums=True, basicAlpha = 'abcdefghijklmnopqrstuvwxyz'):
	"""
	Encrypted form one alphabet to another
	text: string to be encrypted
	Generator: creates the key alphabet to code into, fo76 method
	standardFormat: whether all caps, not spaces, no punctuation format it used
	incNums: Whether numbers get taken out of text
	basicAlpha: original alphabet
	returns encrypted text
	"""
	#Requires: filterString, keyAlphabet, alphaToKey
	if standardFormat:
		text = filterString(text, incNums)

	keyAlpha = keyAlphabet(generator, basicAlpha)
	cypherText = ''

	for char in text:
		#cap to keep track is char was uppercase
		cap = False
		#if uppercase cap set true and char put in lowercase
		if char <= 'Z' and char >= 'A':
			cap = True
			char = char.lower()
		#if checks if char was in the original alphabet, but its saved as lowercase
		#	so any caps are put into lowercase, so a bunch of extra stuff
		if char in basicAlpha:
			newChar = alphaToKey(char, keyAlpha, basicAlpha)
			#tertiary operator in python
			#if cap is true newChar set to uppercase vertion, lowercase otherwise
			newChar = newChar.upper() if cap else newChar
			cypherText = cypherText + newChar
		else:
			#tertiary for same thing
			char = char.upper() if cap else char
			cypherText = cypherText + char

	return cypherText

def fibonacciString(root, length, floatHandling=0):
	"""
	Makes a fibonacci sequence from the root number, and then turns it into a string.
	root: maybe be int or float
	floatHandling: determines how floats are delt with when added to string
		0: decimal part dropped
		1: unchanged
		2: floor
		3: round
		4: ceil
	returns fibonacci string
	"""
	#Requires: sumHandleFloat, filterString
	penultNum = root
	ultNum = root
	#adding first two digits of sequence with floatHandling, we want first element of its output
	fibString = str( sumHandleFloat(penultNum,0,floatHandling)[0] ) + str( sumHandleFloat(0,ultNum,floatHandling)[0] )
	
	#while loop to make sure the fibonacci sequence is long enough
	while len(filterString(fibString)) < length:
		#for loop does so while conditional function get called 10x less
		#	does that help? idk but I felt rude
		for n in range(10):
			#next number is found by adding previous two
			#nextNumList is a list of length two, the first elemetn is to be used in the string
			#	the second element is for calculations
			nextNumList = sumHandleFloat(penultNum, ultNum, floatHandling)
			#the second to last number is set to the last number
			penultNum = ultNum
			#the last number is get to element 0
			ultNum = nextNumList[1]
			#new number is added to string
			fibString = fibString + str(nextNumList[0])
			#continues going forward in list
	return filterString(fibString)

def sumHandleFloat(penultNum, ultNum, floatHandling=0):
	"""
	Adds two numbers and uses chosen method to deal with floats
	penultNum: number to be added
	ultNum: number to be added
	floatHandling: determines how floats are delt with when added to string
		0:  decimal part dropped
		1: unchanged
		2: floor
		3: round
		4: ceil
	returns list [0]: handled sum, [1]: unchanged sum
	"""
	#Requires: math.floor, math.ceil
	nextNum = penultNum + ultNum
	#used to handle rounding issues from base conversion, for round in return statement
	#Converts number string, reverses string, finds index of decimal point, which is equal
	#	to number of digits
	maxDecimals = str(penultNum)[::-1].find('.')
	nextNumDecimals = str(ultNum)[::-1].find('.')
	#tertiary operator to make sure the highest number of decimals is saved
	maxDecimals = maxDecimals if maxDecimals > nextNumDecimals else nextNumDecimals
	#if the number was no decimals then '.' won't be found and return -1
	#	we need it to be 0 instead
	if maxDecimals == -1:
		maxDecimals = 0
	#python ghetto switch statement actually a dictionary
	switch = {
		1: nextNum,
		2: floor(nextNum),
		3: round(nextNum),
		4: ceil(nextNum)
		}
	#return list, first is meant to be used in string and has the floatHandling applied, the other
	#	is the mathematically accurate result for calculating new values
	return [round( switch.get(floatHandling, int(nextNum)), maxDecimals ), round(nextNum, maxDecimals)]

def fibonacciCypher(text, root, floatHandling=0, pattern=1, inversePattern=False, cyphNums=True, standardFormat=True, incNums=True):
	"""
	Encrypts text using fibonacci-like series a key
	text: string to be encrypted
	root: number used to generate fibonacci sequence string
	floatHandling: determines how floats are delt with when added to string
		0:  decimal part dropped
		1: unchanged
		2: floor
		3: round
		4: ceil
	pattern: creates a pattern for positive or negative shift using mod.
		example with 0 representing positive and 1 representing negative:
			pattern 1: 0000000000
			pattarn 2: 0101010101
			pattern 3: 0110110110
	inversePattern: flips the sights given by pattern
	cyphNums: whether or not numbers get shifted
	standardFormat: whether all caps, not spaces, no punctuation format it used
	incNums: Whether numbers get taken out of text
	returns encrypted text
	"""
	#Requires: filterString, fibonacciString, seriesCypher
	if standardFormat:
		text = filterString(text, incNums)
	
	length = len(text)
	
	fibString = fibonacciString(root, length, floatHandling)

	cyphText = seriesCypher(text, fibString, floatHandling, pattern, inversePattern, cyphNums, standardFormat, incNums)
	return cyphText

def seriesCypher(text, series, floatHandling=0, pattern=1, inversePattern=False, cyphNums=True, standardFormat=True, incNums=True):
	"""
	Encrypts text using any series of numbers as a key, treats each digit as the shift value
	text: string to be encrypted
	series: a string of numbers, equal to or longer than the text
	floatHandling: determines how floats are delt with when added to string
		0:  decimal part dropped
		1: unchanged
		2: floor
		3: round
		4: ceil
	pattern: creates a pattern for positive or negative shift using mod.
		example with 0 representing positive and 1 representing negative:
			pattern 1: 0000000000
			pattarn 2: 0101010101
			pattern 3: 0110110110
	inversePattern: flips the sights given by pattern
	cyphNums: whether or not numbers get shifted
	standardFormat: whether all caps, not spaces, no punctuation format it used
	incNums: Whether numbers get taken out of text
	returns encrypted text
	"""
	#Requires: filterString, isAlpha
	if standardFormat:
		text = filterString(text, incNums)
	
	cyphText = ''
	index=0
	for char in text:
		#only shift alphanumeric
		if isAlphaNum(char, cyphNums):
			#gets shift value and applied pattern using % operator
			value = int(series[index]) if index%pattern == 0 else -int(series[index])
			#if inversePattern is true this will inverse values
			if inversePattern:
				value = -value
			char = shift(char, value)
			#incrementing
			index = index + 1
		cyphText = cyphText + char

	return cyphText

def pascalString(root, length, floatHandling=0):
	"""
	Creates a string of numbers based on the pascal triangle using the root number
	root: a number to generate all numbers
	length: length the string must be at least equal to
	floatHandling: determines how floats are delt with when added to string
		0:  decimal part dropped
		1: unchanged
		2: floor
		3: round
		4: ceil
	returns series string
	"""
	#Requires: sumHandleFloat, filterString
	
	#get number decimals
	rootLength = str(root)[::-1].find('.')
	if rootLength == -1:
		rootLength = 0
	currLine = [root, root]
	nextLine = []
	
	#pascal's will always start with the root repeated three times
	#this starts the string with the root floathandled and repreated three times
	pascString = str( sumHandleFloat(root,0,floatHandling)[0] )*3 
	
	#This entire loop could definitely be written better
	while len( filterString(pascString) ) < length:
		#for cuz I felt rude making the while do everything  ¯\_(ツ)_/¯
		for n in range(5):
			#index to go through each line
			index=1
			#nextline will always begin with root
			nextLine = nextLine + [ root ]
			#get length of current line
			lenCurrLine = len(currLine)
			#loop through line
			while index < lenCurrLine:
				#add numbers to get numbers for next line
				sum = round(currLine[index-1] + currLine[index] ,rootLength )
				#add it to next line
				nextLine = nextLine + [ sum ]
				#increment
				index = index + 1
			#nextline will always end in root
			nextLine = nextLine + [ root ]
			#next become current
			currLine = nextLine
			#loop to add new values to string and apply floathandling
			for val in currLine:
				val = sumHandleFloat(val,0,floatHandling)[0]
				pascString = pascString + str(val)
			#reset nextline
			nextLine = []
	#filter the string to get rid of decimals
	pascString = filterString(pascString)
	return pascString


def pascalCypher(text, root, floatHandling=0, pattern=1, inversePattern=False, cyphNums=True, standardFormat=True, incNums=True):
	"""
	Encrypts text using pascal-like series a key
	text: string to be encrypted
	root: number used to generate pascal sequence string
	floatHandling: determines how floats are delt with when added to string
		0:  decimal part dropped
		1: unchanged
		2: floor
		3: round
		4: ceil
	pattern: creates a pattern for positive or negative shift using mod.
		example with 0 representing positive and 1 representing negative:
			pattern 1: 0000000000
			pattarn 2: 0101010101
			pattern 3: 0110110110
	inversePattern: flips the sights given by pattern
	cyphNums: whether or not numbers get shifted
	standardFormat: whether all caps, not spaces, no punctuation format it used
	incNums: Whether numbers get taken out of text
	returns encrypted text
	"""
	#Requires: filterString, pascalString, seriesCypher
	if standardFormat:
		text = filterString(text, incNums)

	pascString = pascalString(root, len(text), floatHandling)

	cypherText = seriesCypher(text, pascString, floatHandling, pattern, inversePattern, cyphNums, standardFormat, incNums)
	return cypherText

def filterStringSpaced(text, incNums=True, toUpper=True):
	"""
	Used to filter a string but keeps spaces
	text: string to be filtered
	incNums: whether number stay or are filtered, False filters numbers
	toUpper: whether or not string is put into uppercase
	returns filted string
	"""
	#Requires: isAlphaNum
	newString=''
	#like the other one but with spaces too, and also choice of uppercase
	for char in text:
		if isAlphaNum(char, incNums) or char == ' ':
			if toUpper:
				char = char.upper()
			newString = newString + char
	return newString

def findSpaces(text, filterPunc=True, incNums=True):
	"""
	find the indices of the spaces in a string and returns a list of them, the 
		last element of the list is the length of the string
	text: string to be searched
	filterPunc: will look at text as if no punctuaion
	incNums: whether of not numbers are included
	"""
	#Requires: filterStringSpaced
	if filterPunc:
		text = filterStringSpaced(text, incNums, toUpper=True)

	spaceIndices = []
	index = -1

	#pseudo do-while cuz python doesn't have one
	while True:
		#finds the index of space and loops to find next
		index = text.find(' ', index+1)
		#when one cannot be found, str.find() returns -1 so the loop breaks
		if index == -1:
			break
		spaceIndices = spaceIndices + [index]
	#length text added as last element for reasons
	spaceIndices = spaceIndices + [len(text)]

	return spaceIndices

def wordLengths(text, filterPunc=True, incNums=True):
	"""
	Determines the length of all words in a string
	text: string
	filterPunc: whether or not punctuation is counted toward to the length
	incNums: whether or not numbers are counted as words or part of words
	returns list of lengths in order
	"""
	#Requires: findSpaces
	
	#Add -1 as first element to help get length of first word
	spaceIndices = [-1] + findSpaces(text, filterPunc, incNums)
	wordLen = []
	
	#for range
	numSpaces = len(spaceIndices)
	
	#iterating through list of spaces, taking differences between adjacent elements -1
	#	to get the lengths of the words. length 0 is ignored and indicates a double space
	for n in range(1,numSpaces):
		length = spaceIndices[n] - spaceIndices[n-1] - 1
		if length != 0:
			wordLen = wordLen + [length]
	return wordLen
	
def listToString(list):
	"""
	Turns a list into a string
	list: the list
	returns the string
	"""
	#gg ez
	string = ''
	for element in list:
		string = string + str(element)
	return string

def wordLengthCypher(text, floatHandling=0, pattern=1, inversePattern=False, cyphNums=True, standardFormat=False, incNums=True, filterPunc=True):
	"""
	Encrypts text using lengths of words as series key
	text: string to be encrypted
	floatHandling: determines how floats are delt with when added to string
		0:  decimal part dropped
		1: unchanged
		2: floor
		3: round
		4: ceil
	pattern: creates a pattern for positive or negative shift using mod.
		example with 0 representing positive and 1 representing negative:
			pattern 1: 0000000000
			pattarn 2: 0101010101
			pattern 3: 0110110110
	inversePattern: flips the sights given by pattern
	cyphNums: whether or not numbers get shifted
	standardFormat: whether all caps, not spaces, no punctuation format it used
	incNums: Whether numbers get taken out of text
	filterPunc: whether or not punctuation is filtered out
	returns encrypted text
	"""
	#Requires: wordLengths, listToString, math.ceil, seriesCypher
	#too lazy to check a bunch of cases right now
	wordLenList = wordLengths(text, filterPunc)
	wordLenString = listToString(wordLenList)

	wordLenString = wordLenString * ceil( len(text)/len(wordLenString) )

	cyphText = seriesCypher(text, wordLenString, floatHandling, pattern, inversePattern, cyphNums, standardFormat, incNums)
	return cyphText


class mutableKey():
	def __init__(self, key='', alpha='abcdefghijklmnopqrstuvwxyz'):
		self.key = key
		self.alpha = alpha
	
	#adds a letter to the kay
	def add(self, char):
		self.key = self.key + char

	#finds index of letter in key
	def ind(self, char):
		return self.key.find(char)

	#removes letter from key and its pair in alpha
	def rem(self, keyChar, alphaChar):
		self.key = self.key.replace(keyChar,'')
		self.alpha = self.alpha.replace(alphaChar,'')

	#gets the corresponding letter
	#goes from key to alpha
	def get(self, char):
		index = self.ind(char)
		newChar = self.alpha[index]
		self.rem(char, newChar)
		return newChar

def mutKeyCharCypher(text, generator, standardFormat=True, incNums=True, basicAlpha='abcdefghijklmnopqrstuvwxyz'):
	"""
	Encrypts with continuously changing alphabets, if a character is not included in the generator or basicAlpha
		then it will not be encrypted
	text: string to be encoded
	generator: creates key alphabet with fo76 method
	standardFormat: if true string returns as only uppercase alphanumerics
	incNums: whether or not numbers are included in standard format
	basicAlpha: the alphabet shifted into
	"""
	if standardFormat:
		text = filterString(text, incNums)

	cypherText = ''
	#tracker will keep track of what mutableKey a given letter is in
	tracker = {}
	#generate keyAlpha to be used
	keyAlpha = keyAlphabet(generator, basicAlpha)
	#fill tracker with all character that can be encrypted
	for char in keyAlpha:
		tracker[char] = 0

	#holds the different mutableKeys, given a number to call by for given char tracker value
	keyDict = {0: mutableKey(keyAlpha, basicAlpha)}


	for char in text:
		#tracking upeprcase
		cap=False
		if char.isupper():
			cap=True
			char = char.lower()
		#if character belongs to set it will be encrypted
		if char in keyAlpha:
			#get char's mutableKey level
			n = tracker[char]
			#increment char's value
			tracker[char] = n+1
			#get encrypted char by calling the mutableKey it is in calling .get method
			newChar = keyDict[n].get(char)
			#if the mutableKey object for level has not been created yet, create it
			if n+1 not in keyDict:
				keyDict[n+1] = mutableKey(char, alpha=basicAlpha)
			else:
				#if it has then add the next char to the key
				keyDict[n+1].add(char)
		#if not encrypted dont do anything, reassign to newChar for gg ez
		else:
			newChar = char
		#if need recap
		newChar = newChar.upper() if cap else newChar
		#making new string
		cypherText = cypherText + newChar

	return cypherText

