from Tkinter import *  # Imports
import tkFont
import tkMessageBox as tkBox
import sqlite3

conn = sqlite3.connect('example.db')
c = conn.cursor()

#c.execute("CREATE TABLE IF NOT EXISTS KeyWords (Key text, Code int)")
#c.execute("CREATE TABLE IF NOT EXISTS Fixes (Code int, Fix text)")
#c.execute("INSERT INTO KeyWords VALUES ('Display', 0)")
#c.execute("INSERT INTO Fixes VALUES (0, 'Try fully charging the device')")

#conn.commit()

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

        self.contactBtn["text"] = "Query database"
        self.contactBtn["command"] = self.run_query
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

    def run_query(self):

        self.qWindow = Toplevel(self) # Main frame to hold content

        self.qMessage = Label(self.qWindow)
        self.qInputBox = Entry(self.qWindow)
        self.qSubmit = Button(self.qWindow)

        self.qMessage["text"] = "Submit your query"
        self.qMessage.pack({"padx": 10, "pady": 10, "side": "left"})
        self.qInputBox.pack({"side": "left", "padx": 10, "pady": 10})

        self.qSubmit["text"] = "Enter"
        self.qSubmit["command"] = self.query
        self.qSubmit.pack({"side": "right", "padx": 10, "pady": 10})

    def query(self):

        text = self.qInputBox.get()

        if not validate_input(text): return

        keyWords = text.split(' ')
        results = []
        endResults = []

        for keyWord in keyWords:
            query = str(keyWord).upper()
            c.execute("SELECT * FROM KeyWords WHERE Key=?", (query,))
            data = c.fetchall()
            for row in data:
                results.append(row[1])

        for result in results:
            c.execute("SELECT * FROM Fixes WHERE Code=?", (int(result),))
            data = c.fetchall()
            for row in data:
                endResults.append(row[1])

        fix = ""
        for result in endResults:
            if fix is "":
                fix += str(result)
            else:
                fix += "\n\n" + str(result)

        if fix is not "":
            tkBox.showinfo('Fix!', fix)
        else:
            tkBox.showerror('None!', "No possible fixes have been found in our database")

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
