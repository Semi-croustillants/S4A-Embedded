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
        kwds["style"] = (wx.MINIMIZE_BOX |
                         wx.SYSTEM_MENU |
                         wx.CLOSE_BOX |
                         wx.CAPTION |
                         wx.CLIP_CHILDREN)
        wx.Frame.__init__(self, *args, **kwds)
        wx.Frame.SetIcon(self,
                         wx.Icon("view/res/icon.png", wx.BITMAP_TYPE_PNG, 96, 96))

        self.SetTitle(("ScratchV2 To Ino"))
        self.__set_layout()

    def __set_layout(self):
        # main container
        frame_sizer = wx.BoxSizer(wx.VERTICAL)
        grid_sizer = wx.FlexGridSizer(5, 1, 1, 1)

        # label
        self.__label_file_loaded = wx.StaticText(self, wx.ID_ANY, (u"No file loaded"))
        self.__label_status_conv = wx.StaticText(self, wx.ID_ANY, (u"No file sent"))

        # button
        bitmap_button_launch_conv = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap("view/res/go.png"))

        bitmap_button_load_file = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap("view/res/load_local.png"))
        bitmap_button_load_file.SetMinSize((240, 240))

        # button event
        self.Bind(wx.EVT_BUTTON, self.__choose_file, bitmap_button_load_file)
        self.Bind(wx.EVT_BUTTON, self.__scratch_into_arduino, bitmap_button_launch_conv)

        # radio button
        self.__radio_box_arduino_type = wx.RadioBox(
            self, wx.ID_ANY,
            ("Arduino type"),
            choices=[("Uno"), ("Other")],
            majorDimension=2,
            style=wx.RA_SPECIFY_ROWS)
        self.__radio_box_arduino_type.SetSelection(0)

        # radio button event
        self.Bind(wx.EVT_BUTTON, self.__set_arduino_type, self.__radio_box_arduino_type)

        # add to container
        grid_sizer.Add(bitmap_button_load_file, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 15)
        grid_sizer.Add(self.__label_file_loaded, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 15)
        grid_sizer.Add(self.__radio_box_arduino_type, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 15)
        grid_sizer.Add(bitmap_button_launch_conv, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 15)
        grid_sizer.Add(self.__label_status_conv, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 15)

        frame_sizer.Add(grid_sizer, proportion=1, flag=wx.ALL | wx.ALIGN_CENTER_HORIZONTAL)
        self.SetSizer(frame_sizer)
        frame_sizer.SetSizeHints(self)
        self.SetSize((400, 150))

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
            self.__label_file_loaded.SetLabel(new_label_value)
        dlg.Destroy()
        self.Layout()

    def __scratch_into_arduino(self, event):
        if self.__scratch_file is None:
            wx.MessageBox("Please set a file", 'Error',
                          wx.OK | wx.ICON_ERROR)

        else:
            arduino_type = 1 if self.__radio_box_arduino_type.GetStringSelection() == "Other" else 0
            self.controller.scratch_into_arduino(self.__scratch_file, arduino_type)

    # PATTERN OBSERVER
    def notify(self, err, error_msg=""):
        print "here"
        if err:
            self.__label_status_conv.SetLabel(error_msg)
        else:
            self.__label_status_conv.SetLabel("Succeed")
        self.Layout()

if __name__ == "__main__":
    gettext.install("app")  # replace with the appropriate catalog name

    app = wx.App(0)
    # wx.InitAllImageHandlers()
    mainWindow = ScratchInoConvWindow("", None, wx.ID_ANY, "")
    app.SetTopWindow(mainWindow)
    mainWindow.Show()
    app.MainLoop()