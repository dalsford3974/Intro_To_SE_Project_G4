import sqlite3
import random


class OrderHistory:

    def __init__(self, databaseName="methods.db"):
        self.databaseName = databaseName

    def viewHistory(self, userID):
        try:
            connection = sqlite3.connect(self.databaseName)

        except:
            print("Failed database connection.")

            # Exits the program if unsuccessful
            sys.exit()

        # Cursor to send queries through
        cursor = connection.cursor()

        # SELECT Everything FROM Orders WHERE User's Orders
        query = "SELECT * FROM Orders WHERE UserID=?"

        cursor.execute(query, (userID,))
        results = cursor.fetchall()

        if len(results) == 0:
            print("Your order history is empty")
        else:
            for result in results:
                print(f"Order Number: {result[0]}")
                print(f"Items Ordered: {result[2]}")
                print(f"Cost {result[3]}")
                print(f"Date Ordered: {result[4]}")
                print("\n")

        cursor.close()

    def viewOrder(self, userID, OrderNumber):
        try:
            connection = sqlite3.connect(self.databaseName)

        except:
            print("Failed database connection.")

            # Exits the program if unsuccessful
            sys.exit()

        # Cursor to send queries through
        cursor = connection.cursor()

        # SELECT Everything FROM Orders WHERE User's Orders
        query0 = "SELECT * FROM Orders WHERE OrderNumber=? and UserID=?"

        cursor.execute(query0, (userID, OrderNumber,))

        orders = cursor.fetchall()

        # Check if order belongs to user requesting or exists
        for order in orders:
            if not order[0]:
                print("Order does not exist or you don't have permission to view it")
                return

        # SELECT Everything from OrderItems WHERE it is that OrderNumber
        query1 = "SELECT * FROM OrderItems WHERE OrderNumber=? "

        cursor.execute(query1, (OrderNumber,))
        results0 = cursor.fetchall()

        for result0 in results0:

            # For each OrderedItem in OrderNumber: SELECT Evererything from the Inventory WHERE ISBN coresponds
            query2 = "SELECT * FROM Inventory WHERE ISBN=? "

            cursor.execute(query2, (result0[1],))

            results = cursor.fetchall()

            if len(results) == 0:
                print("Order does not exist")
            else:
                for result in results:
                    print(f"ISBN: {result[0]}")
                    print(f"{result[1]} by {result[2]}")
                    print(f"A {result[4]} page {result[3]} released in {result[5]}")
                    print(f"${result[6]} per book, {result0[2]} ordered")
                    print()

        cursor.close()

    def createOrder(self, userID, quantitiy, cost, date):

        try:
            connection = sqlite3.connect(self.databaseName)

        except:
            print("Failed database connection.")

            # Exits the program if unsuccessful
            sys.exit()

        # Cursor to send queries through
        cursor = connection.cursor()

        # SELECTing OrderNumber FROM Orders for new ID comparison
        query0 = "SELECT OrderNumber FROM Orders"

        cursor.execute(query0,)

        orders = cursor.fetchall()

        orderID = random.randint(100000, 999999)

        cost = str(cost)
        cost = ("$" + cost)

        # Unique OrderNumber verification (orderID,) converts orderID to tuple for comparison
        while (orderID,) in orders:
            orderID = random.randint(100000, 999999)

        # INSERT Order Data INTO Orders
        query = "INSERT INTO Orders (OrderNumber, UserID, ItemNumber, Cost, Date) VALUES (?, ?, ?, ?, ?)"

        cursor.execute(query, (orderID, userID, quantitiy, cost, date,))

        connection.commit()
        cursor.close()

        # Order creation comfirmation
        print(f"Order {orderID} Created.\n")

        # Returns OrderNumber as String
        return str(orderID)

    def addOrderItems(self, userID, orderID):
        try:
            connection = sqlite3.connect(self.databaseName)

        except:
            print("Failed database connection.")

            # Exits the program if unsuccessful
            sys.exit()

        # Cursor to send queries through
        cursor = connection.cursor()

        # SELECT OrderNumber FROM Oders and verify it belongs to user
        query0 = "SELECT OrderNumber FROM Orders WHERE OrderNumber=? AND UserID=?"
        cursor.execute(query0, (orderID, userID))

        if not cursor.fetchone():
            print("Order does not exist or you don't have permission")
            return

        # SELECT ISBNs and Quantities from User's Cart
        query = "SELECT ISBN, Quantity FROM Cart WHERE UserID=?"
        cursor.execute(query, (userID,))
        items = cursor.fetchall()

        if not items:
            print("Cart is empty")
            return
        else:
            # Insert each cart item INTO OrderItems
            for isbn, quantity in items:
                insert_query = "INSERT INTO OrderItems (OrderNumber, ISBN, Quantity) VALUES (?, ?, ?)"
                cursor.execute(insert_query, (orderID, isbn, quantity))

                connection.commit()
                print(f"Successfully added items to Order {orderID}")

        cursor.close()
