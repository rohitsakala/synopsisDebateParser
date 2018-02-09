#/usr/bin/env python

import re

def removeNumbers(data):
	return ''.join([i for i in data if not i.isdigit()])

def toLowerCase(data):
	return data.lower()

def removeWhiteSpace(data):
	return data.replace(" ","")

def removeNewLine(data):
	return data.replace("\n","")

def getUpperCharacters(data):
	return ''.join(c for c in data if c.isupper())

def removeSpecialCharacters(data):
	data = re.sub('[^a-zA-Z0-9 \n\.]', '', data)
	return data

def sort(data):
	return ''.join(sorted(data))

def debateTypePreprocess(data):
	data = toLowerCase(data)
	data = removeWhiteSpace(data)
	data = removeSpecialCharacters(data)
	data = removeNewLine(data)
	return data

def billPreprocess(data):
	data = toLowerCase(data)
	data = removeWhiteSpace(data)
	data = removeSpecialCharacters(data)
	data = removeNewLine(data)
	return data

def memberNamePreprocess(data):
	data = toLowerCase(data)
	data = removeSpecialCharacters(data)
	data = removeNewLine(data)
	data = sort(data)
	return data

def debateTypeSpecialPreprocess(data):
	data = removeSpecialCharacters(data)
	data = removeNewLine(data)
	data = removeWhiteSpace(data)
	data = removeNumbers(data)
	return data
