from sqlalchemy import Column, Integer, String, Time, ForeignKey
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users' 
    userID = Column(Integer, primary_key=True)
    firstName = Column(String(50), nullable=False)
    lastName = Column(String(50), nullable=False)
    address = Column(String(50), nullable=False)
    city = Column(String(50), nullable=False)
    state = Column(String(50), nullable=False)
    zipCode = Column(String(50), nullable=False)
    isAdmin = Column(Integer, nullable=False)
    
