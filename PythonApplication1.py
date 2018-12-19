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
	for char in text:
		if isAlphaNum(char, incNums):
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
	char = ord(char)
	if ( type(factor)==str and len(factor)==1 ):
		factor = ord(factor)
		if(factor >= 48 and factor <= 57):
			factor = factor - 48
		elif(factor >= 65 and factor <=90):
			factor = factor - 64
		else:
			factor = factor -96

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
			cypherText = cypherText + shift(char, keyword[n % keylength] )
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

	for char in generator:
		try:
			i = original.index(char)
			#replace with .find(char)?
		except:
			continue
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
		cap = False
		if char <= 'Z' and char >= 'A':
			cap = True
			char = char.lower()
		if char in basicAlpha:
			newChar = alphaToKey(char, keyAlpha, basicAlpha)
			newChar = newChar.upper() if cap else newChar
			cypherText = cypherText + newChar
		else:
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

	fibString = str( sumHandleFloat(penultNum,0,floatHandling)[0] ) + str( sumHandleFloat(0,ultNum,floatHandling)[0] )
	
	while len(filterString(fibString)) < length:
		for n in range(10):
			nextNumList = sumHandleFloat(penultNum, ultNum, floatHandling)
			penultNum = ultNum
			ultNum = nextNumList[1]
			fibString = fibString + str(nextNumList[0])
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
	maxDecimals = str(penultNum)[::-1].find('.')
	nextNumDecimals = str(ultNum)[::-1].find('.')
	maxDecimals = maxDecimals if maxDecimals > nextNumDecimals else nextNumDecimals
	if maxDecimals == -1:
		maxDecimals = 0

	switch = {
		1: nextNum,
		2: floor(nextNum),
		3: round(nextNum),
		4: ceil(nextNum)
		}
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
		if isAlphaNum(char, cyphNums):
			value = int(series[index]) if index%pattern == 0 else -int(series[index])
			if inversePattern:
				value = -value
			char = shift(char, value)
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
	
	rootLength = str(root)[::-1].find('.')
	if rootLength == -1:
		rootLength = 0
	currLine = [root, root]
	nextLine = []

	pascString = str( sumHandleFloat(root,0,floatHandling)[0] )*3 

	while len( filterString(pascString) ) < length:
		for n in range(5):
			index=1
			nextLine = nextLine + [ root ]
			lenCurrLine = len(currLine)
			while index < lenCurrLine:
				sum = round(currLine[index-1] + currLine[index] ,rootLength )
				nextLine = nextLine + [ sum ]
				index = index + 1
			nextLine = nextLine + [ root ]
			currLine = nextLine
			for val in currLine:
				val = sumHandleFloat(val,0,floatHandling)[0]
				pascString = pascString + str(val)
			nextLine = []
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
	for char in text:
		if isAlphaNum(char, incNums) or char == ' ':
			if toUpper:
				char = char.upper()
			newString = newString + char
	return newString

def findSpaces(text, filterPunc=True, incNums=True):
	"""
	find the indices of the spaces in a string and returns a list of them
	text: string to be searched
	filterPunc: will look at text as if no punctuaion
	incNums: whether of not numbers are included
	"""
	#Requires: filterStringSpaced
	if filterPunc:
		text = filterStringSpaced(text, incNums, toUpper=True)

	spaceIndices = []
	index = -1

	while True:
		index = text.find(' ', index+1)
		if index == -1:
			break
		spaceIndices = spaceIndices + [index]
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
	spaceIndices = [-1] + findSpaces(text, filterPunc, incNums)
	wordLen = []

	numSpaces = len(spaceIndices)

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

