#/usr/bin/env python

from pymongo import MongoClient
from bs4 import BeautifulSoup
import mongoOps
import constants
import requests
import urllib
import re
import os
from datetime import datetime
import dateutil.parser as dparser

def fetchAllFiles():
	# For possible years
	table = mongoOps.getTable('synopsis','years')
	years = []
	for document in table.find():
		years.append(int(document['year']))
	for year in years:
		print "For Year : " + str(year) + "\n"
		# For directories for each year
		page = requests.get(constants.LOKSABHA_SYNOPSIS_URL + '/' + str(year)).text
		soup = BeautifulSoup(page, 'html.parser')
		sessions = []
		for node in soup.find_all('a')[1:]:
			sessions.append(node.string)
	 	for session in sessions:
	 		print "For Session : " + str(session) + "\n"
		 	# For directories for each session
		 	page = requests.get(constants.LOKSABHA_SYNOPSIS_URL + '/' + str(year) + '/' + str(session)).text
			soup = BeautifulSoup(page, 'html.parser')
			files = []
			dates = set([])
			for node in soup.find_all('a')[1:]:
				files.append(node['href'].split("/")[-1])
				file_url = constants.LOKSABHA_BASE_URL + '/' + node['href']
				match = re.search(r'\d{2}-\d{2}-\d{4}', node.string)
				match1 = re.search(r'\d{2}-\d{2}-\d{2}', node.string)
				if "2Supp+Supp+Synopsis-15-03-2017" in node.string:
					continue
				if match:
					print "Node String : " + node.string
					date = datetime.strptime(match.group(), '%d-%m-%Y').date()
					if date not in dates:
						dates.add(date)
						cmd = "wget -O {0} '{1}'".format(date,file_url)
						os.system(cmd)
						dest = "./files/" + str(date)
						cmd = "pdf2txt.py {0} > {1}".format(date,dest)
						#cmd = "pdftotext {0} {1}".format(date,dest)
						os.system(cmd)
						cmd = "sed 's/\o14//g' {0} >> {1}".format(dest,"temp")
						os.system(cmd)
						cmd = "mv {0} {1}".format("temp",dest)
						os.system(cmd)
						cmd = "rm ./{0}".format(date)
						os.system(cmd)
				elif match1:
					print "Node String : " + node.string
					date = datetime.strptime(match1.group(), '%d-%m-%y').date()
					if date not in dates:
						dates.add(date)
						cmd = "wget -O {0} {1}".format(date,file_url)
						os.system(cmd)
						dest = "./files/" + str(date)
						cmd = "pdf2txt.py {0} > {1}".format(date,dest)
						#cmd = "pdftotext {0} {1}".format(date,dest)
						os.system(cmd)
						cmd = "sed 's/\o14//g' {0} >> {1}".format(dest,"temp")
						os.system(cmd)
						cmd = "mv {0} {1}".format("temp",dest)
						os.system(cmd)
						cmd = "rm ./{0}".format(date)
						os.system(cmd)

if __name__ == "__main__":
	fetchAllFiles()
