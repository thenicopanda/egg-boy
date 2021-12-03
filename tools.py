# Imports
import json
from math import floor, log
from decimal import Decimal

def load(which):
    """Load Stuff"""
    with open("bot.json") as botJson:
        bot = json.load(botJson)
        return(bot[which])



# Format a users ID into a normal string to be used when saving data
def getid(rawid):
    """Format Discord User Id into something eaiser to work with"""
    rawid = rawid.replace("<", "")
    rawid = rawid.replace(">", "")
    rawid = rawid.replace("@", "")
    rawid = rawid.replace("!", "")
    rawid = int(rawid)
    return rawid
    

def loadMerits(userid):
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

            # Make Egg Boy add the user to the merit file





def EggFindUser(userid):
    """Load A User From The users.json file"""
    """Essential in egg.py"""
    userid = str(userid)
    #with file open and read/write permissions
    with open("user.json", 'r+') as usersJson:
        #save JSON file as a variable
        data = json.load( usersJson )
        # if the user already exists
        if (userid) in data:
            #return the users information
            return data[userid]
        #if the user is not already in the file
        else:
            #default information
            newUserDefaultInfo = {
                "nickname"     : "",
                "eb"           : "",
                "letter"       : "",
                "soulEggs"     : "",
                "prophecyEggs" : ""
            }
            #create the user in the dictionary
            data[userid] = newUserDefaultInfo
            #go to the beginning of the file
            usersJson.seek(0)
            #update the JSON file
            json.dump(data, usersJson, indent =2)
            #return user info
            usersJson.truncate()
            return data[userid]
            



def UpdateEggUser(userId, displayName, eb, letter, soulEggs, prophecyEggs):
    userId = str(userId)
    with open("user.json", 'r+') as userJson:
        data = json.load (userJson)
        userCurrentInformation = EggFindUser(userId)
        newUserInformation = {
            "nickname"     : displayName,
            "eb"           : eb,
            "letter"       : letter,
            "soulEggs"     : soulEggs,
            "prophecyEggs" : prophecyEggs
        }
        data[userId] = newUserInformation
        userJson.seek(0)
        json.dump(data, userJson, indent=2)
        userJson.truncate()
        return data[userId]


# Function to sort the leaderboard
def sortFunc(tup):
    """Function to sort items in the updateLeaderboard() function"""
    key, d = tup
    return d['eb']


# Function to sort the leaderboard and send it back to caller
def updateLeaderboard():
    with open ("user.json", 'r+') as usersJson:
        n = 0
        # Define the Dictionaries to be used for each letter
        dList = {}
        nList = {}
        oList = {}
        SList = {}
        sList = {}
        QList = {}
        qList = {}
        tList = {}
        bList = {}
        mList = {}
        kList = {}
        extraList = {}

        data = json.load(usersJson)
        for user in data.values():
            n += 1
            eb = user["eb"]
            username = user["nickname"]
            letter = user["letter"]
            sampleDict = {
                "eb" : eb,
                "letter" : letter,
                "nickname" : username
            }
            if letter == "d":
                dList[n] = sampleDict
            elif letter == "N":
                nList[n] = sampleDict 
            elif letter == "o":
                oList[n] = sampleDict
            elif letter == "S":
                SList[n] = sampleDict
            elif letter == "s":
                sList[n] = sampleDict
            elif letter == "Q":
                QList[n] = sampleDict
            elif letter == "q":
                qList[n] = sampleDict
            elif letter == "t":
                tList[n] = sampleDict
            elif letter == "b":
                bList[n] = sampleDict
            elif letter == "m":
                mList[n] = sampleDict
            elif letter == "k":
                kList[n] = sampleDict
            else:
                extraList[n] = sampleDict
        dList = sorted(dList.items(), key = sortFunc, reverse=True)
        nList = sorted(nList.items(), key = sortFunc, reverse=True)
        oList = sorted(oList.items(), key = sortFunc, reverse=True)
        SList = sorted(SList.items(), key = sortFunc, reverse=True)
        sList = sorted(sList.items(), key = sortFunc, reverse=True)
        QList = sorted(QList.items(), key = sortFunc, reverse=True)
        qList = sorted(qList.items(), key = sortFunc, reverse=True)
        tList = sorted(tList.items(), key = sortFunc, reverse=True)
        bList = sorted(bList.items(), key = sortFunc, reverse=True)
        mList = sorted(mList.items(), key = sortFunc, reverse=True)
        kList = sorted(kList.items(), key = sortFunc, reverse=True)
        extraList = sorted(extraList.items(), key = sortFunc, reverse=True)
        returnList = [dList, nList, oList, SList, sList, QList, qList, tList, bList, mList, kList, extraList]
        return returnList


def human_format(number):
    units = ['', 'k', 'm', 'b', 'T', 'q', 'Q', 's', 'S', 'o', 'N', 'd', 'U', 'D', 'Td', 'qd', 'Qd', 'sd', 'Sd', 'Od', 'Nd', 'V', 'uV', 'dV', 'tV', 'qV', 'sV', 'SV', 'OV', 'NV', 'tT']
    k = Decimal(1000.0)
    magnitude = int(floor(log(number, k)))
    return '%.3f%s' % (number / k**magnitude, units[magnitude])

def calculateEB(soulEggs: str, prophecyEggs: Decimal, prophecyBonus: Decimal, soulFood: Decimal, human: bool):
    if soulEggs == "0":
        return "E1"
    if soulEggs.endswith("k"):
        soulEggs = (soulEggs[:-1]) 
        soulEggs = soulEggs * 1000    
    elif soulEggs.endswith("m"):
        soulEggs = Decimal(soulEggs[:-1]) 
        soulEggs = soulEggs * 1000000
    elif soulEggs.endswith("b"):
        soulEggs = Decimal(soulEggs[:-1]) 
        soulEggs = soulEggs * 1000000000
    elif soulEggs.endswith('t'):
        soulEggs = Decimal(soulEggs[:-1]) 
        soulEggs = soulEggs * 1000000000000
    elif soulEggs.endswith('q'):
        soulEggs = Decimal(soulEggs[:-1]) 
        soulEggs = soulEggs * 1000000000000000
    elif soulEggs.endswith('Q'):
        soulEggs = Decimal(soulEggs[:-1]) 
        soulEggs = soulEggs * 1000000000000000000
    elif soulEggs.endswith('s'):
        soulEggs = Decimal(soulEggs[:-1]) 
        soulEggs = soulEggs * 1000000000000000000000
    elif soulEggs.endswith('S'):
        soulEggs = Decimal(soulEggs[:-1]) 
        soulEggs = soulEggs * 1000000000000000000000000  
    elif soulEggs.endswith('o'):
        soulEggs = Decimal(soulEggs[:-1]) 
        soulEggs = soulEggs * 1000000000000000000000000000
    elif soulEggs.endswith('N'):
        soulEggs = Decimal(soulEggs[:-1]) 
        soulEggs = soulEggs * 1000000000000000000000000000000
    else:
        soulEggs = Decimal(soulEggs)
    try:
        prophecyEggBonus = (1 + 0.05 + (0.01 * prophecyBonus))**prophecyEggs * (10 + soulFood)
        EB = Decimal(prophecyEggBonus) * soulEggs
        if human == True:
            EB = human_format(EB)
        return EB
    except:
        return False






botPrefix = load("botPrefix")
botName = load("botName")


