# Personal Expense Tracker

## 1. Project Title
Personal Expense Tracker

## 2. Project Description
The Personal Expense Tracker is a command-line Python application that helps users record daily expenses, monitor their remaining balance, and organize their expense records. The program stores all expenses in text files using a structured format and updates the user’s balance every time a new expense is added.

The project also includes a shell script that moves older expense files into an archive folder and logs every archival operation. This script also makes it possible to search for archived expense files by date.

This application was created as part of the Lab 3 Individual Coding Assignment. It focuses on using Python for file handling, menu-driven interaction, input validation, and modular programming, as well as using Bash scripting for file automation and system tasks.

## 3. Table of Contents
1. Project Title  
2. Project Description  
3. Table of Contents  
4. How to Install and Run the Project  
5. How to Use the Project  
6. Credits  
7. License  

## 4. How to Install and Run the Project

### Requirements
- Python 3 installed  
- A terminal or command prompt  
- Git Bash (for Windows users running the shell script)  

### Installation Steps
1. Download or clone the repository:
   <!-- ```bash -->
   git clone https://github.com/honnete-1/Lab3-Personal-Expense-Tracker_honnete-1.git
2. Navigate into the project folder
    cd   Lab3-Personal-Expense-Tracker_honnete-1
3. Make the shell scipt executable: 
    chmod +x archive_expenses.sh
---

## Running the Python Program
---
To start the expense tracker:
python expenses-tracker.py
or 
python expenses-tracker.py
---
## Running the Archive Script
To archive and search for old expense files:
./archive_expenses.sh
---
## How to Use the Project
./archive_expenses.sh
When the application starts, it displays a menu with four options:
1. Check Remaining Balance
2. View Expenses
3. Add New Expense
4. Exit
Below is what each option does:
1. Check Remaining Balance
This option:

Reads the current balance from balance.txt

Calculates the total expenses across all unarchived daily files

Displays:

Current balance

Total expenses

Available balance

The user is also asked if they want to add money to their balance.
Input validation is applied to make sure the amount is a positive number.
2. Add New Expense
The program asks the user to enter:

A valid date in YYYY-MM-DD format

The name of the item purchased

The amount spent

Before saving:

The program checks if the entered amount is a positive number

It prevents spending more money than the available balance

It shows a full summary for confirmation (y/n)

If confirmed, the expense is saved in a file named:
expenses_YYYY-MM-DD.txt
Each saved expense entry contains:

- A unique sequential ID

- The date

- The exact time of entry

- The item name

- The amount

- The balance is updated automatically.

This ensures the user always has an accurate and up-to-date record of their daily spending.
3. View Expenses
This feature allows the user to look up previous expenses using two search types:

Search by item name (case-insensitive, partial matches allowed)

Search by amount (exact numeric match)

The program searches across all unarchived daily files.
Search results display the file name, ID, date, time, item, and amount
4. Exit
Ends the program safely and returns the user to their terminal.

## Archiving Using the Shell Script

The archive_expenses.sh script is responsible for organizing old expense files.

The script:

Checks if the archives/ directory exists and creates it if needed

Moves a selected daily expense file into the archive folder

Renames the archived file with a timestamp

Logs the operation in archive_log.txt

Allows searching for archived files by date

This ensures:

The main project folder stays clean

Old data is never lost

Archival history is always tracked

Note:
Archived expense files are not searchable inside the Python program.
They can only be accessed using the shell script, which follows the assignment requirement.

## License

This project is for academic and educational use.
Feel free to view, study, or modify the code for learning purposes.

