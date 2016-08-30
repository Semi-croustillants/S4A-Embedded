#!/bin/python2.7
# coding=utf-8


class Message(object):

    """
    Error
    """
    ERROR_MESSAGE = 0

    """
    the operation succeed
    """
    SUCCEED_MESSAGE = 1

    """

    """
    CONSOLE_LOG = 2
    CONSOLE_LOG_ERR = 3

    def __init__(self, code, message=""):
        self.code = code
        self.message = message
