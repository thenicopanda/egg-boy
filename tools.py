# Imports
import json, yaml
from math import floor, log
from decimal import Decimal
from ei import *

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
    return n > 1 and all(n % i for i in range(2, int(n ** 0.5) + 1))

"""
#############
Begin Merits
#############
"""

def loadMerits(userid):
    """Load a users merits"""
    userid = str(userid)
    with open ("merits.json", "r+") as meritJson:
        data = json.load(meritJson)
        if userid in data:
            merits = data[userid]
            return merits
        else:
            newMeritUser = [
            ]
            data[userid] = newMeritUser
            meritJson.seek(0)
            json.dump(data, meritJson, indent = 2)
            meritJson.truncate()
            return False


def addMerits(userid, message):
    """Add A Merit to a User"""
    userid = str(userid)
    with open("merits.json", "r+") as meritJson:
        data = json.load(meritJson)
        if userid in data:
            currentMerits = data[userid]
            currentMerits.append(message)
            data[userid] = currentMerits
            meritJson.seek(0)
            json.dump(data, meritJson, indent = 2)
        else:
            newMeritUser = [
                message
            ]
            data[userid] = newMeritUser
            meritJson.seek(0)
            json.dump(data, meritJson, indent = 2)
            meritJson.truncate()

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
                return 1
            data[userid] = currentMerits
            meritJson.seek(0)
            json.dump(data, meritJson, indent = 2)
            meritJson.truncate()
            return 3
        else: 
            return 2

"""
#############
End Merits
#############
"""

"""
###########
Begin Egg
###########
"""

def updateLeaderboard():
    updateAllUsers()
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
                "nickname" : username
            }
            peopleList.append(sampleDict)

        peopleList = sorted(peopleList, key = lambda i: Decimal(i['eb']), reverse=True)

        return peopleList
def addAccount(eid, nickname, discordId):
    with open("user.json", "r+") as usersJson:
        try:
            data = json.load(usersJson)
            backup = firstContactRequest(eid)
            info = getEB(backup)
            newPerson = info 
            newPerson["nickname"] = nickname
            data[discordId] = newPerson
            usersJson.seek(0)
            json.dump(data, usersJson, indent=2)
            usersJson.truncate()
            return True
        except:
            return False

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

"""
###########
End Egg
###########
"""
