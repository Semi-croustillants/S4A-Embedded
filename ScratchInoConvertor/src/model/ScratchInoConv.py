#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

from gst._gst import Message

from model import JsonInoConvertorWithARTKV3 as JsonInoConvertor, UploadArduino, AutoDetectSerial, Message
from AutoDetectSerial import AutoDetectSerialError
from UploadArduino import UploadArduinoError
from Message import Message as Message
import threading


class ScratchInoConv(object):
    TMP_FOLDER = "tmp"
    INO_EXTENSION = ".ino"

    def __init__(self):
        self.__observers = []

        self.__json_ino_convertor = JsonInoConvertor.JsonInoConvertor()
        self.__auto_detect_serial = AutoDetectSerial.AutoDetectSerial()
        # self.__upload_arduino = UploadArduino.UploadArduino()

        # create a tmp folder if it doesn't exist
        if not os.path.exists(self.TMP_FOLDER):
            os.makedirs(self.TMP_FOLDER)

    # PATTERN OBSERVER
    def __possessed_observers(self):
        """
        test if this instance has at least one observer
        :return: true if has an observer, false else
        """
        return len(self.__observers) > 0

    def __notify_observers(self, message):
        """
        send for each observer a message object
        :param message: Message object which contains a code identifier and a string method
        """
        for obs in self.__observers:
            obs.notify(message)

    def add_observer(self, obs):
        """
        add an observer
        :param obs: an object with a notify method
        :return:
        """
        if not hasattr(obs, 'notify'):
            raise ValueError("First argument must be object with notify method")
        self.__observers.append(obs)

    def __display_msg(self, message):
        """
        display a message for the user
        detect if there is an observer and send it the message
        else print the message
        :param message: Message class with code identifier and a string message
        """
        if not isinstance(message, Message):
            raise ValueError("Error: a Message object is expected")

        if self.__possessed_observers():
            self.__notify_observers(message)
        else:
            print message.message

    # CONV
    def scratch_into_arduino(self, scratch_file, arduino_type=0):
        """
        upload the scratch code into the arduino board
        :param scratch_file: the scratch file
        :param arduino_type: the arduino type, 0 = uno, else = other
        :return:
        """
        try:
            # get serial port where the arduino board is connected
            arduino_serial = self.__auto_detect_serial.get_arduinos_path()[0]

            # prepare the folder where the ino file will be
            arduino_folder = self.TMP_FOLDER + os.sep + os.path.basename(scratch_file)
            if not os.path.exists(arduino_folder):
                os.makedirs(arduino_folder)

            # prepare the ino file
            arduino_ino_file_name = arduino_folder + os.sep + os.path.basename(scratch_file) + self.INO_EXTENSION

            # Start conversion: scratch to ino
            self.__json_ino_convertor = JsonInoConvertor.JsonInoConvertor(typeArduino=arduino_type)
            self.__json_ino_convertor.convertSpriteScripts(scratch_file, arduino_ino_file_name)

            # Start upload
            self.__upload_arduino = UploadArduino.UploadArduino(arduino_serial[1], arduino_serial[0],
                                                                arduino_ino_file_name, self.__display_msg)
            self.__upload_arduino.start()

            # display succeed message
            # self.__display_msg(Message(Message.SUCCEED_MESSAGE))

            # display error message
        except AutoDetectSerialError, e:
            self.__display_msg(Message(Message.ERROR_MESSAGE, ''.join(str(e1) for e1 in e.args)))
        except UploadArduinoError, e:
            self.__display_msg(Message(Message.ERROR_MESSAGE, ''.join(str(e1) for e1 in e.args)))
        except Exception, e:
            self.__display_msg(Message(Message.ERROR_MESSAGE, ''.join(str(e1) for e1 in e.args)))
