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
import serial


class UploadArduinoError(Exception):
    pass


class UploadArduino:

    def __init__(self):
        # TODO link every board name to package:arch:board
        # https://github.com/arduino/_arduino/blob/ide-1.5.x/build/shared/manpage.adoc
        self.__arduino_type = {"uno": "arduino:avr:uno"}
        pass

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
            raise UploadArduinoError("Error: Arduino UI is not installed, please install it")

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
                raise UploadArduinoError("Error: Arduino UI is not installed, please install it")
        return val + "\\arduino.exe"

    def __get_arduino_arch_board(self, arduino_type):
        """
        get the architecture board
        :param arduino_type: the arduino type
        :return: the architecture
        """
        arduino_type = arduino_type.lower()

        for key in self.__arduino_type:
            arduino_arch = search(key, arduino_type)
            if arduino_arch:
                return self.__arduino_type[key]

        raise UploadArduinoError("Error: the Arduino board architecture is unknown, please contact us to support it")

    def upload(self, arduino_type, serial_port, arduinofile):
        """
        upload an arduino code to the arduino board
        :param arduino_type: the arduino model: uno, mega…
        :param serial_port: the serial port where the arduino board is connected
        :param arduinofile: the arduino code to upload
        """

        print arduino_type, serial_port, arduinofile

        # get arduino executable path
        if 'nt' in sys.builtin_module_names:
            import _winreg
            arduino_exe = self.__arduino_ui_get_path_windows()
        elif 'posix' in sys.builtin_module_names:
            self.__arduino_ui_is_installed_linux()
            arduino_exe = "arduino"
        else:
            raise UploadArduinoError("Error: unsupported OS")

        # test if the file exist
        if not os.path.isfile(arduinofile):
            raise IOError("Error: no such file")

        # get the architecture
        arduino_arch = self.__get_arduino_arch_board(arduino_type)

        # test if serial is reachable
        # exception is thrown else
        ser = serial.Serial(serial_port, 4600, timeout=1)
        ser.close()

        # prepare the command
        command = [arduino_exe, '--board', arduino_arch, '--port',
                   serial_port, '--upload', arduinofile]

        # execute and display
        proc = subprocess.Popen(command, stdout=subprocess.PIPE)
        proc_stdout = proc.stdout.read()

        print proc_stdout

if __name__ == '__main__':
    upload_arduino = UploadArduino()
    upload_arduino.upload("uno", "/dev/ttyACM0", "/home/battosai/Arduino/buzzer/buzzer.ino")
    # upload_arduino.upload("uno", "COM5", "D:\\Mes Documents\\Arduino\\buzzer\\buzzer.ino")
