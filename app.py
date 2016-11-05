from Tkinter import *  # Imports
import tkFont
import tkMessageBox as tkBox
import sqlite3

conn = sqlite3.connect('devices.db')
c = conn.cursor()

#c.execute("CREATE TABLE IF NOT EXISTS Devices (Device text, Path text, Pos int)")
#c.execute("CREATE TABLE IF NOT EXISTS Fixes (Code int, Fix text)")
#c.execute("INSERT INTO KeyWords VALUES ('Display', 0)")
#c.execute("INSERT INTO Fixes VALUES (0, 'Try fully charging the device')")

conn.commit()

class Application(Frame):  # Stores info and functions dedicated to the window

    # Misc Variables
    questionIndex = 0
    questions = ["Has the phone got wet?", "Has the phone been dropped?",
                 "Screen blank or broken?", "Fully charged?",
                 "Power on?", "Phone slow?"]
    fixes = ["Try drying the phone in a bag of rice for 3 days", "NEXT_Q",
             "No solution!, try speaking to our technicians or purchase a new phone!",
             "Charge the phone to 100%", "INDEX_2", "INDEX_2"]
    otherMsg = "Speak to our technicians at 084337"
    yesAnswers = ["Y", "YES"]
    noAnswers = ["N", "NO"]
    yesAnswersIndex = [1, 1, 1, 0, 0, 1]
    answers = []

    def __init__(self, title, master=None):  # Default __init__ method called when instantiated

        Frame.__init__(self, master)  # Creates a new Frame to load components to the master var (root)
        self.pack({"padx": 10, "pady": 10})
        root.title(title)

        # Widgets Instantiation
        self.title = Label(self)
        self.diagnoseBtn = Button(self)
        self.contactBtn = Button(self)

        self.assign_vars()

        # TODO implement technician contact

    def assign_vars(self):
        self.title["text"] = "Welcome"
        self.title.pack({"padx": 100, "pady": 10})

        self.diagnoseBtn["text"] = "Diagnose an Issue"
        self.diagnoseBtn["command"] = self.diagnose_issues  # Diagnose issues launcher
        self.diagnoseBtn.pack({"side": "left"})

        # Change to look for device
        self.contactBtn["text"] = "Look for device"
        self.contactBtn["command"] = self.look_for_device
        self.contactBtn.pack({"side": "right"})

    def diagnose_issues(self):  # Starts the Diagnosis window

        # Assigns the window to the self.window variable
        self.window = Toplevel(self)
        self.frame = Frame(self.window)  # Main frame to hold content
        self.messageDia = Label(self.frame)  # Message
        self.titleDia = Label(self.frame)  # Title
        self.inputBoxDia = Entry(self.frame)  # Input box
        self.enterBtnDia = Button(self.frame)  # Enter button
        self.titleFont = tkFont.Font(self.titleDia, self.titleDia.cget("font"))  # Font

        self.window.wm_title("Diagnosis")
        self.create_diagnosis_widgets()

    def create_diagnosis_widgets(self):  # Creates the elements of the diagnosis page

        self.titleDia["text"] = "Diagnose an issue"
        self.titleDia.pack({"padx": 100, "pady": 10})

        self.messageDia["text"] = str(self.questions[self.questionIndex])
        self.messageDia.pack({"padx": 10, "pady": 10, "side": "left"})

        self.titleFont.configure(underline=True, size=12)
        self.titleDia.configure(font=self.titleFont)

        self.inputBoxDia.pack({"side": "left", "padx": 10, "pady": 10})

        self.enterBtnDia["text"] = "Enter"
        self.enterBtnDia["command"] = self.handle_input
        self.enterBtnDia.pack({"side": "right", "padx": 10, "pady": 10})

        self.frame.pack({"padx": 10, "pady": 10})  # Create

    def handle_input(self):  # Decides what to do when an answer is submitted

        if not validate_input(self.inputBoxDia.get()):  # checks if the box is not empty
            tkBox.showerror("Invalid", "Please submit a valid answer")
            return  # Escape the method

        yes = False  # Assign vars
        no = False
        other = True

        for value in self.yesAnswers:  # Checks if the user as inputted a yes
            if str(self.inputBoxDia.get()).upper() == value:  # Reduces errors by capitalising all the characters
                yes = True
                other = False

        for value in self.noAnswers:  # See above
            if str(self.inputBoxDia.get()).upper() == value:
                no = True
                other = False

        # If the input is a yes and the question answer is a yes (1) or the input is a no and the answer is no
        if yes and (self.yesAnswersIndex[self.questionIndex] == 1) or \
                (self.yesAnswersIndex[self.questionIndex] == 0 and no):
            # Skips the question if the answer does not produce a final query
            if self.fixes[self.questionIndex] == "NEXT_Q":
                self.questionIndex += 1
                if self.questionIndex < len(self.questions):
                    self.messageDia["text"] = self.questions[self.questionIndex]
                    self.answers.append(str(self.inputBoxDia.get()))
                    self.messageDia.pack({"padx": 10, "pady": 10, "side": "left"})
                else:
                    self.close_window()
            # Shows correct message if shorthand is detected
            elif self.fixes[self.questionIndex] == "INDEX_2":
                tkBox.showinfo("Fix!", self.fixes[2])
                self.close_window()
            else:  # Shows default message
                tkBox.showinfo("Fix!", self.fixes[self.questionIndex])
                self.close_window()
        # if input is no or answer is no and input is yes
        elif no or (self.yesAnswersIndex[self.questionIndex] == 0 and yes):
            self.questionIndex += 1
            # Default behaviour
            if self.questionIndex < len(self.questions):
                self.messageDia["text"] = self.questions[self.questionIndex]
                self.answers.append(str(self.inputBoxDia.get()))
                self.messageDia.pack({"padx": 10, "pady": 10, "side": "left"})
            # For the last question
            elif self.questionIndex == len(self.questions):
                tkBox.showinfo("Fix!", self.fixes[2])
                self.close_window()
            else:
                self.close_window()
        # If the answer was not a yes or a no
        elif other:
            # TODO Look for clues here
            tkBox.showinfo("Problem", "Try calling a technician on 889088908")
        else:
            tkBox.showerror("Error", "An error has occurred")

    def look_for_device(self):

        self.dWindow = Toplevel(self) # Main frame to hold content
        self.dFrame = Frame(self.dWindow)

        self.dListBox = Listbox(self.dFrame)
        self.dSelectBtn = Button(self.dFrame)

        self.dFrame.pack({"padx": "10", "pady": "10"})

        c.execute("SELECT * FROM Devices")
        data = c.fetchall()
        for row in data:
            self.dListBox.insert(row[2], row[0])

        self.dListBox.pack({"side": "left"})

        self.dSelectBtn["text"] = "Select"
        self.dSelectBtn["command"] = self.start_search
        self.dSelectBtn.pack({"side": "right", "padx": "5"})

    def start_search(self):

        selection = self.dListBox.get(self.dListBox.curselection())

        self.dev_questions = []
        self.dev_questionTypes = []
        self.dev_questionAns = []

        c.execute("SELECT * FROM Devices WHERE Device=?", (selection,))
        for row in c.fetchall():
            self.dev_device = row[0]
            self.dev = sqlite3.connect(row[1])
            self.devC = self.dev.cursor()
            #devC.execute("CREATE TABLE IF NOT EXISTS DataQuestions (Question text, Pos int, ResAns int)")
            #devC.execute("CREATE TABLE IF NOT EXISTS Answers (Answer text, Pos int)")
            self.devC.execute("SELECT * FROM DataQuestions")
            for row in self.devC.fetchall():
                self.dev_questions.append(row[0])
                self.dev_questionTypes.append(row[1])
                self.dev_questionAns.append(row[2])

        self.open_questions_panel()
        self.dWindow.destroy()  # kill look for devices panel

    def open_questions_panel(self):
        self.qWindow = Toplevel(self)  # Main frame to hold content
        self.qFrame = Frame(self.qWindow)

        self.qLabel = Label(self.qFrame)
        self.qInput = Entry(self.qFrame)
        self.qButton = Button(self.qFrame)

        self.dev_index = 0;
        self.data = []

        self.qLabel["text"] = str(self.dev_questions[self.dev_index])
        self.qLabel.pack({"padx": 10, "pady": 10, "side": "left"})

        self.qInput.pack({"side": "left", "padx": 10, "pady": 10})

        self.qButton["text"] = "Enter"
        self.qButton["command"] = self.ans_question
        self.qButton.pack({"side": "right", "padx": 10, "pady": 10})

        self.qFrame.pack({"padx": 10, "pady": 10})  # Create

    def ans_question(self):

        ans = self.qInput.get()

        if not validate_input(str(ans)): return

        questionType = self.dev_questionTypes[self.dev_index]
        questionAnsIndex = self.dev_questionAns[self.dev_index]

        yes = False  # Assign vars
        no = False
        other = True

        for value in self.yesAnswers:  # Checks if the user as inputted a yes
            if str(self.qInput.get()).upper() == value:  # Reduces errors by capitalising all the characters
                yes = True
                other = False

        for value in self.noAnswers:  # See above
            if str(self.qInput.get()).upper() == value:
                no = True
                other = False

        say = ""

        if str(questionType) == "data":
            self.data.append(str(self.dev_device) + " Attribute " + str(ans))
            print self.data
        if (questionAnsIndex is 1 and yes) or (questionAnsIndex is 0 and no):
            self.devC.execute("SELECT * FROM Answers WHERE Pos=?", (questionType,))
            for row in self.devC.fetchall():
                say = row[0]
            tkBox.showinfo("Fix", say)
        elif self.dev_index < len(self.dev_questions)-1:
            if str(questionType) != "data":
                self.data.append(str(self.dev_questions[self.dev_index]) + " Ans " + str(ans))
                print self.data
            self.dev_index += 1
            self.qLabel["text"] = str(self.dev_questions[self.dev_index])
            self.qLabel.pack({"padx": 10, "pady": 10, "side": "left"})
        else:
            var = tkBox.askyesno('Send Data', "Send data to technician?")
            if var == 1:

                self.send_data()

                tkBox.showinfo('Sent', 'Sent data to technician')
                self.qWindow.destroy()
            else:
                tkBox.showinfo('Canceled', 'No data was sent')
                self.qWindow.destroy()

    def send_data(self):

        #c.execute("CREATE TABLE IF NOT EXISTS CaseNumbers (Number int)")
        c.execute("SELECT * FROM CaseNumbers")
        num = 1
        for row in c.fetchall():
            num = int(row[0]) + 1
        c.execute("INSERT INTO CaseNumbers (Number) VALUES (?)", (num,))
        conn.commit()
        path = "CaseFiles/" + str(num) + ".txt"
        file = open(path, 'w')
        file.write(str(self.data))
        file.close()

    # Close window method
    def close_window(self):
        self.window.destroy()


# Returns True of False if there is text
def validate_input(text):

    if text != "":
        return True
    else:
        return False

root = Tk()
app = Application("Application", master=root)  # Attach the application to the root of TK
app.mainloop()  # Initiate the main loop
conn.close()
root.destroy()  # Called on mainloop stopped
