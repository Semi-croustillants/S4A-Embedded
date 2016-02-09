#!/bin/python2.7
# coding=utf-8

import subprocess
import re
import sys
import serial.tools.list_ports


class AutoDetectSerialError(Exception):
    pass


class AutoDetectSerial(object):

    def __init__(self):
        pass

    def __get_usb_devices_linux(self):
        '''
        get usb devices information with a shell script
        :return: [ "usb device information" ]
        '''
        proc = subprocess.Popen('./model/getUsbDevices.sh', stdout=subprocess.PIPE)
        usb_device_tmp = proc.stdout.read()
        usb_device = usb_device_tmp.split("\n")
        return usb_device

    def __get_arduinos_path_linux(self):

        '''
        get arduinos information on linux system
        comment:
            serial.tools.list_ports.comports():
                can retun "none" for arduino description
                that's why we call a shell script
        :return: [ ( "arduino path", "arduino description") ]
        '''

        usb_devices = self.__get_usb_devices_linux()
        arduino_devices = []
        for usb_device in usb_devices:
            usb_arduino_devices_found = re.findall(
                '(\/dev\/.*) -(.*Arduino.*)', usb_device)
            if usb_arduino_devices_found != []:
                arduino_devices.append(usb_arduino_devices_found[0])
        return arduino_devices

    def __get_arduino_path_windows(self):

        '''
        get arduinos information on windows system
        :return: [ ( "arduino path", "arduino description") ]
        '''
        devices = list(serial.tools.list_ports.comports())

        arduino_devices = []

        for device in devices:
            if device[1].startswith("Arduino"):
                arduino_devices.append((device[0], device[1]))
        return arduino_devices

    def get_arduinos_path(self):
        '''
        get arduinos information, description content depends on OS
        :return: [ ( "arduino path", "arduino description") ]
        '''
        arduino_paths = []
        if sys.platform.startswith('linux'):
            print "_linux"
            arduino_paths = self.__get_arduinos_path_linux()

        elif sys.platform.startswith('win'):
            print "_windows"
            arduino_paths = self.__get_arduino_path_windows()

        if arduino_paths == []:
            raise AutoDetectSerialError("Error: no Arduino board is connected")

        return arduino_paths


if __name__ == '__main__':
    auto_detect_serial = AutoDetectSerial()
    arduino_serial = auto_detect_serial.get_arduinos_path()
    arduino_serial = arduino_serial[0]
    print arduino_serial[0], arduino_serial[1]
