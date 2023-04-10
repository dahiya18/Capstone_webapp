import time
import json
import re
import requests
from J2735tool import DSRC

### Configuration Constants
Send_Interval = 5 #minimul interval between each send request
Testing_flag = 0  #set to 1 for testing without sending any request
URL = "https://effy5f4s1k.execute-api.ca-central-1.amazonaws.com/receiveMSG"          #URL for the server

#J2735 Message Class for storing , decoding, and sending messages

class J2735_Message:
    IntersectionID = 0
    IntersectionStatus = 0  
    payload = ""        #raw hex encoding of message
    payloadJER = ""     #json decoding of message

    def __init__(self):
        self.MessageFrame = DSRC.MessageFrame
        pass

    def setIntersectionID(self, id):
        self.IntersectionID = id
        #print("Set ID : " + id)

    def setIntersectionStatus(self, status):
        self.IntersectionStatus = status
        #print("Set status : " + status)

    def setPayload(self, payload):
        #accept payload as UPER J2735_1603 encoded in hex string
        self.payload = payload
        #print("Set payload : " + payload)
        #TODO : Translate payload
        # 
        byte_message = bytes.fromhex(payload)
        self.MessageFrame.from_uper(byte_message)
        self.payloadJER = self.MessageFrame.to_jer()


    def sendMessage(self):
        send_json_obj = json.loads(self.payloadJER) 
        send_json_obj["Intersection_id"] = self.IntersectionID
        send_json_obj["Intersection_status"] = self.IntersectionStatus
        print("Sending the following json")
        print(send_json_obj)
        if(Testing_flag == 0):
            #sending http request
            res = requests.post(URL, json = send_json_obj)
            print("Request sent with response code " + str(res.status_code))


###############################################################################
#Main:

#tail spatTx Json File
SPaT_Message = J2735_Message()
last_send_timer = 0

logfile = open("./logs/spatTx.json","r")
logfile.seek(0,2)

#loop for tailing the SpatTX file
while True:
    line = logfile.readline()
    if not line:
        time.sleep(0.1)
    else:
        if("IntersectionID" in line):
            #SPaT_Message.setIntersectionID()
            x = re.findall('[0-9]+', line)
            SPaT_Message.setIntersectionID(x[0])

        elif("IntersecionStatus" in line):
            x = re.findall('[0-9]+', line)
            SPaT_Message.setIntersectionStatus(x[0])

        elif("payload" in line):
            #load payload
            x = re.findall('"([^"]*)"', line)
            SPaT_Message.setPayload(x[1])
            #send message with interval
            if(time.time() - last_send_timer >= Send_Interval):
                SPaT_Message.sendMessage()
                last_send_timer = time.time()