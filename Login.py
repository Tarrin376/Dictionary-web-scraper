while True:
    try:
        from tkinter import *
        from tkinter import messagebox, ttk
        import sqlite3, re
        from copy import copy
        break
    except ImportError as err:
        print(f"ERROR! {err}")
        user_input = input("Would you like to try again?: ")
        if user_input.lower() == "no":
            quit()


class Menu: # Main menu of GUI class.
    def __init__(self, calculator=None, toDoList=None, dictionary=None): # Class Attributes needed for the Menu.
        self.calcualtor = calculator
        self.toDoList = toDoList
        self.dictionary = dictionary


    def settings(self):
        window = Toplevel() # Opens new window when settings button is clicked.
        window.geometry("300x220") # Size of window.
        window.configure(background='#D7D4D4')
        window.title("Settings")
        
        title = Label(window, text="Settings", font=("Arial", 20))
        title.grid(row=1, column=5)
    

    def menuLayout(self, Email, password):
        menu = Toplevel()
        menu.geometry("1200x630") # Size of window.
        menu.title("Menu")
        menu.configure(background='#D7D4D4')

        email_data = Label(menu, text=f"Logged in as: {Email}", font=("Arial", 12))
        welcome = Label(menu, text="Welcome!", font=("Arial", 25))
        subheading = Label(menu, text="Chose an option below:\n\n\n\n\n", font=("Arial", 15))
        Label(menu, text="              ").grid(row=3, column=3)
        Label(menu, text="              ").grid(row=3, column=5)
        Label(menu, text="              ").grid(row=5, column=4)

        Sets = Menu()
        calculator = Calculator() # Assigning calculator variable to Calculator class call so a function can be called from a different class.
        toDo = ToDoList()
        dictionary = Dictionary()
        settings = Button(menu, text="Settings", command=lambda: Sets.settings(), height=7, width=20, font=("Arial", 12, 'bold'), bg="#137FC7", activebackground="#D0CBCB", fg="white")
        self.calculator = Button(menu, text="Calculator", height=7, width=20, font=("Arial", 12, 'bold'), bg="#137FC7", activebackground="#D0CBCB", fg="white", command=lambda: calculator.calcLayout())
        self.toDoList = Button(menu, text="To Do list", height=7, width=20, font=("Arial", 12, 'bold'), bg="#9B5AFD", activebackground="#D0CBCB", fg="white", command=lambda: toDo.listLayout())
        self.dictionary = Button(menu, text="Dictionary", height=7, width=20, font=("Arial", 12, 'bold'), bg="#EB5757", activebackground="#D0CBCB", fg="white", command=lambda: dictionary.dictLayout())
        self.contact = Button(menu, text="Contact Me", height=7, width=20, font=("Arial", 12, 'bold'), bg="#EB5757", activebackground="#D0CBCB", fg="white")
        logout = Button(menu, text="LOG OUT", height=7, width=20, font=("Arial", 12, 'bold'), bg='#959292', activebackground="#D0CBCB", fg="white", command=lambda: logout_user(Email)) # Calling logout function.

        email_data.grid(row=0, column=0)
        welcome.grid(row=2, column=4)
        subheading.grid(row=3, column=4)
        settings.grid(row=6, column=2)
        self.calculator.grid(row=4, column=2)
        self.toDoList.grid(row=4, column=4)
        self.dictionary.grid(row=4, column=6)
        self.contact.grid(row=6, column=4)
        logout.grid(row=6, column=6)

        """
        Gridding layout for the titles and entries.
        """

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
                            return f"ERROR {error}"
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
            return f"ERROR {error}"
            exit()

        csr.execute("SELECT * FROM information") # Grabs all of the data from the db.
        data = csr.fetchall() # Stored tuples of all the data in db in variable.
        for i in data: # Looping through db.
            if i[0] == Email.get() and i[1] == Pass.get(): # Checking if details exist or not.
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

        self.img1 = PhotoImage(file='C:\\Users\\Spec\\Pictures\\Camera Roll\\login.png') 
        self.loginImg = self.img1.subsample(4, 4) 
        self.img2 = PhotoImage(file='C:\\Users\\Spec\\Pictures\\Camera Roll\\create.png') 

        """ Images for login and logout buttons """

        title = Label(self.master, text="\nSign in\n", font=("Arial", 25))
        self.email = Entry(self.master, width=40)
        self.password = Entry(self.master, width=40)
        loginButton = Button(self.master, image=self.loginImg, command=lambda: self.loginPress(self.email, self.password, self.master), relief=FLAT)
        createAcc = Button(self.master, image=self.img2, command=lambda: self.createAccLayout(), relief=FLAT)
        text1 = Label(self.master, text="\nEmail:\n", font=("Roboto Medium", 12))
        text2 = Label(self.master, text="\nPassword:\n", font=("Roboto Medium", 12))

        title.grid(row=0, column=5)
        self.email.grid(row=1, column=5) 
        self.password.grid(row=2, column=5)
        loginButton.grid(row=3, column=5)
        createAcc.grid(row=4, column=5)
        text1.grid(row=1, column=0)
        text2.grid(row=2, column=0)
        
        # Layout of the login page.

  
class Calculator(LoginSystem):
    def __init__(self, master=None, email=None, password=None, userInput=None): # Class attributes needed for Calculator.
        super().__init__(master, email, password) # Inheriting attributes from LoginSystem class.
        self.userInput = userInput

    
    def calcLayout(self):
        self.master = Toplevel() # Creating new window.
        self.master.geometry("508x515")
        self.master.title("Calculator")
        self.master.configure(background="#878D98")
        large_font = ('Courier',29)
        
        self.userInput = Entry(self.master, font=large_font, relief=FLAT, justify="right", bg="#878D98", fg="white")
        C = Button(self.master, text="C", width=13, height=4, font=("Arial", 11, 'bold'), bg="#7B818D", activebackground="#D0CBCB", fg="white")
        Sqrt = Button(self.master, text="%", width=13, height=4, font=("Arial", 11, 'bold'), bg="#7B818D", activebackground="#D0CBCB", fg="white")
        Sqr = Button(self.master, text="x²", width=13, height=4, font=("Arial", 11, 'bold'), bg="#7B818D", activebackground="#D0CBCB", fg="white")
        Mod = Button(self.master, text="🢠", width=13, height=4, font=("Arial", 11, 'bold'), bg="#262E3D", activebackground="#D0CBCB", fg="white")
        Num1 = Button(self.master, text="1", width=13, height=4, font=("Arial", 11, 'bold'), bg="#525965", activebackground="#D0CBCB", fg="white")
        Num2 = Button(self.master, text="2", width=13, height=4, font=("Arial", 11, 'bold'), bg="#525965", activebackground="#D0CBCB", fg="white")
        Num3 = Button(self.master, text="3", width=13, height=4, font=("Arial", 11, 'bold'), bg="#525965", activebackground="#D0CBCB", fg="white")
        Add = Button(self.master, text="+", width=13, height=4, font=("Arial", 11, 'bold'), bg="#262E3D", activebackground="#D0CBCB", fg="white")
        Num4 = Button(self.master, text="4", width=13, height=4, font=("Arial", 11, 'bold'), bg="#525965", activebackground="#D0CBCB", fg="white")
        Num5 = Button(self.master, text="6", width=13, height=4, font=("Arial", 11, 'bold'), bg="#525965", activebackground="#D0CBCB", fg="white")
        Num6 = Button(self.master, text="6", width=13, height=4, font=("Arial", 11, 'bold'), bg="#525965", activebackground="#D0CBCB", fg="white")
        Minus = Button(self.master, text="-", width=13, height=4, font=("Arial", 11, 'bold'), bg="#262E3D", activebackground="#D0CBCB", fg="white")
        Num7 = Button(self.master, text="7", width=13, height=4, font=("Arial", 11, 'bold'), bg="#525965", activebackground="#D0CBCB", fg="white")
        Num8 = Button(self.master, text="8", width=13, height=4, font=("Arial", 11, 'bold'), bg="#525965", activebackground="#D0CBCB", fg="white")
        Num9 = Button(self.master, text="9", width=13, height=4, font=("Arial", 11, 'bold'), bg="#525965", activebackground="#D0CBCB", fg="white")
        Mult = Button(self.master, text="x", width=13, height=4, font=("Arial", 11, 'bold'), bg="#262E3D", activebackground="#D0CBCB", fg="white")
        Num0 = Button(self.master, text="0", width=13, height=4, font=("Arial", 11, 'bold'), bg="#262E3D", activebackground="#D0CBCB", fg="white")
        Dec = Button(self.master, text=".", width=13, height=4, font=("Arial", 11, 'bold'), bg="#525965", activebackground="#D0CBCB", fg="white")
        Equal = Button(self.master, text="=", width=13, height=4, font=("Arial", 11, 'bold'), bg="#E62E59", activebackground="#D0CBCB", fg="white")
        Div = Button(self.master, text="/", width=13, height=4, font=("Arial", 11, 'bold'), bg="#262E3D", activebackground="#D0CBCB", fg="white")

        self.userInput.grid(row=1, column=0, columnspan=10, pady=20)
        C.grid(row=2, column=0, sticky="nsew")
        Sqrt.grid(row=2, column=1, sticky="nsew")
        Sqr.grid(row=2, column=2, sticky="nsew")
        Mod.grid(row=2, column=3, sticky="nsew")
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
        notes.configure(background="#E6E680")
        large_font = ('Courier',10)
        add_note_window.destroy()
        
        notesList, griddedvals = [], []
        with open('notes.txt', 'r') as f:
            for line in f:
                notesList.append(line)

        for i in notesList:
            if i not in griddedvals:
                noteVal = Text(notes)
                noteVal.insert(END, f"Note {notesList.index(i)}:\n{i}")
                noteVal.configure(font=large_font, background="#FAF7A4", width=25, height=10)
                noteVal.grid(row=0, column=notesList.index(i))
                griddedvals.append(i)

        def close(window):
            window.destroy()


    @staticmethod
    def submitNote(note, window):
        if note.get() != "":
            Label(window, text="Note added to library!").grid(row=5, column=1)
            with open('notes.txt', 'a') as f:
                f.write(f"{note.get()}\n")
                f.close()
            Button(window, text="View notes", command=lambda: ToDoList.Notes(note.get(), window)).grid(row=6, column=1)
        else:
            messagebox.showwarning("Warning!", "Title or note is blank!")


    def listLayout(self):
        self.window = Toplevel()
        self.window.geometry("530x400")
        self.window.title("To Do List")
        large_font = ('Courier',29)
        
        noteText = Label(self.window, text="Note", font=("Calibri", 15))
        noteEntry = Entry(self.window, relief=SUNKEN, bg="#878D98", fg="white", font=("Calibri", 10))
        submit = Button(self.window, text="Add Note", command=lambda: ToDoList.submitNote(noteEntry, self.window))

        Label(self.window, text="To Do List", font=large_font).grid(row=1, column=1, pady=50)
        noteText.grid(row=3, column=0)
        noteEntry.grid(row=3, column=1, ipadx=150, ipady=60, pady=10)
        submit.grid(row=4, column=1)


class Dictionary:
    def __init__(self, definition=None, word=None):
        self.definition = definition
        self.word = word
    

    def dictLayout(self):
        print("yo")
        

if __name__ == "__main__": # Checking if program is in main before running code.
    root = Tk()
    root.geometry("370x330") # Setting size of the window.

    login = LoginSystem(root)
    login.layout()
    
    root.mainloop() # Keep root window open while the program is running.



