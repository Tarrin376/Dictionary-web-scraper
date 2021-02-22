from tkinter import *
from tkinter import messagebox
import sqlite3
import re
from copy import copy

class Menu(object):
    def yo(Email, password, createRoot):
        new = Toplevel(createRoot)
        new.geometry("700x500")
        new.title("Menu")

        email_data = Label(new, text=f"Logged in as: {Email}", font=("Arial", 12))
        email_data.grid(row=0, column=0)

        logout = Button(new, text="LOG OUT", command=lambda: logout(Email))
        logout.grid(row=1, column=0)

        def logout(email):
            message = Label(new, text=f"Logging out {email}...")
            message.grid(row=2, column=0)
            new.destroy()


class LoginSystem:
    def __init__(self, master, email=None, password=None):
        self.email = email
        self.master = master
        self.password = password
        self.title = self.master.title("Login")
    
    def createAccount(self, Email, Pass, Pass2, createRoot):
        if re.search(r'^[a-zA-|0-9]+[\._]?[a-zA-Z0-9]+[@]\w+[.]\w{2,3}$', Email.get()):
            password_validator = [
                (lambda x: True if any(i.isupper() for i in x) else False)(Pass.get()),
                (lambda x: True if any(i.isdigit() for i in x) else False)(Pass.get()),
                (lambda x: True if any(i.isupper() for i in x) else False)(Pass2.get()),
                (lambda x: True if any(i.isdigit() for i in x) else False)(Pass2.get())
            ]
            if all(condition == True for condition in password_validator):
                if re.search(r'[@_!#$%^&*()<>?/\|}{~:]', Pass.get()) and len(Pass.get()) > 7:
                    if Pass2.get() == Pass.get():
                        try:
                            connect = sqlite3.connect("Details.db")
                            csr = connect.cursor()
                            csr.execute("INSERT INTO Details VALUES (?, ?)", (Email.get(), Pass.get()))
                            connect.commit() # Committing changes to database and closing the connection.
                            connect.close()
                            createRoot.destroy()
                        except ConnectionError as error:
                            return f"ERROR {error}"
                    else:
                        Label(createRoot, text="Warning!").grid(row=9, column=5)
                        Label(createRoot, text="Passwords do not match").grid(row=10, column=5)
                else:
                    Label(createRoot, text="Warning!").grid(row=9, column=5)
                    Label(createRoot, 
                        text="Password length needs to be more than 7 and needs to contain special character"
                    ).grid(row=10, column=5)
            else:
                Label(createRoot, text="Warning!").grid(row=9, column=5)
                Label(createRoot, text="Uppercase characters and numbers needed").grid(row=10, column=5)
        else:
            messagebox.showwarning("Warning!", "Invalid Email")


    def createAccLayout(self):
        create = Toplevel()
        create.title("Create Account")
        create.geometry("295x310") # Setting window size for create account page.
        title = Label(create, text="\nCreate Account\n", font=("Arial", 20))

        new_email = Entry(create, width=40)
        new_email.grid(row=3, column=5)

        new_pass = Entry(create, width=40)
        new_pass.grid(row=5, column=5)

        new_pass2 = Entry(create, width=40)
        new_pass2.grid(row=7, column=5)
        
        title.grid(row=0, column=5)

        createAcc = Button(create, text="Create Account", command=lambda: self.createAccount(new_email, new_pass, new_pass2, create))
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
            connect = sqlite3.connect("Details.db")
            csr = connect.cursor()
        except ConnectionError as error: # Throw exception if user is unable to connect to database.
            return f"ERROR {error}"
            exit()

        csr.execute("SELECT * FROM Details") # Grabs all of the data from the db.
        data = csr.fetchall() # Stored tuples of data in db in variable.

        for i in data:
            print(i)
            if i[0] == Email.get() and i[1] == Pass.get(): # Checking if details exist or not.
                loggedEmail = copy(Email.get())
                Email.delete(0, END)
                Pass.delete(0, END) 
                menu = Menu.yo(loggedEmail, Pass, Master)
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
        
        loginButton = Button(self.master, text="Login", command=lambda: self.loginPress(self.email, self.password, self.master))
        # Calling function loginPress when user has entered their details.
        createAcc = Button(self.master, text="Create Account", command=lambda: self.createAccLayout()) 
        # Calling createAccLayout function.

        Label(self.master, text="\nEmail: \n").grid(row=1, column=0)
        Label(self.master, text="\nPassword: \n").grid(row=2, column=0)

        title.grid(row=0, column=5)
        self.email.grid(row=1, column=5) # Layout of the login page.
        self.password.grid(row=2, column=5)
        loginButton.grid(row=3, column=5, pady=10)
        createAcc.grid(row=5, column=5, padx=20, pady=10)


if __name__ == "__main__": # Checking if program is in main before running code.
    root = Tk()
    root.geometry("350x330") # Setting size of the window.

    login = LoginSystem(root)
    login.layout()
    
    root.mainloop()



