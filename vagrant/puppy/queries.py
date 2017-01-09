from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Shelter, Puppy

import datetime

engine = create_engine('sqlite:///puppies.db')

Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)

session = DBSession()


def queryone():
	puppies = session.query(Puppy).order_by(Puppy.name).all()

	for puppy in puppies:
		print puppy.name

	result = session.query(Puppy.name).order_by(Puppy.name.asc()).all()
	for item in result:
		print item[0]

def querytwo():
	today = datetime.date.today()

	if passesLeapDay(today):
		sixMonthsAgo = today - datetime.timedelta(days = 183)
	else:
		sixMonthsAgo = today - datetime.timedelta(days = 182)
		result = session.query(Puppy.name, Puppy.dateOfBirth)\
		.filter(Puppy.dateOfBirth >= sixMonthsAgo)\
		.order_by(Puppy.dateOfBirth.desc())

	# print the result with puppy name and dob
	for item in result:
		print "{name}: {dob}".format(name=item[0], dob=item[1])


def querythree():
	result = session.query(Puppy.name, Puppy.weight).order_by(Puppy.weight.asc()).all()

	for item in result:
		print item[0], item[1]


def queryfour():
	result = session.query(Shelter, func.count(Puppy.id)).join(Puppy).group_by(Shelter.id).all()

	for item in result:
		print item[0].id, item[0].name, item[1]


def passesLeapDay(today):
	"""
	Returns true if most recent February 29th occured after or exactly 183 days ago (366 / 2)
	"""
	thisYear = today.timetuple()[0]
	if isLeapYear(thisYear):
		sixMonthsAgo = today - datetime.timedelta(days = 183)
		leapDay = datetime.date(thisYear, 2, 29)
		return leapDay >= sixMonthsAgo
	else:
		return False


def isLeapYear(thisYear):
	"""
	Returns true iff the current year is a leap year.
	Implemented according to logic at https://en.wikipedia.org/wiki/Leap_year#Algorithm
	"""
	if thisYear % 4 != 0:
		return False
	elif thisYear % 100 != 0:
		return True
	elif thisYear % 400 != 0:
		return False
	else:
		return True

#queryone()
#querytwo()
#querythree()
queryfour()

