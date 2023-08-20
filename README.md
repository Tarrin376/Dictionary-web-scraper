### About this project (built in 2021)
- This is a Python project that uses the library Tkinter to create the GUI. 
- It has a login system and a create account system so the user can sign into the program.
- Features of the program: 
  :point_right: Web Scaper Dictionary, contact me page, To Do List and a calculator 
- Project finished :stopwatch:

### Setting up the project locally

1. Clone this project
2. Install the "virtualenv" package if you haven't already by running "pip install virtualenv".
2. Create a new virtual environment in the root directory "virtualenv {environment_name}".
3. Activate the virtual environment "source {environment_name}/bin/activate" on Linux and "{environment_name}\Scripts\activate" on Windows.
2. Run "pip install requirements.txt" to install all necessary modules.
3. Finally, spin up the app by running "python Main.py".

### What I learned

I learned many things after I completed this project. Firstly, I learned what web scraping is and how we can navigate through HTML documents to obtain valuable information. Additionally, I also learned how to build a CRUD application using SQL and how we can execute raw queries against the database.

However, there are also some valuable takeaways from building this project. Firstly, I should have researched into database security before implementing a log-in system as my project stores each user's information in plain text, making it easy for malicious users to access all
signed-up accounts. Furthermore, I should have paid more attention to UI design as my project does not implement any modern UI design features.

### Libraries that are used:
- Tkinter
- SQLite3
- re - (Regular Expressions)
- requests, os, smtplib, operator
- copy
- Beautiful Soup
- email.message
