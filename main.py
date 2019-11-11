#--------------------------------------------------#
# Credit to Libraries that I used:                 #
#                                                  #
# WxPython(GUI programming): www.wxpython.org      #
# sys(sys): Part of the standard python libraries  # 
#      https://docs.python.org/3/py-modindex.html  #
# threading(multithreading): Part of the standard  # 
#    python libraries                              #
#      https://docs.python.org/3/py-modindex.html  #
# json(reading json settings file): Part of the    # 
#   standard python libraries                      #
#      https://docs.python.org/3/py-modindex.html  #
#--------------------------------------------------#

import wx
import sys
import threading
import json

#? List Order:
#? Name, Class

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

def engine(DataTable):
    #? Schedule Table levels:
    #? Level 1: The days of the week
    #? level 2: The hours in the days of the week
    #? Level 3 (Dictionary): The rooms in which the hours of the days of the week can take place
    #? Values for Level 3 (Dictionary): A certain subject in a specific room in an hour of a day of a week (An hour is a key, A subject is the value)
    Rooms = ["201", "202", "203", "204", "205", "206", "207"]
    Subjects = ["Math", "LA", "Grammar", "Science", "CS", "PE", "Spanish"]
    GradeClass = ["7A", "7B", "7C", "7D"]
    NumbTimesSubjectOccurWeek = {"Math":4, "LA":4, "Grammar":4, "Science":4, "CS":4, "PE":4, "Spanish":4}
    NumbTimesOccuredWeek = {"7A":[0, 0, 0, 0, 0, 0, 0], "7B":[0, 0, 0, 0, 0, 0, 0], "7C":[0, 0, 0, 0, 0, 0, 0], "7D":[0, 0, 0, 0, 0, 0, 0]}
    NumberOfSlotsPerDay = 7
    SchedulePoint = {}
    ScheduleTable = []
    ExitLoop = False
    ExitLoop1 = False
    # for i in range(len(Rooms)):
    #     SchedulePoint[Rooms[i]] = Subjects[i]
    for x in range(5): #? Setup the schedule list / dictionary thing. (Days)
        ScheduleRow = []
        for y in range(NumberOfSlotsPerDay): #? Setup the schedule list / dictionary thing. (Rows in a Day)
            SchedulePoint = {}
            for z in range(len(Rooms)):
                SchedulePoint[Subjects[z]] = ["[EMPTY]", Rooms[z]]
            ScheduleRow.append(SchedulePoint)
        ScheduleTable.append(ScheduleRow)

    #* DEPRECATED
    # for x in range(5): #? Run the schedule table through scheduling logic 
    #     for y in range(NumberOfSlotsPerDay):
    #         for z in range(len(Rooms)):
    #             try: #? Fill a certain time slot with a certain class that's taking a subject that's occuring during that time slot
    #                 if NumbTimesOccuredWeek[GradeClass[z]][z] <= NumbTimesSubjectOccurWeek[z]: #? Checking if the No. times a subject has occured in a week has exceeded the maximum amount of times that subject can appear in a week.
    #                     ScheduleTable[x][y][Subjects[z]][0] = GradeClass[z]
    #                     NumbTimesOccuredWeek[GradeClass[z]][z] += 1
    #             except Exception as err: #? Checking for index out of range to skip.
    #                 print("Left empty!" + str(err))
    #         Subjects.append(Subjects[0])
    #         Subjects.pop(0)
    #         for c in NumbTimesOccuredWeek:
    #             NumbTimesOccuredWeek[c].append(NumbTimesOccuredWeek[c][0])
    #             NumbTimesOccuredWeek[c].pop(0)
    #         NumbTimesSubjectOccurWeek.append(NumbTimesSubjectOccurWeek[0])
    #         NumbTimesSubjectOccurWeek.pop(0)
    #* DEPRECATED
    
    for x in range(5): #? Loop for 5 the 5 days in the chart
        n = 0 #? Set the current GradeClass indicator
        for y in range(NumberOfSlotsPerDay): #? Loop for all 7 slots in a day
            for z in range(len(Rooms)): #? Loop for all different subjects that could occur during one slot for the number of rooms there are.
                ExitLoop = False
                print(ScheduleTable[x][y])
                try:
                    if ScheduleTable[x][y][Subjects[z]][0] == "[EMPTY]": #? Check if the current slot is empty
                        for i in range(NumberOfSlotsPerDay): #? Loop for check below
                            if ScheduleTable[x][i][Subjects[z]][0] == GradeClass[n]: #? Check if subject has already been taken by a specific class in a certain other timeslot
                                # print("x", x, "i", i, "GradeClass", GradeClass[n], "Subject", Subjects[z], ScheduleTable[x][i][Subjects[z]][0])
                                # ScheduleTable[x][y][Subjects[z]][0] = "[EMPTY]"
                                ExitLoop = True
                                break
                        if ExitLoop == True:
                            continue
                        for i in range(len(Rooms)): #? Loop for check below
                            if ScheduleTable[x][y][Subjects[i]][0] == GradeClass[n]: #? Check if subject has already been filled in by specific class in current timeslot
                                ExitLoop = True
                                break
                        if ExitLoop == False: #? If this slot and it's subject hasn't been filled before by a specific class then:
                            if NumbTimesOccuredWeek[GradeClass[n]][z] < NumbTimesSubjectOccurWeek[Subjects[z]]: #? If this specific subject hasn't already appeared throughout the week specific # of times
                                ExitLoop1 = False
                                for i in range(len(NumbTimesOccuredWeek[GradeClass[n]])): #? Loop to check if there is a better slot
                                    if NumbTimesOccuredWeek[GradeClass[n]][z] > NumbTimesOccuredWeek[GradeClass[n]][i]: #? Check if there is a better slot that this class can occupy (Normalize the final chart table result)
                                        ScheduleTable[x][y][Subjects[i]][0] = GradeClass[n]
                                        NumbTimesOccuredWeek[GradeClass[n]][i] += 1
                                        ExitLoop1 = True
                                        break
                                if ExitLoop1 == False: #? Occupy the slot
                                    ScheduleTable[x][y][Subjects[z]][0] = GradeClass[n]
                                    NumbTimesOccuredWeek[GradeClass[n]][z] += 1

                except Exception as err: #? Exception for index out of range
                    if str(err) != "list index out of range":
                        print(str(err))
                if n < len(GradeClass):
                    n += 1
                else:
                    n = 0
    print(NumbTimesOccuredWeek)
    
    f = open("log.txt", "w") #? <DEBUG>
    for row in ScheduleTable: 
        print("--------------------------------------------------------------------------------------------------------")
        f.write("--------------------------------------------------------------------------------------------------------\n")
        for point in row:
            print(point)
            f.write(str(point) + "\n")
    f.close() #? </DEBUG>
    

def settingsFunc():
    with open("settings.json") as settings_file:
        settings = json.load(settings_file)
        for SettingOpts in settings["settings"]:
            for SettingNo in SettingOpts:
                for setting in SettingOpts[SettingNo]:
                    print(SettingNo + " - " + setting + ": " + str(SettingOpts[SettingNo][setting]))
        console()
        # print("Input the new value for a setting #. ([Setting#]-[New Value])")
        # NewValue = input(" > ")

def helpFunc():
    global HelpMenu
    print(HelpMenu)

def guiFunc():
    #TODO: Finish the damn GUI
    print("Code for the GUI is there, but is currently too unstable to actually do anything, will continue to work on gui after program is finished.")
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
    engine(DataTable)

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