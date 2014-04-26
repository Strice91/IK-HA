#!/usr/bin/python3.3

import getMail
import unittest
from unittest.mock import MagicMock


class TestGetMail(unittest.TestCase):

    def setUp(self):
    	pass
    def test_connect(self):

        # create fake socket
        mockedSocket = MagicMock()
        mockedSocket.connect = MagicMock()
        mockedSocket.recv = MagicMock(return_value=b"+OK")

        # mock socket module
        getMail.socket = MagicMock(return_value=mockedSocket)

        # mock print
        getMail.print = MagicMock()

        # set host and port

        getMail.host = "test"
        getMail.port = 123

        the_returned_socket = getMail.connect(getMail.host, getMail.port)

        self.assertEqual(mockedSocket, the_returned_socket)
        # check that no error occured
        self.assertEqual(0, getMail.print.call_count)

        # check socket call is ok
        mockedSocket.connect.assert_called_once_with(("test", 123))

    def test_send_user_correct(self):
        # mock socket
        mockSocket = MagicMock()
        mockSocket.send = MagicMock()
        # return ok
        mockSocket.recv = MagicMock(return_value=b"+OK")

        # mock print
        getMail.print = MagicMock()

        # set user
        getMail.user = "test"

        # test function
        getMail.send_user(mockSocket, getMail.user)

        # check if socket call is ok
        mockSocket.send.assert_called_once_with(b"user test\r\n")

        # check output
        self.assertEqual(0, getMail.print.call_count)

    def test_send_user_incorrect(self):
        # mock socket
        mockSocket = MagicMock()
        mockSocket.send = MagicMock()
        # return an error
        mockSocket.recv = MagicMock(return_value=b"+ERROR")

        # mock print
        getMail.print = MagicMock()

        # set user
        getMail.user = "test"

        # test function
        getMail.send_user(mockSocket, getMail.user)

        # check if socket call is ok
        mockSocket.send.assert_called_once_with(b"user test\r\n")

        # check if error message is ok
        getMail.print.assert_called_once_with("User not known.")

    def test_send_pass_correct(self):
         # mock socket
        mockSocket = MagicMock()
        mockSocket.send = MagicMock()
        # return ok
        mockSocket.recv = MagicMock(return_value=b"+OK")

        # mock print
        getMail.print = MagicMock()

        # set password
        getMail.password = "test"

        # test function
        getMail.send_pass(mockSocket, getMail.password)

        # check if socket call is ok
        mockSocket.send.assert_called_once_with(b"pass test\r\n")

        # check output
        self.assertEqual(0, getMail.print.call_count)

    def test_send_pass_incorrect(self):
         # mock socket
        mockSocket = MagicMock()
        mockSocket.send = MagicMock()
        # return ok
        mockSocket.recv = MagicMock(return_value=b"+ERROR")

        # mock print
        getMail.print = MagicMock()

        # set password
        getMail.password = "test"

        # test function
        getMail.send_pass(mockSocket, getMail.password)

        # check if socket call is ok
        mockSocket.send.assert_called_once_with(b"pass test\r\n")

         # check if error message is ok
        getMail.print.assert_called_once_with("Password falsch")

    def test_send_list(self):
         # mock socket
        mockSocket = MagicMock()
        mockSocket.send = MagicMock()
        # return ok
        mockSocket.recv = MagicMock(return_value=b"+OK\r\nHallo\r\nWelt")

        # mock print
        getMail.print = MagicMock()

        # test function
        output_list = getMail.send_list(mockSocket)

        # check if socket call is ok
        mockSocket.send.assert_called_once_with(b"LIST\r\n")

        # check output
        self.assertEqual(0, getMail.print.call_count)
        self.assertEqual(["+OK", "Hallo", "Welt"], output_list)

    def test_close_connection(self):
        # mock socket
        mockSocket = MagicMock()
        mockSocket.send = MagicMock()
        # return ok
        mockSocket.recv = MagicMock(return_value=b"+OK")

        # test function
        output_list = getMail.close_connection(mockSocket)

        # check if socket call is ok
        mockSocket.send.assert_called_once_with(b"QUIT\r\n")

    def test_send_rset(self):
        # mock socket
        mockSocket = MagicMock()
        mockSocket.send = MagicMock()
        # return ok
        mockSocket.recv = MagicMock(return_value=b"+OK\r\n")

        # mock print
        getMail.print = MagicMock()

        # test function
        getMail.send_rset(mockSocket)

        # check if socket call is ok
        mockSocket.send.assert_called_once_with(b"RSET\r\n")

        # check output
        self.assertEqual(0, getMail.print.call_count)

    def test_retr_mail(self):
        # mock socket
        mockSocket = MagicMock()
        mockSocket.send = MagicMock()
        # return ok
        mockSocket.recv = MagicMock(
            return_value=b"+OK\r\nfrom: sender\r\nsubject: subject\r\nto: reciever\r\ndate: 1.1.90\r\n\r\nThis is the text\r\n\r\n")

        # mock print
        getMail.printMail = MagicMock()

        # test function
        getMail.retr_mail(mockSocket, "1", "test")

        # check if socket call is ok
        mockSocket.send.assert_called_once_with(b"RETR 1\r\n")

        # check output
        self.assertEqual(1, getMail.printMail.call_count)
        getMail.printMail.assert_called_once_with(
            "sender", "reciever", "subject", "1.1.90", "This is the text\r\n")

    def test_retr_header(self):
       # mock socket
        mockSocket = MagicMock()
        mockSocket.send = MagicMock()
        # return ok
        mockSocket.recv = MagicMock(
            return_value=b"+OK\r\nfrom: sender\r\nsubject: subject\r\n\r\n")

        # mock print
        getMail.printMailHeader = MagicMock()

        # test function
        getMail.retr_header(mockSocket, 0, ["1"])

        # check if socket call is ok
        mockSocket.send.assert_called_once_with(b"RETR 1\r\n")

        # check output
        self.assertEqual(1, getMail.printMailHeader.call_count)
        getMail.printMailHeader.assert_called_once_with("1",
                                                        "sender", "subject")

    def test_get_specific_mail(self):
        # mock
        connect_function = getMail.connect
        getMail.connect = MagicMock(return_value="dummySocket")

        send_user_function = getMail.send_user
        getMail.send_user = MagicMock()

        send_pass_function = getMail.send_pass
        getMail.send_pass = MagicMock()

        retr_mail_function = getMail.retr_mail
        getMail.retr_mail = MagicMock()

        send_rset_function = getMail.send_rset
        getMail.send_rset = MagicMock()

        close_connection_function = getMail.close_connection
        getMail.close_connection = MagicMock()

        getMail.printEnd = MagicMock()

        # test function
        getMail.getSpecificMail(["", "host", 110, "user", "password", "1"])

        # check output
        getMail.connect.assert_called_once_with("host", 110)
        getMail.send_user.assert_called_once_with("dummySocket", "user")
        getMail.send_pass.assert_called_once_with("dummySocket", "password")
        getMail.retr_mail.assert_called_once_with("dummySocket", "1", "user")
        getMail.send_rset.assert_called_once_with("dummySocket")
        getMail.close_connection.assert_called_once_with("dummySocket")
        self.assertEqual(1, getMail.printEnd.call_count)

        getMail.connect = connect_function
        getMail.send_user = send_user_function
        getMail.send_pass = send_pass_function
        getMail.retr_mail = retr_mail_function
        getMail.send_rset = send_rset_function
        getMail.close_connection = close_connection_function

    def test_get_all_mail(self):
        # mock
        connect_function = getMail.connect
        getMail.connect = MagicMock(return_value="dummySocket")

        send_user_function = getMail.send_user
        getMail.send_user = MagicMock()

        send_pass_function = getMail.send_pass
        getMail.send_pass = MagicMock()

        retr_header_function = getMail.retr_header
        getMail.retr_header = MagicMock()

        send_list_function = getMail.send_list
        getMail.send_list = MagicMock(return_value=["1", "2", "3", "4"])

        send_rset_function = getMail.send_rset
        getMail.send_rset = MagicMock()

        close_connection_function = getMail.close_connection
        getMail.close_connection = MagicMock()

        getMail.printEnd = MagicMock()

        # test function
        getMail.getAllMails(["", "host", 110, "user", "password", "1"])

        # check output
        getMail.connect.assert_called_once_with("host", 110)
        getMail.send_user.assert_called_once_with("dummySocket", "user")
        getMail.send_pass.assert_called_once_with("dummySocket", "password")
        getMail.retr_header.assert_called_once_with(
            "dummySocket", 1, ["1", "2", "3", "4"])
        getMail.send_rset.assert_called_once_with("dummySocket")
        getMail.close_connection.assert_called_once_with("dummySocket")
        self.assertEqual(1, getMail.printEnd.call_count)

        getMail.connect = connect_function
        getMail.send_user = send_user_function
        getMail.send_pass = send_pass_function
        getMail.send_list = send_list_function
        getMail.retr_header = retr_header_function
        getMail.send_rset = send_rset_function
        getMail.close_connection = close_connection_function


if __name__ == '__main__':
    unittest.main()
