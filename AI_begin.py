import random as ran
import datetime as dt
import re
class AI:
    def __init__(self, name, creator, /):
        self.name = name
        self.creator = creator

    # Method to introduce the AI
    def intro(self, /):
        user = input("Hello, what is your name")
        self.user = user.title()
        print(f"Hello {self.user}, my name is {self.name} ready to assist you when need be. "+
            f"I was created by {self.creator}, a very smart person\n")
        
        # Account Sign in
        print("Before you continue you must sign in to your account ")
        have_account = input("Do you have an account: \n").lower()
        if re.search("yes",have_account):
            self.account_verification()
        elif re.search("no", have_account):
            self.account_creation()
        else:
            print("Invalid input")
            
    # Method to control which method is used
    def brain(self, /):
        print("\nIf you would like to end the program type end")
        while True:
            prompt = input("\nWhat would you like me to do today: ").lower()
            if re.search(r"\bdate\b",prompt):
                self.date()
            elif re.search(r"\bgame\b",prompt):
                self.game()
            elif re.search(r"\bquote\b",prompt):
                self.quote()
            elif re.search(r"\bend\b", prompt):
                print("I am always here to assist you if need be. \nBye")
                break
            else:
                print("Sorry I am unable to perform that task")

    # Method to create an account
    def account_creation(self, /):
        # Email verification
        user_file = open("user_acc_info.txt", "a")
        # Ensures the user only has 3 tries to make his account
        for tries in range(3):
            # Validates the email given
            email = input("Enter your email: ").lower()
            if not(re.search(r"\b.+(@)\w+(.)\w{3}",email)):
                print("Email is invalid")
                continue
                
            # Password Verification
            password = input("Enter your password: ")
            confirm_password = input("Confirm your password: ")
            if password == confirm_password:
                print("Your account has sucessfully been created\n")
                user_file.write(f"{email}:{password}\n")
                self.brain()
                break
            print("Passwords do not match, please try again \n")
        else:
            print("You have exceeded your number of tries")
        user_file.close()

    # This is to verify the account if the user already has one
    def account_verification(self, /):
        user_file = open("user_acc_info.txt","r")
        email = input("Enter your email: ").lower()
        password = input("Enter your password: ")
        com_input = f"{email}:{password}"
        for line in user_file:
            if com_input == line[:-1]:
                print ("Account login is successful")
                self.brain()
                break
        else:
            print("Username or password is incorrect")
        user_file.close()

    # Method to give an inspirational quote
    def quote(self):
        quotes = [
            "Forget the pain but never the lessons you learnt",
            "A boat is safer in the harbour but that is not what it was built for",
            "Everything good in life demans something, even heaven demands death",
            "Never wast your energy on people who do not support you",
            "The only person you should try and beat is the person you were yesterday",
            "Words are like keys, they can open any heart but shut any mouth"
        ] 
        randnum = ran.randint(0,len(quotes)-1)
        print(ran.choice(quotes))

    # Method to play a game
    def game(self, /):
        chambers = [0,0,0,0,0,0]
        # while 0 in chambers:
        chamber = 0
        while chamber<len(chambers)-1:
            
            # Ensures the bullet is not put within the same chamber
            index = ran.randint(0,5)
            if chambers[index] == 0:
                chambers[index] = 1
            else:
                continue
                
            # User input process
            user = int(input("Enter a number from 1 to 6: "))
            if chambers[user-1] ==1:
                print("You are dead")
                print(chambers)
                break
            else:
                print ("You are lucky this time \n")
                # comment this to make the game easier
                ran.shuffle(chambers)
            chamber+=1
        else:
            print("Congrats, you survived")
            print(chambers)

    # Method to tell the date
    def date(self, /):
        self.date = dt.date.today()
        day = dt.date.weekday(self.date)
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.day = days[day]
        print(f"Today is {self.day} and the date is {self.date}")

MyAI = AI("A2","Davina")
MyAI.intro()