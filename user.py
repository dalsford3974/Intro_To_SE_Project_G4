import sqlite3
import sys
import random

class User:

    ## constructor
    def __init__(self, databaseName="website.db"):
        self.databaseName = databaseName

        self.loggedIn = False
        self.userID = ""

    ## functional requirement functions
    def login(self):
        email = input("Email: ")
        password = input("Password: ")


        ## setup database and query the database
        try:
            connection = sqlite3.connect(self.databaseName)

        except:
            print("Failed database connection.")

            ## exits the program if unsuccessful

            ## sys.exit()

        ## cursor to send queries through
        cursor = connection.cursor()

        ## sets up query and uses user input for the constraint
        ## selects password to compare against user input password
        query = "SELECT UserID, Password FROM User WHERE Email=?"
        data = (email,)

        cursor.execute(query, data)
        result = cursor.fetchall()

        ## nothing was grabbed
        if(len(result) == 0):
            print("\nUser/Password combination is not in the system.")

            ## these are mainly set for safety's sake
            self.userID = ""
            self.loggedIn = False

            return False

        ## grabs result 
        ## --> [0][0] UserID
        ## --> [0][1] Password
        userID = result[0][0]
        token = result[0][1]

        ## closes connection
        cursor.close()
        connection.close()

        ## successful login
        if(password == token):
            print("\nLogging user in...")

            ## set the class variables
            self.userID = userID
            self.loggedIn = True

            return True

        ## unsuccessful login
        else:
            print("\nUser/Password combination is not in the system.")

            ## these are mainly set for safety's sake
            self.userID = ""
            self.loggedIn = False

            return False

    def logout(self):
        self.userID = ""
        self.loggedIn = False

        return False

    def viewAccountInformation(self):
        ## setup database and query the database
        try:
            connection = sqlite3.connect(self.databaseName)

        except:
            print("Failed database connection.")

            ## exits the program if unsuccessful
            sys.exit()

        ## cursor to send queries through
        cursor = connection.cursor()

        ## sets up query and uses UserID from the currently logged in user
        ## does NOT display the password or userID
        query = "SELECT Email, FirstName, LastName, Address, City, State, Zip, Payment FROM User WHERE UserID=?"
        data = (self.userID,)

        cursor.execute(query, data)
        result = cursor.fetchall()

        ## grabs results
        ## --> [0][0] Email
        ## --> [0][0] FirstName
        ## --> [0][1] LastName
        ## --> [0][2] Address
        ## --> [0][3] City
        ## --> [0][4] State
        ## --> [0][5] Zip
        ## --> [0][6] Payment
        email = result[0][0]
        first = result[0][1]
        last = result[0][2]
        address = result[0][3]
        city = result[0][4]
        state = result[0][5]
        zipcode = result[0][6]
        payment = result[0][7]

        ## displays results
        print("Name:", first, last)
        print("Email:", email, end='\n\n')

        print("Address:")
        print(address)
        print(city, ", ", state, " ", zipcode, sep="", end="\n\n")

        print("Payment method:", payment)

        ## closes connection
        cursor.close()
        connection.close()

    def createAccount(self):
        ## database connection
        try:
            connection = sqlite3.connect(self.databaseName)

        except:
            print("Failed database connection.")

            ## exits the program if unsuccessful
            
            ## sys.exit()

        ## cursor to send queries through
        cursor = connection.cursor()


        ## woefully inefficient ID creation
        ## shouldn't need to actually loop because our sample set is so small
        ## but just in case...
        while(1):
            ## creates ID
            newID = str(random.randint(10,99)) + "-" + str(random.randint(1000,9999))
            
            ## checks if it's in the database already
            query = "SELECT * FROM User WHERE UserID=?"
            data = (newID,)

            cursor.execute(query, data)
            result = cursor.fetchall()

            ## nothing was grabbed
            if(len(result) == 0):
                ## we're free!
                break

        ## continue with account creation

        print("Welcome to account creation!")
        print("Please type in your items for the prompts, hitting enter when you're done with each one.\n")

        ## email is the only thing we need to loop to make sure they don't have a duplicate
        while(1):
            email = input("Email: ")

            ## checks if it's in the database already
            query = "SELECT * FROM User WHERE Email=?"
            data = (email,)

            cursor.execute(query, data)
            result = cursor.fetchall()

            ## nothing was grabbed
            if(len(result) == 0):
                ## we're free!
                break

            else:
                print("\nThat email is already in the system. Please try again.")

        password = input("Password: ")
        first = input("\nFirst name: ")
        last = input("Last name: ")
        address = input("\nAddress: ")
        city = input("City: ")
        state = input("State: ")
        zipcode = input("Zip code: ")
        payment = input("\nPayment method: ")

        ## tries to insert into the database
        query = "INSERT INTO User (UserID, Email, Password, FirstName, LastName, Address, City, State, Zip, Payment) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        data = (newID, email, password, first, last, address, city, state, zipcode, payment)

        cursor.execute(query, data)
        connection.commit()

        print("\nAccount created.")

    ## NOT FOR ADMIN

    def deleteAccount(self):

        print("Are you sure you want to delete your account.\n")
        answer = input("(Y/N)?")

        if(answer == "Y"):
            try:
                connection = sqlite3.connect(self.databaseName)

            except:
                print("Failed database connection.")

            cursor = connection.cursor()

            query = "DELETE FROM User WHERE UserID=?"
            data = (self.userID)

            cursor.execute(query, data)
            connection.commit()

            self.logout()

        else:
            return
        
    
    def editAccount(self):
        return
    
    def returnItem(self):
        return
    
    ## for admin only
    
    def viewAccount(self):
        return
    
    def removeAccount(self):
        return

    ## getters
    def getLoggedIn(self):
        return self.loggedIn

    def getUserID(self):
        return self.userID