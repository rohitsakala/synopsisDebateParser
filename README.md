# Parliamentary Debate Parser

The project aims to create a parser for the Parliamentary debates wherein final result will be filling entities, attributes and relationships. Only synopsis is being scrapped as of now.

Contact me if anyone interested

##Progress

Debate Type - Submissions by Members scrapping is done as of now.

Other 54 debate types need to be scrapped.

### Note :- Under development

### Contact :- rohitsakala@gmail.com

## Information to be stored

* Synopsis
* Member Attendances
* Party Names

## Manual Work

* Create synopsis database
* Create years table in it and populate it
* Create debateTypes table in it and populate it
* Create secretaryGenerals table and populate it
* Create ministries table and populate it
* Create bills table and populate it
* 736 line number in 2015-05-05

## TODO

* Automate extraction of members list from http://164.100.47.194/Loksabha/Members/AlphabeticalList.aspx and other related information about members
* Generic classes for 57 debate types
* GetdebateType - exception cases too long then handle
* Automate extraction of ministers and and their ministries
* Union Budget - 16-03-2017 -  Add Sub title parsing
* Parse members in tables like in oath or affirmation etc
* Need to do Resignation of members and oath of members ?
* Need to scrape according to size of the files
* Need to parse D377 in another manner.
* Need to scrape Question and Answers

## Points to Remember

* Statuory Resolutions are also like debates
* Matter under rtull 377 before 2016 May are having different structures

## Tweaks

None till now
