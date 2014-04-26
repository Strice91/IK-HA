#!/usr/bin/python3.3

import delMail
import unittest
from unittest.mock import MagicMock


class TestDeleteMail(unittest.TestCase):

    def setUp(self):
        pass

    def test_connect(self):

        # create fake socket
        mockedSocket = MagicMock()
        mockedSocket.connect = MagicMock()
        mockedSocket.recv = MagicMock(return_value=b"+OK")

        # mock socket module
        delMail.socket = MagicMock(return_value=mockedSocket)

        # mock print
        delMail.print = MagicMock()

        # set host and port

        delMail.host = "test"
        delMail.port = 123

        the_returned_socket = delMail.connect()

        self.assertEqual(mockedSocket, the_returned_socket)
        # check that no error occured
        self.assertEqual(0, delMail.print.call_count)

        # check socket call is ok
        mockedSocket.connect.assert_called_once_with(("test", 123))

    def test_send_user_correct(self):
        # mock socket
        mockSocket = MagicMock()
        mockSocket.send = MagicMock()
        # return ok
        mockSocket.recv = MagicMock(return_value=b"+OK")

        # mock print
        delMail.print = MagicMock()

        # set user
        delMail.user = "test"

        # test function
        delMail.send_user(mockSocket)

        # check if socket call is ok
        mockSocket.send.assert_called_once_with(b"user test\r\n")

        # check output
        self.assertEqual(0, delMail.print.call_count)

    def test_send_user_incorrect(self):
        # mock socket
        mockSocket = MagicMock()
        mockSocket.send = MagicMock()
        # return an error
        mockSocket.recv = MagicMock(return_value=b"+ERROR")

        # mock print
        delMail.print = MagicMock()

        # set user
        delMail.user = "test"

        # test function
        delMail.send_user(mockSocket)

        # check if socket call is ok
        mockSocket.send.assert_called_once_with(b"user test\r\n")

        # check if error message is ok
        delMail.print.assert_called_once_with("User not known.")

    def test_send_pass_correct(self):
         # mock socket
        mockSocket = MagicMock()
        mockSocket.send = MagicMock()
        # return ok
        mockSocket.recv = MagicMock(return_value=b"+OK")

        # mock print
        delMail.print = MagicMock()

        # set password
        delMail.password = "test"

        # test function
        delMail.send_pass(mockSocket)

        # check if socket call is ok
        mockSocket.send.assert_called_once_with(b"pass test\r\n")

        # check output
        self.assertEqual(0, delMail.print.call_count)

    def test_send_pass_incorrect(self):
         # mock socket
        mockSocket = MagicMock()
        mockSocket.send = MagicMock()
        # return ok
        mockSocket.recv = MagicMock(return_value=b"+ERROR")

        # mock print
        delMail.print = MagicMock()

        # set password
        delMail.password = "test"

        # test function
        delMail.send_pass(mockSocket)

        # check if socket call is ok
        mockSocket.send.assert_called_once_with(b"pass test\r\n")

         # check if error message is ok
        delMail.print.assert_called_once_with("Password falsch")

    def test_send_list(self):
         # mock socket
        mockSocket = MagicMock()
        mockSocket.send = MagicMock()
        # return ok
        mockSocket.recv = MagicMock(return_value=b"+OK\r\nHallo\r\nWelt")

        # mock print
        delMail.print = MagicMock()

        # test function
        output_list = delMail.send_list(mockSocket)

        # check if socket call is ok
        mockSocket.send.assert_called_once_with(b"LIST\r\n")

        # check output
        self.assertEqual(0, delMail.print.call_count)
        self.assertEqual(["+OK", "Hallo", "Welt"], output_list)

    def test_delete_all_mails(self):
         # mock socket
        mockSocket = MagicMock()
        mockSocket.send = MagicMock()
        # return ok
        mockSocket.recv = MagicMock(return_value=b"+OK")

        mocketList = ["Bla", "Hallo", "Welt", "Test", "Test"]
        # test function
        output_list = delMail.delete_all_mails(mockSocket, mocketList)

        # check if socket call is ok
        mockSocket.send.assert_no_call(b"DELE Bla\r\n")
        mockSocket.send.assert_no_call(b"DELE Test\r\n")
        mockSocket.send.assert_any_call(b"DELE Hallo\r\n")
        mockSocket.send.assert_any_call(b"DELE Welt\r\n")

        # check output

    def test_close_connection(self):
        # mock socket
        mockSocket = MagicMock()
        mockSocket.send = MagicMock()
        # return ok
        mockSocket.recv = MagicMock(return_value=b"+OK")

        # test function
        output_list = delMail.close_connection(mockSocket)

        # check if socket call is ok
        mockSocket.send.assert_called_once_with(b"QUIT\r\n")

if __name__ == '__main__':
    unittest.main()
