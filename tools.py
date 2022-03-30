# Imports
import json, yaml
from math import floor, log, sqrt
from decimal import *
from ei import *
from datetime import datetime

def load(which):
    """Load Configuration Information"""
    with open("bot.yaml", "r") as botConfig:
        bot = yaml.safe_load(botConfig)
        return(bot[which])
        
def triviaLoad():
    """Load the trivia from trivia.json"""
    with open("trivia.json", "r") as triviaJSON:
        trivia = json.load(triviaJSON)
        return trivia
# Define a couple 'global' things to use throughout the bot.
botPrefix = load("botPrefix")
botName = load("botName")

def is_prime(n):
    return n > 1 and all(n % i for i in range(2, int(n ** 0.5) + 1)) # IDK how this works, but don't touch it pls

def is_square(n):
    if sqrt(n).is_integer():
        return sqrt(n)
    else:
        return False

def loadMerits(userid):
    """Load a users merits"""
    userid = str(userid) # Convert user ID to a string (sometimes gets passed in weird)
    with open ("merits.json", "r+") as meritJson: 
        data = json.load(meritJson)
        if userid in data: # If the user already exists in the merit list
            merits = data[userid] # Pull the merits
            return merits # return the list of merits
        else: # If user not in the merit list
            newMeritUser = [
            ]
            data[userid] = newMeritUser # Create a blank object for them in the merit file
            meritJson.seek(0) # Move to the beginning of the file
            json.dump(data, meritJson, indent = 2) # Dump the new data into the file
            meritJson.truncate() # Remove excess data that's left behind.
            return False # let whoever called the function know that there were no merits

def addMerits(userid, message):
    """Add A Merit to a User"""
    userid = str(userid)
    with open("merits.json", "r+") as meritJson:
        data = json.load(meritJson)
        if userid in data: # If the user already exists in the merit list
            currentMerits = data[userid] # Pull the current list of merits
            currentMerits.append(message) # Add the new merit to the list
            data[userid] = currentMerits # update the data with the new merit
            meritJson.seek(0) # Move to the beginning of the file
            json.dump(data, meritJson, indent = 2)
        else: # If user not in the merit list
            newMeritUser = [
                message
            ]
            data[userid] = newMeritUser # Update the list with the first merit
            meritJson.seek(0) # Move to the beginning of the file
            json.dump(data, meritJson, indent = 2) # Dump the data into the file
            meritJson.truncate() # Cleanup excess data

def removeMerit(userid, meritNumber):
    """Remove a merit from a user."""
    userid = str(userid)
    meritNumber -= 1
    with open("merits.json", "r+") as meritJson:
        data = json.load(meritJson)
        if userid in data:
            currentMerits = data[userid]
            try:
                currentMerits.pop(meritNumber)
            except IndexError:
                return 1 # Merit does not exist
            data[userid] = currentMerits
            meritJson.seek(0)
            json.dump(data, meritJson, indent = 2)
            meritJson.truncate()
            return 3 # Merit deleted and saved
        else: 
            return 2 # User has no merits


########################################################################################################################

        
def getEB(backup):
    """Pull all relavent EB data from backup"""
    backup = backup["backup"]
    researchList = backup["game"]["epicResearch"]
    soulFood = 0
    prophecyBonus = 0
    for research in researchList:
        if research["id"] == "soul_eggs":
            soulFood = research["level"]
        if research["id"] == "prophecy_bonus":
            prophecyBonus = research["level"]
    prophecyEggs = backup["game"]["eggsOfProphecy"]
    soulEggs = backup["game"]["soulEggsD"]
    
    returndict = {
        "soulFood" : soulFood,
        "prophecyBonus" : prophecyBonus,
        "soulEggs" : soulEggs,
        "prophecyEggs" : prophecyEggs
    }
    return returndict

def human_format(number: Decimal):
    units = ['', 'k', 'm', 'b', 'T', 'q', 'Q', 's', 'S', 'o', 'N', 'd', 'U', 'D', 'Td', 'qd', 'Qd', 'sd', 'Sd', 'Od', 'Nd', 'V', 'uV', 'dV', 'tV', 'qV', 'sV', 'SV', 'OV', 'NV', 'tT']
    k = Decimal(1000.0)
    magnitude = int(floor(log(number, k)))
    return '%.3f%s' % (number / k**magnitude, units[magnitude])

def formatLargeNumber(largeNumber: str):
    if largeNumber == "0":
        return "E1"
    if largeNumber.endswith("k"):
        largeNumber = (largeNumber[:-1]) 
        largeNumber = largeNumber * 1000    
    elif largeNumber.endswith("m"):
        largeNumber = Decimal(largeNumber[:-1]) 
        largeNumber = largeNumber * 1000000
    elif largeNumber.endswith("b"):
        largeNumber = Decimal(largeNumber[:-1]) 
        largeNumber = largeNumber * 1000000000
    elif largeNumber.endswith('t'):
        largeNumber = Decimal(largeNumber[:-1]) 
        largeNumber = largeNumber * 1000000000000
    elif largeNumber.endswith('q'):
        largeNumber = Decimal(largeNumber[:-1]) 
        largeNumber = largeNumber * 1000000000000000
    elif largeNumber.endswith('Q'):
        largeNumber = Decimal(largeNumber[:-1]) 
        largeNumber = largeNumber * 1000000000000000000
    elif largeNumber.endswith('s'):
        largeNumber = Decimal(largeNumber[:-1]) 
        largeNumber = largeNumber * 1000000000000000000000
    elif largeNumber.endswith('S'):
        largeNumber = Decimal(largeNumber[:-1]) 
        largeNumber = largeNumber * 1000000000000000000000000  
    elif largeNumber.endswith('o'):
        largeNumber = Decimal(largeNumber[:-1]) 
        largeNumber = largeNumber * 1000000000000000000000000000
    elif largeNumber.endswith('N'):
        largeNumber = Decimal(largeNumber[:-1]) 
        largeNumber = largeNumber * 1000000000000000000000000000000
    else:
        largeNumber = Decimal(largeNumber)
    return largeNumber

def calculateEB(soulEggs: Decimal, prophecyEggs: Decimal, prophecyBonus: Decimal, soulFood: Decimal, human: bool):
    try:
        prophecyEggBonus = (Decimal(1) + Decimal(0.05) + (Decimal(0.01) * Decimal(prophecyBonus)))**Decimal(prophecyEggs) * (Decimal(10) + Decimal(soulFood))
        EB = Decimal(prophecyEggBonus) * Decimal(soulEggs)
        if human == True:
            EB = human_format(EB)
        return EB
    except:
        return False



def addAccount(eid, nickname, discordId):
    with open("user.json", "r+") as usersJson:
        try:
            data = json.load(usersJson)
            backup = firstContactRequest(eid)
            info = getEB(backup)
            newPerson = info 
            newPerson["nickname"] = nickname
            newPerson['discord'] = discordId
            data[eid] = newPerson
            usersJson.seek(0)
            json.dump(data, usersJson, indent=2)
            usersJson.truncate()
            return True
        except:
            return False

def deleteAccount(eid, discordID):
    with open("user.json", "r+") as usersJson:
        users = json.load(usersJson)
        try:
            verificationThing = users[eid]
        except KeyError:
            return False
        if verificationThing["discord"] == discordID:
            try:
                users.pop(eid)
                usersJson.seek(0)
                json.dump(users, usersJson, indent=2)
                usersJson.truncate()
                return True
            except:
                return False
        else:
            return False

def searchByDiscordID(discordID):
    with open("user.json", "r+") as usersJson:
        accounts = json.load(usersJson)
        results = {}
        for eid, account in accounts.items():
            if account["discord"] == discordID:
                sampleDict = {
                    "soulFood": account["soulFood"],
                    "prophecyBonus": account["prophecyBonus"],
                    "soulEggs": account["soulEggs"],
                    "prophecyEggs": account["prophecyEggs"],
                }
                results[eid] = sampleDict
        return results

def updateLeaderboard():
    #updateAllUsers()
    with open ("user.json", 'r+') as usersJson:
        data = json.load(usersJson) # Load the data
        n = 0 # declare the number
        peopleList = []
        for user in data.values():
            n += 1
            eb = calculateEB(user["soulEggs"], user["prophecyEggs"], user["prophecyBonus"], user["soulFood"], False)
            username = user["nickname"]
            sampleDict = {
                "eb" : str(eb),
                "nickname" : username,
                "rank" : getOom(eb),
                "discord" : user['discord']
            }
            peopleList.append(sampleDict)

        peopleList = sorted(peopleList, key = lambda i: Decimal(i['eb']), reverse=True)

        return peopleList

def updateSoulLeaderboard():
    with open ("user.json", 'r+') as usersJson:
        data = json.load(usersJson) # Load the data
        n = 0 # declare the number
        peopleList = []
        for user in data.values():
            n += 1
            sampleDict = {
                "soulEggs" : str(user["soulEggs"]),
                "discord" : user['discord']
            }
            peopleList.append(sampleDict)

        peopleList = sorted(peopleList, key = lambda i: Decimal(i['soulEggs']), reverse=True)

        return peopleList

def updateAllUsers():
    with open("user.json", "r+") as usersJson:
        data = json.load(usersJson)
        for eid, person in data.items():
            try:
                backup = firstContactRequest(eid)
                personInfo = getEB(backup)
                personInfo["nickname"] = person["nickname"]
                personInfo["discord"] = person["discord"]
                data[eid] = personInfo
            except:
                print(f"{eid} failed to update at {datetime.now()}")

        usersJson.seek(0)
        json.dump(data, usersJson, indent=2)
        usersJson.truncate()


def getOom(eb: Decimal):
    units = ['Farmer','Farmer','Farmer', # 0-2
             'Farmer', 'Farmer II', 'Farmer III', # 3-7
             'Kilofarmer', 'Kilofarmer II', 'Kilofarmer III', # 9
             'Megafarmer', 'Megafarmer II', 'Megafarmer III', # 12
             'Gigafarmer', 'Gigafarmer II', 'Gigafarmer III', # 15
             'Terafarmer', 'Terafarmer II', 'Terafarmer III', # 18
             'Petafarmer', 'Petafarmer II', 'Petafarmer III', # 21
             'Exafarmer', 'Exafarmer II', 'Exafarmer III', # 24
             'Zettafarmer', 'Zettafarmer II', 'Zettafarmer III', # 27
             'Yottafarmer', 'Yottafarmer II', 'Yottafarmer III', # 30
             'Xennafarmer', 'Xennafarmer II', 'Xennafarmer III', # 33
             'Weccafarmer', 'Weccafarmer II', 'Weccafarmer III', # 36
             'Vendafarmer', 'Vendafarmer II', 'Vendafarmer III', # 39
             'Uadafarmer', 'Uadafarmer II', 'Uadafarmer III', # 42
             'Treidafarmer', 'Treidafarmer II', 'Treidafarmer III', # 45 
             'Quadafarmer', 'Quadafarmer II', 'Quadafarmer III', # 48
             'Pendafarmer', 'Pendafarmer II', 'Pendafarmer III', # 51
             'Exedafarmer', 'Exedafarmer II', 'Exedafarmer III'] # 54
    magnitude = len(str(round(eb)))
    if magnitude >= 55:
        return 'Infinifarmer'
    return units[magnitude]
