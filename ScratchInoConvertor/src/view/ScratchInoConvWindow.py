#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import wx
import gettext
import controller.Controller as Controller


class ScratchInoConvWindow(wx.Frame):
    def __init__(self, controller, *args, **kwds):
        if not isinstance(controller, Controller.Controller):
            raise ValueError("Error: a Controller object is expected")

        # Set attribut
        self.controller = controller
        self.__scratch_file = None

        # WX
        # kwds["style"] = (wx.MINIMIZE_BOX |
        #                  wx.SYSTEM_MENU |
        #                  wx.CLOSE_BOX |
        #                  wx.CAPTION |
        #                  wx.CLIP_CHILDREN)
        wx.Frame.__init__(self,
                          None,
                          -1,
                          "ScratchV2 To Ino",
                          style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.CAPTION | wx.CLIP_CHILDREN)

        wx.Frame.SetIcon(self,
                         wx.Icon("view/res/icon.png", wx.BITMAP_TYPE_PNG, 96, 96))

        # self.SetTitle(("ScratchV2 To Ino"))
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
        console = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.__text_scratch_file = wx.TextCtrl(self, wx.ID_ANY, "", size=(-1, 30), style=wx.TE_READONLY)

        # Choice
        choice_board_type = wx.ListBox(self, wx.ID_ANY, size=(-1, 30), choices=[])
        # list_box_serial_port = wx.ListBox(self, wx.ID_ANY, [], wx.LB_SINGLE)

        # add to container
        # line 1
        bag_sizer.Add(label_scratch_file, pos=(0, 0))
        bag_sizer.Add(self.__text_scratch_file, pos=(0, 1), flag=wx.EXPAND)
        bag_sizer.Add(button_browse_scratch_file, pos=(0, 2))

        # line 2
        bag_sizer.Add(label_board_type, pos=(1, 0))
        bag_sizer.Add(choice_board_type, pos=(1, 1), span=(1, 2), flag=wx.EXPAND)

        # line 3
        bag_sizer.Add(label_status, pos=(2, 0))
        bag_sizer.Add(self.__label_status_msg, pos=(2, 1), span=(1, 2), flag=wx.EXPAND)

        # line 4
        bag_sizer.Add(button_start_upload, pos=(3, 0), span=(1, 3), flag=wx.EXPAND)

        # line 5
        console_panel.Add(console, 1, wx.EXPAND)

        # grow able col
        bag_sizer.AddGrowableCol(1)

        frame_sizer.Add(bag_sizer, 0, wx.EXPAND)
        frame_sizer.Add(console_panel, 1, wx.EXPAND)

        self.SetSizer(frame_sizer)
        frame_sizer.SetSizeHints(self)
        self.SetSize((400, 150))
        self.Fit()

    # EVENT FUNCTION
    def __set_arduino_type(self, event):
        self.__radio_box_arduino_type.GetStringSelection()
        event.Skip()

    def __choose_file(self, event):
        dlg = wx.FileDialog(
            self, "Open ScratchV2 project", os.getcwd(), "", "*.sb2", wx.OPEN)

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            file_name = os.path.basename(path)
            folder_name = dlg.GetDirectory()

            self.__scratch_file = folder_name + os.sep + file_name
            new_label_value = file_name + ' is charged   '
            self.__text_scratch_file.SetValue(path)
        dlg.Destroy()
        self.Layout()

    def __scratch_into_arduino(self, event):
        if self.__scratch_file is None:
            wx.MessageBox("Please set a file", 'Error',
                          wx.OK | wx.ICON_ERROR)

        else:
            # arduino_type = 1 if self.__radio_box_arduino_type.GetStringSelection() == "Other" else 0
            self.controller.scratch_into_arduino(self.__scratch_file, 0)

    # PATTERN OBSERVER
    def notify(self, err, error_msg=""):
        print "here"
        if err:
            self.__label_status_msg.SetLabel(error_msg)
        else:
            self.__label_status_msg.SetLabel("Succeed")
        self.Layout()


if __name__ == "__main__":
    gettext.install("app")  # replace with the appropriate catalog name

    app = wx.App(0)
    # wx.InitAllImageHandlers()
    mainWindow = ScratchInoConvWindow("", None, wx.ID_ANY, "")
    app.SetTopWindow(mainWindow)
    mainWindow.Show()
    app.MainLoop()
