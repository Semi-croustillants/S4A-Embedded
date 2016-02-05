#!/bin/python2.7
# coding=utf-8

#
# https://github.com/arduino/Arduino/blob/ide-1.5.x/build/shared/manpage.adoc
#

import subprocess
import sys
import os.path
import re

# TODO add exception
#   - user not in group tty… to upload to the board (Linux)
#   - arduino UI not install


class UploadArduino:

    def __init__(self):
        self.__arduinoType = {}

        # TODO link every board name to package:arch:board
        # https://github.com/arduino/Arduino/blob/ide-1.5.x/build/shared/manpage.adoc

        self.__arduinoType["uno"] = "arduino:avr:uno"

        pass

    def __arduinoUiIsInstallLinux(self):
        return os.path.isfile("/usr/bin/arduino")

    def __arduinoUiIsInstallWindows(self):
        pass

    def __getArduinoArchBoard(self, arduinoType):
        arduinoType = arduinoType.lower()

        for key in self.__arduinoType:
            arduinoArch = re.search(key, arduinoType)
            if arduinoArch:
                return self.__arduinoType[key]

        return ""

    def __uploadLinux(self, arduinoType, serialPort, arduinofile):
        if not self.__arduinoUiIsInstallLinux():
            print "Error, Arduino UI is not install on your machine"
            sys.exit(1)

        arduinoArch = self.__getArduinoArchBoard(arduinoType)

        if arduinoArch == "":
            print "Error, the Arduino board architecture is unknown"
            sys.exit(1)

        #
        # TODO manage sudo error:
        # can't open device "/dev/...": no such file or directory
        #

        # arduino --board arduino:avr:uno --port /dev/ttyACM0
        # --upload /home/battosai/Arduino/buzzer/buzzer.ino
        command = ['arduino', '--board', arduinoArch, '--port',
                   serialPort, '--upload', arduinofile]

        proc = subprocess.Popen(command, stdout=subprocess.PIPE)
        procStdout = proc.stdout.read()

        print procStdout

    def __uploadWindows(self, arduinoType, serialPort, arduinofile):
        pass

    def upload(self, arduinoType, serialPort, arduinofile):

        print arduinoType, serialPort, arduinofile

        if sys.platform.startswith('linux'):
            print "Linux"
            return self.__uploadLinux(arduinoType, serialPort, arduinofile)

        elif sys.platform.startswith('win'):
            print "Windows"
            return self.__uploadWindows(arduinoType, serialPort, arduinofile)

if __name__ == '__main__':
    uploadArduino = UploadArduino()
    uploadArduino.upload("uno", "/dev/ttyACM0",
                         "/home/battosai/Arduino/buzzer/buzzer.ino")
