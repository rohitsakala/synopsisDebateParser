# /usr/bin/env python

from models import MatterUnderThreeSevenSeven
from models import ObituaryReference
from models import General
from models import GovernmentBills
from models import MinisterStatement
from models import SubmissionMembers
from models import PrivateMemberBill
from models import StatutoryResolutions
from models import ParliamentaryDelegates
from models import References
from models import Felicitations
from models import PrivateMemberResolution
from models import CallingAttention
from models import ChairAddress
from models import SpeakerObservation
from models import SpeakerRuling
from models import OathAffirmation
from models import SpeakerAnnouncement
from models import Discussion
from models import PersonalExplanation
from models import SuspensionMembers
from models import Motion
from models import PresidentThanks
from models import ObservationSilence

from collections import OrderedDict
import utils
import mongoOps
import sys
import json

def parseObituaryReference(file, session): #Lite
    obituaryDebateInstance = ObituaryReference.ObituaryReference(utils.getDebateText(file,session))
    data = obituaryDebateInstance.getDict()
    print json.dumps(data,indent=4)
    session["debates"][str(session["debateType"])] = mongoOps.insertDocument("synopsis","debates", data)
    #print session
    return session

def parseMatterUnderThreeSevenSeven(file, session): #Lite
    matterUnderThreeSevenSeven = MatterUnderThreeSevenSeven.MatterUnderThreeSevenSeven()
    session["debates"][str(session["debateType"])] = mongoOps.insertDocument("synopsis","debates", matterUnderThreeSevenSeven.getMapData(file,session))
    return session

def parseGeneral(file,session):
    general = General.General()
    if "debates" in session.keys():
        debates = session["debates"]
        if "5999644a37335cad52ecd861" in debates.keys():
            if debates["5999644a37335cad52ecd861"]:
                length = len(session["debates"][str(session["debateType"])])
                session["debates"][str(session["debateType"])][str(length)] = mongoOps.insertDocument("synopsis","debates", general.getMapData(file,session))
            else:
                session["debates"][str(session["debateType"])] = OrderedDict()
                session["debates"][str(session["debateType"])]["0"] = mongoOps.insertDocument("synopsis","debates", general.getMapData(file,session)) 
        if "5999645137335cad52ecd862" in debates.keys():
            if debates["5999645137335cad52ecd862"]:
                length = len(session["debates"][str(session["debateType"])])
                session["debates"][str(session["debateType"])][str(length)] = mongoOps.insertDocument("synopsis","debates", general.getMapData(file,session))
            else:
                session["debates"][str(session["debateType"])] = OrderedDict()
                session["debates"][str(session["debateType"])]["0"] = mongoOps.insertDocument("synopsis","debates", general.getMapData(file,session))
    return session

def parseChairAddress(file,session):       #Lite
    chairAddress = ChairAddress.ChairAddress()
    session["debates"][str(session["debateType"])] = mongoOps.insertDocument("synopsis","debates", chairAddress.getData(file,session))
    return session

def parseGovernmentBills(file,session):
    governmentBills = GovernmentBills.GovernmentBills()
    if "debates" in session.keys():
        debates = session["debates"]
        if debates["5999649f37335cad52ecd86b"]:
            billid = session["billId"]
            session.pop("billId",None)
            length = len(session["debates"][str(session["debateType"])])
            session["debates"][str(session["debateType"])][str(length)] = OrderedDict()
            session["debates"][str(session["debateType"])][str(length)]["billId"] = str(billid)
            session["debates"][str(session["debateType"])][str(length)]["bill"] = mongoOps.insertDocument("synopsis","debates", governmentBills.getMapData(file,session))
        else:
            billid = session["billId"]
            session.pop("billId",None)
            session["debates"][str(session["debateType"])] = OrderedDict()
            session["debates"][str(session["debateType"])]["0"] = OrderedDict()
            session["debates"][str(session["debateType"])]["0"]["billId"] = str(billid)
            session["debates"][str(session["debateType"])]["0"]["bill"] = mongoOps.insertDocument("synopsis","debates", governmentBills.getMapData(file,session)) 
    return session
    #print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    #print session["billId"]
    #print mongoOps.getDocument("synopsis","bills",session["billId"])
    #print "-------------------------------------------------------"
    #session["debates"][str(session["billId"])] = mongoOps.insertDocument("synopsis","debates", governmentBills.getMapData(file,session))
    #session["billId"] = session["billId_e"]
    #print "------------------------------------------------------"
    #print mongoOps.getDocument("synopsis","bills",session["billId"])
    #return session

def parsePresidentThanks(file,session):  #Lite
	presidentThanks = PresidentThanks.PresidentThanks()
	session["debates"][str(session["debateType"])] = mongoOps.insertDocument("synopsis","debates", presidentThanks.getMapData(file,session))
	return session

def parsePrivateMemberBill(file,session):
    privateMemberBill = PrivateMemberBill.PrivateMemberBill()
    if "debates" in session.keys():
        debates = session["debates"]
        if debates["59d0d7f12589e39d8102872e"]:
            length = len(session["debates"][str(session["debateType"])])
            session["debates"][str(session["debateType"])][str(length)] = mongoOps.insertDocument("synopsis","debates", privateMemberBill.getMapData(file,session))
        else:
            session["debates"][str(session["debateType"])] = OrderedDict()
            session["debates"][str(session["debateType"])]["0"] = mongoOps.insertDocument("synopsis","debates", privateMemberBill.getMapData(file,session)) 
	return session

def parseMinisterStatement(file,session):  # Lite
    ministerStatement = MinisterStatement.MinisterStatement()
    if "debates" in session.keys():
        debates = session["debates"]
        if debates["599965d837335cad52ecd88b"]:
            length = len(session["debates"][str(session["debateType"])])
            session["debates"][str(session["debateType"])][str(length)] = mongoOps.insertDocument("synopsis","debates", ministerStatement.getData(file,session))
        else:
            session["debates"][str(session["debateType"])] = OrderedDict()
            session["debates"][str(session["debateType"])]["0"] = mongoOps.insertDocument("synopsis","debates", ministerStatement.getData(file,session))
    return session

def parseParliamentaryDelegates(file,session): #Lite
    parliamentaryDelegates = ParliamentaryDelegates.ParliamentaryDelegates()
    session["debates"][str(session["debateType"])] = mongoOps.insertDocument("synopsis","debates", parliamentaryDelegates.getData(file,session))
    return session

def parseReferences(file,session):  #Lite
    references = References.References()
    session["debates"][str(session["debateType"])] = mongoOps.insertDocument("synopsis","debates", references.getData(file,session))
    return session

def parseOathAffirmation(file,session):  #Lite
    oathAffirmation = OathAffirmation.OathAffirmation()
    session["debates"][str(session["debateType"])] = mongoOps.insertDocument("synopsis","debates", oathAffirmation.getData(file,session))
    return session

def parseSpeakerRuling(file,session):  #Lite
    speakerRuling = SpeakerRuling.SpeakerRuling()
    session["debates"][str(session["debateType"])] = mongoOps.insertDocument("synopsis","debates", speakerRuling.getData(file,session))
    return session

def parseSuspensionMembers(file,session):  #Lite
    suspensionMembers = SuspensionMembers.SuspensionMembers()
    session["debates"][str(session["debateType"])] = mongoOps.insertDocument("synopsis","debates", suspensionMembers.getData(file,session))
    return session

def parseSpeakerAnnouncement(file,session): #Lite
    speakerAnnouncement = SpeakerAnnouncement.SpeakerAnnouncement()
    session["debates"][str(session["debateType"])] = mongoOps.insertDocument("synopsis","debates", speakerAnnouncement.getData(file,session))
    return session

def parseObervationSilence(file,session): #Lite
    observationSilence = ObservationSilence.ObservationSilence()
    session["debates"][str(session["debateType"])] = mongoOps.insertDocument("synopsis","debates", observationSilence.getData(file,session))
    return session

def parsePersonalExplanation(file,session): #Lite
    personalExplanation = PersonalExplanation.PersonalExplanation()
    session["debates"][str(session["debateType"])] = mongoOps.insertDocument("synopsis","debates", personalExplanation.getData(file,session))
    return session

def parseSpeakerObservation(file,session): #Lite
    speakerObservation = SpeakerObservation.SpeakerObservation()
    session["debates"][str(session["debateType"])] = mongoOps.insertDocument("synopsis","debates", speakerObservation.getData(file,session))
    return session

def parseFelicitations(file,session): #Lite
    felicitations = Felicitations.Felicitations()
    session["debates"][str(session["debateType"])] = mongoOps.insertDocument("synopsis","debates", felicitations.getData(file,session))
    return session

def parsePrivateMemberResolution(file,session):
    privateMemberResolution = PrivateMemberResolution.PrivateMemberResolution()
    if "debates" in session.keys():
        debates = session["debates"]
        if debates["5999659437335cad52ecd883"]:
            length = len(session["debates"][str(session["debateType"])])
            session["debates"][str(session["debateType"])][str(length)] = mongoOps.insertDocument("synopsis","debates", privateMemberResolution.getData(file,session))
        else:
            session["debates"][str(session["debateType"])] = OrderedDict()
            session["debates"][str(session["debateType"])]["0"] = mongoOps.insertDocument("synopsis","debates", privateMemberResolution.getData(file,session))
    return session

def parseSubmissionMembers(file,session):
    submissionMembers = SubmissionMembers.SubmissionMembers()
    if "debates" in session.keys():
        debates = session["debates"]
        if debates["5999660437335cad52ecd890"]:
            length = len(session["debates"][str(session["debateType"])])
            session["debates"][str(session["debateType"])][str(length)] = mongoOps.insertDocument("synopsis","debates", submissionMembers.getData(file,session))
        else:
            session["debates"][str(session["debateType"])] = OrderedDict()
            session["debates"][str(session["debateType"])]["0"] = mongoOps.insertDocument("synopsis","debates", submissionMembers.getData(file,session))
    return session

def parseMotion(file,session): #Lite
    motion = Motion.Motion()
    session["debates"][str(session["debateType"])] = mongoOps.insertDocument("synopsis","debates", motion.getData(file,session))
    return session

def parseDiscussion(file,session):
    discussion = Discussion.Discussion()
    session["debates"][str(session["debateType"])] = mongoOps.insertDocument("synopsis","debates", discussion.getData(file,session))
    return session

def parseCallingAttention(file,session):
    callingAttention = CallingAttention.CallingAttention()
    session["debates"][str(session["debateType"])] = mongoOps.insertDocument("synopsis","debates", callingAttention.getData(file,session))
    return session

def parseStatutoryResolutions(file,session):
    statutoryResolutions = StatutoryResolutions.StatutoryResolutions()
    if "debates" in session.keys():
        debates = session["debates"]
        if debates["599965fa37335cad52ecd88f"]:
            length = len(session["debates"][str(session["debateType"])])
            session["debates"][str(session["debateType"])][str(length)] = mongoOps.insertDocument("synopsis","debates", statutoryResolutions.getData(file,session))
        else:
            session["debates"][str(session["debateType"])] = OrderedDict()
            session["debates"][str(session["debateType"])]["0"] = mongoOps.insertDocument("synopsis","debates", statutoryResolutions.getData(file,session)) 
    return session
