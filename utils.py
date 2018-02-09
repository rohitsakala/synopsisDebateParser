# /usr/bin/env python

import difflib
import mongoOps
import sys
import json
import utils
import preprocess

reload(sys)
sys.setdefaultencoding('utf8')

def getSimilarity(a, b):
    return difflib.SequenceMatcher(None, a, b).ratio()

def startDebate(line):
    if line.find(":") >= 0:
        return True
    else:
        return False

def endDebate(line,session):
    # Debate is always in Upper Characters
    temp = line
    table = mongoOps.getTable('synopsis','secretaryGenerals')
    for general in table.find():
        if line.find(general["name"]) >= 0:
            session["secretaryGeneralName"] = general["name"]
            return True
    table = mongoOps.getTable('synopsis','debateTypes')
    debateTypes = []
    billId = getBillMatch(line)
    if billId != None:
        session["billId"] = billId
        return True
    for debateType in table.find():
        dtype = preprocess.debateTypePreprocess(debateType['type'])
        debateTypes.append(dtype)
    for index,dtype in enumerate(debateTypes):
        line =  preprocess.debateTypePreprocess(line)
        value = utils.getSimilarity(line,dtype)
        if value >= 0.8:
            if dtype == "governmentbills":
                if value >= 0.9:
                    return True
            else:
                if preprocess.debateTypeSpecialPreprocess(temp).isupper():
                    return True
    table = mongoOps.getTable('synopsis','endDebateConnectives')
    for connective in table.find():
        line =  preprocess.debateTypePreprocess(line)
        dtype = preprocess.debateTypePreprocess(connective["name"])
        value = utils.getSimilarity(line,dtype)
        if value >= 0.8:
            return True
    ####### Special Cases ########
    if "FELICITAITON BY THE SPEAKER" in temp or "FELICITATION BY SPEAKER" in temp or "FELICITATIONS BY SPEAKER" in temp or "MOTION OF THANKS ON THE" in temp or "DISCUSSION UNDER RULE 193" in temp or "PRIVATE MEMBERS' BILLS" in temp or "OATH BY MEMBERS" in temp or "ADDRESS BY THE SPEAKER" in temp or "WELCOME TO PARLIAMENTARY DELEGATION" in temp or  "WELCOME TO THE PARLIAMENTARY DELEGATION" in temp or "REFERENCE BY THE SPEAKER" in temp or "UNION BUDGET" in temp or \
        "FELICITATIONS BY THE SPEAKER" in temp or "FELICITATION BY THE SPEAKER" in temp or "REFERENCE BY SPEAKER" in temp:
        print "srgvsdfgvas"
        return True
    if "NATIONAL CAPITAL TERRITORY OF DELHI" in temp or "RESOLUTION" in temp  or "SUSPENSION OF MEMBERS" in temp or "UNION BUDGET" in temp or "CALLING ATTENTION" in temp:
        if preprocess.debateTypeSpecialPreprocess(temp).isupper():
            return True
    return False

def seenMinisterTag(line):
    table = mongoOps.getTable('synopsis','ministries')
    for mini in table.find():
        if mini["name"] in line:
            return True
    return False

def seenMemberName(line):
    if "laid" in line:
        memberName = line.split("laid")[0]
        maxIndex = getMemberId(memberName)
        return True
    if ":" in line or "responding" in line:
        memberName = line[line.find("(")+1:line.find(")")]
        maxIndex = getMemberId(memberName)
        if maxIndex is None:
            return False
        return True
    return False

def getMemberId(data):
    table = mongoOps.getTable('synopsis','members')
    maxValue = 0
    maxIndex = 0
    for mem in table.find():
        value = getSimilarity(preprocess.memberNamePreprocess(mem["name"]),preprocess.memberNamePreprocess(preprocess.getUpperCharacters(data)))
        if maxValue < value:
            maxValue = value
            maxIndex = mem["_id"]
    if maxValue > 0.8:
        return maxIndex
    else:
        return None

def fetchMemberName(file,session):
    while True:
        pos = file.tell()
        line = file.readline()
        if "laid" in line:
            memberName = line.split("laid")[0]
            maxIndex = getMemberId(memberName)
            file.seek(pos)
            return maxIndex
        if ":" in line or "responding" in line or "MINISTER" in line:
            memberName = line[line.find("(")+1:line.find(")")]
            maxIndex = getMemberId(memberName)
            file.seek(pos)
            return maxIndex


def findBlockMap(file,session,mattersMap):
    table = mongoOps.getTable('synopsis','members')
    session["endDebate"] = False
    while True:
        pos = file.tell()
        line = file.readline()
        maxValue = 0
        maxIndex = 0
        for mem in table.find():
            value = getSimilarity(preprocess.memberNamePreprocess(mem["name"]),preprocess.memberNamePreprocess(preprocess.getUpperCharacters(line)))
            if maxValue < value:
                maxValue = value
                maxIndex = mem["_id"]
        if maxValue > 0.7:
            mattersMap[str(maxIndex)] = getBlockText(file,session)
        if "secretaryGeneralName" in session:
            return mattersMap
        if session["endDebate"]:
            return mattersMap

def getDebateText(file,session):
    while True:
        line = file.readline()
        text = ""
        if startDebate(line):
            text += line.split(":")[1]
            while True:
                pos = file.tell()
                line = file.readline()
                ##print line
                if endDebate(line,session):
                    file.seek(pos)
                    return text
                else:
                    text += line

########################  Used by SubmissionMembers ########################

def fetchMemberName(file,session):
    while True:
        pos = file.tell()
        line = file.readline()
        if "laid" in line:
            memberName = line.split("laid")[0]
            maxIndex = getMemberId(memberName)
            file.seek(pos)
            return maxIndex
        if ":" in line or "responding" in line or "MINISTER" in line:
            memberName = line[line.find("(")+1:line.find(")")]
            maxIndex = getMemberId(memberName)
            file.seek(pos)
            return maxIndex

def getBlockText(file,session):
    line = file.readline()
    text=""
    if ":" in line:
        text = line.split(":")[1]
    elif "responding" in line:
        text = line.split("responding")[1]
    if "laid" in line:
        text = line.split("laid")[1]
    while True:
        pos = file.tell()
        line = file.readline()
        if seenMinisterTag(line):
            file.seek(pos)
            return text
        if seenMemberName(line):
            file.seek(pos)
            return text
        if endDebate(line,session):
            file.seek(pos)
            session["endDebate"] = True
            return text
        text += line



def findBlockMapSemi(file,session,mattersMap):
    table = mongoOps.getTable('synopsis','members')
    while True:
        line = file.readline()
        text = ""
        if startDebate(line):
            name = line.split(":")[0]
            maxIndex = getMemberId(name)
            text = line.split(":")[1]
            pos= ''
            while True:
                pos = file.tell()
                line = file.readline()
                if startDebate(line):
                    name = line.split(":")[0]
                    maxIndex = getMemberId(name)
                    if maxIndex != None:
                        break
                text += line
                if endDebate(line,session):
                    return mattersMap
            mattersMap[str(maxIndex)] = text
            file.seek(pos)

def getMinisterText(file,session):
    while True:
        line = file.readline()
        text = ""
        if startDebateMinister(line):
            if line.find(":") >= 0:
                text += line.split(":")[1]
            elif line.find(")") >= 0:
                text += line.split(")")[1]
            while True:
                pos = file.tell()
                line = file.readline()
                if endDebate(line,session):
                    file.seek(pos)
                    return text
                else:
                    text += line

## Identifying Bills

def getBillMatch(line):
    table = mongoOps.getTable('synopsis','bills')
    if "Contd" in line:
        line = line.replace("Contd","")
    if "contd" in line:
        line = line.replace("contd","")
    if "CONTD" in line:
        line = line.replace("CONTD","")
    if not preprocess.debateTypeSpecialPreprocess(line).isupper():
        return None
    line = preprocess.billPreprocess(line)
    found = False
    for bill in table.find():
        billPre = preprocess.billPreprocess(bill["name"])
        value = utils.getSimilarity(line,billPre)
        #print "BillPre " + str(billPre)
        #print "Line " + str(line)
        if value > 0.5:
            if line in billPre or billPre in line:
                return bill["_id"]
                break
    return None
