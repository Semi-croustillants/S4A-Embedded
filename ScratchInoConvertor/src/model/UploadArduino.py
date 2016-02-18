#!/bin/python2.7
# coding=utf-8

#
# https://github.com/arduino/_arduino/blob/ide-1.5.x/build/shared/manpage.adoc
#
import os
import subprocess
import sys
from re import search

# TODO add exception
#   - user not in group tty… to upload to the board (_linux)
from time import sleep

import serial
import threading
from model.Message import Message


class UploadArduinoError(Exception):
    pass


class UploadArduino(threading.Thread):

    def __init__(self, arduino_type, serial_port, arduino_file, callback_log=None):
        """
        upload an arduino code to the arduino board
        :param arduino_type: the arduino model: uno, mega…
        :param serial_port: the serial port where the arduino board is connected
        :param arduinofile: the arduino code to upload
        :callback_log: Message(code, message), see the Message class
        """

        super(UploadArduino, self).__init__()

        # TODO link every board name to package:arch:board
        # https://github.com/arduino/_arduino/blob/ide-1.5.x/build/shared/manpage.adoc
        self.__arduino_type_list = {"uno": "arduino:avr:uno"}

        self.__arduino_type = arduino_type
        self.__serial_port = serial_port
        self.__arduino_file = arduino_file
        self.__callback_log = callback_log

    def __arduino_ui_is_installed_linux(self):
        """
        test if arduino is installed
        """
        try:
            # pipe output to /dev/null for silence
            null = open("/dev/null", "w")
            sub = subprocess.Popen("arduino", stdout=null, stderr=null)
            sub.terminate()
            null.close()
        except OSError:
            self.__display_error("Error: Arduino UI is not installed, please install it")

    def __arduino_ui_get_path_windows(self):
        """
        search into windows registry if Arduino is installed
        :return: the execution path
        """

        # only on windows. cannot be import for all the class
        import _winreg

        # 32 bits installation
        try:
            a_reg = _winreg.ConnectRegistry(None, _winreg.HKEY_LOCAL_MACHINE)
            a_key = _winreg.OpenKey(a_reg, r"Software\\Wow6432Node\\Arduino")
            val = _winreg.QueryValueEx(a_key, "Install_Dir")[0]
        except WindowsError:
            # 64 bits installation
            try:
                a_reg = _winreg.ConnectRegistry(None, _winreg.HKEY_LOCAL_MACHINE)
                a_key = _winreg.OpenKey(a_reg, r"Software\\Arduino")
                val = _winreg.QueryValueEx(a_key, "Install_Dir")[0]
            except WindowsError:
                self.__display_error("Error: Arduino UI is not installed, please install it")
        return val + "\\arduino.exe"

    def __get_arduino_arch_board(self, arduino_type):
        """
        get the architecture board
        :param arduino_type: the arduino type
        :return: the architecture
        """
        arduino_type = arduino_type.lower()

        for key in self.__arduino_type_list:
            arduino_arch = search(key, arduino_type)
            if arduino_arch:
                return self.__arduino_type_list[key]

        self.__display_error("Error: the Arduino board architecture is unknown, please contact us to support it")

    def __display_error(self, error):
        if self.__callback_log is not None:
            # self.__callback_log(Message(Message.ERROR_MESSAGE, error))
            print "ERROR: " + error
        else:
            raise UploadArduinoError(error)

    def run(self):
        """
        upload an arduino code to the arduino board
        """

        # get arduino executable path
        if 'nt' in sys.builtin_module_names:
            import _winreg
            arduino_exe = self.__arduino_ui_get_path_windows()

        elif 'posix' in sys.builtin_module_names:
            self.__arduino_ui_is_installed_linux()
            arduino_exe = "arduino"

        else:
            self.__display_error("Error: unsupported OS")

        # test if the file exist
        if not os.path.isfile(self.__arduino_file):
            raise IOError("Error: no such file")

        # get the architecture
        arduino_arch = self.__get_arduino_arch_board(self.__arduino_type)

        # test if serial is reachable
        # exception is thrown else
        try:
            ser = serial.Serial(self.__serial_port, 4600, timeout=1)
            ser.close()
        except serial.SerialException, e:
            self.__display_error("could not open port " + self.__serial_port + " verify your permission")

        # prepare the command
        command = [arduino_exe, '--board', arduino_arch, '--port',
                   self.__serial_port, '--upload', self.__arduino_file]

        # execute and display
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # concat because the ui doesn't like
        # receiving line one after the other
        lines = ""
        for line in iter(proc.stderr.readline, b''):
            lines = lines + line
        # print lines

        # lines = ""
        for line in iter(proc.stdout.readline, b''):
            lines = lines + line
        print lines

        # wait and get the script status
        # print if no callback, else give to callback
        proc.wait()
        if proc.poll() == 0:
            if self.__callback_log is None:
                print "SUCCEED"
            else:
                self.__callback_log(Message(Message.SUCCEED_MESSAGE))
        else:
            if self.__callback_log is None:
                print "SUCCEED"
            else:
                self.__callback_log(Message(Message.ERROR_MESSAGE))

if __name__ == '__main__':
    upload_arduino = UploadArduino("uno", "/dev/ttyACM0", "/home/battosai/Arduino/buzzer/buzzer.ino")
    upload_arduino.start()
