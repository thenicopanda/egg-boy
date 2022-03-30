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

def kickPlayerRequest(ei_user_id_to_kick, contract_id, coop_name):
    url = "https://www.auxbrain.com/ei/kick_player_coop"
    kendrome = "EI5223299518300160"
    kickPlayerRequest = ei.KickPlayerCoopRequest()
    kickPlayerRequest.rinfo.MergeFrom(basicRequestInfo(kendrome))
    kickPlayerRequest.player_identifier = ei_user_id_to_kick
    kickPlayerRequest.contract_identifier = contract_id
    kickPlayerRequest.coop_identifier = coop_name    
    kickPlayerRequest.requesting_user_id = kendrome
    kickPlayerRequest.reason = 4 # Private coop

    # Serialize and encode the payload
    data = b64encode(kickPlayerRequest.SerializeToString())
    # Get and save the response
    resp = requests.post(url, data={'data' : data.decode(), 'user' : kendrome}) 

    
    # Decode the content
    response =resp.content.decode() 
    return response


def createCoopRequest(ei_user_id, contract_id, coop_name, eop):
    url = "https://www.auxbrain.com/ei/create_coop"
    platform = ei.Platform.Value(device_id)
    createCoopRequest = ei.CreateCoopRequest()
    responseObject = ei.CreateCoopResponse()
    authenticatedMessage = ei.AuthenticatedMessage()
    createCoopRequest.rinfo.MergeFrom(basicRequestInfo(ei_user_id)) # 10
    createCoopRequest.contract_identifier = contract_id # 1
    createCoopRequest.coop_identifier = coop_name # 2
    createCoopRequest.platform = platform # 6
    createCoopRequest.league = 0 # 9
    createCoopRequest.client_version = client_version # 7
    createCoopRequest.user_id = ei_user_id

    # Serialize and encode the payload
    data = b64encode(createCoopRequest.SerializeToString())
    # Get and save the response
    resp = requests.post(url, data={'data' : data.decode(), 'user' : ei_user_id}) 


    # Decode the content
    response = b64decode( resp.content.decode() )

    responseObject.ParseFromString(response)

    # Create and return dictionary with backup
    return MessageToDict(responseObject)
