"""
Actual trash design because I didnt even try to layout the
	logic first
"""

from random import randint

def rotorGen(length):
	temp=[]
	rotor=[]
	for n in range(length):
		temp = temp + [n]

	while 0 < length:
		num = temp[randint(0,length-1)]
		rotor = rotor + [num]
		temp.remove(num)
		length = length - 1
	
	return rotor

def toStandard(text):
	newText = ''
	for char in text:
		if char.isalnum():
			newText = newText + char.upper()
	return newText

def isValidReflector(reflector):
	for n in range(len(reflector)):
		try:
			if n != reflector[reflector[n]]:
				return False
		except:
			return False
			
	return True

def reflectorGen(length):
	#distribution of values not linear for some reason but close so im ok with it
	reflector=[]
	temp=[]
	refDict={}
	longness =  length
	for n in range(length):
		temp = temp + [n]
	index=0
	while 1 < length:
		while index in refDict:
			index = index + 1
		num = temp[randint(0, length-1)]
		refDict[index] = num
		refDict[num] = index
		temp.remove(num)
		if num != index:
			temp.remove(index)
			length = length - 1
		index = index + 1
		length = length - 1

	if length == 1:
		refDict[temp[0]] = temp[0]

	for n in range(longness):
		reflector = reflector + [ refDict[n] ]

	return reflector

def distCheck():
	d={}
	for n in range(20):
		d[n]=0
	for n in range(2000):
		h=reflectorGen(20)
		if isValidReflector(h) == False:
			return False
		for m in h:
			d[m] = d[m] + h[m]
	sum = 0
	for v in d:
		sum = sum + d[v]
	for k in d:
		d[k] = round(d[k]/sum,3)
	for l in d:
		print(l,"==",d[l])
	
	return d

def generalizedEnigmaCypher(text, layers=3, turnCond=[],switchTable=[], alpha='abcdefghijklmnopqrstuvwxyz' ,standardForm=True, rotorDict={}, pairedReflector=True ):
	if standardForm:
		text = toStandard(text)

	switchDict = {}
	for char in alpha:
		switchDict[char] = char

	for pair in switchTable:
		switchDict[pair[0]] = pair[1]
		switchDict[pair[1]] = pair[0]

	lengthText =  len(text) 
	#bad naming because I dont wanna go and rename everyhting
	length = len(alpha)
	cypherText = ''




	for n in range(layers):
		if (rotorDict.setdefault(n) != None) and  ( len(rotorDict[n]) == length):
			continue
		else:
			rotorDict[n] = rotorGen(length)

	if pairedReflector:
		if not isValidReflector(rotorDict[layers-1]):
			rotorDict[layers-1] = reflectorGen(length)


	tooLarge = False
	for n in range(layers):
		try:
			cond = turnCond[n]
			if cond > lengthText or cond ==0:
				turnCond[n] = lengthText+1
		except:
			if not tooLarge:
				cond = length**n
				tooLarge = cond > lengthText
			else:
				cond = lengthText + 1
			turnCond = turnCond + [cond]
	#reflector forbidden from rotating, it represents wall of machine
	#	not an actual rotor
	turnCond[layers-1] = lengthText+1
	
	count = -1
	for char in text:
		isCap = False
		if char.isupper():
			isCap = True
			char = char.lower()
		if char in alpha:
			char = switchDict[char]
			count = count + 1
			index = alpha.find(char)
			for n in range(layers):
				if n >= layers:
					n = (n-1) - n%layers
				index = (index + ( count//turnCond[n] ) ) % length
				index = rotorDict[n][index]
			value = index
			for n in range(-layers+2,1):
				n = -n
				value = rotorDict[n].index(value)
				value = (value - (count//turnCond[n] ) ) % length
			char = alpha[value]
			char = switchDict[char]
		if isCap:
			char = char.upper()
		cypherText = cypherText + char

	return [cypherText, layers, turnCond, switchTable,alpha, rotorDict]

