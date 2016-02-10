#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

from model import JsonInoConvertorWithARTKV3 as JsonInoConvertor, UploadArduino, AutoDetectSerial
from AutoDetectSerial import AutoDetectSerialError
from UploadArduino import UploadArduinoError


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

    def __notify_observers(self, err, error_msg=""):
        for obs in self.observers:
            obs.notify(err, error_msg)

    def add_observer(self, obs):
        if not hasattr(obs, 'notify'):
            raise ValueError("First argument must be object with notify method")
        self.observers.append(obs)

    def __display_msg(self, err, object_error=None):
        if self.__possessed_observers():
            if err:
                self.__notify_observers(err, ''.join(str(e1) for e1 in object_error.args))
            else:
                self.__notify_observers(True, "Succeed")
        else:
            if err:
                raise object_error
            else:
                print "Succeed"

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
            self.upload_arduino.upload(arduino_serial[1], arduino_serial[0], arduino_ino_file_name)

            self.__display_msg(False)
        except AutoDetectSerialError, e:
            self.__display_msg(True, e)
        except UploadArduinoError, e:
            self.__display_msg(True, e)
        except Exception, e:
            self.__display_msg(True, e)
