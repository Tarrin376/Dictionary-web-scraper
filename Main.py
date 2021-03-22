""" 
    Importing all of the packages into the program that are required.
    Try catch blocks are used to prevent any import error from crashing the program.
    The user will be prompted with a message asking if they would like to try run it again if 
    an import exception is thrown.
"""
while True:
    try:
        from tkinter import *
        from tkinter import messagebox
        import sqlite3, re, requests, os, smtplib, operator
        from copy import copy
        from bs4 import BeautifulSoup
        from email.message import EmailMessage
        break
    except ImportError as err:
        print(f"IMPORT ERROR: {err}")
        user_input = input("Would you like to try again?: ")
        if user_input.lower() == "no": 
            quit()


class Menu: 
    """
    This class defines the layout of the main menu of the application.
    The class attributes that are needed for the menu are seen below.
    The menuLayout function is the function that creates the whole GUI for the main menu.
    """
    def __init__(self, calculator=None, toDoList=None, dictionary=None, contact=None): # Class Attributes needed for the Menu.
        self.calcualtor = calculator
        self.toDoList = toDoList
        self.dictionary = dictionary
        self.contact = contact
    
    def menuLayout(self, Email, password):
        # Customize the window for the main menu interface.
        # Geometry defines the size of the window.
        # The menu window has been customized by changing the colour and the title.
        # This class is has been created to show the menu interface and the window size.

        menu = Toplevel()
        menu.geometry("1200x630") 
        menu.title("Menu")
        menu.configure(background='#D7D4D4')
        menu.resizable(False, False)

        email_data = Label(menu, text=f"Logged in as: {Email}", font=("Arial", 12))
        welcome = Label(menu, text="Welcome!", font=("Arial", 25))
        subheading = Label(menu, text="Chose an option below:\n\n\n\n\n", font=("Arial", 15))

        Label(menu, text="\t").grid(row=3, column=3)
        Label(menu, text="\t").grid(row=3, column=5)
        Label(menu, text="\t").grid(row=5, column=4)
        
        # Assiging the variables to the calling of the classes so specific functions within the classes can be directly called.
        calculator, toDo, dictionary, contact, sets = Calculator(), ToDoList(), Dictionary(), ContactMe(), Settings() 
        
        """
        Each of these buttons are created on the main menu's GUI.
        When the user clicks any of the buttons that are defined below,
        code in a different class will run so the user can use the features.
        """
        settings = Button(menu, text="Settings", command=lambda: sets.settings(), height=7, width=20, font=("Arial", 12, 'bold'), bg="#137FC7", 
        activebackground="#D0CBCB", fg="white")
        self.calculator = Button(menu, text="Calculator", height=7, width=20, font=("Arial", 12, 'bold'), bg="#137FC7", activebackground="#D0CBCB", fg="white", 
        command=lambda: calculator.calcLayout())
        self.toDoList = Button(menu, text="To Do list", height=7, width=20, font=("Arial", 12, 'bold'), bg="#9B5AFD", activebackground="#D0CBCB", fg="white", 
        command=lambda: toDo.listLayout())
        self.dictionary = Button(menu, text="Dictionary", height=7, width=20, font=("Arial", 12, 'bold'), bg="#EB5757", activebackground="#D0CBCB", fg="white", 
        command=lambda: dictionary.dictLayout())
        self.contact = Button(menu, text="Contact Me", height=7, width=20, font=("Arial", 12, 'bold'), bg="#EB5757", activebackground="#D0CBCB", fg="white", 
        command=lambda: contact.contactLayout())
        logout = Button(menu, text="LOG OUT", height=7, width=20, font=("Arial", 12, 'bold'), bg='#959292', activebackground="#D0CBCB", fg="white", 
        command=lambda: logoutUser(Email)) 
        
        # Gridding all of the elements that will make up the GUI.
        # This includes all of the buttons and also a welcome message to the user.

        email_data.grid(row=0, column=0)
        welcome.grid(row=2, column=4)
        subheading.grid(row=3, column=4)
        settings.grid(row=6, column=2)
        self.calculator.grid(row=4, column=2)
        self.toDoList.grid(row=4, column=4)
        self.dictionary.grid(row=4, column=6)
        self.contact.grid(row=6, column=4)
        logout.grid(row=6, column=6)

        def closeLogout(window):
            # Close the logout confirmation message page.
            # When the user wants to close the login page window,
            # the user can click the close button which will destroy
            # the whole window.
            window.destroy() 
        
        def logoutUser(email):
            """
            This function will run when the user has decided to log out of the 
            software program. When the logout button is pressed, the main menu
            window will close.
            """
            # The user can then decide to sign back in as the login window will
            # always be open throughout the use of the program.
            menu.destroy() 
            logout = Toplevel()
            logout.geometry("430x100")
            logout.resizable(False, False)

            Label(logout, text="\t").grid(row=0, column=0)
            Label(logout, text="\t").grid(row=1, column=0)
            Label(logout, text="You have successfully logged out!", font=("Arial", 15, 'bold')).grid(row=0, column=1)
            Button(logout, text="Continue", command=lambda: closeLogout(logout)).grid(row=1, column=1)


class LoginSystem:
    """
    This is the LoginSystem class that displays the GUI for logging into the program.
    The login GUI is the first window that will be displayed when the user runs the
    program, so they can sign in or create an account
    """
    # self.master is the TopLevel() window.
    # self.email is the entry box that will read the email that the user
    # inputs into the program.
    # self.password is the entry box that will read the password that the user inputs.
     
    def __init__(self, master, email=None, password=None):
        self.email = email
        self.master = master
        self.password = password
    
    """
    This function is used to check all of the inputs from the user.
    Packages such as re are used to validate the user's input through
    regular expressions.
    """
    def createAccount(self, Email, Pass, Pass2, createRoot):
        if re.search(r'^[a-zA-|0-9]+[\._]?[a-zA-Z0-9]+[@]\w+[.]\w{2,3}$', Email.get()):
            password_validator = [
                (lambda x: True if any(i.isupper() for i in x) else False)(Pass.get()), 
                (lambda x: True if any(i.isdigit() for i in x) else False)(Pass.get())
            ] 
            if all(condition == True for condition in password_validator): 
                if re.search(r'[@_!#$%^&*()<>?/\|}{~:]', Pass.get()) and len(Pass.get()) > 7: 
                    if Pass2.get() == Pass.get():
                        try:
                            # Connecting to the DB and inserting the INFO.
                            connect = sqlite3.connect("Info.db") 
                            csr = connect.cursor()
                            csr.execute("INSERT INTO information VALUES (?, ?)", (Email.get(), Pass.get())) 
                            connect.commit() 
                            connect.close() 
                            createRoot.destroy() # Create account window is then destroyed.
                        except ConnectionError as error: 
                            print(f"ERROR CONNECTING: {error}")
                            return
                    else:
                        Label(createRoot, text="Passwords do not match").grid(row=10, column=5)
                else:
                    Label(createRoot, text="Needs one special character").grid(row=10, column=5)
                    Label(createRoot, text="Or please use at least 7 characters").grid(row=11, column=5)
            else:
                Label(createRoot, text="Password needs numbers").grid(row=10, column=5)
                Label(createRoot, text="Or password needs uppercase characters").grid(row=11, column=5)
        else:
            messagebox.showwarning("Warning!", "Invalid Email")
    
    """
    Code for creating the layout of the create account page. 
    E.g. Email entry, pass entry etc.
    Assiging rows and columns to each entry.
    """
    def createAccLayout(self):
        create = Toplevel()
        create.title("Create Account")
        create.geometry("295x310") 
        create.resizable(False, False)

        # Change background colour if settings background is changed.
        try:
            create.configure(background=var.get())
        except NameError:
            pass

        # The layout of the create account window so the user can input information into the program.
        title = Label(create, text="\nCreate Account\n", font=("Arial", 20))
        new_email = Entry(create, width=40)
        new_pass = Entry(create, width=40) 
        new_pass2 = Entry(create, width=40)
        createAcc = Button(create, text="Create Account", command=lambda: self.createAccount(new_email, new_pass, new_pass2, create), bg='#74F3D1')
        
        title.grid(row=0, column=5)
        new_email.grid(row=3, column=5)
        new_pass.grid(row=5, column=5)
        new_pass2.grid(row=7, column=5)
        createAcc.grid(row=8, column=5, pady=10)
        Label(create, text="Email").grid(row=2, column=5)
        Label(create, text="Password").grid(row=4, column=5)
        Label(create, text="Re-Enter pass").grid(row=6, column=5)
        Label(create, text="       ").grid(row=0, column=0)

    def loginPress(self, Email, Pass, Master):
        # Connecting to SQLite3 database.
        # Throw exception if user is unable to connect to database.
        try:
            connect = sqlite3.connect("Info.db") 
            csr = connect.cursor()
        except ConnectionError as error: 
            print(f"ERROR {error}")
            return
        
        # Grabs all of the data from the db.
        csr.execute("SELECT * FROM information")
        data = csr.fetchall() 
        
        """
        Loops through the SQLite DB to see if the user's email and password
        matches any of the rows. If the user's information is valid and is found in 
        the database, the text in the entries will be wiped.
        """
        for i in data: 
            if i[0] == Email.get() and i[1] == Pass.get(): 
                global loggedEmail
                loggedEmail = copy(Email.get())
                Email.delete(0, END)
                Pass.delete(0, END)
                menu = Menu()
                menu.menuLayout(loggedEmail, Pass) 
                return 
        
        # Make entries blank when login button is pressed.
        Email.delete(0, END) 
        Pass.delete(0, END)  
        messagebox.showwarning("Warning!", "Email or password is incorrect!")
        
        # Committing changes to database and closing the connection.
        connect.commit()
        connect.close()

    def layout(self):
        # Creating the size of the login GUI.
        # The login title has been set to Login.
        # Each of the pictures that are defined are used for the buttons.
        self.master.title("Login")
        self.master.geometry("450x500")
        self.master.resizable(False, False)
        self.img1 = PhotoImage(file='C:\\Users\\Spec\\Pictures\\Camera Roll\\login.png') 
        self.loginImg = self.img1.subsample(4, 4) 
        self.img2 = PhotoImage(file='C:\\Users\\Spec\\Pictures\\Camera Roll\\create.png') 
        
        # Changes background colour if settings background is changed.
        try:
            self.master.configure(background=var.get())
        except NameError:
            pass

        """
        Gridding for the login layout. It has entries such as the email and password
        entries so the user is able to input information into the program.
        There is also a createAccount button if the user has not signed up yet
        """
        title = Label(self.master, text="\nSign in\n", font=("Arial", 25))
        self.email = Entry(self.master, width=40)
        self.password = Entry(self.master, width=40)
        loginButton = Button(self.master, image=self.loginImg, command=lambda: self.loginPress(self.email, self.password, self.master), relief=FLAT)
        createAcc = Button(self.master, image=self.img2, command=lambda: self.createAccLayout(), relief=FLAT)
        emailText = Label(self.master, text="\nEmail:\n", font=("Roboto Medium", 12))
        passText = Label(self.master, text="\nPassword:\n", font=("Roboto Medium", 12))

        title.grid(row=0, column=5)
        self.email.grid(row=1, column=5) 
        self.password.grid(row=2, column=5)
        loginButton.grid(row=3, column=5)
        createAcc.grid(row=4, column=5)
        emailText.grid(row=1, column=0)
        passText.grid(row=2, column=0)


class Calculator(LoginSystem):
    """
    This calculator class is a simple GUI that allows the user to input
    numbers and operators to perform mathematical calculations.
    Self.master is the window of the GUI.
    """
    # Class attributes needed for Calculator.
    # Inheriting attributes from LoginSystem class.
    def __init__(self, master=None, userInput=None, count=0): 
        super().__init__(master) 
        self.userInput = userInput
        self.count = count
    
    # This function performs the mathematical calculations based
    # on what the user inputs into the program.
    # Operators are used so the program can understand what the user wants to do.
    def calculations(self, entryBox, value):
        self.count += 1
        calc = [] 
        ops = {
            "%": operator.mod, "+": operator.add,
            "-": operator.sub, "*": operator.mul,
            "/": operator.truediv, "^": operator.pow
        }
         
        # When the user wants to see the result.
        # Looping through the entry box and outputting the result.
        if value == "=":
            calc.append(entryBox.get())
            for j in range(len(calc[0])):
                if calc[0][j] in ops.keys():
                    try: 
                        entryBox.delete(0, END)
                        entryBox.insert(END, ops[calc[0][j]]
                        (float(calc[0][:j]), float(calc[0][j+1:])))
                    except ValueError:
                        entryBox.insert(END, "INVALID CALCULATION")
        
        # If the value is not an operator and is not a number.
        # self.count is the length of the value in the entry box.
        if value not in ops and type(value) == str:
            if value == "C": entryBox.delete(0, END)
            if value == "🢠": 
                entryBox.delete(self.count - 2, self.count - 1)
                if self.count == 1:
                    entryBox.delete(0, END)
                else:
                    self.count = self.count - 2
            if value == ".": entryBox.insert(END, value)
        else:
            calc.append(value)
            entryBox.insert(END, value)
        
    def calcLayout(self):
        """
        This function is used to create the layout of the calculator's
        GUI. The size of the window is 508x515 and the title is called 
        Calculator. 
        Each of the buttons call the calculation() function so the value
        can be stored and used later on for mathematical operations.
        """
        self.master = Toplevel() 
        self.master.geometry("508x515")
        self.master.title("Calculator")
        self.master.configure(background="#878D98")
        self.master.resizable(False, False)
        large_font = ('Courier',29)
        calc = Calculator()
        
        self.userInput = Entry(self.master, font=large_font, relief=FLAT, justify="right", bg="#878D98", fg="white")
        C = Button(self.master, text="C", width=13, height=4, font=("Arial", 11, 'bold'), bg="#7B818D", activebackground="#D0CBCB", fg="white", 
        command=lambda: calc.calculations(self.userInput, "C"))
        Mod = Button(self.master, text="%", width=13, height=4, font=("Arial", 11, 'bold'), bg="#7B818D", activebackground="#D0CBCB", fg="white", 
        command=lambda: calc.calculations(self.userInput, "%"))
        Sqr = Button(self.master, text="x^y", width=13, height=4, font=("Arial", 11, 'bold'), bg="#7B818D", activebackground="#D0CBCB", fg="white", 
        command=lambda: calc.calculations(self.userInput, "^"))
        Back = Button(self.master, text="🢠", width=13, height=4, font=("Arial", 11, 'bold'), bg="#262E3D", activebackground="#D0CBCB", fg="white", 
        command=lambda: calc.calculations(self.userInput, "🢠"))
        Num1 = Button(self.master, text="1", width=13, height=4, font=("Arial", 11, 'bold'), bg="#525965", activebackground="#D0CBCB", fg="white", 
        command=lambda: calc.calculations(self.userInput, 1))
        Num2 = Button(self.master, text="2", width=13, height=4, font=("Arial", 11, 'bold'), bg="#525965", activebackground="#D0CBCB", fg="white", 
        command=lambda: calc.calculations(self.userInput, 2))
        Num3 = Button(self.master, text="3", width=13, height=4, font=("Arial", 11, 'bold'), bg="#525965", activebackground="#D0CBCB", fg="white", 
        command=lambda: calc.calculations(self.userInput, 3))
        Add = Button(self.master, text="+", width=13, height=4, font=("Arial", 11, 'bold'), bg="#262E3D", activebackground="#D0CBCB", fg="white", 
        command=lambda: calc.calculations(self.userInput, "+"))
        Num4 = Button(self.master, text="4", width=13, height=4, font=("Arial", 11, 'bold'), bg="#525965", activebackground="#D0CBCB", fg="white", 
        command=lambda: calc.calculations(self.userInput, 4))
        Num5 = Button(self.master, text="5", width=13, height=4, font=("Arial", 11, 'bold'), bg="#525965", activebackground="#D0CBCB", fg="white", 
        command=lambda: calc.calculations(self.userInput, 5))
        Num6 = Button(self.master, text="6", width=13, height=4, font=("Arial", 11, 'bold'), bg="#525965", activebackground="#D0CBCB", fg="white", 
        command=lambda: calc.calculations(self.userInput, 6))
        Minus = Button(self.master, text="-", width=13, height=4, font=("Arial", 11, 'bold'), bg="#262E3D", activebackground="#D0CBCB", fg="white", 
        command=lambda: calc.calculations(self.userInput, "-"))
        Num7 = Button(self.master, text="7", width=13, height=4, font=("Arial", 11, 'bold'), bg="#525965", activebackground="#D0CBCB", fg="white", 
        command=lambda: calc.calculations(self.userInput, 7))
        Num8 = Button(self.master, text="8", width=13, height=4, font=("Arial", 11, 'bold'), bg="#525965", activebackground="#D0CBCB", fg="white", 
        command=lambda: calc.calculations(self.userInput, 8))
        Num9 = Button(self.master, text="9", width=13, height=4, font=("Arial", 11, 'bold'), bg="#525965", activebackground="#D0CBCB", fg="white", 
        command=lambda: calc.calculations(self.userInput, 9))
        Mult = Button(self.master, text="x", width=13, height=4, font=("Arial", 11, 'bold'), bg="#262E3D", activebackground="#D0CBCB", fg="white", 
        command=lambda: calc.calculations(self.userInput, "*"))
        Num0 = Button(self.master, text="0", width=13, height=4, font=("Arial", 11, 'bold'), bg="#262E3D", activebackground="#D0CBCB", fg="white", 
        command=lambda: calc.calculations(self.userInput, 0))
        Dec = Button(self.master, text=".", width=13, height=4, font=("Arial", 11, 'bold'), bg="#525965", activebackground="#D0CBCB", fg="white", 
        command=lambda: calc.calculations(self.userInput, "."))
        Equal = Button(self.master, text="=", width=13, height=4, font=("Arial", 11, 'bold'), bg="#E62E59", activebackground="#D0CBCB", fg="white", 
        command=lambda: calc.calculations(self.userInput, "="))
        Div = Button(self.master, text="/", width=13, height=4, font=("Arial", 11, 'bold'), bg="#262E3D", activebackground="#D0CBCB", fg="white", 
        command=lambda: calc.calculations(self.userInput, "/"))

        self.userInput.grid(row=1, column=0, columnspan=10, pady=20)
        C.grid(row=2, column=0, sticky="nsew")
        Mod.grid(row=2, column=1, sticky="nsew")
        Sqr.grid(row=2, column=2, sticky="nsew")
        Back.grid(row=2, column=3, sticky="nsew")
        Num1.grid(row=3, column=0, sticky="nsew")
        Num2.grid(row=3, column=1, sticky="nsew")
        Num3.grid(row=3, column=2, sticky="nsew")
        Add.grid(row=3, column=3, sticky="nsew")
        Num4.grid(row=4, column=0, sticky="nsew")
        Num5.grid(row=4, column=1, sticky="nsew")
        Num6.grid(row=4, column=2, sticky="nsew")
        Minus.grid(row=4, column=3, sticky="nsew")
        Num7.grid(row=5, column=0, sticky="nsew")
        Num8.grid(row=5, column=1, sticky="nsew")
        Num9.grid(row=5, column=2, sticky="nsew")
        Mult.grid(row=5, column=3, sticky="nsew")
        Num0.grid(row=6, column=0, sticky="nsew")
        Dec.grid(row=6, column=1, sticky="nsew")
        Equal.grid(row=6, column=2, sticky="nsew")
        Div.grid(row=6, column=3, sticky="nsew")
    

class ToDoList:
    # This is the ToDoList class that allows the user to make and save notes.
    # The Notes() function is used to display the notes that the user submits
    # to the program.
    # Each notes can also be DELETED from the GUI through the __delitem__ dunder method.
    @staticmethod
    def createNotes(note, add_note_window):
        """
        The size of the ToDoList window is 1400x750. This function loops over
        the notes.txt file and displays any of the information on that file.
        When the Notes window is displayed, the add_note_window is destroyed.
        """
        note = Toplevel()
        note.geometry("1400x750")
        note.title("Current notes")
        add_note_window.destroy()

        # Changes background colour if settings background is changed.
        try:
            note.configure(background=var.get())
        except NameError:
            pass
        
        notesList = []
        with open('notes.txt', 'r') as f:
            lines = f.readlines()
            [notesList.append(line) for line in lines if line not in notesList]
        
        for i in notesList:
            # Looping through all of the notes submitted by the user.
            noteVal = Text(note)
            noteVal.insert(END, f"Note {notesList.index(i)}:\n{i}")
            noteVal.configure(font=('Courier',10), background="#FAFAFA", width=25, height=10)
            noteVal.grid(row=2, column=notesList.index(i), padx=5)
        
        removeAll = Button(note, text="Remove All Notes", pady=10, command=lambda: ToDoList.deleteAllNotes('notes.txt', notesList, note))
        removeNote = Entry(note, font=("Courier", 12), bg="#878D98", fg="white")
        title = Label(note, text="To Do List", font=("Courier", 15))
        removeNoteSubmit = Button(note, text="Remove", height=3, width=12, font=("Arial", 9, 'bold'), bg="#9B5AFD", 
        activebackground="#D0CBCB", fg="white", command=lambda: ToDoList.deleteNote(removeNote.get(), 'notes.txt', notesList, note))

        removeAll.grid(row=0, column=0)
        title.grid(row=7, column=0, pady=10)
        removeNote.grid(row=9, column=0)
        removeNoteSubmit.grid(row=10, column=0, pady=7)
        Label(note, text="\n\n\n").grid(row=0, column=1)
        Label(note, text="Remove Note (number): ").grid(row=8, column=0)

    # This function writes the users input into a text file.
    # The text files content is then displayed on the window.
    @staticmethod
    def submitNote(note, window):
        if note.get() != "":
            Label(window, text="Note added to library!").grid(row=5, column=1)
            with open('notes.txt', 'a') as f:
                f.write(f"{note.get()}\n") # Writing note to 'notes.txt' file.
                f.close()
            note.delete(0, END)
            Button(window, text="View notes", height=2, width=10, font=("Arial", 12, 'bold'), bg="#9B5AFD", 
            activebackground="#D0CBCB", fg="white", 
            command=lambda: ToDoList.createNotes(note.get(), window)).grid(row=6, column=1, pady=5)
        else:
            messagebox.showwarning("Warning!", "Note is blank!")
    
    # This function deletes the note that the user requests to delete.
    # It will write all of the notes to the 'notes.txt' file.
    def deleteNote(noteNumber, notesFile, noteLi, window):
        curWindow = window
        with open(notesFile, 'r') as f:
            lines = f.readlines()
            try:
                if int(noteNumber) < len(noteLi):
                    with open(notesFile, 'w') as f:
                        [f.write(noteLi[line]) for line in range(len(noteLi)) if line != int(noteNumber)]
                        [noteLi[note] == '' for note in range(len(noteLi)) if note == int(noteNumber)]
                    Label(curWindow, text="Note has been deleted", font=("Roboto", 12)).grid(row=1, column=0)
                else:
                    Label(curWindow, text="Invalid note number", font=("Roboto", 12)).grid(row=11, column=0)
            except ValueError:
                Label(curWindow, text="Invalid note number", font=("Roboto", 12)).grid(row=11, column=0)
    
    # Deletes all the contents in the 'notes.txt' file.
    def deleteAllNotes(notesFile, noteLi, window):
        noteLi = []
        with open(notesFile, 'r+') as f:
            f.truncate(0)
            f.close()
    
    def listLayout(self):
        """The GUI layout of the To Do List"""
        self.window = Toplevel()
        self.window.geometry("575x475")
        self.window.title("To Do List")
        self.window.resizable(False, False)
        large_font = ('Courier',29)
        
        # Changes background colour if settings background is changed.
        try:
            self.window.configure(background=var.get())
        except NameError:
            pass
        
        noteText = Label(self.window, text="Note", font=("Calibri", 15))
        noteEntry = Entry(self.window, relief=SUNKEN, bg="#ECFFFF", fg="#6B6B6B", font=("Calibri", 13, 'bold'))
        submit = Button(self.window, text="Add Note", height=2, width=10, font=("Arial", 12, 'bold'), bg="#9B5AFD", 
        activebackground="#D0CBCB", fg="white", 
        command=lambda: ToDoList.submitNote(noteEntry, self.window))

        Label(self.window, text="To Do List", font=large_font).grid(row=1, column=1, pady=50)
        noteText.grid(row=3, column=0)
        noteEntry.grid(row=3, column=1, ipadx=150, ipady=60, pady=10)
        submit.grid(row=4, column=1, pady=10)


class Dictionary(object):
    # self.definition is the definition of the word.
    # self.window is the GUI window.
    # word is the user's input - Class variable.
    word = None
    def __init__(self, source=None, definition=None):
        self.source = source
        self.definition = definition
    
    #The web scraper that scrapes the definition from https://dictionary.cambridge.org/dictionary/english/[example word].
    #Setting HEADER to FireFox to allow the program to scape the information from the site.
    def webScraper(self, master, word):
        headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
        try:
            self.source = requests.get(f'https://dictionary.cambridge.org/dictionary/english/{word}', headers=headers).text
            soup = BeautifulSoup(self.source, 'lxml')
        except requests.exceptions.HTTPError as err1:
            print(f"HTTP ERROR: \n{err1}")
            return
        except requests.exceptions.ConnectionError as err2:
            print(f"ERROR CONNECTING: \n{err2}")
            return
        except requests.exceptions.Timeout as err3:
            print(f"TIMEOUT ERROR: \n{err3}")
            return
        except requests.exceptions.RequestException as err4:
            print(f"ERROR REQUESTING: \n{err4}")
            return
        
        # Looping through the HTML of the site to try and find the definition.
        # Will then print the text of the certain class in the HTML of the site.
        for dictionary in soup.find_all('body'):
            try:
                defClass = dictionary.find('div', class_="def ddef_d db").get_text()
                Label(master, text="Definition:", font=("Courier", 12)).grid(row=7, column=0, pady=20)
                self.definition = Text(master)
                self.definition.insert(END, defClass)
                self.definition.configure(font=('Roboto',12), background="#FAFAFA", height=4)
                self.definition.grid(row=7, column=1)
            except TypeError as err:
                print(f"ERROR! {err}")
            except AttributeError:
                # If the class cannot be found on the site E.g. INVALID WORD causing HTTP ERROR.
                Label(master, text="Error:", font=("Courier", 12)).grid(row=9, column=0)
                Label(master, text="This word is not a valid word in the dictionary", font=("Robot", 13, "bold")).grid(row=9, column=1)
    
    # Checking the user's input to make sure that it is valid.
    def checkInput(self, window, userWord, dictClass):
        if re.search(r'[@_!#$%^&*()<>?/\|}{~:]', userWord) or re.search(r'[0-9]', userWord):
            Label(window, text="Error:", font=("Courier", 12)).grid(row=9, column=0)
            Label(window, text="This word is not a valid word in the dictionary", font=("Robot", 13, "bold")).grid(row=9, column=1)
        elif userWord == "":
            Label(window, text="Error:", font=("Courier", 12)).grid(row=9, column=0)
            Label(window, text="This word is not a valid word in the dictionary", font=("Robot", 13, "bold")).grid(row=9, column=1)
        else:
            Label(window, text=f"Searching for word...", font=("Roboto", 10, "bold")).grid(row=5, column=1, pady=20)
            dictClass.webScraper(window, userWord)

    @classmethod    
    def dictLayout(cls):
        """ Layout of the Dictionary's GUI"""
        # TopLevel() creates a new window for the online dictionary.
        window = Toplevel()
        window.title("Dictionary")
        window.geometry("1150x600")
        window.resizable(False, False)
        check = Dictionary()
        
        # Changes background colour if settings background is changed.
        try:
            window.configure(background=var.get())
        except NameError:
            pass
        
        # Gridding and adding elements for the GUI.
        title = Label(window, text="Dictionary\n\n\n", font=("Courier", 25))
        cls.word = Entry(window, relief=SUNKEN, bg="#ECFFFF", fg="#6B6B6B", font=("Calibri", 20))
        definition = Button(window, text="Definition", height=2, width=10, font=("Arial", 12, 'bold'), bg="#9B5AFD", activebackground="#D0CBCB", fg="white", 
        command=lambda: check.checkInput(window, cls.word.get(), check))

        Label(window, text="\t\t\t\t").grid(row=0, column=0)
        Label(window, text="Word:", font=("Courier", 12)).grid(row=2, column=0)
        Label(window, text="This dictionary scrapes the web to find the definition of your chosen word!", font=("Courier", 12)).grid(row=0, column=1)
        Label(window, text="\t\t\t\t").grid(row=0, column=2)

        title.grid(row=0, column=1)
        cls.word.grid(row=2, column=1, ipadx=50, ipady=50, pady=10, sticky="nsew")
        definition.grid(row=3, column=1, pady=10, ipady=20, ipadx=20)


class ContactMe:
    def __init__(self, master=None, firstName=None, lastName=None, usersEmail=None):
        self.master = master
        self.firstName = firstName
        self.lastName = lastName
        self.usersEmail = usersEmail
    
    """Function that retrieves the user's name, last name and email"""
    # It then uses these values to send an email to the user.
    # This is done through the use of an environment variable (sender of the email)
    def sendEmail(self, firstName, lastName, emailAdd):
        EMAIL_ADDRESS = os.environ.get('Gmail Email')
        EMAIL_PASS = os.environ.get('Gmail Pass')

        EmailMs = EmailMessage()
        EmailMs['Subject'] = "Contact Request"
        EmailMs['From'] = EMAIL_ADDRESS
        EmailMs['To'] = emailAdd
        EmailMs.set_content(f"""
        Hello {firstName} {lastName} ({emailAdd}), you have requested to get in contact with me. 
        If you would like to ask a question, please reply with your question. Thank you!
        """)
        
        # Requesting an SMTP protocol to Gmail.
        # Signing into Gmail using Environment variables.
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASS)
            smtp.send_message(EmailMs)
    
    # Checking the user's input to make sure that the details are valid.
    # Using REGEX to validate inputs.
    def confirmRequest(self, first, last, email, master, contact):
        if re.search(r'[0-9@_!#$%^&*()<>?/\|}{~:]', first.get()) or re.search(r'[0-9@_!#$%^&*()<>?/\|}{~:]', last.get()):
            Label(master, text="Invalid first or last name").grid(row=6, column=4, pady=10)
        elif first.get() == "" or last.get() == "":
            Label(master, text="Boxes can't be empty").grid(row=8, column=4, pady=10)
        else:
            if email.get() == loggedEmail:
                Label(master, text="Submission Successful").grid(row=8, column=4, pady=10)
                contact.sendEmail(first.get(), last.get(), email.get())
                first.delete(0, END)
                last.delete(0, END)
                email.delete(0, END)
            else:
                messagebox.showwarning("Unmatched Email", "Email doesn't matched logged in email")
    
    def contactLayout(self):
        # Layout of the contact page GUI.
        # self.master is the window that is set to 630x400.
        self.master = Toplevel()
        self.master.geometry("630x400")
        self.master.title("Contact Me")
        self.master.resizable(False, False)
        contact = ContactMe()
        
        # Changes background colour if settings background is changed.
        try:
            self.master.configure(background=var.get())
        except NameError:
            pass
        
        # Creating the elements for the contact page.
        title = Label(self.master, text="Contact Me\n", font=("Courier", 17, "bold"))
        firstText = Label(self.master, text="First Name: ", font=("Courier", 10))
        lastText = Label(self.master, text="Last Name: ", font=("Courier", 10))
        emailText = Label(self.master, text="Confirm Email:", font=("Courier", 10))

        self.firstName = Entry(self.master, relief=SUNKEN, bg="#ECFFFF", fg="#6B6B6B", font=("Calibri", 15))
        self.lastName = Entry(self.master, relief=SUNKEN, bg="#ECFFFF", fg="#6B6B6B", font=("Calibri", 15))
        self.usersEmail = Entry(self.master, relief=SUNKEN, bg="#ECFFFF", fg="#6B6B6B", font=("Calibri", 15))
        confirmRequest = Button(
            self.master, text="Submit", height=2, width=10, font=("Arial", 12, 'bold'), bg="#9B5AFD", activebackground="#D0CBCB", fg="white",
            command=lambda: contact.confirmRequest(self.firstName, self.lastName, self.usersEmail, self.master, contact)
        )
        
        # Gridding the elements to the contact page GUI.
        Label(self.master, text="\t\t   ").grid(row=0, column=0)
        title.grid(row=0, column=4)
        firstText.grid(row=2, column=3, ipady=20)
        lastText.grid(row=3, column=3, ipady=20)
        emailText.grid(row=4, column=3, ipady=20)
        self.firstName.grid(row=2, column=4, ipadx=20, ipady=10, pady=10)
        self.lastName.grid(row=3, column=4, ipadx=20, ipady=10, pady=10)
        self.usersEmail.grid(row=4, column=4, ipadx=20, ipady=10, pady=10)
        confirmRequest.grid(row=5, column=4, ipadx=20, ipady=10, pady=10)
    

class Settings:
    """
    This class allows the user to modify the GUI to their needs
    applySettings() function closes the window of the settings page
    when requested
    """
    def applySettings(self, settingsPage):
        settingsPage.destroy()

    def settings(self):
        # Opens new window when settings button is clicked.
        # Size of window is 300x220.
        window = Toplevel() 
        window.geometry("300x220") 
        window.configure(background='#D7D4D4')
        window.title("Settings")
        window.resizable(False, False)
        sets = Settings()
        
        # Value that will be used to change the background colour.
        global var
        var = StringVar()
        var.set("#f0f0ed")
        
        # Creating the elements for the settings GUI.
        title = Label(window, text="Settings\n", font=("Arial", 20))
        background = Label(window, text="Background:\t")
        lightMode = Radiobutton(window, text="\nLight: ", variable=var, value="#F0F0ED")
        darkMode = Radiobutton(window, text="Dark: \n", variable=var, value="#A8A8A8")
        submitSets = Button(window, text="Apply", command=lambda: sets.applySettings(window))
        
        # Gridding the elements for the settings GUI.
        title.grid(row=1, column=5)
        background.grid(row=2, column=0)
        lightMode.grid(row=3, column=0)
        darkMode.grid(row=4, column=0)
        submitSets.grid(row=6, column=5)


if __name__ == "__main__": # Checking if program is in main before running code.
    root = Tk()
    root.geometry("370x330") # Setting size of the window.
    login = LoginSystem(root)
    login.layout()
    root.mainloop() # Keep root window open while the program is running.