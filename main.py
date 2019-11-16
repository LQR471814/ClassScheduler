#---------------------------------------------------------#
# DISCLAIMER: THIS PROGRAM IS NOT LISCENED TO ANYONE IN   #
# ANY SHAPE OR FORM, FEEL FREE TO EDIT IT HOW EVER YOU    #
# LIKE.                                                   #
#---------------------------------------------------------#
# Credit to Libraries that I used:                        #
#                                                         #
# WxPython(GUI programming): https://www.wxpython.org     #
# sys(system functions): Part of the standard python      #
#   libraries                                             #
#      https://docs.python.org/3/py-modindex.html         #
# threading(multithreading): Part of the standard         #
#   python libraries                                      #
#      https://docs.python.org/3/py-modindex.html         #
# json(reading json settings file): Part of the           #
#   standard python libraries                             #
#      https://docs.python.org/3/py-modindex.html         #
#---------------------------------------------------------#

import wx
import wx.lib.newevent as WxNewevent
import sys
import threading
import json

#? Custom Events:
ExternalClose, EVT_EXT_CLOSE = WxNewevent.NewEvent()

#? GUI Code

class settingsEditor(wx.Frame): #? A more user friendly settings editor than a JSON file
    def __init__(self, title): #? Initialize window
        #? Initialize

        wx.Frame.__init__(self, None, title=title, pos=(50, 50), size=(680, 720)) #? Initialize the window with a bunch of parameters
        panel = wx.Panel(self, -1) #? Add a panel
        panel.Layout() #? Use the panel
        
        #? Load settings
        
        self.SettingsFile = open("settings.json")
        self.JsonSettings = json.load(self.SettingsFile)
        self.JsonSettingsKey = []
        for i in range(len(self.JsonSettings["settings"])):
            for SettingKey in self.JsonSettings["settings"][i][str(i + 1)]:
                self.JsonSettingsKey.append(SettingKey)
        textCtrl1 = wx.TextCtrl(self, -1, self.JsonSettings["settings"][0]["1"][self.JsonSettingsKey[0]], size=(125, -1))
        listCtrl1 = wx.ListCtrl(self, -1, size=(200, 100), style=wx.LC_EDIT_LABELS)
        listCtrl1.InsertCollumn(0, "")
        listCtrl1.InsertCollumn(1, "")

        
        #? Bind and setup
        
        self.SetBackgroundColour("WHITE") #? Totally unneccesary
        self.Bind(wx.EVT_CLOSE, self.OnClosed) #? Catch event for closing
        self.Bind(EVT_EXT_CLOSE, self.OnExtClose) #? Catch custom event for closing from other causes ie. (quitFunc)
        panel.Bind(wx.EVT_KEY_DOWN, self.OnKeyPressed) #? Catch event for keystrokes to close window with [ESC]
        
    def OnKeyPressed(self, event):
        global Continue
        keycode = event.GetKeyCode()
        if keycode == 27:
            Continue = False
            self.Destroy()
        
    def OnClosed(self, event):
        global Continue
        Continue = False
        self.Destroy()

    def OnExtClose(self, event):
        self.Destroy()

#* UNUSED
# class mainBox(wx.Frame):
#     def __init__(self, title):

#         wx.Frame.__init__(self, None, title=title,
#                           pos=(50, 50), size=(640, 480))
#         panel = wx.Panel(self, -1)
#         panel.Layout()
#         self.SetBackgroundColour("WHITE")
#         self.Bind(wx.EVT_CLOSE, self.OnClosed)

#     def OnClosed(self, event):
#         self.Destroy()
#* UNUSED

#? Command functions

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

#? Scheduling engine

def createPerDayPerClassDict(gradeClassList):
    #? this is only used for per day assignment
    #? return a dictionary, where key is the gradeclass, value is a another dict, key is subject, value is a set of assigned subjects
    r = {}
    for gclass in gradeClassList:
        r[gclass] = set()
    return r


def selectAssignment(gradeClassList, perSubjectOccurenceDict, availabeTable):
    #? perClassWeeklySubjectOccuranceDict, key is gradeclass name, value is another dict,
    #? key is subject name, value is current number of occurance, initialized to 0
    perClassWeeklySubjectOccuranceDict = {}
    for gclass in gradeClassList:
        perClassWeeklySubjectOccuranceDict[gclass] = {}
        for subject in perSubjectOccurenceDict:
            perClassWeeklySubjectOccuranceDict[gclass][subject] = 0

    for weekday in range(5):
        per_class_unique_subject_stats = createPerDayPerClassDict(
            gradeClassList)
        for timeSlot in range(len(availabeTable[weekday])):
            slotClassmappingSet = set()
            for schoolSubject in availabeTable[weekday][timeSlot]:
                for gclass in gradeClassList:
                    if availabeTable[weekday][timeSlot][schoolSubject] == "[EMPTY]" and not(schoolSubject in per_class_unique_subject_stats[gclass]) and not(gclass in slotClassmappingSet):
                        if perClassWeeklySubjectOccuranceDict[gclass][schoolSubject] < perSubjectOccurenceDict[schoolSubject]:
                            availabeTable[weekday][timeSlot][schoolSubject] = gclass
                            perClassWeeklySubjectOccuranceDict[gclass][schoolSubject] += 1
                            per_class_unique_subject_stats[gclass].add(
                                schoolSubject)
                            slotClassmappingSet.add(gclass)


def engine():
    #? Schedule Table levels:
    #? Level 1: The days of the week
    #? level 2: The hours in the days of the week
    #? Level 3 (Dictionary): The rooms in which the hours of the days of the week can take place
    #? Values for Level 3 (Dictionary): A certain subject in a specific room in an hour of a day of a week (An hour is a key, A subject is the value)
    SettingsFile = open("settings.json")
    JsonSettings = json.load(SettingsFile)
    JsonSettingsKey = []
    for i in range(len(JsonSettings["settings"])):
        for SettingKey in JsonSettings["settings"][i][str(i + 1)]:
            JsonSettingsKey.append(SettingKey)
    OutputTable = {}
    Week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    #? Input Values from settings (The commented out parts are default values)
    SubjAmnt = len(JsonSettings["settings"][1]["2"][JsonSettingsKey[1]])
    # SubjAmnt = 7
    NumberOfSlotsPerDay = JsonSettings["settings"][0]["1"][JsonSettingsKey[0]]
    # NumberOfSlotsPerDay = 5
    NumbTimesSubjectOccurWeek = {}
    for c in JsonSettings["settings"][1]["2"][JsonSettingsKey[1]]:
        NumbTimesSubjectOccurWeek[c] = JsonSettings["settings"][1]["2"][JsonSettingsKey[1]][c]
    # Subjects = ["Math", "LA", "Grammar", "Science", "CS", "PE", "Spanish"]
    Subjects = []
    for c in JsonSettings["settings"][1]["2"][JsonSettingsKey[1]]:
        Subjects.append(c)
    # NumbTimesSubjectOccurWeek = {"Math":5, "LA":5, "Grammar":5, "Science":4, "CS":4, "PE":4, "Spanish":4}
    GradeClass = JsonSettings["settings"][2]["3"][JsonSettingsKey[2]]
    # GradeClass = ["7A", "7B", "7C", "7D"]

    NumbTimesOccuredWeek = {"7A": [0, 0, 0, 0, 0, 0, 0], "7B": [
        0, 0, 0, 0, 0, 0, 0], "7C": [0, 0, 0, 0, 0, 0, 0], "7D": [0, 0, 0, 0, 0, 0, 0]}
    SchedulePoint = {}
    ScheduleTable = []
    ExitLoop = False
    ExitLoop1 = False
    # for i in range(SubjAmnt):
    #     SchedulePoint[Rooms[i]] = Subjects[i]
    for x in range(5):  #? Setup the schedule list / dictionary thing. (Days)
        ScheduleRow = []
        #? Setup the schedule list / dictionary thing. (Rows in a Day)
        for y in range(NumberOfSlotsPerDay):
            SchedulePoint = {}
            for z in range(SubjAmnt):
                SchedulePoint[Subjects[z]] = "[EMPTY]"
            ScheduleRow.append(SchedulePoint)
        ScheduleTable.append(ScheduleRow)

    selectAssignment(GradeClass, NumbTimesSubjectOccurWeek, ScheduleTable)
    # * DEPRECATED
    # for x in range(5): #? Run the schedule table through scheduling logic
    #     for y in range(NumberOfSlotsPerDay):
    #         for z in range(SubjAmnt):
    #             for n in range(len(GradeClass)):
    #                 try: #? Fill a certain time slot with a certain class that's taking a subject that's occuring during that time slot
    #                     if NumbTimesOccuredWeek[GradeClass[z]][z] <= NumbTimesSubjectOccurWeek[Subjects[z]]: #? Checking if the No. times a subject has occured in a week has exceeded the maximum amount of times that subject can appear in a week.
    #                         ExitLoop = False
    #                         for i in range(NumberOfSlotsPerDay):
    #                             if ScheduleTable[x][i][Subjects[z]] == GradeClass[n]:
    #                                 ExitLoop = True
    #                                 break
    #                         if ExitLoop == False:
    #                             ScheduleTable[x][y][Subjects[z]] = GradeClass[n]
    #                             NumbTimesOccuredWeek[GradeClass[z]][z] += 1
    #                         else:
    #                             break
    #                 except Exception as err: #? Checking for index out of range to skip.
    #                     if "list index out of range" != str(err):
    #                         print("err:", str(err))
    # Subjects.append(Subjects[0])
    # Subjects.pop(0)
    # for c in NumbTimesOccuredWeek:
    #     NumbTimesOccuredWeek[c].append(NumbTimesOccuredWeek[c][0])
    #     NumbTimesOccuredWeek[c].pop(0)
    # NumbTimesSubjectOccurWeek.append(NumbTimesSubjectOccurWeek[0])
    # NumbTimesSubjectOccurWeek.pop(0)
    # * DEPRECATED

    # * DEPRECATED
    # for x in range(5):  #? Loop for 5 the 5 days in the chart
    #     n = 0  #? Set the current GradeClass indicator
    #     for y in range(NumberOfSlotsPerDay):  #? Loop for all 7 slots in a day
    #         #? Loop for all different subjects that could occur during one slot for the number of rooms there are.
    #         for z in range(SubjAmnt):
    #             ExitLoop = False
    #             try:
    #                 #? Check if the current slot is empty
    #                 if ScheduleTable[x][y][Subjects[z]] == "[EMPTY]":
    #                     for i in range(NumberOfSlotsPerDay):  #? Loop for check below
    #                         #? Check if subject has already been taken by a specific class in a certain other timeslot
    #                         if ScheduleTable[x][i][Subjects[z]] == GradeClass[n]:
    #                             ExitLoop = True
    #                             break
    #                     if ExitLoop == True:
    #                         continue
    #                     for i in range(SubjAmnt):  #? Loop for check below
    #                         #? Check if subject has already been filled in by specific class in current timeslot
    #                         if ScheduleTable[x][y][Subjects[i]] == GradeClass[n]:
    #                             ExitLoop = True
    #                             break
    #                     #? If this slot and it's subject hasn't been filled before by a specific class then:
    #                     if ExitLoop == False:
    #                         #? If this specific subject hasn't already appeared throughout the week specific # of times
    #                         if NumbTimesOccuredWeek[GradeClass[n]][z] < NumbTimesSubjectOccurWeek[Subjects[z]]:
    #                             ExitLoop1 = False
    #                             #? Loop to check if there is a better slot
    #                             for i in range(len(NumbTimesOccuredWeek[GradeClass[n]])):
    #                                 #? Check if there is a better slot that this class can occupy (Normalize the final chart table result)
    #                                 if NumbTimesOccuredWeek[GradeClass[n]][z] > NumbTimesOccuredWeek[GradeClass[n]][i]:
    #                                     ScheduleTable[x][y][Subjects[i]
    #                                                         ] = GradeClass[n]
    #                                     NumbTimesOccuredWeek[GradeClass[n]][i] += 1
    #                                     ExitLoop1 = True
    #                                     break
    #                             if ExitLoop1 == False:  #? Occupy the slot
    #                                 ScheduleTable[x][y][Subjects[z]
    #                                                     ] = GradeClass[n]
    #                                 NumbTimesOccuredWeek[GradeClass[n]][z] += 1

    #             except Exception as err:  #? Exception for index out of range
    #                 if str(err) != "list index out of range":
    #                     print(str(err))
    #             if n < len(GradeClass):
    #                 n += 1
    #             else:
    #                 n = 0
    # * DEPRECATED

    # f = open("log.txt", "w")  #? <DEBUG>
    # for row in ScheduleTable:
    #     print("--------------------------------------------------------------------------------------------------------")
    #     f.write("--------------------------------------------------------------------------------------------------------\n")
    #     for point in row:
    #         print(point)
    #         f.write(str(point) + "\n")
    # f.close()  #? </DEBUG>

    for c in GradeClass:  #? Setup table for output
        OutputTable[c] = {}
    for c in GradeClass:
        for day in Week:
            OutputTable[c][day] = []

    n = 0
    for x in range(5):  #? Add values to the output table
        for y in range(NumberOfSlotsPerDay):
            for z in range(SubjAmnt):
                for n in range(len(GradeClass)):
                    if ScheduleTable[x][y][Subjects[z]] == GradeClass[n]:
                        OutputTable[GradeClass[n]][Week[x]].append(
                            [ScheduleTable[x][y][Subjects[z]], Subjects[z]])

    for c in OutputTable:  #? Write values from output table to 4 seperate .csv files
        f = open(c + ".csv", "w")
        f.write(", ")
        for i in range(NumberOfSlotsPerDay):
            f.write("Period " + str(i + 1) + ", ")
        f.write("\n")
        for day in OutputTable[c]:
            f.write(day + ", ")
            for info in OutputTable[c][day]:
                f.write(info[1] + ", ")
            f.write("\n")
        f.close()

    print("[FINISHED]")

def settingsFunc():
    global Continue
    with open("settings.json") as settings_file:
        settings = json.load(settings_file)
        for SettingOpts in settings["settings"]:
            for SettingNo in SettingOpts:
                for setting in SettingOpts[SettingNo]:
                    print(SettingNo + " - " + setting + ": " +
                          str(SettingOpts[SettingNo][setting]))
        Continue = True
        console()
        # print("Input the new value for a setting #. ([Setting#]-[New Value])")
        # NewValue = input(" > ")

def helpFunc():
    global HelpMenu
    print(HelpMenu)

def guiFunc():
    # TODO: Finish the damn GUI
    print("Code for the GUI is there, but is currently too unstable to actually do anything, will continue to work on gui after program is finished.")
    # app = wx.App(False)
    # frame = mainBox("GUI")
    # frame.Show(True)
    # app.MainLoop()

def quitFunc():
    global frame
    global Continue
    global Exit
    Exit = True
    if Continue == True:
        output = ExternalClose(content="destroy")
        wx.PostEvent(frame, output)
    sys.exit(0)

#! Variables

Continue = False
Exit = False

commands = {"help": helpFunc,
            "gui": guiFunc,
            "run": engine,
            "quit": quitFunc,
            "settings": settingsFunc
            }

HelpMenu = """
 ------------ <HELP> ------------
 > help: Show this menu
 > gui: Enable experimental GUI
 > run: Runs the program
 > settings: Shows the settings.
 > quit: Quits the control shell
"""

#! Initalize: Threads and other.

print(HelpMenu)

t1 = threading.Thread(target=console)
t1.start()

while True:
    if Continue == True:
        break
    if Exit == True:
        break
if Continue == True:
    app = wx.App()
    frame = settingsEditor("Settings")
    frame.Show()
    app.MainLoop()
