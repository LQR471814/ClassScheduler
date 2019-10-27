#--------------------------------------------------#
# Credit to Libraries that I used:                 #
#                                                  #
# WxPython: www.wxpython.org                       #
# sys: Part of the standard python libraries       # 
#      https://docs.python.org/3/py-modindex.html  #
# threading: Part of the standard python libraries #
#      https://docs.python.org/3/py-modindex.html  #
# json: Part of the standard python libraries      #
#      https://docs.python.org/3/py-modindex.html  #
#--------------------------------------------------#

import wx
import sys
import threading
import json

#? List Order:
#? Name, Class, Elective

#! GUI Code
class mainBox(wx.Frame):
    def __init__(self, title):

        wx.Frame.__init__(self, None, title=title, pos=(50, 50), size=(640, 480))
        panel = wx.Panel(self, -1)
        panel.Layout()
        self.SetBackgroundColour("WHITE")
        self.Bind(wx.EVT_CLOSE, self.OnClosed)
    
    def OnClosed(self, event):
        self.Destroy()

#! Command functions
def console():
    global commands
    global HelpMenu
    global Usage
    while True:
        UserInp = input(" > ")
        for command in commands:
            if UserInp == command:
                commands[command]()
                break

def settingsFunc():
    with open("settings.json") as settings_file:
        settings = json.load(settings_file)
        for SettingNo in settings["settings"]:
            for setting in SettingNo:
                print(setting + ": " + str(SettingNo[setting]))
        # print("Input the new value for a setting #. ([Setting#]-[New Value])")
        # NewValue = input(" > ")

def helpFunc():
    global HelpMenu
    print(HelpMenu)

def guiFunc():
    #TODO: Finish the damn GUI
    print("Code for the GUI is there, but is currently too unstable to actually do anything, will continue after program is finished.")
    # app = wx.App(False)
    # frame = mainBox("GUI")
    # frame.Show(True)
    # app.MainLoop()

def startFunc():
    global Usage
    global path

    f = ""
    fObj = None
    InpTable = []
    DataTable = {}
    #? Get input
    print(Usage)
    print("Please input the full path of the .csv file! (ex. C:\\Users\\Joe\\Documents\\class.csv or ~/Downloads/class.csv)")
    path = input(" @: ")
    if path != "test": #? DEBUG
        try:
            fObj = open(path, "r")
        except:
            print("That isn't a valid path!")
            return
    else: #? DEBUG
        fObj = open("C:\\Users\\Sid\\Documents\\Codes\\Scheduler\\test.csv", "r")
    f = fObj.read()
    InpTable = f.split("\n")
    for i in range(len(InpTable)):
        InpTable[i] = InpTable[i].split(",")
    for i in range(len(InpTable)):
        DataTable[InpTable[i][0]] = InpTable[i][1]
    for row in DataTable:
        print(row + ": " + DataTable[row])
    

def quitFunc():
    sys.exit(0)

#! Variables

path = ""

commands = {"help":helpFunc,
            "gui":guiFunc,
            "start":startFunc,
            "quit":quitFunc,
            "settings":settingsFunc
            }

HelpMenu = """
 ------------ <HELP> ------------
 > help: Show this menu
 > gui: Enable experimental GUI
 > start: Starts the program
 > settings: Shows the settings.
 > quit: Quits the control shell
"""
Usage = """
 ------------ <How to get a CSV file!> ------------
- Get your excel document
- Go to file
- Save as
- There should be a dropdown menu where you 
    can see what file extensions you can
    save the file as.
- Select .csv file extension.
- Choose a location to save your file.
"""

#! Initalize: Threads and other.

print(HelpMenu)

t1 = threading.Thread(target=console)
t1.start()