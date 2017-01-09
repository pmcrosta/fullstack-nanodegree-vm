import sys

from sqlalchemy import Column, ForeignKey, Integer, String, Date, Enum, Numeric

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()


class Shelter(Base):
	__tablename__ = 'shelter'
	name = Column(String(80), nullable = False)
	id = Column(Integer, primary_key=True)
	address = Column(String(150))
	city = Column(String(150))
	state = Column(String(25))
	zipCode = Column(String(10))
	website = Column(String(150))


class Puppy(Base):
	__tablename__ = 'puppy'
	name = Column(String(80), nullable = False)
	id = Column(Integer, primary_key=True)
	dateOfBirth = Column(Date())
	gender = Column(Enum('male', 'female', name='gender'), nullable=False)
	weight = Column(Numeric(10))
	picture = Column(String)
	shelter_id = Column(Integer, ForeignKey('shelter.id'))
	shelter = relationship(Shelter)

engine = create_engine('sqlite:///puppies.db')

Base.metadata.create_all(engine)