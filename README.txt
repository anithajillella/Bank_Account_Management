# BANK ACCOUNT MANAGEMENT SYSTEM

## Project Description

This is a Python-based Bank Account Management System developed using
Python, Tkinter, and MySQL.

## Technologies Used

1. Python
2. Tkinter
3. MySQL
4. MySQL Connector/Python

## Features

1. Create Bank Account
2. View Account Details
3. Deposit Money
4. Withdraw Money
5. Transfer Money
6. View Transaction History

## Project Files

main.py
Main Python application containing the banking GUI and functions.

database.py
Contains the MySQL database connection configuration.

test_connection.py
Used to test the connection between Python and MySQL.

**pycache**
Automatically generated Python cache files.

## Database

Database Name:
bank_management

Main Tables:

1. customers
2. accounts
3. transactions

## How to Run the Project

Step 1:
Make sure MySQL Server is running.

Step 2:
Open Command Prompt.

Step 3:
Go to the project folder:

C:\Users\anitha\OneDrive\Desktop\Bank_Account_Management_FINAL

Step 4:
Test the database connection:

python test_connection.py

Expected output:

Database connected successfully!
Connection closed.

Step 5:
Run the banking application:

python main.py

The Bank Account Management System GUI will open.

## Banking Operations

Create Account:
Creates a new customer and bank account.

View Account:
Displays customer and account details.

Deposit Money:
Adds money to an active account.

Withdraw Money:
Withdraws money if sufficient balance is available.

Transfer Money:
Transfers money from one active account to another.

Transaction History:
Displays all transactions for a selected account.

## Database Connection

The application uses MySQL for storing customer,
account, and transaction information.

## Project Status

Project completed and tested successfully.

## Author

Anitha
B.Tech - Information Technology
