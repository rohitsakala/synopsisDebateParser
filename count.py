#/usr/bin/env python
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

from flask_pymongo import PyMongo
from pymongo import MongoClient
from bson.objectid import ObjectId
import numpy as np
from os import listdir
from os.path import isfile, join
import re
import json
from random import randint
from sklearn.decomposition import NMF
import tensorflow as tf
import datetime
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import word_tokenize, pos_tag, ne_chunk
import operator
import os,sys
from sklearn.feature_extraction.text import TfidfVectorizer

nouns_pos = ["NN", "NNS", "NNP" , "NNPS", "GP" ]

def display_topics(model, feature_names, no_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print "Topic %d:" % (topic_idx)
        print " ".join([feature_names[i]
                        for i in topic.argsort()[:-no_top_words - 1:-1]])

def getFrequency():
	client = MongoClient('localhost:27017')
	database = client["synopsis"]
	sessions = database["sessions"]
	countGeneral = 0
	countGovernmentBills = 0
	countMinisterStatement = 0
	countSubmissionMembers = 0
	countPrivateMemberBill = 0
	countStatutoryResolutions = 0
	countReferences = 0
	countPrivateMemberResolution = 0
	countCallingAttention = 0
	countDiscussion = 0
	countMotion = 0
	countPresidentThanks = 0
	countMatterUnderThreeSevenSeven = 0
	for session in sessions.find():
		if "debates" in session.keys():
			for debate in session["debates"].keys():
				if debate == "5999644a37335cad52ecd861" or debate == "5999645137335cad52ecd862": # General
					countGeneral = countGeneral + 1
				elif debate == "5999649f37335cad52ecd86b":
					countGovernmentBills = countGovernmentBills + 1
				elif debate == "599965d837335cad52ecd88b":
					countMinisterStatement = countMinisterStatement + 1
				elif debate == "5999660437335cad52ecd890":
					countSubmissionMembers = countSubmissionMembers + 1
				elif debate == "59d0d7f12589e39d8102872e":
					countPrivateMemberBill = countPrivateMemberBill + 1
				elif debate == "599965fa37335cad52ecd88f":
					countStatutoryResolutions = countStatutoryResolutions + 1
				elif debate == "599965ab37335cad52ecd885":
					countReferences = countReferences + 1
				elif debate == "5999659437335cad52ecd883":
					countPrivateMemberResolution = countPrivateMemberResolution + 1
				elif debate == "5999646837335cad52ecd865":
					countCallingAttention = countCallingAttention + 1
				elif debate == "59dce640a7401a6088699006":
					countDiscussion = countDiscussion + 1
				elif debate == "59de7e808363ad7bd6d9b762":
					countMotion = countMotion + 1
				elif debate == "5999650a37335cad52ecd876":
					countPresidentThanks = countPresidentThanks + 1
				elif debate == "599964df37335cad52ecd872":
					countMatterUnderThreeSevenSeven = countMatterUnderThreeSevenSeven + 1

	print "General " + str(countGeneral)
	print "GovernmentBills " + str(countGovernmentBills)
	print "MinisterStatement " + str(countMinisterStatement)
	print "SubmissionMembers " + str(countSubmissionMembers)
	print "PrivateMemberBill " + str(countPrivateMemberBill)
	print "StatutoryResolutions " + str(countStatutoryResolutions)
	print "References " + str(countReferences)
	print "PrivateMemberResolution " + str(countPrivateMemberResolution)
	print "CallingAttention " + str(countCallingAttention)
	print "MatterUnderThreeSevenSeven " + str(countMatterUnderThreeSevenSeven)
	print "PresidentThanks " + str(countPresidentThanks)
	print "Motion " + str(countMotion)
	print "Discussion " + str(countDiscussion)
	

def getWordCount():
	client = MongoClient('localhost:27017')
	database = client["synopsis"]
	debates = database["debates"]
	sessions = database["sessions"]
	wordcount = set()
	for session in sessions.find():
		if "debates" in session.keys():
			for debate in session["debates"]:
				#print session["debates"][debate]
				if isinstance(session["debates"][debate], dict):
					if "0" in session["debates"][debate].keys():
						#print session["debates"][debate]
						if isinstance(session["debates"][debate]['0'], list): # List
							for debateId in session["debates"][debate]['0']:
								data = debates.find_one({'_id': ObjectId(debateId)})
								if "mattersMap" in data:
				
									for speech in data["mattersMap"]:
										tokens = word_tokenize(data["mattersMap"][speech]["speech"])
										for token in tokens:
											wordcount.add(token)
						elif isinstance(session["debates"][debate]['0'], ObjectId):
							for debateId in session["debates"][debate]:
									data = debates.find_one({'_id': ObjectId(session["debates"][debate][debateId])})
									if "mattersMap" in data:
										for count in data["mattersMap"]:
											if count != "_id" and count != "replyText":
												tokens = word_tokenize(data["mattersMap"][count]["speech"])
												for token in tokens:
													wordcount.add(token)
									else:
										for count in data:
											if count != "_id" and count != "replyText":
												tokens = word_tokenize(data[count]["speech"])
												for token in tokens:
													wordcount.add(token)
						elif "bill" in session["debates"][debate]['0']: # bill anbd bill id
								for debateId in session["debates"][debate]:
									data = debates.find_one({'_id': ObjectId(session["debates"][debate][debateId]["bill"])})
									if "mattersMap" in data:
										for count in data["mattersMap"]:
											if count != "_id" and count != "replyText":
												tokens = word_tokenize(data["mattersMap"][count]["speech"])
												for token in tokens:
													wordcount.add(token)
									else:
										for count in data:
											if count != "_id" and count != "replyText":
												tokens = word_tokenize(data[count]["speech"])
												for token in tokens:
													wordcount.add(token)
				elif isinstance(session["debates"][debate], list):
					for debateId in session["debates"][debate]:
						data = debates.find_one({'_id': ObjectId(debateId)})
						if "mattersMap" in data:
							for count in data["mattersMap"]:
								if count != "_id" and count != "replyText" and len(count) < 15:
									tokens = word_tokenize(data["mattersMap"][count]["speech"])
									for token in tokens:
										wordcount.add(token)
						else:
							for count in data:
								if count != "_id" and count != "replyText" and count != "text" and count != "debatableText":
									tokens = word_tokenize(data[count]["speech"])
									for token in tokens:
										wordcount.add(token)
								if count == "text" and count != "debatableText":
									tokens = word_tokenize(data["text"])
									for token in tokens:
										wordcount.add(token)
								if count == "debatableText":
									tokens = word_tokenize(data["text"])
									for token in tokens:
										wordcount.add(token)
				elif isinstance(session["debates"][debate], ObjectId):
					data = debates.find_one({'_id': ObjectId(session["debates"][debate])})
					if "mattersMap" in data:
						for count in data["mattersMap"]:
							if count != "_id" and count != "replyText" and len(count) < 15:
								tokens = word_tokenize(data["mattersMap"][count]["speech"])
								for token in tokens:
									wordcount.add(token)
					else:
						for count in data:
							#print count
							if count != "_id" and count != "replyText" and count != "text" and count != "debatableText" and len(count) < 15 and count != "title" and count !="debaterName":
								tokens = word_tokenize(data[count]["speech"])
								for token in tokens:
									wordcount.add(token)
							if count == "text" and count != "debatableText":
								tokens = word_tokenize(data["text"])
								for token in tokens:
									wordcount.add(token)
							if count == "debatableText":
								tokens = word_tokenize(data["text"])
								for token in tokens:
									wordcount.add(token)

	print "WordCount : " + str(len(wordcount))

def getWordCount():
	client = MongoClient('localhost:27017')
	database = client["synopsis"]
	debates = database["debates"]
	sessions = database["sessions"]
	wordcount = set()
	for session in sessions.find():
		if "debates" in session.keys():
			for debate in session["debates"]:
				#print session["debates"][debate]
				if isinstance(session["debates"][debate], dict):
					if "0" in session["debates"][debate].keys():
						#print session["debates"][debate]
						if isinstance(session["debates"][debate]['0'], list): # List
							for debateId in session["debates"][debate]['0']:
								data = debates.find_one({'_id': ObjectId(debateId)})
								if "mattersMap" in data:
									for count in data["mattersMap"]:
										tokens = word_tokenize(data["mattersMap"][count]["speech"])
										for token in tokens:
											wordcount.add(token)
						elif isinstance(session["debates"][debate]['0'], ObjectId):
							for debateId in session["debates"][debate]:
									data = debates.find_one({'_id': ObjectId(session["debates"][debate][debateId])})
									if "mattersMap" in data:
										for count in data["mattersMap"]:
											if count != "_id" and count != "replyText":
												tokens = word_tokenize(data["mattersMap"][count]["speech"])
												for token in tokens:
													wordcount.add(token)
									else:
										for count in data:
											if count != "_id" and count != "replyText":
												tokens = word_tokenize(data[count]["speech"])
												for token in tokens:
													wordcount.add(token)
						elif "bill" in session["debates"][debate]['0']: # bill anbd bill id
								for debateId in session["debates"][debate]:
									data = debates.find_one({'_id': ObjectId(session["debates"][debate][debateId]["bill"])})
									if "mattersMap" in data:
										for count in data["mattersMap"]:
											if count != "_id" and count != "replyText":
												tokens = word_tokenize(data["mattersMap"][count]["speech"])
												for token in tokens:
													wordcount.add(token)
									else:
										for count in data:
											if count != "_id" and count != "replyText":
												tokens = word_tokenize(data[count]["speech"])
												for token in tokens:
													wordcount.add(token)
				elif isinstance(session["debates"][debate], list):
					for debateId in session["debates"][debate]:
						data = debates.find_one({'_id': ObjectId(debateId)})
						if "mattersMap" in data:
							for count in data["mattersMap"]:
								if count != "_id" and count != "replyText" and len(count) < 15:
									tokens = word_tokenize(data["mattersMap"][count]["speech"])
									for token in tokens:
										wordcount.add(token)
						else:
							for count in data:
								if count != "_id" and count != "replyText" and count != "text" and count != "debatableText":
									tokens = word_tokenize(data[count]["speech"])
									for token in tokens:
										wordcount.add(token)
								if count == "text" and count != "debatableText":
									tokens = word_tokenize(data["text"])
									for token in tokens:
										wordcount.add(token)
				elif isinstance(session["debates"][debate], ObjectId):
					data = debates.find_one({'_id': ObjectId(session["debates"][debate])})
					if "mattersMap" in data:
						for count in data["mattersMap"]:
							if count != "_id" and count != "replyText" and len(count) < 15:
								tokens = word_tokenize(data["mattersMap"][count]["speech"])
								for token in tokens:
									wordcount.add(token)
					else:
						for count in data:
							#print count
							if count != "_id" and count != "replyText" and count != "text" and count != "debatableText" and len(count) < 15 and count != "title" and count !="debaterName":
								tokens = word_tokenize(data[count]["speech"])
								for token in tokens:
									wordcount.add(token)
							if count == "text" and count != "debatableText":
								tokens = word_tokenize(data["text"])
								for token in tokens:
									wordcount.add(token)

	print "WordCount : " + str(len(wordcount))

def getTfIdfWords():
	client = MongoClient('localhost:27017')
	database = client["synopsis"]
	debates = database["debates"]
	sessions = database["sessions"]
	docs = []
	for session in sessions.find():
			if "debates" in session.keys():
				for debate in session["debates"]:
					if isinstance(session["debates"][debate], dict):
						if "0" in session["debates"][debate].keys():
							if isinstance(session["debates"][debate]['0'], list): # List
								for debateId in session["debates"][debate]['0']:
									data = debates.find_one({'_id': ObjectId(debateId)})
									if "mattersMap" in data:
										for count in data["mattersMap"]:
											docs.append(data["mattersMap"][count]["speech"])
							elif isinstance(session["debates"][debate]['0'], ObjectId):
								for debateId in session["debates"][debate]:
										data = debates.find_one({'_id': ObjectId(session["debates"][debate][debateId])})
										if "mattersMap" in data:
											for count in data["mattersMap"]:
												if count != "_id" and count != "replyText":
													docs.append(data["mattersMap"][count]["speech"])
										else:
											for count in data:
												if count != "_id" and count != "replyText":
													docs.append(data[count]["speech"])
							elif "bill" in session["debates"][debate]['0']: # bill anbd bill id
									for debateId in session["debates"][debate]:
										data = debates.find_one({'_id': ObjectId(session["debates"][debate][debateId]["bill"])})
										if "mattersMap" in data:
											for count in data["mattersMap"]:
												if count != "_id" and count != "replyText":
													docs.append(data["mattersMap"][count]["speech"])
										else:
											for count in data:
												if count != "_id" and count != "replyText":
													docs.append(data[count]["speech"])
													if "infrastructure" in data[count]["speech"] and "city" in data[count]["speech"] and "lost" in data[count]["speech"]:
														print data[count]["speech"]
														print data[count]["name"]
														print "5"
														raw_input()
														print session["debates"][debate][debateId]["bill"]
														print session
					elif isinstance(session["debates"][debate], list):
						for debateId in session["debates"][debate]:
							data = debates.find_one({'_id': ObjectId(debateId)})
							if "mattersMap" in data:
								for count in data["mattersMap"]:
									if count != "_id" and count != "replyText" and len(count) < 15:
										docs.append(data["mattersMap"][count]["speech"])
							else:
								for count in data:
									if count != "_id" and count != "replyText" and count != "text" and count != "debatableText":
										docs.append(data[count]["speech"])
									if count == "text":
										docs.append(data["text"])
					elif isinstance(session["debates"][debate], ObjectId):
						data = debates.find_one({'_id': ObjectId(session["debates"][debate])})
						if "mattersMap" in data:
							for count in data["mattersMap"]:
								if count != "_id" and count != "replyText" and len(count) < 15:
									docs.append(data["mattersMap"][count]["speech"])
						else:
							for count in data:
								if count != "_id" and count != "replyText" and count != "text" and count != "debatableText" and len(count) < 15 and count != "title" and count !="debaterName":
									docs.append(data[count]["speech"])
									if "infrastructure" in data[count]["speech"] and "city" in data[count]["speech"] and "lost" in data[count]["speech"]:
										print data["mattersMap"][count]["speech"]
										print "10"
										raw_input()
								if count == "text":
									docs.append(data["text"])

	#vectorizer = TfidfVectorizer(min_df=1)
	#X = vectorizer.fit_transform(docs)
	#idf = vectorizer._tfidf.idf_
	#ans = dict(zip(vectorizer.get_feature_names(), idf))
	#ans = sorted(ans.items(), key=operator.itemgetter(1))
	#print json.dumps(ans, indent=4)
	#for an in ans:
	#	fd = word_tokenize(an[0])
	#	tagged = pos_tag(fd)
	#	if tagged[0][1] in nouns_pos:
	#		print tagged[0][0]
	#NMF_run(docs)



def NMF_run(docsList):
	documents = docsList
	no_features = 10000

	# NMF is able to use tf-idf
	tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, max_features=no_features, stop_words='english')
	tfidf = tfidf_vectorizer.fit_transform(documents)
	tfidf_feature_names = tfidf_vectorizer.get_feature_names()

	no_topics = 10

	#Run NMF
	nmf = NMF(n_components=no_topics, random_state=1, alpha=.1, l1_ratio=.5, init='nndsvd').fit(tfidf)

	no_top_words = 1
	
	print "NMF Topics"
	return display_topics(nmf, tfidf_feature_names, no_top_words)

def getSpeechesCount():
	client = MongoClient('localhost:27017')
	database = client["synopsis"]
	debates = database["debates"]
	members = database["members"]
	sessions = database["sessions"]
	stats = {}
	docs = []
	for session in sessions.find():
		if "debates" in session.keys():
				for debate in session["debates"]:
					if isinstance(session["debates"][debate], dict):
						if "0" in session["debates"][debate].keys():
							if isinstance(session["debates"][debate]['0'], list): # List
								for debateId in session["debates"][debate]['0']:
									data = debates.find_one({'_id': ObjectId(debateId)})
									if "mattersMap" in data:
										for count in data["mattersMap"]:
											memberId = data["mattersMap"][count]["name"]
											memberdata = members.find_one({'_id': ObjectId(memberId)})
											if memberdata["party"] not in stats:
												stats[str(memberdata["party"])] = 1
											else:
												stats[str(memberdata["party"])] = stats[str(memberdata["party"])] + 1
							elif isinstance(session["debates"][debate]['0'], ObjectId):
								for debateId in session["debates"][debate]:
										data = debates.find_one({'_id': ObjectId(session["debates"][debate][debateId])})
										if "mattersMap" in data:
											for count in data["mattersMap"]:
												if count != "_id" and count != "replyText":
													memberId = data["mattersMap"][count]["name"]
													if memberId != "None":
														memberdata = members.find_one({'_id': ObjectId(memberId)})
														if memberdata["party"] not in stats:
															stats[str(memberdata["party"])] = 1
														else:
															stats[str(memberdata["party"])] = stats[str(memberdata["party"])] + 1
							elif "bill" in session["debates"][debate]['0']: # bill anbd bill id
									for debateId in session["debates"][debate]:
										data = debates.find_one({'_id': ObjectId(session["debates"][debate][debateId]["bill"])})
										if "mattersMap" in data:
											for count in data["mattersMap"]:
												if count != "_id" and count != "replyText":
													memberId = data["mattersMap"][count]["name"]
													memberdata = members.find_one({'_id': ObjectId(memberId)})
													if memberdata["party"] not in stats:
														stats[str(memberdata["party"])] = 1
													else:
														stats[str(memberdata["party"])] = stats[str(memberdata["party"])] + 1
										else:
											for count in data:
												if count != "_id" and count != "replyText":
													memberId = data[count]["name"]
													memberdata = members.find_one({'_id': ObjectId(memberId)})
													if memberdata["party"] not in stats:
														stats[str(memberdata["party"])] = 1
													else:
														stats[str(memberdata["party"])] = stats[str(memberdata["party"])] + 1
					elif isinstance(session["debates"][debate], list):
						for debateId in session["debates"][debate]:
							data = debates.find_one({'_id': ObjectId(debateId)})
							if "mattersMap" in data:
								for count in data["mattersMap"]:
									if count != "_id" and count != "replyText" and len(count) < 15:
										memberId = data["mattersMap"][count]["name"]
										memberdata = members.find_one({'_id': ObjectId(memberId)})
										if memberdata["party"] not in stats:
											stats[str(memberdata["party"])] = 1
										else:
											stats[str(memberdata["party"])] = stats[str(memberdata["party"])] + 1
							else:
								for count in data:
									if count != "_id" and count != "replyText" and count != "text" and count != "debatableText":
										memberId = data[count]["name"]
										memberdata = members.find_one({'_id': ObjectId(memberId)})
										if memberdata["party"] not in stats:
											stats[str(memberdata["party"])] = 1
										else:
											stats[str(memberdata["party"])] = stats[str(memberdata["party"])] + 1
					elif isinstance(session["debates"][debate], ObjectId):
						data = debates.find_one({'_id': ObjectId(session["debates"][debate])})
						if "mattersMap" in data:
							for count in data["mattersMap"]:
								if count != "_id" and count != "replyText" and len(count) < 15:
									memberId = data["mattersMap"][count]["name"]
									memberdata = members.find_one({'_id': ObjectId(memberId)})
									if memberdata["party"] not in stats:
										stats[str(memberdata["party"])] = 1
									else:
										stats[str(memberdata["party"])] = stats[str(memberdata["party"])] + 1
						else:
							for count in data:
								if count != "_id" and count != "replyText" and count != "text" and count != "debatableText" and len(count) < 15 and count != "title" and count !="debaterName":
									memberId = data[count]["name"]
									memberdata = members.find_one({'_id': ObjectId(memberId)})
									if memberdata["party"] not in stats:
										stats[str(memberdata["party"])] = 1
									else:
										stats[str(memberdata["party"])] = stats[str(memberdata["party"])] + 1

	print sorted(stats.items(), key=operator.itemgetter(1),reverse = True)


if __name__ == '__main__':
	#getFrequency()
	#getWordCount()
	getTfIdfWords()
	#getSpeechesCount()