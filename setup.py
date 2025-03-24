import sqlite3
import sys

## attempts to connect to the database
try:
    connection = sqlite3.connect("introToSE.db")

    print("Successful connection.")

except:
    print("Failed connection.")

    ## exits the program if unsuccessful
    sys.exit()

## cursor to send queries through
cursor = connection.cursor()
print("\n--------------------------------------------")

## inventory table

print("\nCreating Inventory table...")

inventory = """CREATE TABLE Items (
    ItemID varchar(14) NOT NULL,
    Title varchar(50),
    UserID varchar(50),
    Price decimal(4,2),
    Stock int(4),
    PRIMARY KEY(ItemID),
    FOREIGN KEY(UserID) REFERENCES User(UserID)
);"""

cursor.execute(inventory)
print("Finished creating Inventory table.")
print("\nFinished building Inventory table.")
print("\n--------------------------------------------")



## user table

print("\nCreating User table...")

user = """CREATE TABLE User (
    UserID varchar(7) NOT NULL,
    Email varchar(100) NOT NULL UNIQUE,
    Password varchar(100),
    FirstName varchar(50),
    LastName varchar(50),
    Address varchar(100),
    City varchar(50),
    State varchar(2),
    Zip int(5),
    Payment varchar(50),
    PRIMARY KEY(UserID)
);"""

cursor.execute(user)
print("Finished creating User table.")
print("\nAdding User records...")

## user inserts

query = "INSERT INTO User (UserID, Email, Password, FirstName, LastName, Address, City, State, Zip, Payment) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
data = [
    ('00-0000', 'admin@gmail.com', 'admin1', 'Admin', 'Admin', 'null', 'null', 'null', 'null', 'null')
]

cursor.executemany(query, data)
connection.commit()

## shows changes
print(cursor.rowcount, "record(s) inserted.")
print("\nFinished building User table.")
print("\n--------------------------------------------")




## cart table

print("\nCreating Cart table...")

cart = """CREATE TABLE Cart (
    UserID varchar(7) NOT NULL,
    ItemID varchar(14) NOT NULL,
    Quantity int(3),
    FOREIGN KEY(UserID) REFERENCES User(UserID),
    FOREIGN KEY(ItemID) REFERENCES Inventory(ItemID)
);"""

cursor.execute(cart)
print("Finished creating Cart table.")
print("\nFinished building Cart table.")
print("\n--------------------------------------------")




## orders table

print("\nCreating Orders table...")

order = """CREATE TABLE Orders (
    OrderID varchar(6) NOT NULL,
    UserID varchar(7) NOT NULL,
    ItemNumber int(5),
    Cost varchar(10),
    Date varchar(25),
    PRIMARY KEY(OrderID),
    FOREIGN KEY(UserID) REFERENCES User(UserID)
);"""

cursor.execute(order)
print("Finished creating Orders table.")
print("\nFinished building Orders table.")
print("\n--------------------------------------------")




## order items table

print("\nCreating OrderItems table...")

order = """CREATE TABLE OrderItems (
    OrderID varchar(6) NOT NULL,
    ItemID varchar(14) NOT NULL,
    Quantity int(3),
    FOREIGN KEY(OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY(ItemID) REFERENCES Inventory(ItemID)
);"""

cursor.execute(order)
print("Finished creating OrderItems table.")
print("\nFinished building OrderItems table.")
print("\n--------------------------------------------")



## close the cursor and connection once you're done
cursor.close()
connection.close()
