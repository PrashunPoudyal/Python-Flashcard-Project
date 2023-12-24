import tkinter as tk
from tkinter import ttk

# os import will be used to retrieve and save information to local folders
import os
# pickle is an import that allows me to save class instances into folders and be retrieved and loaded without it having
# to be saved as if it was a string
import pickle

'''
FileManager class is one of the classes within this program that is required for it to run

FileManager's job is to handle all things that are related to file management, such as retrieving file information,
saving file information, and building the required folders to run. In theory, to run this program for the first time,
there only needs to be one main.py file, and the FileManager class will run to produce all the necessary folders.
 
FileManager has two types of functions, one is the startup functions, which are run regardless, and the other is called
by the main program so that it can run
'''
class FileManager():
    def __init__(self):
        # list of all programs
        self.programList = []
        # default information will be saved into the computer on first startup with all kinds of user data
        self.defaultInformation = {
            'test': 'test'
        }

        self.onStartupConfirm()

    # -------- FUNCTIONS RAN BY THE MANAGER ITSELF --------------------

    '''
    Ran on startup when FileManager instance is created to ensure the program can run well
    
    @return     void
    '''
    def onStartupConfirm(self):
        # self.initialization is responsible for ensuring that all program files are there and ready to go
        self.initialization()

        # now that the information is confirmed to be there, it will read off that and create fileInformation
        # that will be used throughout the program
        self.genProgramList()

    def createConfigFolder(self):
        if not os.path.exists("configFolder"):
            os.mkdir("configFolder")

    def createProgramFolder(self):
        if not os.path.exists("Programs"):
            os.mkdir("Programs")

    def createRetrieveConfigFile(self):
        try:
            configFile = open(r"configFolder\config.dat", "rb")
            pickle.load(configFile)
            configFile.close()
        except Exception:
            configFile = open(r"configFolder\config.dat", "wb")
            pickle.dump(self.defaultInformation, configFile)
            configFile.close()

    def createRetrieveGenFile(self):
        try:
            genFile = open(r"Programs\gen.dat", "r")
            verify = genFile.read()
            genFile.close()
        except Exception:
            genFile = open(r"Programs\gen.dat", "w")
            genFile.write("genFile")
            genFile.close()

    def initialization(self):
        self.createProgramFolder()
        self.createConfigFolder()
        self.createRetrieveConfigFile()
        self.createRetrieveGenFile()

    def genProgramList(self):
        programList = os.listdir("Programs")
        self.programList = programList

    # ----------- FUNCTIONS CALLED BY THE MAIN PROGRAM CLASS -------------------

    def retrieveProgramFile(self, filename):
        try:
            programFile = open("Programs\\" + filename + ".dat", "rb")
            programInformation = pickle.load(programFile)
            programFile.close()

        except Exception as e:
            print(e)
            programInformation = "Error"

        return programInformation

    def saveProgramFile(self, filename, programInformation):
        programFile = open("Programs\\"+filename+".dat", "wb")
        pickle.dump(programInformation, programFile)
        programFile.close()

        return 'confirm'


class Program:
    def __init__(self, name):
        self.programName = name
        self.listOfCards = []


class Card:
    def __init__(self, side1, side2):
        self.side1 = side1
        self.side2 = side2


class UserInterfaceHandler:
    def __init__(self):
        self.programFileName = ""
        self.startMenu()
        if self.programFileName == "New Program":
            self.handleNewProgramCreation()
            program = Program(self.programFileName)
            fileManager.saveProgramFile(self.programFileName, program)
        else:
            self.handleProgramSelection()

    def startMenu(self):
        programList = fileManager.programList
        userProgramList = []
        for program in programList:
            if program == "gen.dat":
                userProgramList.append("New Program")
            else:
                userProgramList.append(program.removesuffix('.dat'))

        root = tk.Tk()
        root.title("Select a Program")

        # Adjust size
        root.geometry("500x100")

        # Change the label text
        def show():
            label.config(text=clicked.get())
            self.programFileName = clicked.get()
            root.destroy()


        # datatype of menu text
        clicked = tk.StringVar()

        # initial menu text
        clicked.set("New Program")

        # Create Label
        label = tk.Label(root, text="SELECT A PROGRAM FROM THE DROPDOWN MENU", font=('Helvetica bold', 12))
        label.pack()


        # Create Dropdown menu
        drop = tk.OptionMenu(root, clicked, *userProgramList)
        drop.pack()

        # Create button, it will change label text
        button = tk.Button(root, text="Enter", command=show).pack()



        # Execute tkinter
        root.mainloop()

    def enterNewProgramName(self):
        root = tk.Tk()

        root.title("Enter Program Name")
        # setting the windows size
        root.geometry("300x200")

        # declaring string variable
        # for storing name and password
        name_var = tk.StringVar()

        # defining a function that will
        # get the name and password and
        # print them on the screen
        def submit():
            self.programFileName = name_var.get()
            root.destroy()

        # creating a label for
        # name using widget Label
        nameLabel = tk.Label(root, text='Enter Program Name: ', font=('calibre', 10, 'bold'))

        # creating a entry for input
        # name using widget Entry
        nameEntry = tk.Entry(root, textvariable=name_var, font=('calibre', 10, 'normal'))

        # creating a button using the widget
        # Button that will call the submit function
        submitButton = tk.Button(root, text='Submit', command=submit)

        # placing the label and entry in
        # the required position using grid
        # method
        nameLabel.grid(row=0, column=0)
        nameEntry.grid(row=0, column=1)
        submitButton.grid(row=2, column=1)

        # performing an infinite loop
        # for the window to display
        root.mainloop()

    def enterNewCard(self):
        pass

    def handleProgramSelection(self):
        loadedProgram = fileManager.retrieveProgramFile(self.programFileName)

    def handleNewProgramCreation(self):
        self.enterNewProgramName()

    def handleNewCardCreation(self):
        pass


fileManager = FileManager()
uiHandler = UserInterfaceHandler()
