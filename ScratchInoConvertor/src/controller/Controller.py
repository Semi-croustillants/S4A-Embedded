#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import model.ScratchInoConv as ScratchInoConv


class Controller(object):

    def __init__(self, scratch_ino_conv):
        if not isinstance(scratch_ino_conv, ScratchInoConv.ScratchInoConv):
            raise ValueError("Error: a ScratchInoConv object is expected")
        self.__scratch_ino_conv = scratch_ino_conv

    def scratch_into_arduino(self, scratch_file, arduino_type):
        self.__scratch_ino_conv.scratch_into_arduino(scratch_file, arduino_type)
