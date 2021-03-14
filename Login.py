while True:
    try:
        from tkinter import *
        from tkinter import messagebox
        import sqlite3, re, requests, os, smtplib
        from copy import copy
        from bs4 import BeautifulSoup
        from email.message import EmailMessage
        import operator
        break
    except ImportError as err:
        print(f"ERROR! {err}")
        user_input = input("Would you like to try again?: ")
        if user_input.lower() == "no":
            quit()


class Menu: # Main menu of GUI class.
    def __init__(self, calculator=None, toDoList=None, dictionary=None, contact=None): # Class Attributes needed for the Menu.
        self.calcualtor = calculator
        self.toDoList = toDoList
        self.dictionary = dictionary
        self.contact = contact
    

    def menuLayout(self, Email, password):
        menu = Toplevel()
        menu.geometry("1200x630") # Size of window.
        menu.title("Menu")
        menu.configure(background='#D7D4D4')

        email_data = Label(menu, text=f"Logged in as: {Email}", font=("Arial", 12))
        welcome = Label(menu, text="Welcome!", font=("Arial", 25))
        subheading = Label(menu, text="Chose an option below:\n\n\n\n\n", font=("Arial", 15))
        Label(menu, text="\t").grid(row=3, column=3)
        Label(menu, text="\t").grid(row=3, column=5)
        Label(menu, text="\t").grid(row=5, column=4)

        calculator = Calculator() # Assigning calculator variable to Calculator class call so a function can be called from a different class.
        toDo = ToDoList()
        dictionary = Dictionary()
        contact = ContactMe()
        sets = Settings()

        settings = Button(menu, text="Settings", command=lambda: sets.settings(), height=7, width=20, font=("Arial", 12, 'bold'), bg="#137FC7", activebackground="#D0CBCB", fg="white")
        self.calculator = Button(menu, text="Calculator", height=7, width=20, font=("Arial", 12, 'bold'), bg="#137FC7", activebackground="#D0CBCB", fg="white", 
        command=lambda: calculator.calcLayout())
        self.toDoList = Button(menu, text="To Do list", height=7, width=20, font=("Arial", 12, 'bold'), bg="#9B5AFD", activebackground="#D0CBCB", fg="white", 
        command=lambda: toDo.listLayout())
        self.dictionary = Button(menu, text="Dictionary", height=7, width=20, font=("Arial", 12, 'bold'), bg="#EB5757", activebackground="#D0CBCB", fg="white", 
        command=lambda: dictionary.dictLayout())
        self.contact = Button(menu, text="Contact Me", height=7, width=20, font=("Arial", 12, 'bold'), bg="#EB5757", activebackground="#D0CBCB", fg="white", 
        command=lambda: contact.contactLayout())
        logout = Button(menu, text="LOG OUT", height=7, width=20, font=("Arial", 12, 'bold'), bg='#959292', activebackground="#D0CBCB", fg="white", 
        command=lambda: logout_user(Email)) # Calling logout function.

        email_data.grid(row=0, column=0)
        welcome.grid(row=2, column=4)
        subheading.grid(row=3, column=4)
        settings.grid(row=6, column=2)
        self.calculator.grid(row=4, column=2)
        self.toDoList.grid(row=4, column=4)
        self.dictionary.grid(row=4, column=6)
        self.contact.grid(row=6, column=4)
        logout.grid(row=6, column=6)


        """""""""""""""""""""""""""""""""""""""""
        Gridding layout for the titles and entries.
        """""""""""""""""""""""""""""""""""""""""


        def close_logout(window):
            window.destroy() # Close the logout confirmation message page.
        

        def logout_user(email):
            menu.destroy() # Closes the main menu window.
            
            logout = Toplevel()
            logout.geometry("430x100")
            Label(logout, text="\t").grid(row=0, column=0)
            Label(logout, text="\t").grid(row=1, column=0)
            Label(logout, text="You have successfully logged out!", font=("Arial", 15, 'bold')).grid(row=0, column=1)
            Button(logout, text="Continue", command=lambda: close_logout(logout)).grid(row=1, column=1)


class LoginSystem:
    def __init__(self, master, email=None, password=None): # Class attributes needed for login system.
        self.email = email
        self.master = master
        self.password = password

    
    def createAccount(self, Email, Pass, Pass2, createRoot):
        if re.search(r'^[a-zA-|0-9]+[\._]?[a-zA-Z0-9]+[@]\w+[.]\w{2,3}$', Email.get()):
            password_validator = [
                (lambda x: True if any(i.isupper() for i in x) else False)(Pass.get()), # Lambda expressions to check if passwords meet the conditions.
                (lambda x: True if any(i.isdigit() for i in x) else False)(Pass.get())
            ] 
            if all(condition == True for condition in password_validator):
                if re.search(r'[@_!#$%^&*()<>?/\|}{~:]', Pass.get()) and len(Pass.get()) > 7: # Using email regular expression to check validity of email.
                    if Pass2.get() == Pass.get(): # Making sure that the re-entered password matches the original.
                        try:
                            connect = sqlite3.connect("Info.db")
                            csr = connect.cursor()
                            csr.execute("INSERT INTO information VALUES (?, ?)", (Email.get(), Pass.get())) # Adding new email and password to database.
                            connect.commit() # Committing changes to database and closing the connection.
                            connect.close() # Closing the connection.
                            createRoot.destroy()
                        except ConnectionError as error:
                            print(f"ERROR {error}")
                            return
                    else:
                        Label(createRoot, text="Passwords do not match").grid(row=10, column=5) # If passwords dont match.
                else:
                    Label(createRoot, text="Needs one special character").grid(row=10, column=5)
                    Label(createRoot, text="Or please use at least 7 characters").grid(row=11, column=5)
            else:
                Label(createRoot, text="Password needs numbers").grid(row=10, column=5)
                Label(createRoot, text="Or password needs uppercase characters").grid(row=11, column=5)
        else:
            messagebox.showwarning("Warning!", "Invalid Email") # Warning box if the email does not match the regex expression.


    def createAccLayout(self):
        create = Toplevel()
        create.title("Create Account")
        create.geometry("295x310") # Setting window size for create account page.

        try:
            create.configure(background=var.get())
        except NameError:
            pass

        title = Label(create, text="\nCreate Account\n", font=("Arial", 20))
        new_email = Entry(create, width=40)
        new_pass = Entry(create, width=40) # User inputs for creating a new account.
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


        """
            Code for creating the layout of the create account page. 
            E.g. Email entry, pass entry etc.
            Assiging rows and columns to each entry.
        """


    def loginPress(self, Email, Pass, Master):
        try:
            connect = sqlite3.connect("Info.db") # Connecting to SQLite3 database.
            csr = connect.cursor()
        except ConnectionError as error: # Throw exception if user is unable to connect to database.
            print(f"ERROR {error}")
            return

        csr.execute("SELECT * FROM information") # Grabs all of the data from the db.
        data = csr.fetchall() # Stored tuples of all the data in db in variable.

        for i in data: # Looping through db.
            if i[0] == Email.get() and i[1] == Pass.get(): # Checking if details exist or not.
                global loggedEmail
                loggedEmail = copy(Email.get())
                Email.delete(0, END)
                Pass.delete(0, END)
                menu = Menu()
                menu.menuLayout(loggedEmail, Pass) # Calling menuLayout function in Menu class.
                return # Prevent code from continuing after function call.
                                             
        Email.delete(0, END) # Make entries blank when login button is pressed.
        Pass.delete(0, END) 
          
        messagebox.showwarning("Warning!", "Email or password is incorrect!")

        connect.commit() # Committing changes to database and closing the connection.
        connect.close()


    def layout(self):
        self.master.title("Login")
        self.master.geometry("450x500")

        try:
            self.master.configure(background=var.get())
        except NameError:
            pass

        self.img1 = PhotoImage(file='C:\\Users\\Spec\\Pictures\\Camera Roll\\login.png') 
        self.loginImg = self.img1.subsample(4, 4) 
        self.img2 = PhotoImage(file='C:\\Users\\Spec\\Pictures\\Camera Roll\\create.png') 

        """ Images for login and logout buttons """

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
        
        # Layout of the login page.

  
class Calculator(LoginSystem):
    def __init__(self, master=None, userInput=None): # Class attributes needed for Calculator.
        super().__init__(master) # Inheriting attributes from LoginSystem class.
        self.userInput = userInput
    

    def calculations(self, entryBox, value):
        calc = []
        ops = {
            "%": operator.mod,
            "+": operator.add,
            "-": operator.sub,
            "*": operator.mul,
            "/": operator.truediv,
            "^": operator.pow
        }

        if value == "=":
            calc.append(entryBox.get())
            for j in range(len(calc[0])):
                if calc[0][j] in ops.keys():
                    try: 
                        entryBox.delete(0, END)
                        entryBox.insert(END, ops[calc[0][j]](float(calc[0][:j]), float(calc[0][j+1:])))
                    except ValueError as err:
                        print(f"INVALID CALCULATION: {err}")
                        entryBox.delete(0, END)

        if value not in ops and type(value) == str:
            if value == "C": entryBox.delete(0, END)
            if value == "🢠": entryBox.delete(0, END)
            if value == ".": entryBox.insert(END, value)
        else:
            calc.append(value)
            entryBox.insert(END, value)
        

    def calcLayout(self):
        self.master = Toplevel() # Creating new window.
        self.master.geometry("508x515")
        self.master.title("Calculator")
        self.master.configure(background="#878D98")
        large_font = ('Courier',29)
        calc = Calculator()
        
        self.userInput = Entry(self.master, font=large_font, relief=FLAT, justify="right", bg="#878D98", fg="white")
        C = Button(self.master, text="C", width=13, height=4, font=("Arial", 11, 'bold'), bg="#7B818D", activebackground="#D0CBCB", fg="white", 
        command=lambda: calc.calculations(self.userInput, "C"))
        Mod = Button(self.master, text="%", width=13, height=4, font=("Arial", 11, 'bold'), bg="#7B818D", activebackground="#D0CBCB", fg="white", 
        command=lambda: calc.calculations(self.userInput, "%"))
        Sqr = Button(self.master, text="x²", width=13, height=4, font=("Arial", 11, 'bold'), bg="#7B818D", activebackground="#D0CBCB", fg="white", 
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
        
        """ Gridding/layout of page """


class ToDoList:
    @staticmethod
    def Notes(note, add_note_window):
        notes = Toplevel()
        notes.geometry("1400x750")
        notes.title("Current notes")
        notes.configure(background="#83B7C1")
        add_note_window.destroy()
        
        notesList = []
        with open('notes.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line not in notesList: notesList.append(line)

        for i in notesList:
            noteVal = Text(notes)
            noteVal.insert(END, f"Note {notesList.index(i)}:\n{i}")
            noteVal.configure(font=('Courier',10), background="#FAFAFA", width=25, height=10)
            noteVal.grid(row=2, column=notesList.index(i))
            curNote = Button(notes, text="Remove Note", pady=10, command=lambda: removeNote(i, 'notes.txt', notesList, notes))
            curNote.grid(row=3, column=notesList.index(i))

        Label(notes, text="\n\n\n").grid(row=0, column=1)
        Label(notes, text="\t\t\t\t\t\t").grid(row=0, column=7)
        title = Label(notes, text="To Do List", font=("Courier", 25))
        close = Button(notes, text="Close", command=lambda: close(notes))

        title.grid(row=0, column=7)
        close.grid(row=0, column=0, pady=10)

        def close(window):
            window.destroy()

        def removeNote(currentNote, notesFile, noteLi, window):
            with open(notesFile, 'r') as f:
                lines = f.readlines()
            with open(notesFile, 'w') as f:
                for line in lines:
                    if line != currentNote: f.write(line)
            
            for note in noteLi:
                if note == currentNote: 
                    note.replace(note, '')
            
            curWindow = window
            Label(curWindow, text="Note has been deleted").grid(row=1, column=0)
            

    @staticmethod
    def submitNote(note, window):
        if note.get() != "":
            Label(window, text="Note added to library!").grid(row=5, column=1)
            with open('notes.txt', 'a') as f:
                f.write(f"{note.get()}\n")
                f.close()
            Button(window, text="View notes", command=lambda: ToDoList.Notes(note.get(), window)).grid(row=6, column=1)
        else:
            messagebox.showwarning("Warning!", "Note is blank!")


    def listLayout(self):
        self.window = Toplevel()
        self.window.geometry("530x400")
        self.window.title("To Do List")
        large_font = ('Courier',29)

        try:
            self.window.configure(background=var.get())
        except NameError:
            pass
        
        noteText = Label(self.window, text="Note", font=("Calibri", 15))
        noteEntry = Entry(self.window, relief=SUNKEN, bg="#878D98", fg="white", font=("Calibri", 10))
        submit = Button(self.window, text="Add Note", command=lambda: ToDoList.submitNote(noteEntry, self.window))

        Label(self.window, text="To Do List", font=large_font).grid(row=1, column=1, pady=50)
        noteText.grid(row=3, column=0)
        noteEntry.grid(row=3, column=1, ipadx=150, ipady=60, pady=10)
        submit.grid(row=4, column=1)


class Dictionary:
    def __init__(self, window=None, master=None, definition=None, word=None):
        self.master = master
        self.definition = definition
        self.word = word
        self.window = window
    

    def webScraper(self, master, word):
        headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
        try:
            source = requests.get(f'https://dictionary.cambridge.org/dictionary/english/{word}', headers=headers).text
            soup = BeautifulSoup(source, 'lxml')
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
        
        for dictionary in soup.find_all('body'):
            try:
                defClass = dictionary.find('div', class_="def ddef_d db").get_text()
                Label(master, text="Definition:", font=("Courier", 12)).grid(row=7, column=0, pady=20)
                definition = Text(master)
                definition.insert(END, defClass)
                definition.configure(font=('Courier',10), background="#FAFAFA", height=3)
                definition.grid(row=7, column=1)
            except TypeError as err:
                print(f"ERROR! {err}")
            except AttributeError:
                Label(master, text="Error:", font=("Courier", 12)).grid(row=9, column=0)
                Label(master, text="This word is not a valid word in the dictionary", font=("Robot", 13, "bold")).grid(row=9, column=1)


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
            

    def dictLayout(self):
        self.window = Toplevel()
        self.window.title("Dictionary")
        self.window.geometry("1150x600")
        check = Dictionary()

        try:
            self.window.configure(background=var.get())
        except NameError:
            pass

        title = Label(self.window, text="Dictionary\n\n\n", font=("Courier", 25))
        word = Entry(self.window, relief=SUNKEN, bg="#878D98", fg="white", font=("Calibri", 20))
        definition = Button(self.window, text="Definition", font=("Courier", 10), command=lambda: check.checkInput(self.window, word.get(), check))

        Label(self.window, text="\t\t\t\t").grid(row=0, column=0)
        Label(self.window, text="Word:", font=("Courier", 12)).grid(row=2, column=0)
        Label(self.window, text="This dictionary scrapes the web to find the definition of your chosen word!", font=("Courier", 12)).grid(row=0, column=1)
        Label(self.window, text="\t\t\t\t").grid(row=0, column=2)

        title.grid(row=0, column=1)
        word.grid(row=2, column=1, ipadx=50, ipady=50, pady=10, sticky="nsew")
        definition.grid(row=3, column=1, pady=10, ipady=20, ipadx=20)


class ContactMe:
    def __init__(self, master=None, firstName=None, lastName=None, usersEmail=None):
        self.firstName = firstName
        self.lastName = lastName
        self.usersEmail = usersEmail
    

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

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASS)
            smtp.send_message(EmailMs)
    

    def confirmRequest(self, first, last, email, master, contact):
        if re.search(r'[0-9@_!#$%^&*()<>?/\|}{~:]', first.get()) or re.search(r'[0-9@_!#$%^&*()<>?/\|}{~:]', last.get()):
            Label(master, text="Invalid first or last name").grid(row=6, column=4, pady=10)
        elif first.get() == "" or last.get() == "":
            Label(master, text="Boxes can't be empty").grid(row=8, column=4, pady=10)
        else:
            if email.get() == loggedEmail:
                Label(master, text="Submission Successful").grid(row=8, column=4, pady=10)
                contact.sendEmail(first.get(), last.get(), email.get())
            else:
                messagebox.showwarning("Unmatched Email", "Email doesn't matched logged in email")
    

    def contactLayout(self):
        self.master = Toplevel()
        self.master.geometry("630x400")
        self.master.title("Contact Me")
        contact = ContactMe()

        try:
            self.master.configure(background=var.get())
        except NameError:
            pass
        
        title = Label(self.master, text="Contact Me\n", font=("Courier", 17, "bold"))
        firstText = Label(self.master, text="First Name: ", font=("Courier", 10))
        lastText = Label(self.master, text="Last Name: ", font=("Courier", 10))
        emailText = Label(self.master, text="Confirm Email:", font=("Courier", 10))

        self.firstName = Entry(self.master, relief=SUNKEN, bg="#878D98", fg="white", font=("Calibri", 15))
        self.lastName = Entry(self.master, relief=SUNKEN, bg="#878D98", fg="white", font=("Calibri", 15))
        self.usersEmail = Entry(self.master, relief=SUNKEN, bg="#878D98", fg="white", font=("Calibri", 15))
        confirmRequest = Button(
            self.master, text="Submit", height=2, width=7, font=("Arial", 9), bg="#EB5757", activebackground="#D0CBCB", 
            fg="white", command=lambda: contact.confirmRequest(self.firstName, self.lastName, self.usersEmail, self.master, contact)
        )

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
    def applySettings(self, settingsPage):
        settingsPage.destroy()


    def settings(self):
        window = Toplevel() # Opens new window when settings button is clicked.
        window.geometry("300x220") # Size of window.
        window.configure(background='#D7D4D4')
        window.title("Settings")
        sets = Settings()
        
        global var
        var = StringVar()
        var.set("#f0f0ed")
        
        title = Label(window, text="Settings\n", font=("Arial", 20))
        background = Label(window, text="Background:\t")
        lightMode = Radiobutton(window, text="\nLight: ", variable=var, value="#F0F0ED")
        darkMode = Radiobutton(window, text="Dark: \n", variable=var, value="#A8A8A8")

        submitSets = Button(window, text="Apply", command=lambda: sets.applySettings(window))

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