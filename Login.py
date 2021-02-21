from tkinter import *
import sqlite3

class Menu:
    def yo():
        print("hi2")


class LoginSystem:
    def __init__(self, master, email=None, password=None):
        self.email = email
        self.master = master
        self.password = password
    
    @staticmethod
    def createAccount():
        create = Toplevel()
        create.geometry("250x310")
        title = Label(create, text="Create Account\n", font=("Arial", 20))

        Label(create, text="       ").grid(row=0, column=0)
        title.grid(row=0, column=5)


    def loginPress(self, Email, Pass, Master):
        try:
            connect = sqlite3.connect("Details.db")
            csr = connect.cursor()
        except ConnectionError as error:
            return f"ERROR {error}"
            exit()

        csr.execute("SELECT * FROM Details")
        data = csr.fetchall()

        for i in data:
            if i[0] == Email.get() and i[1] == Pass.get():
                root.destroy()
                Menu.yo()
        
        Email.delete(0, END)
        Pass.delete(0, END)

        incorrect = Label(Master, text="Email or Password is incorrect. Try Again.")
        incorrect.grid(row=4, column=5)

        createAcc = Button(Master, text="Create Account", command=lambda: LoginSystem.createAccount())
        createAcc.grid(row=5, column=5, padx=20, pady=10)

        connect.commit()
        connect.close()


    def layout(self):
        title = Label(self.master, text="\nSign in\n", font=("Arial", 25))
        self.email = Entry(self.master, width=40)
        self.password = Entry(self.master, width=40)
        
        loginButton = Button(self.master, text="Login", command=lambda: self.loginPress(self.email, self.password, self.master))


        Label(self.master, text="\nEmail: \n").grid(row=1, column=0)
        Label(self.master, text="\nPassword: \n").grid(row=2, column=0)
        title.grid(row=0, column=5)
        self.email.grid(row=1, column=5)
        self.password.grid(row=2, column=5)
        loginButton.grid(row=3, column=5, pady=10)


if __name__ == "__main__":
    root = Tk()
    root.geometry("350x330")

    login = LoginSystem(root)
    login.layout()
    
    root.mainloop()



