# -*- coding: utf-8 -*-
#
# generated by wxGlade 0.6.8 on Wed Feb 18 22:17:21 2015
#

from __future__ import unicode_literals

import wx

# begin wxGlade: dependencies
import gettext
import urllib
import os
import sys
import subprocess
# end wxGlade

# begin wxGlade: extracode
# end wxGlade
import JsonInoConvertorWithARTKV3 as JsonInoConvertor
import AutoDetectSerial as AutoDetectSerial
import UploadArduino as UploadArduino


class MainWindow(wx.Frame):

    ArduinoSketchPath = str()
    ArduinoExecPath = str()
    ID_REINIT_PARAMETER = wx.NewId()

    def __init__(self, *args, **kwds):
        # begin wxGlade: test3.__init__
        kwds["style"] = (wx.MINIMIZE_BOX |
                         wx.SYSTEM_MENU |
                         wx.CLOSE_BOX |
                         wx.CAPTION |
                         wx.CLIP_CHILDREN)
        wx.Frame.__init__(self, *args, **kwds)
        wx.Frame.SetIcon(self,
                         wx.Icon("res/icon.png", wx.BITMAP_TYPE_PNG, 96, 96))
        self.file = None
        self.bitmap_button_local = wx.BitmapButton(
            self, wx.ID_ANY, wx.Bitmap("res/load_local.png",
                                       wx.BITMAP_TYPE_ANY))

        # Add menu
        parameter_menu = wx.Menu()
        parameter_menu.Append(self.ID_REINIT_PARAMETER, 'Reinit config file',
                              'Reinit configuration file.')
        menu_bar = wx.MenuBar()
        menu_bar.Append(parameter_menu, 'Parameters')
        self.SetMenuBar(menu_bar)
        wx.EVT_MENU(self, self.ID_REINIT_PARAMETER, self.reinitConfiguration)
        # self.bitmap_button_web = wx.BitmapButton(
        #    self, wx.ID_ANY, wx.Bitmap("res/load_web.png",
        #                               wx.BITMAP_TYPE_ANY))
        self.label_1 = wx.StaticText(
            self, wx.ID_ANY, (u"No file loaded"))
        self.radio_box_1 = wx.RadioBox(
            self, wx.ID_ANY,
            ("Arduino type"),
            choices=[("Uno"), ("Other")],
            majorDimension=2,
            style=wx.RA_SPECIFY_ROWS)
        self.bitmap_button_1 = wx.BitmapButton(
            self, wx.ID_ANY, wx.Bitmap("res/go.png", wx.BITMAP_TYPE_ANY))
        self.label_3 = wx.StaticText(
            self, wx.ID_ANY, (u"No file sended"))

        self.initConfiguration()
        self.__set_properties()
        self.__do_layout()

        self.Bind(
            wx.EVT_BUTTON, self.OnChargementLocal, self.bitmap_button_local)
        # self.Bind(wx.EVT_BUTTON, self.OnChargementWeb,
        #          self.bitmap_button_web)
        self.Bind(wx.EVT_BUTTON, self.TypeArduino, self.radio_box_1)
        self.Bind(wx.EVT_BUTTON, self.OnUpload, self.bitmap_button_1)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: test3.__set_properties
        self.SetTitle(("ScratchV2 To Ino"))
        self.bitmap_button_local.SetMinSize((240, 240))
        # self.bitmap_button_web.SetMinSize((140, 140))
        self.radio_box_1.SetSelection(0)
        self.bitmap_button_1.SetSize(self.bitmap_button_1.GetBestSize())
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: test3.__do_layout
        sizer_13 = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_1 = wx.FlexGridSizer(4, 1, 0, 0)
        sizer_15 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_14 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_14.Add(self.bitmap_button_local, 0, wx.ALL, 10)
        # sizer_14.Add(self.bitmap_button_web, 0, wx.ALL, 10)
        grid_sizer_1.Add(sizer_14, 1, wx.EXPAND, 0)
        grid_sizer_1.Add(
            self.label_1, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 20)
        sizer_1.Add(
            self.radio_box_1, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 15)
        sizer_1.Add(self.bitmap_button_1, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer_15.Add(sizer_1, 1, wx.EXPAND, 0)
        grid_sizer_1.Add(sizer_15, 1, wx.EXPAND, 0)
        grid_sizer_1.Add(
            self.label_3, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 15)
        sizer_13.Add(grid_sizer_1, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_13)
        sizer_13.Fit(self)
        self.Layout()
        # end wxGlade

    def OnChargementLocal(self, event):  # wxGlade: test3.<event_handler>
        # print "Event handler 'OnChargementLocal' not implemented!"
        dlg = wx.FileDialog(
            self, "Open ScratchV2 project", os.getcwd(), "",
            "*.sb2", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            mypath = os.path.basename(path)
            chemin = dlg.GetDirectory()
            # print (chemin)
            self.file = chemin + '/' + mypath
            # print (self.file)
            # self.SetStatusText("You selected: %s" % mypath)
            chaine_charge = mypath + ' is charged   '
            # self.label_1.SetMinSize((200, 20))
            # grid_sizer_1.Add(
            #    self.label_1,
            #    0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL |
            #    wx.ALIGN_CENTER_VERTICAL, 10)
            self.label_1.SetLabel(chaine_charge)
        dlg.Destroy()

    def OnChargementWeb(self, event):  # wxGlade: test3.<event_handler>
        # print "Event handler 'OnChargementWeb' not implemented!"
        dlg = wx.TextEntryDialog(self, 'Enter your url', 'download')
        dlg.SetValue("http://")
        if dlg.ShowModal() == wx.ID_OK:
            # self.SetStatusText('You entered: %s\n' % dlg.GetValue())
            # print (dlg.GetValue())
            download(dlg.GetValue(), ExtractionDuNom(dlg.GetValue()))
            self.file = ExtractionDuNom(dlg.GetValue())
            chaine_charge = self.file + ' is charged    '
            self.label_1.SetLabel(chaine_charge)
        dlg.Destroy()
        # event.Skip()

    def OnUpload(self, event):
        if (self.file is None):
            return
        TypeArduino = 0
        if self.radio_box_1.GetStringSelection() == "Other":
            TypeArduino = 1
        fileName = ExtractionDuNomNoExtension(self.file)
        if not os.path.exists(self.ArduinoSketchPath + os.sep + fileName):
            os.makedirs(self.ArduinoSketchPath + os.sep + fileName)
        convertor = JsonInoConvertor.JsonInoConvertor(typeArduino=TypeArduino)
        try:
            convertor.convertSpriteScripts(self.file,
                                           self.ArduinoSketchPath + os.sep +
                                           fileName + os.sep +
                                           fileName + ".ino")
            self.label_3.SetLabel(fileName + " is parsed")


            # call serial port detection
            # then upload on the arduino card

            autoDetectSerial = AutoDetectSerial.AutoDetectSerial()
            arduinoSerial = autoDetectSerial.getArduinosPath()

            if autoDetectSerial == []:
                print "Error, no arduino board is connected"
                sys.exit(1)

            # take the first board connected
            arduinoSerial = arduinoSerial[0]

            filePath = self.ArduinoSketchPath + os.sep +\
                fileName + os.sep + fileName + ".ino"

            uploadArduino = UploadArduino.UploadArduino()
            uploadArduino.upload(arduinoSerial[1], arduinoSerial[0], filePath)


            # try:
            #     filePath = self.ArduinoSketchPath + os.sep +\
            #         fileName + os.sep + fileName + ".ino"
            #     if sys.platform == "win32":
            #         os.startfile(filePath)
            #     else:
            #         subprocess.call([self.ArduinoExecPath, filePath])
            # except:
            #     wx.MessageBox("Can't open automatically .ino file.", 'Warning',
            #                   wx.OK | wx.ICON_EXCLAMATION)
        except Exception as expt:
            error = str()
            for mess in expt.args:
                error += mess + " "
            wx.MessageBox(error, 'Error',
                          wx.OK | wx.ICON_ERROR)
            self.label_3.SetLabel(fileName + " error parsing")
        finally:
            del convertor
            convertor = None

        # commande1 = "JsonInoConvertorWithARTKV3.py " + \
        #     self.file + " " + TypeArduino
        # commande1 = commande1.encode('utf-8')
        # os.system(commande1)
        # event.Skip()

    def TypeArduino(self, event):
        print self.radio_box_1.GetStringSelection()
        event.Skip()

    def initConfiguration(self):
        if os.path.isfile(".config"):
            # read data from .config
            # Lines beginning with # are comment
            # Other are in the form KEY=value
            configFile = open(".config", "r")
            for line in configFile:
                line = line.rstrip('\n')
                if not (line[0] == "#"):
                    if "ARDUINO_SKETCH_PATH=" in line:
                        self.ArduinoSketchPath = line[20:]
                    elif "ARDUINO_EXEC_PATH=" in line:
                        self.ArduinoExecPath = line[18:]
            configFile.close()
        else:
            configFile = open(".config", "w")
            dlg = wx.DirDialog(self, "Select Arduino Sketch Folder",
                               style=1, defaultPath=os.getcwd())
            if dlg.ShowModal() == wx.ID_OK:
                self.ArduinoSketchPath = dlg.GetPath()
                path = dlg.GetPath()
                mypath = os.path.basename(path)
                self.ArduinoSketchPath = path
                configFile.write("# Arduino sketch path\n")
                configFile.write("ARDUINO_SKETCH_PATH=" +
                                 self.ArduinoSketchPath + "\n")
            dlg = wx.FileDialog(self, "Select Arduino IDE executable",
                                os.getcwd(), "", "*", wx.OPEN)
            if dlg.ShowModal() == wx.ID_OK:
                path = dlg.GetPath()
                mypath = os.path.basename(path)
                chemin = dlg.GetDirectory()
                self.ArduinoExecPath = chemin + os.sep + mypath
                configFile.write("# Arduino Exec path\n")
                configFile.write("ARDUINO_EXEC_PATH=" +
                                 self.ArduinoExecPath + "\n")
            configFile.close()
        print "ARDUINO_EXEC_PATH=" + self.ArduinoExecPath
        print "ARDUINO_SKETCH_PATH=" + self.ArduinoSketchPath

    def reinitConfiguration(self, event):
        if os.path.isfile(".config"):
            os.remove(".config")
        self.initConfiguration()


# end of class test3
def download(url, dest):
    dlg = wx.ProgressDialog("Download Progress",
                            "Please wait...",
                            style=wx.PD_CAN_ABORT |
                            wx.PD_APP_MODAL |
                            wx.PD_ELAPSED_TIME | wx.PD_ESTIMATED_TIME)
    dlg.Update(0, "Please Wait...")
    fURL = urllib.urlopen(url)
    header = fURL.info()
    size = None
    max = 100
    outFile = open(dest, 'wb')
    keepGoing = True
    if "Content-Length" in header:
        size = int(header["Content-Length"])
        kBytes = size / 1024
        downloadBytes = size / max
        count = 0
        while keepGoing:
            count += 1
            if count >= max:
                count = 99
                (keepGoing, skip) = dlg.Update(
                    count,
                    "Downloaded " +
                    str(count * downloadBytes / 1024) +
                    " of " + str(kBytes) +
                    "KB")
            b = fURL.read(downloadBytes)
            if b:
                outFile.write(b)
            else:
                break
    else:
        while keepGoing:
            (keepGoing, skip) = dlg.UpdatePulse()
            b = fURL.read(1024 * 8)
            if b:
                outFile.write(b)
            else:
                break
    outFile.close()

    dlg.Update(99, "Downloaded " + str(os.path.getsize(dest) / 1024) + "KB")
    dlg.Destroy()
    return keepGoing
    # end dowload


def ExtractionDuNom(lien):
    taille = len(lien) - 1
    nomFile = ""

    while taille > 0:
        if lien[taille] == "/":
            break
        taille = taille - 1

    while taille < len(lien) - 1:
        nomFile = nomFile + lien[taille + 1]
        taille = taille + 1
        print (taille)

    return nomFile


def ExtractionDuNomNoExtension(lien):
    taille = len(lien) - 1
    nomFile = ""

    while taille > 0:
        if lien[taille] == "/":
            break
        taille = taille - 1

    while taille < len(lien) - 5:
        nomFile = nomFile + lien[taille + 1]
        taille = taille + 1
        print (taille)

    return nomFile

if __name__ == "__main__":
    gettext.install("app")  # replace with the appropriate catalog name

    app = wx.App(0)
    # wx.InitAllImageHandlers()
    mainWindow = MainWindow(None, wx.ID_ANY, "")
    app.SetTopWindow(mainWindow)
    mainWindow.Show()
    app.MainLoop()
