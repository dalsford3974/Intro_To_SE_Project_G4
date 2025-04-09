from sqlalchemy import Column, Integer, String, Time, ForeignKey
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Numeric
from flask_login import UserMixin

db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    userID = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    address = Column(String(50), nullable=False)
    city = Column(String(50), nullable=False)
    state = Column(String(50), nullable=False)
    zipCode = Column(String(50), nullable=False)
    isAdmin = Column(Integer, nullable=False)

    def get_id(self):
        return str(self.userID)

class Inventory(db.Model):
    __tablename__ = 'inventory'
    itemID = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    sellerID = Column(Integer, ForeignKey('users.userID'), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, nullable=False)


class Cart(db.Model):
    __tablename__ = 'cart'
    cartID = Column(Integer, primary_key=True)
    userID = Column(Integer, ForeignKey('users.userID'), nullable=False)
    itemID = Column(Integer, ForeignKey('inventory.itemID'), nullable=False)
    quantity = Column(Integer, nullable=False)


class Orders(db.Model):
    __tablename__ = 'orders'
    orderID = Column(Integer, primary_key=True)
    userID = Column(Integer, ForeignKey('users.userID'), nullable=False)
    itemNumber = Column(Integer, nullable=False)
    cost = Column(Numeric(10, 2), nullable=False)
    date = Column(String, nullable=False)


class OrderItems(db.Model):
    __tablename__ = 'orderitems'
    historyID = Column(Integer, primary_key=True)
    orderID = Column(Integer, ForeignKey('orders.orderID'), nullable=False)
    itemID = Column(Integer, ForeignKey('inventory.itemID'), nullable=False)
    quantity = Column(Integer, nullable=False)
