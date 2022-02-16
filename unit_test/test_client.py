import sys
import os
sys.path.append(os.path.join(os.getcwd(), '..'))
import common.utils as u
import unittest


class TestClient(unittest.TestCase):
    #creating server and client sockets at setup, sending message
    def setUp(self):
        self.s = u.getServerSocket('localhost', 7777)
        self.c = u.getClientSocket('localhost', 7777)
        self.sender = self.s.accept()[0]
        u.sendData(self.c, {'action': 'msg', 'time': 'time', 'message':'testmessage'})

    #closing sockets after tests
    def tearDown(self):
        self.c.close()
        self.s.close()

    #testing getData
    def testGetData(self):
        self.assertEqual(u.getData(self.sender), {'action': 'msg', 'time': 'time', 'message':'testmessage'})

    #sending wrong data
    def testSendData(self):
        with self.assertRaises(TypeError):
            u.sendData()


if __name__ == '__main__':
    unittest.main()