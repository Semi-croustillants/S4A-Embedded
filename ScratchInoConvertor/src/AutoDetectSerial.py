#!/bin/python2.7
# coding=utf-8

import subprocess
import re
import sys
import serial.tools.list_ports


class AutoDetectSerial(object):

    def __init__(self):
        pass

    def __getUsbDevicesLinux(self):
        '''
        get usb devices information with a shell script
        :return: [ "usb device information" ]
        '''
        proc = subprocess.Popen('./getUsbDevices.sh', stdout=subprocess.PIPE)
        usbDeviceTmp = proc.stdout.read()
        usbDevice = usbDeviceTmp.split("\n")

        return usbDevice

    def __getArduinosPathLinux(self):

        '''
        get arduinos information on linux system
        comment:
            serial.tools.list_ports.comports():
                can retun "none" for arduino description
                that's why we call a shell script
        :return: [ ( "arduino path", "arduino description") ]
        '''

        usbDevices = self.__getUsbDevicesLinux()
        arduinoDevices = []
        for usbDevice in usbDevices:
            usbArduinoDevicesFound = re.findall('(\/dev\/.*) -(.*Arduino.*)', usbDevice)
            if usbArduinoDevicesFound != []:
                arduinoDevices.append(usbArduinoDevicesFound[0])
        return arduinoDevices

    def __getArduinoPathWindows(self):

        '''
        get arduinos information on windows system
        :return: [ ( "arduino path", "arduino description") ]
        '''
        devices = list(serial.tools.list_ports.comports())

        arduinoDevices = []

        for device in devices:
            if device[1].startswith("Arduino"):
                arduinoDevices.append((device[0], device[1]))
        return arduinoDevices


    def getArduinosPath(self):
        '''
        get arduinos information, description content depends on OS
        :return: [ ( "arduino path", "arduino description") ]
        '''
        if sys.platform.startswith('linux'):
            print "Linux"
            return self.__getArduinosPathLinux()

        elif sys.platform.startswith('win'):
            print "Windows"
            return self.__getArduinoPathWindows()


if __name__ == '__main__':
    autoDetectSerial = AutoDetectSerial()
    print autoDetectSerial.getArduinosPath()

    arduinoSerial = autoDetectSerial.getArduinosPath()
    arduinoSerial = arduinoSerial[0]
    print arduinoSerial[0], arduinoSerial[1]
