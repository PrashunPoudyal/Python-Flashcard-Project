import tkinter as tk
from tkinter import ttk

# os import will be used to retrieve and save information to local folders
import os
# pickle is an import that allows me to save class instances into folders and be retrieved and loaded without it having
# to be saved as if it was a string
import pickle
import random


# TODO - Create Game Type Handler / Program Handler For the UIHandler to allow the user to choose what to do once he has selected a Program
# TODO - Make Multiple Game Types other than Multiple Choice Questions - Short Answer, as well as View Cards
# TODO - Improve the UI for the UIHandlers so they don't look utter trash
# TODO - Create Statistics Handler class to handle statistics and store them into the config folders

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

    def multipleChoiceTest(self, questionAmt):
        questions = []

        if questionAmt > len(self.listOfCards):
            return "Err1"

        for i in range(questionAmt):
            question = self.returnTestQuestionMC()
            if question == "Err1":
                return "Err1"
            else:
                questions.append(question)

        return questions

    def returnTestQuestionMC(self):
        usedAnswers = []
        if len(self.listOfCards) < 4:
            return "Err1" # means not enough cards to play

        card = random.choice(self.listOfCards)



        description = card.side2
        answer = card.side1
        ans2 = answer
        ans3 = answer
        ans4 = answer
        while ans2 == answer:
            ans2 = random.choice(self.listOfCards).side1
        while ans3 == answer or ans3 == ans2:
            ans3 = random.choice(self.listOfCards).side1
        while ans4 == answer or ans4 == ans2 or ans4 == ans3:
            ans4 = random.choice(self.listOfCards).side1
        testQuestion = {
            'description': description,
            'correctAns': answer,
            'incorrect1': ans2,
            'incorrect2': ans3,
            'incorrect3': ans4
        }

        return testQuestion



class Card:
    def __init__(self, side1, side2):
        self.side1 = side1
        self.side2 = side2

    def printSides(self):
        print(self.side1, self.side2)


class UserInterfaceHandler:
    def __init__(self):
        fileManager.genProgramList()
        self.programFileName = ""
        self.program = None
        self.side1 = ""
        self.side2 = ""
        self.complete = False
        self.answer = 0
        self.startMenu()
        if self.programFileName == "New Program":
            self.program = Program(self.programFileName)
            self.handleNewProgramCreation()
            fileManager.saveProgramFile(self.programFileName, self.program)
            self.__init__()
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
        nameVar = tk.StringVar()

        # defining a function that will
        # get the name and password and
        # print them on the screen
        def submit():
            self.programFileName = nameVar.get()
            root.destroy()

        # creating a label for
        # name using widget Label
        nameLabel = tk.Label(root, text='Enter Program Name: ', font=('calibre', 10, 'bold'))

        # creating a entry for input
        # name using widget Entry
        nameEntry = tk.Entry(root, textvariable=nameVar, font=('calibre', 10, 'normal'))

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
        self.complete = False

        root = tk.Tk()
        root.geometry("500x300")
        root.title("Create New Card")

        side1Var = tk.StringVar()
        side2Var = tk.StringVar()


        def submit():
            self.side1 = side1Var.get()
            self.side2 = side2Var.get()
            self.complete = False
            root.destroy()

        def complete():
            self.side1 = side1Var.get()
            self.side2 = side1Var.get()
            print("working")
            self.complete = True
            root.destroy()

        nameLabel = tk.Label(root, text='Enter Program Name: ', font=('calibre', 10, 'bold'))

        side1Entry = tk.Entry(root, textvariable=side1Var, font=('calibre', 10, 'normal'))
        side2Entry = tk.Entry(root, textvariable=side2Var, font=('calibre', 10, 'normal'))

        submitButton = tk.Button(root, text='Submit', command=submit)
        finishButton = tk.Button(root, text="Complete", command=complete)

        side1Entry.grid(row=0, column=0)
        side2Entry.grid(row=0, column=1)
        submitButton.grid(row=2, column=1)
        finishButton.grid(row=3, column=1)


        root.mainloop()

        return self.side1, self.side2

    def multipleChoiceQuestion(self, questionLabel, questionNum):
        root = tk.Tk()
        root.geometry("500x300")
        root.title("Question " + str(questionNum))

        var = tk.IntVar()

        def submit():
            self.answer = var.get()
            root.destroy()


        qLabel = tk.Label(root, text=questionLabel, font=('calibre', 10, 'bold'))

        R1 = tk.Radiobutton(root, text="A", variable=var, value=1)
        R2 = tk.Radiobutton(root, text="B", variable=var, value=2)
        R3 = tk.Radiobutton(root, text="C", variable=var, value=3)
        R4 = tk.Radiobutton(root, text="D", variable=var, value=4)

        submitButton = tk.Button(root, text='Submit', command=submit)

        qLabel.grid(row=0, column=0)
        R1.grid(row=1, column=0)
        R2.grid(row=2, column=0)
        R3.grid(row=3, column=0)
        R4.grid(row=4, column=0)

        submitButton.grid(row=2, column=1)

        root.mainloop()

        return self.answer


    def gameTypeHandler(self):
        pass

    def multipleChoiceTestHandler(self, questionNum):
        questionInformation = self.program.multipleChoiceTest(questionNum)
        questionNum = 0
        score = 0

        for question in questionInformation:
            questionNum += 1
            questionOrder = []
            questionOrder.append(question['correctAns'])
            questionOrder.append(question['incorrect1'])
            questionOrder.append(question['incorrect2'])
            questionOrder.append(question['incorrect3'])

            random.shuffle(questionOrder)

            questionLabel = f"{question['description']} \na) {questionOrder[0]} \nb) {questionOrder[1]} \nc) {questionOrder[2]} \nd) {questionOrder[3]}"

            userAnswer = self.multipleChoiceQuestion(questionLabel, questionNum)
            userAnswer -= 1
            print(userAnswer)

            if questionOrder[userAnswer] == question["correctAns"]:
                print("Correct!")
                score += 1
                print(str(score) + "/" + str(questionNum))
            else:
                print("Incorrect!")
                print(str(score) + "/" + str(questionNum))

    def handleProgramSelection(self):
        self.program = fileManager.retrieveProgramFile(self.programFileName)
        print(self.program.listOfCards)
        self.multipleChoiceTestHandler(5)

    def handleNewProgramCreation(self):
        self.enterNewProgramName()
        self.handleNewCardCreation()

    def handleNewCardCreation(self):
        while True:
            newCard = self.enterNewCard()
            print(newCard)
            card = Card(newCard[0], newCard[1])
            self.program.listOfCards.append(card)
            if self.complete:
                break


fileManager = FileManager()
uiHandler = UserInterfaceHandler()