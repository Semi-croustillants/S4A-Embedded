#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import gettext
import wx
import sys

import controller.Controller as Controller
import model.ScratchInoConv as ScratchInoConv
import view.ScratchInoConvWindow as ScratchInoConvWindow


def display_help():
    print "Main.py [OPTION]"
    print "  OPTION LIST:"
    print "      --UI               launch Scratch ino convertor UI"
    print "      -c, --command-line scratch_file [arduino_type]"
    print "                       launch Scratch ino convertor in command line"
    print "                         arduino_type: 0 if uno, 1 else"
    print "      -h,   --help       display this help"

if __name__ == "__main__":
    for arg in sys.argv:
        print arg
    if len(sys.argv) > 1:
        if sys.argv[1] == "--UI":
            # scratch_ino_conv = ScratchInoConv.ScratchInoConv()
            # scratch_ino_conv.scratch_into_arduino("/home/battosai/Documents/Scratch_Projects/buzzer.sb2")
            scratch_ino_conv = ScratchInoConv.ScratchInoConv()
            controller = Controller.Controller(scratch_ino_conv)
            gettext.install("app")  # replace with the appropriate catalog name

            app = wx.App(0)
            # wx.InitAllImageHandlers()
            mainWindow = ScratchInoConvWindow.ScratchInoConvWindow(
                controller, None, wx.ID_ANY, "")
            app.SetTopWindow(mainWindow)
            mainWindow.Show()
            scratch_ino_conv.add_observer(mainWindow)
            app.MainLoop()
        elif sys.argv[1] in ("-h", "--help"):
            display_help()

        elif sys.argv[1] in ("-c", "--command-line"):
            scratch_file = ""
            arduino_type = 0
            if len(sys.argv) >= 3:
                scratch_file = sys.argv[2]

            if len(sys.argv) == 4:
                arduino_type = sys.argv[3]

            if len(sys.argv) < 4:
                raise ValueError("Error: not enough argument")

            if len(sys.argv) > 5:
                raise ValueError("Error: too many arguments")
            scratch_ino_conv = ScratchInoConv.ScratchInoConv()
            scratch_ino_conv.scratch_into_arduino(scratch_file, arduino_type)

    else:
        raise ValueError("Error: not enough argument")
