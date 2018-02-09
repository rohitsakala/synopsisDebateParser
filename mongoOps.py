#/usr/bin/env python

from pymongo import MongoClient
from bson.objectid import ObjectId

def getClient():
	client = MongoClient('localhost:27017')
	return client

def getDatabase(database):
	return getClient()[database]

def getTable(database,table):
	return getClient()[database][table]

def insertDocument(database,table,doc):
	db = getClient()[database][table]
	return db.insert(doc)

def getDocument(database,table,id):
	db = getClient()[database][table]
	return db.find_one({'_id': ObjectId(id)})
