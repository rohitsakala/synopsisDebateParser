#/usr/bin/env python

import json
import os
import sys
import time
import re
import preprocess
import utils
import mongoOps
import difflib
import glob
from collections import OrderedDict
import debateTypePopulate

def getHouseName(file,session):
    # The first line of the session is the name of the house.
    session['houseName'] = file.readline().strip('\n')
    return session

def getDocumentType(file,session):
    # The third line of the session is the name of the document type.
    file.readline()
    session['documentType'] = file.readline().strip('\n')
    return session

def getDates(file,session):
    line = ""
    while True:
        line = file.readline()
        if "/" in line:
            break
    dates = re.split("/",line)
    session['englishDate'] = dates[0]
    session['indianDate'] = dates[1]
    return session

def getDebateType(file,session):
    table = mongoOps.getTable('synopsis','debateTypes')
    # Get debate types in a list and preprocess each debatetype
    debateTypes = []
    originalDebateTypes = []
    for debateType in table.find():
        dtype = preprocess.debateTypePreprocess(debateType['type'])
        debateTypes.append(dtype)
        originalDebateTypes.append(debateType['_id'])
    found = False
    if "billId" in session.keys():
        session["debateType"] = '5999649f37335cad52ecd86b'
        if "5999649f37335cad52ecd86b" not in session["debates"].keys():
            session["debates"][str("5999649f37335cad52ecd86b")] = OrderedDict()
        return session
    while 1:
        pos1 = file.tell()
        line = file.readline()
        resLine = line
        #print "Line " + line
        billId = utils.getBillMatch(line)
        if billId != None:
            session["billId"] = billId
            session["debateType"] = '5999649f37335cad52ecd86b'
            if "5999649f37335cad52ecd86b" not in session["debates"].keys():
                session["debates"][str("5999649f37335cad52ecd86b")] = OrderedDict()
            return session
        ## Exception Cases ##
        if "OBITUARY REFERENCES" in line:
            session["debateType"] = '5999652b37335cad52ecd879'
            session["debates"][str("5999652b37335cad52ecd879")] = ""
            file.seek(pos1)
            return session
        if "MOTION OF THANKS ON THE PRESIDENT'S ADDRESS" in line:
            session["debateType"] = '5999650a37335cad52ecd876'
            session["debates"][str("5999650a37335cad52ecd876")] = ""
            file.seek(pos1)
            return session
        if "DISCUSSION UNDER RULE" in line:
            session["debateType"] = '59dce640a7401a6088699006'
            session["debates"][str("59dce640a7401a6088699006")] = ""
            file.seek(pos1)
            return session
        if "SUSPENSION OF MEMBERS" in line:
            session["debateType"] = '59de0a96c0a9b7b482106cb9'
            session["debates"][str("59de0a96c0a9b7b482106cb9")] = ""
            file.seek(pos1)
            return session
        if "PRIVATE MEMBERS' BILLS" in line:
            session["debateType"] = '59d0d7f12589e39d8102872e'
            if "59d0d7f12589e39d8102872e" not in session["debates"].keys():
                session["debates"][str("59d0d7f12589e39d8102872e")] = ""
            file.seek(pos1)
            return session
        if "WELCOME TO PARLIAMENTARY DELEGATION" in line or "WELCOME TO THE PARLIAMENTARY DELEGATION" in line:                   # Mapping to Introduction to Parliamentary Delegation
            session["debateType"] = '599964cc37335cad52ecd870'
            session["debates"][str("599964cc37335cad52ecd870")] = ""
            file.seek(pos1)
            return session
        if  "ADDRESS BY THE SPEAKER" in line:
            session["debateType"] = '5999642537335cad52ecd85d'
            session["debates"][str("5999642537335cad52ecd85d")] = ""
            file.seek(pos1)
            return session
        if "OATH BY MEMBERS" in line:
            session["debateType"] = '5999652437335cad52ecd878'
            session["debates"][str("5999652437335cad52ecd878")] = ""
            file.seek(pos1)
            return session
        if "REFERENCES BY SPEAKER" in line or "REFRENCE BY SPEAKER" in line or "REFERENCE BY THE SPEAKER" in line or "REFERENCE BY SPEAKER" in line:                                  # Mapping to Introduction to Parliamentary Delegation
            session["debateType"] = '599965ab37335cad52ecd885'
            session["debates"][str("599965ab37335cad52ecd885")] = ""
            return session
        if "FELICITAITON BY THE SPEAKER" in line or "FELICITATION BY SPEAKER" in line or "FELICITATIONS BY SPEAKER" in line or "FELICITATIONS BY THE SPEAKER" in line or "FELICITATION BY THE SPEAKER" in line or "FELICITATION BY SPEAKER" in line:                                  # Mapping to Introduction to Parliamentary Delegation
            session["debateType"] = '5999649837335cad52ecd86a'
            session["debates"][str("5999649837335cad52ecd86a")] = ""
            return session
        if "THE UTTARAKHAND BUDGET, 2016-17 - GENERAL DISCUSSION" in line:
            session["debateType"] = '5999644a37335cad52ecd861'
            if "5999644a37335cad52ecd861" not in session["debates"].keys():
                session["debates"][str("5999644a37335cad52ecd861")] = ""
            return session
        if "CALLING ATTENTION" in line:
            session["debateType"] = '5999646837335cad52ecd865'
            session["debates"][str("5999646837335cad52ecd865")] = ""
            return session
        if "THE BUDGET (RAILWAYS)-2016-17" in line or "THE BUDGET (RAILWAYS)" in line or "BUDGET (RAILWAYS) 2015-2016" in line:
            session["debateType"] = '5999644a37335cad52ecd861'
            if "5999644a37335cad52ecd861" not in session["debates"].keys():
                session["debates"][str("5999644a37335cad52ecd861")] = ""
            return session
        if "BUDGET (GENERAL) - 2016-2017" in line or "GENERAL BUDGET - 2016-2017" in line:
            session["debateType"] = '5999644a37335cad52ecd861'
            if "5999644a37335cad52ecd861" not in session["debates"].keys():
                session["debates"][str("5999644a37335cad52ecd861")] = ""
            return session
        if "BUDGET (GENERAL), 2016-2017" in line:
            session["debateType"] = '5999644a37335cad52ecd861'
            if "5999644a37335cad52ecd861" not in session["debates"].keys():
                session["debates"][str("5999644a37335cad52ecd861")] = ""
            return session
        if "DEMANDS FOR EXCESS GRANTS" in line:
            session["debateType"] = '5999644a37335cad52ecd861'
            if "5999644a37335cad52ecd861" not in session["debates"].keys():
                session["debates"][str("5999644a37335cad52ecd861")] = ""
            return session
        if "BUDGET (GENERAL), 2015-2016-- GENERAL DISCUSSION" in line or "BUDGET (GENERAL)" in line:
            session["debateType"] = '5999644a37335cad52ecd861'
            if "5999644a37335cad52ecd861" not in session["debates"].keys():
                session["debates"][str("5999644a37335cad52ecd861")] = ""
            return session
        if "NATIONAL CAPITAL TERRITORY OF DELHI" in line:
            session["debateType"] = '5999644a37335cad52ecd861'
            if "5999644a37335cad52ecd861" not in session["debates"].keys():
                session["debates"][str("5999644a37335cad52ecd861")] = ""
            return session
        if "SUPPLEMENTARY DEMANDS FOR GRANTS" in line:
            session["debateType"] = '5999644a37335cad52ecd861'
            if "5999644a37335cad52ecd861" not in session["debates"].keys():
                session["debates"][str("5999644a37335cad52ecd861")] = ""
            return session
        if "DEMANDS FOR SUPPLEMENTARY GRANTS" in line:
            session["debateType"] = '5999644a37335cad52ecd861'
            if "5999644a37335cad52ecd861" not in session["debates"].keys():
                session["debates"][str("5999644a37335cad52ecd861")] = ""    
            return session
        if "THE FINANCE BILL" in line:
            session["debateType"] = '5999649f37335cad52ecd86b'
            if "5999649f37335cad52ecd86b" not in session["debates"].keys():
                session["debates"][str("5999649f37335cad52ecd86b")] = ""
            return session
        if "UNION BUDGET" in line:
            session["debateType"] = '5999644a37335cad52ecd861'
            if "5999644a37335cad52ecd861" not in session["debates"].keys():
                session["debates"][str("5999644a37335cad52ecd861")] = ""
            return session
        if "HALF-AN-HOUR DISCUSSION" in line:
            session["debateType"] = '59dce640a7401a6088699006'
            session["debates"][str("59dce640a7401a6088699006")] = ""
            return session
        if "DISCUSSION ON COMMITMENT TO INDIA'S CONSTITUTION AS" in line:
            session["debateType"] = '59dce640a7401a6088699006'
            session["debates"][str("59dce640a7401a6088699006")] = ""
            return session
        if "PRIVATE MEMBER'S RESOLUTION" in line:
            session["debateType"] = '5999659437335cad52ecd883'
            if "5999644a37335cad52ecd861" not in session["debates"].keys():
                session["debates"][str("5999659437335cad52ecd883")] = ""
            return session
        for index,dtype in enumerate(debateTypes):
            line =  preprocess.debateTypePreprocess(line)
            value = utils.getSimilarity(line,dtype)
            if value >= 0.8:
                pos = file.tell()
                session['debateType'] = originalDebateTypes[index]
                if str(originalDebateTypes[index]) not in session["debates"].keys():
                    session["debates"][str(originalDebateTypes[index])] = OrderedDict()
                found = True
            if found:
                break
        if "RESOLUTION" in resLine:
            session["debateType"] = '599965fa37335cad52ecd88f'
            if "599965fa37335cad52ecd88f" not in session["debates"].keys():
                session["debates"][str("599965fa37335cad52ecd88f")] = OrderedDict()
            return session
        if found:
            break
    file.seek(pos)
    return session

def populateDebateData(file, session):
    if "billId" in session:
        session["debateType"] = '5999649f37335cad52ecd86b'
        print "Debate Type: " + "Government Bills" + "\n"
        return debateTypePopulate.parseGovernmentBills(file,session)
    elif str(session["debateType"]) == '5999652b37335cad52ecd879':
        print "Debate Type: " + "Obituary Reference" + "\n"
        return debateTypePopulate.parseObituaryReference(file, session)
    elif str(session["debateType"]) == '599964df37335cad52ecd872':
        print "Debate Type: " + "M377" + "\n"
        return debateTypePopulate.parseMatterUnderThreeSevenSeven(file, session)
    elif str(session["debateType"]) == '5999644a37335cad52ecd861':
        print "Debate Type: " + "General" + "\n"
        return debateTypePopulate.parseGeneral(file,session)
    elif str(session["debateType"]) == '5999645137335cad52ecd862':
        print "Debate Type: " + "Budget Railways" + "\n"
        return debateTypePopulate.parseGeneral(file,session)
    elif str(session["debateType"]) == '599965d837335cad52ecd88b':
        print "Debate Type: " + "Minister Statement" + "\n"
        return debateTypePopulate.parseMinisterStatement(file,session)
    elif str(session["debateType"]) == '5999660437335cad52ecd890':
        print "Debate Type: " + "Submission Members" + "\n"
        return debateTypePopulate.parseSubmissionMembers(file,session)
    elif str(session["debateType"]) == '5999649f37335cad52ecd86b':
        print "Debate Type: " + "Government Bills" + "\n"
        return debateTypePopulate.parseGovernmentBills(file,session)
    elif str(session["debateType"]) == '599965fa37335cad52ecd88f':
        print "Debate Type: " + "Statutory Resolutions" + "\n"
        return debateTypePopulate.parseStatutoryResolutions(file,session)
    elif str(session["debateType"]) == '59d0d7f12589e39d8102872e':
        print "Debate Type: " + "Private Members Bill" + "\n"
        return debateTypePopulate.parsePrivateMemberBill(file,session)
    elif str(session["debateType"]) == '599964cc37335cad52ecd870':
        print "Debate Type: " + "Introduction to Parliamentary Delegates" + "\n"
        return debateTypePopulate.parseParliamentaryDelegates(file,session)
    elif str(session["debateType"]) == '599965ab37335cad52ecd885':
        print "Debate Type: " + "References" + "\n"
        return debateTypePopulate.parseReferences(file,session)
    elif str(session["debateType"]) == '5999649837335cad52ecd86a':
        print "Debate Type: " + "Felicitions" + "\n"
        return debateTypePopulate.parseFelicitations(file,session)
    elif str(session["debateType"]) == '5999659437335cad52ecd883':
        print "Debate Type: " + "Private Member Resolutions" + "\n"
        return debateTypePopulate.parsePrivateMemberResolution(file,session)
    elif str(session["debateType"]) == '5999646837335cad52ecd865':
        print "Debate Type: " + "Calling Attention" + "\n"
        return debateTypePopulate.parseCallingAttention(file,session)
    elif str(session["debateType"]) == '5999642537335cad52ecd85d':
        print "Debate Type: " + "ADDRESS BY THE CHAIR (RULE - 360)" + "\n"
        return debateTypePopulate.parseChairAddress(file,session)
    elif str(session["debateType"]) == '5999661737335cad52ecd892':
        print "Debate Type: " + "References" + "\n"
        return debateTypePopulate.parseReferences(file,session)
    elif str(session["debateType"]) == '59dcb3aaa7401a6088698ffe':
        print "Debate Type: " + "Observation by Speaker" + "\n"
        return debateTypePopulate.parseSpeakerObservation(file,session)
    elif str(session["debateType"]) == '599965c237335cad52ecd888':
        print "Debate Type: " + "Ruling by Speaker" + "\n"
        return debateTypePopulate.parseSpeakerRuling(file,session)
    elif str(session["debateType"]) == '5999652437335cad52ecd878':
        print "Debate Type: " + "Oath or Affirmation" + "\n"
        return debateTypePopulate.parseOathAffirmation(file,session)
    elif str(session["debateType"]) == '59dcb8ffa7401a6088699002':
        print "Debate Type: " + "Announcement by Speaker" + "\n"
        return debateTypePopulate.parseSpeakerAnnouncement(file,session)
    elif str(session["debateType"]) == '59dce640a7401a6088699006':
        print "Debate Type: " + "Discussion under Rule 193" + "\n"
        return debateTypePopulate.parseDiscussion(file,session)
    elif str(session["debateType"]) == '59dde43f101e0cd625d8bbcd':
        print "Debate Type: " + "Personal Explanation by a Member under Rule 357" + "\n"
        return debateTypePopulate.parsePersonalExplanation(file,session)
    elif str(session["debateType"]) == '59de0a96c0a9b7b482106cb9':
        print "Debate Type: " + "Suspension of members" + "\n"
        return debateTypePopulate.parseSuspensionMembers(file,session)
    elif str(session["debateType"]) == '59de7e808363ad7bd6d9b762':
        print "Debate Type: " + "Motion" + "\n"
        return debateTypePopulate.parseMotion(file,session)
    elif str(session["debateType"]) == '5999650a37335cad52ecd876':
        print "Debate Type: " + "Motion of Thanks to President's Address" + "\n"
        return debateTypePopulate.parsePresidentThanks(file,session)
    elif str(session["debateType"]) == '5999643037335cad52ecd85e':
        print "Debate Type: " + "Discussion under Rule 193" + "\n"
        return debateTypePopulate.parseDiscussion(file,session)
    elif str(session["debateType"]) == '5999653b37335cad52ecd87b':
        print "Debate Type: " + "Observation of Silence" + "\n"
        return debateTypePopulate.parseDiscussion(file,session)

def getSecretaryGeneralName(file,session):
    print file.readline()
    print file.readline()
    print file.readline()
    print file.readline()

def getattributes(file,session):
    session = getHouseName(file, session)
    session = getDocumentType(file, session)
    session = getDates(file, session)
    session["debates"] = {}
    while True:
        session = getDebateType(file, session)
        if "2014-07-31" in session["file"] or "2014-07-30" in session["file"] or "2014-08-11" in session["file"] or "2014-08-07" in session["file"] or "2014-08-05" in session["file"] or "2014-08-06" in session["file"] or "2014-11-25" in session["file"] or "2015-04-22" in session["file"] or "2015-04-20" in session["file"] or "2015-08-11" in session["file"] or "2015-05-11" in session["file"] or "2016-05-11" in session["file"] or "2015-12-03" in session["file"] or "2015-08-03" in session["file"] or "2015-08-06" in session["file"]:
            print session["debateType"]
            if str(session["debateType"]) == '599964df37335cad52ecd872':
                session.pop('debateType', None)
                session["debates"].pop(str('599964df37335cad52ecd872'))
                #print session
                print "BROKE"
                continue
        session = populateDebateData(file, session)
        if "secretaryGeneralName" in session.keys():
            break
    #session = getSecretaryGeneralName(file, session)
    # Remove debatetype
    mongoOps.insertDocument("synopsis", "sessions", session)

def iterateFiles():
    path="./files/*"
    #files = ['./files/2017-08-02','./files/03-08-2017','./files/04-08-2017','./files/08-08-2017','./files/09-08-2017','./files/10-08-2017','./files/11-08-2017']
    #files = ['./files/2017-03-15']
    for file in glob.glob(path):
        if "2016-03-01" in file:
            continue
        if "2017" in file or "2016" in file or "2015" in file: 
    #for file in files:
            session = {}
            print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
            print "File : " + file
            session["file"] = file
            f = open(file,'r')
            getattributes(f, session)

def files():
    synopsis = { house : {} }
    synopsis[house]["data"] = {}
    for filename in os.listdir("./files/"):
        open_file(filename,synopsis)
	break

def open_file(filename,synopsis):
    f = open('./files/'+filename,'r')
    synopsis[house]["data"][filename] = {}
    date = f.readline()
    synopsis[house]["data"][filename]["date"] = date
    f.readline()
    debate_type = f.readline()
    debate_type = debate_type.strip()
    while debate_type not in debate_types:
        debate_type = f.readline()
	debate_type = debate_type.strip()
    synopsis[house]["data"][filename]["debate_type"] = debate_type
    if debate_type in submissions_by_members:
        check = f.readline()
	while "Re" not in check:
	    check = f.readline()
        check = f.readline()
        while check == '\n' or check == '':
    	    check = f.readline()
        synopsis[house]["data"][filename]["data"] = {}
	synopsis[house]["data"][filename]["data"]["reply_topic"] = check

if __name__ == "__main__":
    iterateFiles()
