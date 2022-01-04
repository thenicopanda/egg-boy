import json

# Config Information
device_id = "IOS"
client_version = 36
version = "1.22.2"
build = "1.22.2.0"


import ei_pb2 as ei
import requests
from base64 import b64decode, b64encode
from google.protobuf.json_format import MessageToDict

def basicRequestInfo(ei_user_id):
    """Create and return ei.BasicRequestInfo"""
    basicRequestInfo = ei.BasicRequestInfo()
    # Define requred fields for rinfo
    basicRequestInfo.ei_user_id = ei_user_id # 1
    basicRequestInfo.client_version = client_version # 2
    basicRequestInfo.version = version # 3
    basicRequestInfo.build = build # 4
    basicRequestInfo.platform = device_id # 5
    # Return object
    return basicRequestInfo


def firstContactRequest(ei_user_id):
    url = "https://www.auxbrain.com/ei/first_contact"
    # Create the payload object
    firstContactPayload = ei.EggIncFirstContactRequest()
    # Create the platform object
    platform = ei.Platform.Value(device_id)
    # Create the response object
    responseObject = ei.EggIncFirstContactResponse()
    # Create an authenticaed message object
    authenticatedMessage = ei.AuthenticatedMessage()

    # Define fields for the payload
    firstContactPayload.rinfo.MergeFrom(basicRequestInfo(ei_user_id)) # 8
    firstContactPayload.ei_user_id = ei_user_id # 4
    firstContactPayload.platform = platform # 5
    firstContactPayload.client_version = client_version # 2

    # Serialize and encode the payload
    data = b64encode(firstContactPayload.SerializeToString())
    # Get and save the response
    resp = requests.post(url, data={'data' : data.decode(), 'user' : ei_user_id}) 
    
    # Decode the content
    response = b64decode( resp.content.decode() )
    # Authenticate the message
    authenticatedMessage.ParseFromString(response)
    # Turn the authenticated response into a first contact response
    responseObject.ParseFromString(authenticatedMessage.message)

    # Create and return dictionary with backup
    return MessageToDict(responseObject)


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
        "eid" : backup['eiUserId'],
        "soulFood" : soulFood,
        "prophecyBonus" : prophecyBonus,
        "soulEggs" : soulEggs,
        "prophecyEggs" : prophecyEggs
    }
    return returndict


def updateAllUsers():
    with open("user.json", "r+") as usersJson:
        data = json.load(usersJson)
        for userId, person in data.items():
            backup = firstContactRequest(person["eid"])
            personInfo = getEB(backup)
            personInfo["nickname"] = person["nickname"]
            data[userId] = personInfo

        usersJson.seek(0)
        json.dump(data, usersJson, indent=2)
        usersJson.truncate()
            
