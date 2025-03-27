from sqlalchemy import Column, Integer, String, Time, ForeignKey
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Numeric

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


class Inventory(db.Model):
    __tablename__ = 'inventory'
    ItemID = Column(Integer, primary_key=True)
    Title = Column(String(50), nullable=False)
    UserID = Column(Integer, ForeignKey('users.userID'), nullable=False)
    Price = Column(Numeric(10, 2), nullable=False)
    Stock = Column(Integer, nullable=False)


class Cart(db.Model):
    __tablename__ = 'cart'
    CartID = Column(Integer, primary_key=True)
    UserID = Column(Integer, ForeignKey('users.userID'), nullable=False)
    ItemID = Column(Integer, ForeignKey('inventory.ItemID'), nullable=False)
    Quantity = Column(Integer, nullable=False)


class Orders(db.Model):
    __tablename__ = 'orders'
    OrderID = Column(Integer, primary_key=True)
    UserID = Column(Integer, ForeignKey('users.userID'), nullable=False)
    ItemNumber = Column(Integer, nullable=False)
    Cost = Column(Numeric(10, 2), nullable=False)
    Date = Column(String, nullable=False)


class OrderItems(db.Model):
    __tablename__ = 'orderitems'
    HistoryID = Column(Integer, primary_key=True)
    OrderID = Column(Integer, ForeignKey('orders.OrderID'), nullable=False)
    ItemID = Column(Integer, ForeignKey('inventory.ItemID'), nullable=False)
    Quantity = Column(Integer, nullable=False)
