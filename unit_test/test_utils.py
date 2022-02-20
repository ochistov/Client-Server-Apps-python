from email import message
from http import client
import sys
import os
sys.path.append(os.path.join(os.getcwd(), '..'))
import common.utils as u
import common.variables as v
import unittest
import socket
import json

#creating test socket class
class TestSocket:
    def __init__(self, testDict):
        self.testDict = testDict
        self.encodedMessage = None
        self.receivedMessage = None
    
    #emulate send function of socket
    def send(self, message):
        self.encodedMessage = json.dumps(self.testDict).encode(v.ENCODING)
        self.receivedMessage = message
    
    #emulating receive function of socket
    def recv(self, maxLength):
        return json.dumps(self.testDict).encode(v.ENCODING)



class TestUtils(unittest.TestCase):
    #creating test dictionaries
    testDict = {
    "action": "presence",
    "time": "11:11:11",
    "type": "status",
    "user": {
        "account_name": "GUEST"
    }
}
    testOK = {"RESPONSE":200}
    testERR = {"RESPONSE":404, "ERROR":"Not found"}

    
    #test of sending message
    def testMessageSending(self):
        testSocket = TestSocket(self.testDict)
        u.sendData(testSocket, self.testDict)
        self.assertEqual(testSocket.encodedMessage, testSocket.receivedMessage)
    #test of sending wrong type of data as a message
    def testMessageSendingError(self):
        testSocket = TestSocket(self.testDict)
        self.assertRaises(TypeError, u.sendData(testSocket, "something not dictionary"))

    #test getting OK response
    def testGetMessageOK(self):
        testSocket = TestSocket(self.testOK)
        self.assertEqual(u.getData(testSocket), self.testOK)
    #test getting BAD response
    def testGetMessageBAD(self):
        testSocket = TestSocket(self.testERR)
        self.assertEqual(u.getData(testSocket), self.testERR)



if __name__ == '__main__':
    unittest.main()