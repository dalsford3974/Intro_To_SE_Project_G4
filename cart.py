from flask import Flask, request, jsonify, session
from models import db, User
from flask_sqlalchemy import SQLAlchemy
import sys
import random
import sqlite3


class Cart:
    def __init__(self):
        databaseName = ""

    def Cart():
        pass

    def Cart(databaseName):
        #TODO
        databaseName = databaseName

    def viewCart(self, userID):
        """
        Display all books in the logged User's cart. Cooperates with the inventory 
        database to display all the correct information on the inventory items: 
        it just selectively shows the books in the users cart.
        """
        conn = sqlite3.connect('methods.db')
        cursor = conn.cursor()

        query = """
        SELECT Inventory.Title, Inventory.Author, Inventory.Price, Inventory.ISBN, Cart.Quantity
        FROM Cart
        JOIN Inventory ON Cart.ISBN = Inventory.ISBN
        WHERE Cart.UserID = ?
        """

        cursor.execute(query, (str(userID),))
        results = cursor.fetchall()

        count = 0
        for row in results:
            count = count + 1
            print(f'Item {count}:')
            print(f'Title: {row[0]}')
            print(f'Author: {row[1]}')
            print(f'Price: {row[2]}')
            print(f'ISBN: {row[3]}')
            print(f'Quantity: {row[4]}')
            print()
        return
    
    def addToCart(self, UserID, ISBN, quantity=1):
        """
        This relies on the user viewing the inventory previously from the main. Once they select a book,
        this ISBN is used to add the appropriate item and its quantity to the appropriate cart
        can have a default parameter for quantity to be 1
        """
        conn = sqlite3.connect('methods.db')
        cursor = conn.cursor()

        query = "SELECT ISBN FROM Inventory WHERE ISBN = ?"
        cursor.execute(query, (ISBN,))
        book = cursor.fetchone()

        if not book:
            print("Book not found in inventory.")
            return False

        insert_query = """
        INSERT INTO Cart (UserID, ISBN, Quantity)
        VALUES (?, ?, ?)
        """
        cursor.execute(insert_query, (UserID, book[0], quantity))
        conn.commit()

        # Check if the insert was successful
        if cursor.rowcount > 0:
            print(f"Book added to user's cart.")
            return True
        else:
            print(f"Failed to add book to user's cart.")
            return False
    
    def removeFromCart(self, UserID, ISBN):
        """
        This relies on the user viewing the cart previous - from the main. Once they select a book to remove, 
        this ISBN is used to remove an item from the user's cart. (all items)
        """
        conn = sqlite3.connect('methods.db')
        cursor = conn.cursor()

        query = "DELETE FROM Cart WHERE UserID = ? AND ISBN = ?"
        cursor.execute(query, (UserID, ISBN,))
        conn.commit()

        # Check if any rows were deleted
        if cursor.rowcount > 0:
            print(f"Book removed from user's cart.")
            return True
        else:
            print(f"No book found in user's cart.")
            return False
    
    def checkOut(self, userID, inventory, history):
        """
        User checks out.  This does the following:

            Calls the Inventory class fuction to decrease the stock of the books by the correct amount the user bought.

            Creates an order for the cart items.
                Ties into createOrder and addOrderItems from OrderHistory class
                Send over any calculations needed
            
            Removes all cart items from the cart table.
        """
        conn = sqlite3.connect('methods.db')
        cursor = conn.cursor()

        query = """
        SELECT Cart.ISBN, Cart.Quantity, Inventory.Price
        FROM Cart
        JOIN Inventory ON Cart.ISBN = Inventory.ISBN
        WHERE Cart.UserID = ?
        """
        cursor.execute(query, (userID,))
        cart_items = cursor.fetchall()

        if not cart_items:
            print("Cart is empty. Nothing to checkout.")
            return False
        
        cost = 0
        for ISBN, quantity, price in cart_items:
            if not inventory.decreaseStock(ISBN, quantity):
                print(f"Failed to update stock for ISBN: {ISBN}")
                return False
            cost += quantity*price
        
        current_date = datetime.date.today()
        #orderID = history.createOrder(userID, quantity, cost, current_date)

        if not orderID:
            print("Failed to create an order.")
            return False
        
        # if not history.addOrderItems(userID, orderID):
        #     print(f"Failed to add item ISBN: {ISBN} to the order.")
        #     return False
            
        delete_query = "DELETE FROM Cart WHERE UserID = ?"
        cursor.execute(delete_query, (userID,))
        conn.commit()

        print("Checkout completed successfully.")
        return True
