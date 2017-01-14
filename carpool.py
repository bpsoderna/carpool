import pickle
import string
import random

USERS = []
GROUPS = []
loggedInUser = None

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

class Group(object):

    count = 0
    keys = set()

    def __init__(self,name=None,membersList=None):
        if name==None: self.name = "group"+str(Group.count)
        else: self.name = name
        if membersList==None: self.membersList = []
        else: self.membersList = membersList
        self.events = []
        self.key = Group.createKey()
        Group.count += 1

    def __hash__(self):
        return hash(self.key)

    def addMember(self, member):
        self.membersList.append(member)

    @staticmethod
    def createKey():
        key = ""
        letters = string.ascii_letters + string.digits
        for i in range(3):
            for j in range(3):
                key += letters[random.randint(0,len(letters))]
            key += "-"
        if key in Group.keys:
            Group.createKey()
        else:
            Group.keys.add(key)
            print(key)
            return key

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
        getLoginUser(username)
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

def getLoginUser(username):
    global loggedInUser
    for user in USERS:
        if user.username == username:
            loggedInUser = user
            break

def options():
    key = None
    while key != "O":
        key = input("press O to see options: ").upper()
    print("G - see current groups")
    print("C - create new group")
    print("J - join new group")
    key = None
    while key is None or key not in "CJGO":
        key = input("press key to begin: ").upper()
        if key == "G":
            pass
        elif key == "C":
            createGroup()
        elif key == "J":
            pass
        elif key == "O":
            options()
        key = None

def createGroup():
    print("creating a new group")
    name = input("enter a group name: ")
    membersText = input("enter usernames of members separated by commas: ")
    membersList = membersText.split(",")
    newGroup = Group(name, membersList)
    GROUPS.append(newGroup)
    print("group created successfully")
    loggedInUser.groups.append(newGroup)
    print("your group key is %s give this key to other users to be added to this group" % (newGroup.key))
    options()

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

#takes formatted string and turns into username/password dict
def makeUserDict(allUsers):
    #all users formatted as "user0:password0,user1:password1..."
    userDict = {}
    for user in allUsers.split(","):
        username = user[0:user.find(":")]
        password = user[user.find(":")+1:]
        userDict[username] = password
    return userDict

#sets all golbal varibales to data from programData        
def getData():
    global USERS
    global GROUPS
    data = readFile("programData.txt")
    try: [USERS, GROUPS] = pickle.loads(data)
    except EOFError: 
        USERS = []
        GROUPS = []

#saves all global variables to programData
def saveData():
    global USERS
    global GROUPS
    data = [USERS, GROUPS]
    saveContent = pickle.dumps(data)
    writeFile("programData.txt",saveContent)

def reset():
    saveData()
    getData()

################################################################################
# RUN
################################################################################

reset() #running this line before start() clears previoulsy saved data, but not login info
start()
saveData()