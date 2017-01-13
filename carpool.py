import pickle
import string

def readFile(path):
    with open(path,"rb") as f:
        return f.read()

def writeFile(path,contents):
    with open(path,"wb") as f:
        f.write(contents)

def start():
    print("welcome to carpool")
    data = input("to login press L, new users press N: ").upper()
    if data == "N": #new user
        newUser()
        data = "L"
    if data == "L":
        login() 
    else: start()
        
def newUser():
    allUserText = readFile("users.txt")
    try: allUsers = pickle.loads(allUserText)
    except EOFError: allUsers = ""
    userDict = makeUserDict(allUsers)
    username = input("enter a username: ")
    while username in userDict:
        print("that username already exists")
        username = input("enter a username: ")
    password = "a"
    password2 = "b"
    while password != password2:
        password = input("enter password: ")
        password2 = input("confirm password: ")
    userDict[username] = password
    allUserText = makeUserText(userDict)
    saveContent = pickle.dumps(allUserText)
    writeFile("users.txt",saveContent)

def makeUserText(userDict):
    result = ""
    for user in userDict:
        result += user + ":" + userDict[user] + ","
    return result

def login():
    allUserText = readFile("users.txt")
    allUsers = pickle.loads(allUserText)
    userDict = makeUserDict(allUsers)
    print("Login")
    username = input("username: ")
    if username in userDict:
        password = input("password: ")
        while userDict[username] != password:
            password = input("invalid password try again: ")
        print("congrat's you're logged in")
    else:
        print("that user doesnt exist")
        retry = input("press N to create a new account or R to retry").upper()
        if retry == "N":
            newUser()
        elif retry == "R":
            login()

def makeUserDict(allUsers):
    #all users formatted as "user0:password0,user1:password1..."
    userDict = {}
    for user in allUsers.split(","):
        username = user[0:user.find(":")]
        password = user[user.find(":")+1:]
        userDict[username] = password
    return userDict


start()