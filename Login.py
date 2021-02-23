from tkinter import *
from tkinter import messagebox, ttk
import sqlite3
import re
from copy import copy


class Menu(object): # Main menu of GUI class.
    def settings():
        global window
        window = Toplevel() # Opens new window when settings button is clicked.
        window.geometry("300x220") # Size of window.
        window.configure(background='#D7D4D4')
        window.title("Settings")
        
        title = Label(window, text="Settings", font=("Arial", 20))
  

        title.grid(row=1, column=5)
    

    def menuLayout(Email, password, createRoot):
        menu = Toplevel(createRoot)
        menu.geometry("1200x600") # Size of window.
        menu.title("Menu")
        menu.configure(background='#D7D4D4')

        logout = Button(menu, text="LOG OUT", command=lambda: logout(Email), font=("Arial", 8, 'bold'), bg='#959292', fg="white") # Calling logout function.
        logout.grid(row=1, column=0)

        email_data = Label(menu, text=f"Logged in as: {Email}", font=("Arial", 12))
        welcome = Label(menu, text="Welcome!", font=("Arial", 25))
        subheading = Label(menu, text="Chose an option below:\n\n\n\n\n", font=("Arial", 15))
        Label(menu, text="              ").grid(row=3, column=3)
        Label(menu, text="              ").grid(row=3, column=5)
        Label(menu, text="              ").grid(row=5, column=4)
        settings = Button(menu, text="Settings", command=lambda: Menu.settings(), height=7, width=20, font=("Arial", 12, 'bold'), bg="#137FC7", fg="white")
        calculator = Button(menu, text="Calculator", height=7, width=20, font=("Arial", 12, 'bold'), bg="#137FC7", fg="white")
        toDoList = Button(menu, text="To Do list", height=7, width=20, font=("Arial", 12, 'bold'), bg="#9B5AFD", fg="white")
        dictionary = Button(menu, text="Dictionary", height=7, width=20, font=("Arial", 12, 'bold'), bg="#EB5757", fg="white")
        

        def logout(email):
            global window
            menu.destroy() # Closes the main menu window.
            if "window" == root.state():
                window.destroy() # Closes the settings window if open.

        
        email_data.grid(row=0, column=0)
        welcome.grid(row=2, column=4)
        subheading.grid(row=3, column=4)
        settings.grid(row=6, column=4)
        calculator.grid(row=4, column=2)
        toDoList.grid(row=4, column=4)
        dictionary.grid(row=4, column=6)
        

        """
        Gridding layout for the titles and entries.
        """


class LoginSystem:
    def __init__(self, master, email=None, password=None): # Class attributes needed for login system.
        self.email = email
        self.master = master
        self.password = password
        self.title = self.master.title("Login")
    
    def createAccount(self, Email, Pass, Pass2, createRoot):
        if re.search(r'^[a-zA-|0-9]+[\._]?[a-zA-Z0-9]+[@]\w+[.]\w{2,3}$', Email.get()):

            password_validator = [
                (lambda x: True if any(i.isupper() for i in x) else False)(Pass.get()),
                (lambda x: True if any(i.isdigit() for i in x) else False)(Pass.get())
            ] # Lambda expressions to check if passwords meet the conditions.

            if all(condition == True for condition in password_validator):
                if re.search(r'[@_!#$%^&*()<>?/\|}{~:]', Pass.get()) and len(Pass.get()) > 7: # Using email regular expression to check validity of email.
                    if Pass2.get() == Pass.get(): # Making sure that the re-entered password matches the original.
                        try:
                            connect = sqlite3.connect("Details.db")
                            csr = connect.cursor()
                            csr.execute("INSERT INTO Details VALUES (?, ?)", (Email.get(), Pass.get())) # Adding new email and password to database.
                            connect.commit() # Committing changes to database and closing the connection.
                            connect.close() # Closing the connection.
                            createRoot.destroy()
                        except ConnectionError as error:
                            return f"ERROR {error}"
                    else:
                        Label(createRoot, text="Passwords do not match").grid(row=10, column=5) # If passwords dont match.
                else:
                    Label(createRoot, 
                        text="Need one special character & length > 7"
                    ).grid(row=10, column=5)
            else:
                Label(createRoot, text="Uppercase characters and numbers needed").grid(row=10, column=5)
        else:
            messagebox.showwarning("Warning!", "Invalid Email") # Warning box if the email does not match the regex expression.


    def createAccLayout(self):
        create = Toplevel()
        create.title("Create Account")
        create.geometry("295x310") # Setting window size for create account page.

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

        """
            Code for creating the layout of the create account page. 
            E.g. Email entry, pass entry etc.
            Assiging rows and columns to each entry.
        """

        Label(create, text="Email").grid(row=2, column=5)
        Label(create, text="Password").grid(row=4, column=5)
        Label(create, text="Re-Enter pass").grid(row=6, column=5)
        Label(create, text="       ").grid(row=0, column=0)


    def loginPress(self, Email, Pass, Master):
        try:
            connect = sqlite3.connect("Details.db") # Connecting to SQLite3 database.
            csr = connect.cursor()
        except ConnectionError as error: # Throw exception if user is unable to connect to database.
            return f"ERROR {error}"
            exit()

        csr.execute("SELECT * FROM Details") # Grabs all of the data from the db.
        data = csr.fetchall() # Stored tuples of data in db in variable.

        for i in data:
            if i[0] == Email.get() and i[1] == Pass.get(): # Checking if details exist or not.
                loggedEmail = copy(Email.get())
                Email.delete(0, END)
                Pass.delete(0, END) 
                menu = Menu.menuLayout(loggedEmail, Pass, Master)
                return
                                             
        Email.delete(0, END) # Make entries blank when login button is pressed.
        Pass.delete(0, END) 
          
        messagebox.showwarning("Warning!", "Email or password is incorrect!")

        connect.commit() # Committing changes to database and closing the connection.
        connect.close()


    def layout(self):
        title = Label(self.master, text="\nSign in\n", font=("Arial", 25))
        self.email = Entry(self.master, width=40)
        self.password = Entry(self.master, width=40)
        
        loginButton = Button(self.master, text="Login", command=lambda: self.loginPress(self.email, self.password, self.master), font=("Arial", 8, 'bold'), bg='#959292', fg="white")
        # Calling function loginPress when user has entered their details.
        createAcc = Button(self.master, text="Create Account", command=lambda: self.createAccLayout(), font=("Arial", 8, 'bold'), bg='#959292', fg="white")
        # Calling createAccLayout function.

        text1 = Label(self.master, text="\nEmail: \n", font=("Roboto Medium", 12))
        text2 = Label(self.master, text="\nPassword: \n", font=("Roboto Medium", 12))

        title.grid(row=0, column=5)
        self.email.grid(row=1, column=5) # Layout of the login page.
        self.password.grid(row=2, column=5)
        loginButton.grid(row=3, column=5, pady=10)
        createAcc.grid(row=5, column=5, padx=20, pady=10)
        text1.grid(row=1, column=0)
        text2.grid(row=2, column=0)


if __name__ == "__main__": # Checking if program is in main before running code.
    root = Tk()
    root.geometry("370x330") # Setting size of the window.

    login = LoginSystem(root)
    login.layout()
    
    root.mainloop()



