import sys
import os
sys.path.append(os.path.join(os.getcwd(), '..'))
import common.utils as u
import unittest
import socket


class TestServer(unittest.TestCase):
    #getting server socket on setup
    def setUp(self):
        self.s = u.getServerSocket('localhost', 7777)
    #closing socket after tests
    def tearDown(self):
        self.s.close()
    #test if server's socket is instance of socket.socket
    def testServerSocketIsSocket(self):
        self.assertIsInstance(self.s, socket.socket)
    #test if socket ip and port is equal localhost and 7777 from setup
    def testServerSocketAddr(self):
        self.assertEqual(self.s.getsockname(), ('127.0.0.1', 7777))


if __name__ == '__main__':
    unittest.main()