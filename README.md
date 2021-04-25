# LibraryManagementSystem

# Prerequisites
1) git installed, can be downloaded from https://git-scm.com/downloads 
2) python installed with pip configured, can be downloaded and installed from https://www.python.org/downloads/
3) While installing python remember to tick the checkbox- ADD python {version} to PATH
4) django module of python installed, to install type the following in terminal- pip install django
5) dotenv module of python installed, to install type the following in terminal- pip install python-dotenv

# Running the Application
1) First clone this repo on your computer
2) Open terminal and go inside the LibManage Directory in the cloned repo, which has manage.py file
3) then execute the following command: python LibManage/key_generator.py
4) then to start the server, execute the following code: python manage.py runserver
5) In your terminal, you will get a message - "Starting development server at {URL}"
6) open that URL in the browser

# Sample Accounts
Some acounts are already created in the database for testing purposes, the credentials for which are given below:
1) Account 1 - Access Level: Admin,
    username:admin,
    password:admin
2) Account 2 - Access Level: Librarian,
    username:user1,
    password:pass1
3) Account 3 - Access Level: Librarian,
    username:user2,
    password:pass2
4) Account 4 - Access Level: User,
    username:user3,
    password:pass3
5) Account 5 - Access Level: User,
    username:user4,
    password:pass4
6) Account 6 - Access Level: User,
    username:user5,
    password:pass5

# Notes
1) Bootstrap has been used to give basic styling to the website, so while running this locally on your computer on the development server, stay connected to internet to see the actual website.
2) The available field in database is redundant, it is replaced with quantity at most places, but not all so it is not yet deleted from Book model.