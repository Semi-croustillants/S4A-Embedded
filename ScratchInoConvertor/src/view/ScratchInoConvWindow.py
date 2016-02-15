#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os

import sys
import wx
import gettext
from threading import Thread
import controller.Controller as Controller
from model.Message import Message


class ScratchInoConvWindow(wx.Frame):
    def __init__(self, controller, *args, **kwds):
        if not isinstance(controller, Controller.Controller):
            raise ValueError("Error: a Controller object is expected")

        # Set attribut
        self.controller = controller
        self.__scratch_file = None

        # WX
        wx.Frame.__init__(self,
                          None,
                          -1,
                          "ScratchV2 To Ino",
                          style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.CAPTION | wx.CLIP_CHILDREN)

        wx.Frame.SetIcon(self, wx.Icon("view/res/icon.png", wx.BITMAP_TYPE_PNG, 96, 96))
        self.__set_layout()

    def __set_layout(self):
        # main container
        frame_sizer = wx.BoxSizer(wx.VERTICAL)

        # panel
        bag_sizer = wx.GridBagSizer(hgap=5, vgap=5)
        console_panel = wx.BoxSizer(wx.VERTICAL)

        # label
        label_scratch_file = wx.StaticText(self, wx.ID_ANY, (u"Scratch File:"), size=(100, 30))
        label_board_type = wx.StaticText(self, wx.ID_ANY, (u"Board Type:"), size=(100, 30))
        label_status = wx.StaticText(self, wx.ID_ANY, (u"Status:"), size=(100, 30))
        self.__label_status_msg = wx.StaticText(self, wx.ID_ANY, (u"Not Started Yet"), size=(100, 30))
        # label_serial_port = wx.StaticText(self, wx.ID_ANY, (u"Serial Port:"))

        # button
        button_browse_scratch_file = wx.Button(self, 1, "Browse", size=(100, 30))
        # button_refresh_port = wx.Button(self, 2, "Refresh")
        button_start_upload = wx.Button(self, 3, "Start Upload", size=(-1, 30))

        # button event
        button_browse_scratch_file.Bind(wx.EVT_BUTTON, self.__choose_file)
        button_start_upload.Bind(wx.EVT_BUTTON, self.__scratch_into_arduino)

        # input text
        self.__console = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH)
        self.__text_scratch_file = wx.TextCtrl(self, wx.ID_ANY, "", size=(-1, 30), style=wx.TE_READONLY)

        # sys.stderr = self.__console
        sys.stdout = self.__console

        # Choice
        self.__choice_board_type = wx.ComboBox(self, wx.ID_ANY, size=(-1, 30),
                                               choices=["Uno", "Others"], style=wx.TE_READONLY)
        # list_box_serial_port = wx.ListBox(self, wx.ID_ANY, [], wx.LB_SINGLE)

        # add to container
        # line 1
        bag_sizer.Add(label_scratch_file, pos=(0, 0))
        bag_sizer.Add(self.__text_scratch_file, pos=(0, 1), flag=wx.EXPAND)
        bag_sizer.Add(button_browse_scratch_file, pos=(0, 2))

        # line 2
        bag_sizer.Add(label_board_type, pos=(1, 0))
        bag_sizer.Add(self.__choice_board_type, pos=(1, 1), span=(1, 2), flag=wx.EXPAND)

        # line 3
        bag_sizer.Add(label_status, pos=(2, 0))
        bag_sizer.Add(self.__label_status_msg, pos=(2, 1), span=(1, 2), flag=wx.EXPAND)

        # line 4
        bag_sizer.Add(button_start_upload, pos=(3, 0), span=(1, 3), flag=wx.EXPAND)

        # line 5
        console_panel.Add(self.__console, 1, wx.EXPAND)

        # grow able col
        bag_sizer.AddGrowableCol(1)

        frame_sizer.Add(bag_sizer, 0, wx.EXPAND)
        frame_sizer.Add(console_panel, 1, wx.EXPAND)

        self.SetSizer(frame_sizer)
        frame_sizer.SetSizeHints(self)
        self.SetSize((400, 150))
        self.Fit()

    def __write_in_console(self, code, message):
        """
        write a message in the console
        :param code: Message.CONSOLE_LOG => white | Message.CONSOLE_LOG_ERR => red
        :param message:
        :return:
        """
        self.__console.SetForegroundColour(wx.WHITE)
        if code == Message.CONSOLE_LOG:
            self.__console.AppendText(message)
        elif code == Message.CONSOLE_LOG_ERR:
            self.__console.SetForegroundColour(wx.RED)
            self.__console.AppendText(message)

    # EVENT FUNCTION
    def __choose_file(self, event):
        """
        allow user to choose a scratch file
        :param event:
        :return:
        """

        # choose the file
        dlg = wx.FileDialog(self, "Open ScratchV2 project", os.getcwd(), "", "*.sb2", wx.OPEN)

        if dlg.ShowModal() == wx.ID_OK:
            # get the path
            path = dlg.GetPath()
            self.__scratch_file = path

            # display it
            self.__text_scratch_file.SetValue(path)
        dlg.Destroy()

        # refresh the view
        self.Layout()

    def __scratch_into_arduino(self, event):
        """
        launch the upload
        :param event:
        :return:
        """
        if self.__scratch_file is None:
            wx.MessageBox("Please set a file", 'Error',
                          wx.OK | wx.ICON_ERROR)

        else:
            self.__label_status_msg.SetLabel("In Progress...")
            self.__console.AppendText("\n=========== START UPLOAD ===========\n")
            Thread(target=self.controller.scratch_into_arduino(self.__scratch_file,
                                                               self.__choice_board_type.GetCurrentSelection())).start()

    # PATTERN OBSERVER
    def notify(self, message):
        """
        receive a notification from the observable object
        :param message: Message(code, Message), see Message class
        :return:
        """

        if not isinstance(message, Message):
            raise ValueError("Error: a Message object is expected")

        if message.code == Message.SUCCEED_MESSAGE:
            self.__label_status_msg.SetForegroundColour(wx.GREEN)
            self.__label_status_msg.SetLabel("Succeed")
        elif message.code == Message.ERROR_MESSAGE:
            self.__label_status_msg.SetForegroundColour(wx.RED)
            self.__label_status_msg.SetLabel("Error")
            self.__write_in_console(message.code, message.message)

        elif message.code == Message.CONSOLE_LOG:
            self.__write_in_console(message.code, message.message)

        elif message.code == Message.CONSOLE_LOG_ERR:
            self.__write_in_console(message.code, message.message)

        self.Layout()


if __name__ == "__main__":
    gettext.install("app")  # replace with the appropriate catalog name

    app = wx.App(0)
    # wx.InitAllImageHandlers()
    mainWindow = ScratchInoConvWindow("", None, wx.ID_ANY, "")
    app.SetTopWindow(mainWindow)
    mainWindow.Show()
    app.MainLoop()
