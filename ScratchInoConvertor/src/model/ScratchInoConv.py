#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

from gst._gst import Message

from model import JsonInoConvertorWithARTKV3 as JsonInoConvertor, UploadArduino, AutoDetectSerial, Message
from AutoDetectSerial import AutoDetectSerialError
from UploadArduino import UploadArduinoError
from Message import Message as Message


class ScratchInoConv(object):
    TMP_FOLDER = "tmp"
    INO_EXTENSION = ".ino"

    def __init__(self):
        self.observers = []

        self.json_ino_convertor = JsonInoConvertor.JsonInoConvertor()
        self.auto_detect_serial = AutoDetectSerial.AutoDetectSerial()
        self.upload_arduino = UploadArduino.UploadArduino()

        if not os.path.exists(self.TMP_FOLDER):
            os.makedirs(self.TMP_FOLDER)

    # PATTERN OBSERVER
    def __possessed_observers(self):
        return len(self.observers) > 0

    def __notify_observers(self, message):
        for obs in self.observers:
            obs.notify(message)

    def add_observer(self, obs):
        if not hasattr(obs, 'notify'):
            raise ValueError("First argument must be object with notify method")
        self.observers.append(obs)

    def __display_msg(self, message):
        if not isinstance(message, Message):
            raise ValueError("Error: a Message object is expected")

        if self.__possessed_observers():
            self.__notify_observers(message)
        else:
            print message.message

    # CONV
    def scratch_into_arduino(self, scratch_file, arduino_type=0):
        try:
            arduino_serial = self.auto_detect_serial.get_arduinos_path()[0]

            arduino_folder = self.TMP_FOLDER + os.sep + os.path.basename(scratch_file)

            if not os.path.exists(arduino_folder):
                os.makedirs(arduino_folder)

            arduino_ino_file_name = arduino_folder + os.sep + os.path.basename(scratch_file) + self.INO_EXTENSION

            self.json_ino_convertor = JsonInoConvertor.JsonInoConvertor(typeArduino=arduino_type)
            self.json_ino_convertor.convertSpriteScripts(scratch_file, arduino_ino_file_name)
            self.upload_arduino.upload(arduino_serial[1], arduino_serial[0], arduino_ino_file_name, self.__display_msg)

            self.__display_msg(Message(Message.SUCCEED_MESSAGE))
        except AutoDetectSerialError, e:
            self.__display_msg(Message(Message.ERROR_MESSAGE, ''.join(str(e1) for e1 in e.args)))
            # self.__display_msg(True, e)
        except UploadArduinoError, e:
            # self.__display_msg(True, e)
            self.__display_msg(Message(Message.ERROR_MESSAGE, ''.join(str(e1) for e1 in e.args)))
        except Exception, e:
            self.__display_msg(Message(Message.ERROR_MESSAGE, ''.join(str(e1) for e1 in e.args)))
            # self.__display_msg(True, e)
