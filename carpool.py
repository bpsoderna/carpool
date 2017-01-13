import pickle
import string

USERS = []

################################################################################
# CLASSES
################################################################################

class User(object):
    def __init__(self,username,password):
        self.username = username
        self.password = password

    def updateUserSettings(self):
        print("New Users fill out settings")
        self.kids = validIntInput("how many kids do you have: ")
        self.seats = validIntInput("how many seats are there in your car, excluding the driver: ")
        self.address = input("what is your home address: ")

################################################################################
# PROGRAM EVENTS
################################################################################

#lets users login or create new accounts
def start():
    print("welcome to carpool")
    getData()
    data = input("to login press L, new users press N: ").upper()
    if data == "N": #new user
        newUser()
        data = "L"
    if data == "L":
        login() 
    else: start()

#creates a new user and lets them login
def newUser():
    #get string of current users/passwords and make into dict
    allUserText = readFile("users.txt")
    try: allUsers = pickle.loads(allUserText)
    except EOFError: allUsers = ""
    userDict = makeUserDict(allUsers)
    #checks to make sure username doesn't already exist
    username = input("enter a username: ")
    while username in userDict:
        print("that username already exists")
        username = input("enter a username: ")
    #checks to make sure password entered correctly
    password = True
    password2 = False
    while password != password2:
        password = input("enter password: ")
        password2 = input("confirm password: ")
    #adds username/password to userDict and creats a new user 
    userDict[username] = password
    newUser = User(username, password)
    USERS.append(newUser)
    allUserText = makeUserText(userDict)
    saveContent = pickle.dumps(allUserText)
    writeFile("users.txt",saveContent)
    newUser.updateUserSettings()

#allows existing users to login to program
def login():
    #get string of current users/passwords and make into dict
    allUserText = readFile("users.txt")
    allUsers = pickle.loads(allUserText)
    userDict = makeUserDict(allUsers)
    print("Login")
    #get username and check if it already exists
    username = input("username: ")
    if username in userDict:
        #check if password matches
        password = input("password: ")
        while userDict[username] != password:
            password = input("invalid password try again: ")
        print("congrat's you're logged in")
        options()
    else:
        #wrong username, prompt to retry or make new user
        print("that user doesnt exist")
        retry = input("press N to create a new account or R to retry").upper()
        if retry == "N":
            newUser()
        elif retry == "R":
            login()

def options():
    pass

################################################################################
# HELPER FUNCTIONS
################################################################################

#checks to make sure user inputs an int
def validIntInput(question):
    var = None
    while not isinstance(var, int):
        var = input(question)
        if var in string.digits:
            var = int(var)
    return var

################################################################################
# SAVE AND LOAD THINGS
################################################################################

#taken from the 15-112 course website
def readFile(path):
    with open(path,"rb") as f:
        return f.read()

#taken from the 15-112 course website
def writeFile(path,contents):
    with open(path,"wb") as f:
        f.write(contents)

#takes username/password dict and turns into formatted string
def makeUserText(userDict):
    result = ""
    for user in userDict:
        result += user + ":" + userDict[user] + ","
    return result

#sets all golbal varibales to data from programData        
def getData():
    global USERS
    data = readFile("programData.txt")
    try: USERS = pickle.loads(data)
    except EOFError: USERS = []

#saves all global variables to programData
def saveData():
    global USERS
    saveContent = pickle.dumps(USERS)
    writeFile("programData.txt",saveContent)



def makeUserDict(allUsers):
    #all users formatted as "user0:password0,user1:password1..."
    userDict = {}
    for user in allUsers.split(","):
        username = user[0:user.find(":")]
        password = user[user.find(":")+1:]
        userDict[username] = password
    return userDict

start()
saveData()