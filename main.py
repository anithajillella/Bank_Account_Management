import tkinter as tk
from tkinter import messagebox
from database import get_connection

def create_account():

    # Create account window
    account_window = tk.Toplevel(root)
    account_window.title("Create Bank Account")
    account_window.geometry("500x650")
    account_window.resizable(False, False)

    # ==============================
    # Title
    # ==============================

    tk.Label(
        account_window,
        text="CREATE BANK ACCOUNT",
        font=("Arial", 20, "bold")
    ).pack(pady=20)

    # ==============================
    # Customer Name
    # ==============================

    tk.Label(
        account_window,
        text="Customer Name:",
        font=("Arial", 12)
    ).pack(pady=(10, 2))

    name_entry = tk.Entry(
        account_window,
        width=40
    )

    name_entry.pack()

    # ==============================
    # Phone
    # ==============================

    tk.Label(
        account_window,
        text="Phone Number:",
        font=("Arial", 12)
    ).pack(pady=(10, 2))

    phone_entry = tk.Entry(
        account_window,
        width=40
    )

    phone_entry.pack()

    # ==============================
    # Email
    # ==============================

    tk.Label(
        account_window,
        text="Email:",
        font=("Arial", 12)
    ).pack(pady=(10, 2))

    email_entry = tk.Entry(
        account_window,
        width=40
    )

    email_entry.pack()

    # ==============================
    # Address
    # ==============================

    tk.Label(
        account_window,
        text="Address:",
        font=("Arial", 12)
    ).pack(pady=(10, 2))

    address_entry = tk.Entry(
        account_window,
        width=40
    )

    address_entry.pack()

    # ==============================
    # Date of Birth
    # ==============================

    tk.Label(
        account_window,
        text="Date of Birth (YYYY-MM-DD):",
        font=("Arial", 12)
    ).pack(pady=(10, 2))

    dob_entry = tk.Entry(
        account_window,
        width=40
    )

    dob_entry.pack()

    # ==============================
    # Account Type
    # ==============================

    tk.Label(
        account_window,
        text="Account Type:",
        font=("Arial", 12)
    ).pack(pady=(10, 2))

    account_type = tk.StringVar()
    account_type.set("Savings")

    account_menu = tk.OptionMenu(
        account_window,
        account_type,
        "Savings",
        "Current"
    )

    account_menu.pack()

    # ==============================
    # Initial Deposit
    # ==============================

    tk.Label(
        account_window,
        text="Initial Deposit:",
        font=("Arial", 12)
    ).pack(pady=(10, 2))

    deposit_entry = tk.Entry(
        account_window,
        width=40
    )

    deposit_entry.pack()

    # ==============================
    # Save Account
    # ==============================

    def save_account():

        name = name_entry.get().strip()
        phone = phone_entry.get().strip()
        email = email_entry.get().strip()
        address = address_entry.get().strip()
        dob = dob_entry.get().strip()
        acc_type = account_type.get()
        deposit_text = deposit_entry.get().strip()

        # ==============================
        # Required Fields Validation
        # ==============================

        if not name:
            messagebox.showerror(
                "Validation Error",
                "Please enter the customer name."
            )
            name_entry.focus()
            return

        if not phone:
            messagebox.showerror(
                "Validation Error",
                "Please enter the phone number."
            )
            phone_entry.focus()
            return

        if not email:
            messagebox.showerror(
                "Validation Error",
                "Please enter the email address."
            )
            email_entry.focus()
            return

        if not address:
            messagebox.showerror(
                "Validation Error",
                "Please enter the address."
            )
            address_entry.focus()
            return

        if not dob:
            messagebox.showerror(
                "Validation Error",
                "Please enter the date of birth."
            )
            dob_entry.focus()
            return

        if not deposit_text:
            messagebox.showerror(
                "Validation Error",
                "Please enter the initial deposit."
            )
            deposit_entry.focus()
            return

        # ==============================
        # Name Validation
        # ==============================

        if not name.replace(" ", "").isalpha():

            messagebox.showerror(
                "Validation Error",
                "Name should contain letters and spaces only."
            )

            name_entry.focus()

            return

        # ==============================
        # Phone Validation
        # ==============================

        if not phone.isdigit() or len(phone) != 10:

            messagebox.showerror(
                "Validation Error",
                "Phone number must contain exactly 10 digits."
            )

            phone_entry.focus()

            return

        # ==============================
        # Email Validation
        # ==============================

        if "@" not in email or "." not in email:

            messagebox.showerror(
                "Validation Error",
                "Please enter a valid email address."
            )

            email_entry.focus()

            return

        # ==============================
        # Date Validation
        # ==============================

        try:

            from datetime import datetime

            datetime.strptime(
                dob,
                "%Y-%m-%d"
            )

        except ValueError:

            messagebox.showerror(
                "Validation Error",
                "Date of birth must be in YYYY-MM-DD format.\n"
                "Example: 2005-05-10"
            )

            dob_entry.focus()

            return

        # ==============================
        # Deposit Validation
        # ==============================

        try:

            deposit = float(deposit_text)

        except ValueError:

            messagebox.showerror(
                "Validation Error",
                "Please enter a valid deposit amount."
            )

            deposit_entry.focus()

            return

        if deposit < 0:

            messagebox.showerror(
                "Validation Error",
                "Initial deposit cannot be negative."
            )

            deposit_entry.focus()

            return

        # ==============================
        # Database Operation
        # ==============================

        connection = None

        try:

            connection = get_connection()

            cursor = connection.cursor()

            # Insert customer
            customer_query = """
                INSERT INTO customers
                (name, phone, email, address, date_of_birth)
                VALUES (%s, %s, %s, %s, %s)
            """

            customer_values = (
                name,
                phone,
                email,
                address,
                dob
            )

            cursor.execute(
                customer_query,
                customer_values
            )

            customer_id = cursor.lastrowid

            # Generate account number
            account_number = (
                "100000" + str(customer_id)
            )

            # Insert account
            account_query = """
                INSERT INTO accounts
                (
                    customer_id,
                    account_number,
                    account_type,
                    balance
                )
                VALUES (%s, %s, %s, %s)
            """

            account_values = (
                customer_id,
                account_number,
                acc_type,
                deposit
            )

            cursor.execute(
                account_query,
                account_values
            )

            # Record initial deposit
            if deposit > 0:

                transaction_query = """
                    INSERT INTO transactions
                    (
                        account_number,
                        transaction_type,
                        amount,
                        balance_after
                    )
                    VALUES (%s, %s, %s, %s)
                """

                transaction_values = (
                    account_number,
                    "Deposit",
                    deposit,
                    deposit
                )

                cursor.execute(
                    transaction_query,
                    transaction_values
                )

            # Save database changes
            connection.commit()

            # Success message
            messagebox.showinfo(
                "Account Created",
                f"Account created successfully!\n\n"
                f"Customer Name: {name}\n"
                f"Account Number: {account_number}\n"
                f"Account Type: {acc_type}\n"
                f"Initial Balance: ₹{deposit:.2f}"
            )

            account_window.destroy()

        except Exception as e:

            if connection:
                connection.rollback()

            messagebox.showerror(
                "Database Error",
                str(e)
            )

        finally:

            if connection:
                connection.close()

    # ==============================
    # Create Account Button
    # ==============================

    tk.Button(
        account_window,
        text="CREATE ACCOUNT",
        width=25,
        height=2,
        font=("Arial", 11, "bold"),
        command=save_account
    ).pack(pady=25)


def view_account():

    # ==============================
    # Create View Account Window
    # ==============================

    view_window = tk.Toplevel(root)

    view_window.title("View Account")
    view_window.geometry("500x500")
    view_window.resizable(False, False)

    # ==============================
    # Title
    # ==============================

    tk.Label(
        view_window,
        text="VIEW ACCOUNT",
        font=("Arial", 20, "bold")
    ).pack(pady=20)

    # ==============================
    # Account Number
    # ==============================

    tk.Label(
        view_window,
        text="Enter Account Number:",
        font=("Arial", 12)
    ).pack(pady=5)

    account_entry = tk.Entry(
        view_window,
        width=35
    )

    account_entry.pack(pady=5)

    # ==============================
    # Result Area
    # ==============================

    result_label = tk.Label(
        view_window,
        text="",
        font=("Arial", 12),
        justify="left"
    )

    result_label.pack(pady=20)

    # ==============================
    # Search Account
    # ==============================

    def search_account():

        account_number = account_entry.get().strip()

        # Check account number
        if not account_number:

            messagebox.showerror(
                "Error",
                "Please enter an account number."
            )

            account_entry.focus()

            return

        # Check digits
        if not account_number.isdigit():

            messagebox.showerror(
                "Error",
                "Account number must contain digits only."
            )

            account_entry.focus()

            return

        connection = None

        try:

            # Connect to MySQL
            connection = get_connection()

            cursor = connection.cursor(
                dictionary=True
            )

            # ==============================
            # SQL Query
            # ==============================

            query = """
                SELECT
                    c.name,
                    c.phone,
                    c.email,
                    c.address,
                    c.date_of_birth,
                    a.account_number,
                    a.account_type,
                    a.balance,
                    a.status,
                    a.created_date
                FROM customers c
                JOIN accounts a
                    ON c.customer_id = a.customer_id
                WHERE a.account_number = %s
            """

            cursor.execute(
                query,
                (account_number,)
            )

            account = cursor.fetchone()

            # ==============================
            # Account Found
            # ==============================

            if account:

                result = (
                    f"Customer Name: {account['name']}\n"
                    f"Phone: {account['phone']}\n"
                    f"Email: {account['email']}\n"
                    f"Address: {account['address']}\n"
                    f"Date of Birth: {account['date_of_birth']}\n\n"
                    f"Account Number: "
                    f"{account['account_number']}\n"
                    f"Account Type: "
                    f"{account['account_type']}\n"
                    f"Balance: "
                    f"₹{float(account['balance']):.2f}\n"
                    f"Status: {account['status']}\n"
                    f"Created Date: "
                    f"{account['created_date']}"
                )

                result_label.config(
                    text=result
                )

            # ==============================
            # Account Not Found
            # ==============================

            else:

                result_label.config(
                    text=""
                )

                messagebox.showwarning(
                    "Not Found",
                    "Account number not found."
                )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

        finally:

            if connection:

                connection.close()

    # ==============================
    # Search Button
    # ==============================

    tk.Button(
        view_window,
        text="SEARCH ACCOUNT",
        width=25,
        height=2,
        font=("Arial", 11, "bold"),
        command=search_account
    ).pack(pady=10)


def deposit_money():

    deposit_window = tk.Toplevel(root)

    deposit_window.title("Deposit Money")
    deposit_window.geometry("500x450")
    deposit_window.resizable(False, False)

    # ==============================
    # Title
    # ==============================

    tk.Label(
        deposit_window,
        text="DEPOSIT MONEY",
        font=("Arial", 20, "bold")
    ).pack(pady=25)

    # ==============================
    # Account Number
    # ==============================

    tk.Label(
        deposit_window,
        text="Account Number:",
        font=("Arial", 12)
    ).pack(pady=5)

    account_entry = tk.Entry(
        deposit_window,
        width=35
    )

    account_entry.pack(pady=5)

    # ==============================
    # Deposit Amount
    # ==============================

    tk.Label(
        deposit_window,
        text="Deposit Amount:",
        font=("Arial", 12)
    ).pack(pady=(20, 5))

    amount_entry = tk.Entry(
        deposit_window,
        width=35
    )

    amount_entry.pack(pady=5)

    # ==============================
    # Make Deposit
    # ==============================

    def make_deposit():

        account_number = account_entry.get().strip()
        amount_text = amount_entry.get().strip()

        # ------------------------------
        # Account validation
        # ------------------------------

        if not account_number:

            messagebox.showerror(
                "Validation Error",
                "Please enter an account number."
            )

            account_entry.focus()

            return

        if not account_number.isdigit():

            messagebox.showerror(
                "Validation Error",
                "Account number must contain digits only."
            )

            account_entry.focus()

            return

        # ------------------------------
        # Amount validation
        # ------------------------------

        if not amount_text:

            messagebox.showerror(
                "Validation Error",
                "Please enter the deposit amount."
            )

            amount_entry.focus()

            return

        try:

            amount = float(amount_text)

        except ValueError:

            messagebox.showerror(
                "Validation Error",
                "Please enter a valid numeric amount."
            )

            amount_entry.focus()

            return

        if amount <= 0:

            messagebox.showerror(
                "Validation Error",
                "Deposit amount must be greater than ₹0."
            )

            amount_entry.focus()

            return

        # ------------------------------
        # Database operation
        # ------------------------------

        connection = None

        try:

            connection = get_connection()

            cursor = connection.cursor(
                dictionary=True
            )

            # Find account
            find_query = """
                SELECT balance, status
                FROM accounts
                WHERE account_number = %s
            """

            cursor.execute(
                find_query,
                (account_number,)
            )

            account = cursor.fetchone()

            # Account not found
            if not account:

                messagebox.showerror(
                    "Account Not Found",
                    f"No account found with number:\n"
                    f"{account_number}"
                )

                return

            # Check account status
            if account["status"] != "Active":

                messagebox.showerror(
                    "Account Inactive",
                    "This account is not active."
                )

                return

            # Current balance
            current_balance = float(
                account["balance"]
            )

            # New balance
            new_balance = current_balance + amount

            # Update account
            update_query = """
                UPDATE accounts
                SET balance = %s
                WHERE account_number = %s
            """

            cursor.execute(
                update_query,
                (
                    new_balance,
                    account_number
                )
            )

            # Record transaction
            transaction_query = """
                INSERT INTO transactions
                (
                    account_number,
                    transaction_type,
                    amount,
                    balance_after
                )
                VALUES (%s, %s, %s, %s)
            """

            cursor.execute(
                transaction_query,
                (
                    account_number,
                    "Deposit",
                    amount,
                    new_balance
                )
            )

            # Save changes
            connection.commit()

            # Success message
            messagebox.showinfo(
                "Deposit Successful",
                f"Deposit completed successfully!\n\n"
                f"Account Number: {account_number}\n"
                f"Previous Balance: ₹{current_balance:.2f}\n"
                f"Deposited Amount: ₹{amount:.2f}\n"
                f"New Balance: ₹{new_balance:.2f}"
            )

            # Clear fields
            account_entry.delete(
                0,
                tk.END
            )

            amount_entry.delete(
                0,
                tk.END
            )

        except Exception as e:

            if connection:
                connection.rollback()

            messagebox.showerror(
                "Database Error",
                str(e)
            )

        finally:

            if connection:
                connection.close()

    # ==============================
    # Deposit Button
    # ==============================

    tk.Button(
        deposit_window,
        text="DEPOSIT",
        width=25,
        height=2,
        font=("Arial", 11, "bold"),
        command=make_deposit
    ).pack(pady=30)

def withdraw_money():

    withdraw_window = tk.Toplevel(root)

    withdraw_window.title("Withdraw Money")
    withdraw_window.geometry("500x450")
    withdraw_window.resizable(False, False)

    # ==============================
    # Title
    # ==============================

    tk.Label(
        withdraw_window,
        text="WITHDRAW MONEY",
        font=("Arial", 20, "bold")
    ).pack(pady=25)

    # ==============================
    # Account Number
    # ==============================

    tk.Label(
        withdraw_window,
        text="Account Number:",
        font=("Arial", 12)
    ).pack(pady=5)

    account_entry = tk.Entry(
        withdraw_window,
        width=35
    )

    account_entry.pack(pady=5)

    # ==============================
    # Withdrawal Amount
    # ==============================

    tk.Label(
        withdraw_window,
        text="Withdraw Amount:",
        font=("Arial", 12)
    ).pack(pady=(20, 5))

    amount_entry = tk.Entry(
        withdraw_window,
        width=35
    )

    amount_entry.pack(pady=5)

    # ==============================
    # Make Withdrawal
    # ==============================

    def make_withdrawal():

        account_number = account_entry.get().strip()
        amount_text = amount_entry.get().strip()

        # ------------------------------
        # Account validation
        # ------------------------------

        if not account_number:

            messagebox.showerror(
                "Validation Error",
                "Please enter an account number."
            )

            account_entry.focus()

            return

        if not account_number.isdigit():

            messagebox.showerror(
                "Validation Error",
                "Account number must contain digits only."
            )

            account_entry.focus()

            return

        # ------------------------------
        # Amount validation
        # ------------------------------

        if not amount_text:

            messagebox.showerror(
                "Validation Error",
                "Please enter the withdrawal amount."
            )

            amount_entry.focus()

            return

        try:

            amount = float(amount_text)

        except ValueError:

            messagebox.showerror(
                "Validation Error",
                "Please enter a valid numeric amount."
            )

            amount_entry.focus()

            return

        if amount <= 0:

            messagebox.showerror(
                "Validation Error",
                "Withdrawal amount must be greater than ₹0."
            )

            amount_entry.focus()

            return

        # ------------------------------
        # Database operation
        # ------------------------------

        connection = None

        try:

            connection = get_connection()

            cursor = connection.cursor(
                dictionary=True
            )

            # Find account
            find_query = """
                SELECT balance, status
                FROM accounts
                WHERE account_number = %s
            """

            cursor.execute(
                find_query,
                (account_number,)
            )

            account = cursor.fetchone()

            # Account not found
            if not account:

                messagebox.showerror(
                    "Account Not Found",
                    f"No account found with number:\n"
                    f"{account_number}"
                )

                return

            # Check account status
            if account["status"] != "Active":

                messagebox.showerror(
                    "Account Inactive",
                    "This account is not active."
                )

                return

            # Current balance
            current_balance = float(
                account["balance"]
            )

            # Check sufficient balance
            if amount > current_balance:

                messagebox.showerror(
                    "Insufficient Balance",
                    f"Available Balance: ₹{current_balance:.2f}\n"
                    f"Requested Amount: ₹{amount:.2f}"
                )

                return

            # Calculate new balance
            new_balance = current_balance - amount

            # Update balance
            update_query = """
                UPDATE accounts
                SET balance = %s
                WHERE account_number = %s
            """

            cursor.execute(
                update_query,
                (
                    new_balance,
                    account_number
                )
            )

            # Record transaction
            transaction_query = """
                INSERT INTO transactions
                (
                    account_number,
                    transaction_type,
                    amount,
                    balance_after
                )
                VALUES (%s, %s, %s, %s)
            """

            cursor.execute(
                transaction_query,
                (
                    account_number,
                    "Withdrawal",
                    amount,
                    new_balance
                )
            )

            # Save changes
            connection.commit()

            # Success message
            messagebox.showinfo(
                "Withdrawal Successful",
                f"Withdrawal completed successfully!\n\n"
                f"Account Number: {account_number}\n"
                f"Previous Balance: ₹{current_balance:.2f}\n"
                f"Withdrawn Amount: ₹{amount:.2f}\n"
                f"New Balance: ₹{new_balance:.2f}"
            )

            # Clear fields
            account_entry.delete(
                0,
                tk.END
            )

            amount_entry.delete(
                0,
                tk.END
            )

        except Exception as e:

            if connection:
                connection.rollback()

            messagebox.showerror(
                "Database Error",
                str(e)
            )

        finally:

            if connection:
                connection.close()

    # ==============================
    # Withdraw Button
    # ==============================

    tk.Button(
        withdraw_window,
        text="WITHDRAW",
        width=25,
        height=2,
        font=("Arial", 11, "bold"),
        command=make_withdrawal
    ).pack(pady=30)

def transfer_money():

    transfer_window = tk.Toplevel(root)

    transfer_window.title("Transfer Money")
    transfer_window.geometry("500x550")
    transfer_window.resizable(False, False)

    # ==============================
    # Title
    # ==============================

    tk.Label(
        transfer_window,
        text="TRANSFER MONEY",
        font=("Arial", 20, "bold")
    ).pack(pady=25)

    # ==============================
    # From Account
    # ==============================

    tk.Label(
        transfer_window,
        text="From Account Number:",
        font=("Arial", 12)
    ).pack(pady=5)

    from_account_entry = tk.Entry(
        transfer_window,
        width=35
    )

    from_account_entry.pack(pady=5)

    # ==============================
    # To Account
    # ==============================

    tk.Label(
        transfer_window,
        text="To Account Number:",
        font=("Arial", 12)
    ).pack(pady=(20, 5))

    to_account_entry = tk.Entry(
        transfer_window,
        width=35
    )

    to_account_entry.pack(pady=5)

    # ==============================
    # Transfer Amount
    # ==============================

    tk.Label(
        transfer_window,
        text="Transfer Amount:",
        font=("Arial", 12)
    ).pack(pady=(20, 5))

    amount_entry = tk.Entry(
        transfer_window,
        width=35
    )

    amount_entry.pack(pady=5)

    # ==============================
    # Make Transfer
    # ==============================

    def make_transfer():

        from_account = from_account_entry.get().strip()
        to_account = to_account_entry.get().strip()
        amount_text = amount_entry.get().strip()

        # ------------------------------
        # Sender validation
        # ------------------------------

        if not from_account:

            messagebox.showerror(
                "Validation Error",
                "Please enter the sender account number."
            )

            from_account_entry.focus()

            return

        if not from_account.isdigit():

            messagebox.showerror(
                "Validation Error",
                "Sender account number must contain digits only."
            )

            from_account_entry.focus()

            return

        # ------------------------------
        # Receiver validation
        # ------------------------------

        if not to_account:

            messagebox.showerror(
                "Validation Error",
                "Please enter the receiver account number."
            )

            to_account_entry.focus()

            return

        if not to_account.isdigit():

            messagebox.showerror(
                "Validation Error",
                "Receiver account number must contain digits only."
            )

            to_account_entry.focus()

            return

        # ------------------------------
        # Same account check
        # ------------------------------

        if from_account == to_account:

            messagebox.showerror(
                "Validation Error",
                "Sender and receiver accounts cannot be the same."
            )

            to_account_entry.focus()

            return

        # ------------------------------
        # Amount validation
        # ------------------------------

        if not amount_text:

            messagebox.showerror(
                "Validation Error",
                "Please enter the transfer amount."
            )

            amount_entry.focus()

            return

        try:

            amount = float(amount_text)

        except ValueError:

            messagebox.showerror(
                "Validation Error",
                "Please enter a valid numeric amount."
            )

            amount_entry.focus()

            return

        if amount <= 0:

            messagebox.showerror(
                "Validation Error",
                "Transfer amount must be greater than ₹0."
            )

            amount_entry.focus()

            return

        # ------------------------------
        # Database operation
        # ------------------------------

        connection = None

        try:

            connection = get_connection()

            cursor = connection.cursor(
                dictionary=True
            )

            # Get sender
            sender_query = """
                SELECT balance, status
                FROM accounts
                WHERE account_number = %s
            """

            cursor.execute(
                sender_query,
                (from_account,)
            )

            sender = cursor.fetchone()

            if not sender:

                messagebox.showerror(
                    "Account Not Found",
                    f"Sender account {from_account} "
                    f"was not found."
                )

                return

            if sender["status"] != "Active":

                messagebox.showerror(
                    "Account Inactive",
                    "Sender account is not active."
                )

                return

            # Get receiver
            receiver_query = """
                SELECT balance, status
                FROM accounts
                WHERE account_number = %s
            """

            cursor.execute(
                receiver_query,
                (to_account,)
            )

            receiver = cursor.fetchone()

            if not receiver:

                messagebox.showerror(
                    "Account Not Found",
                    f"Receiver account {to_account} "
                    f"was not found."
                )

                return

            if receiver["status"] != "Active":

                messagebox.showerror(
                    "Account Inactive",
                    "Receiver account is not active."
                )

                return

            # ------------------------------
            # Get balances
            # ------------------------------

            sender_balance = float(
                sender["balance"]
            )

            receiver_balance = float(
                receiver["balance"]
            )

            # ------------------------------
            # Sufficient balance
            # ------------------------------

            if amount > sender_balance:

                messagebox.showerror(
                    "Insufficient Balance",
                    f"Available Balance: "
                    f"₹{sender_balance:.2f}\n"
                    f"Transfer Amount: "
                    f"₹{amount:.2f}"
                )

                return

            # ------------------------------
            # Calculate balances
            # ------------------------------

            new_sender_balance = (
                sender_balance - amount
            )

            new_receiver_balance = (
                receiver_balance + amount
            )

            # ------------------------------
            # Update sender
            # ------------------------------

            update_sender = """
                UPDATE accounts
                SET balance = %s
                WHERE account_number = %s
            """

            cursor.execute(
                update_sender,
                (
                    new_sender_balance,
                    from_account
                )
            )

            # ------------------------------
            # Update receiver
            # ------------------------------

            update_receiver = """
                UPDATE accounts
                SET balance = %s
                WHERE account_number = %s
            """

            cursor.execute(
                update_receiver,
                (
                    new_receiver_balance,
                    to_account
                )
            )

            # ------------------------------
            # Sender transaction
            # ------------------------------

            sender_transaction = """
                INSERT INTO transactions
                (
                    account_number,
                    transaction_type,
                    amount,
                    balance_after
                )
                VALUES (%s, %s, %s, %s)
            """

            cursor.execute(
                sender_transaction,
                (
                    from_account,
                    "Transfer Sent",
                    amount,
                    new_sender_balance
                )
            )

            # ------------------------------
            # Receiver transaction
            # ------------------------------

            receiver_transaction = """
                INSERT INTO transactions
                (
                    account_number,
                    transaction_type,
                    amount,
                    balance_after
                )
                VALUES (%s, %s, %s, %s)
            """

            cursor.execute(
                receiver_transaction,
                (
                    to_account,
                    "Transfer Received",
                    amount,
                    new_receiver_balance
                )
            )

            # ------------------------------
            # Commit
            # ------------------------------

            connection.commit()

            # ------------------------------
            # Success
            # ------------------------------

            messagebox.showinfo(
                "Transfer Successful",
                f"Transfer completed successfully!\n\n"
                f"From Account: {from_account}\n"
                f"To Account: {to_account}\n"
                f"Amount: ₹{amount:.2f}\n\n"
                f"Sender New Balance: "
                f"₹{new_sender_balance:.2f}\n"
                f"Receiver New Balance: "
                f"₹{new_receiver_balance:.2f}"
            )

            # Clear fields
            from_account_entry.delete(
                0,
                tk.END
            )

            to_account_entry.delete(
                0,
                tk.END
            )

            amount_entry.delete(
                0,
                tk.END
            )

        except Exception as e:

            if connection:
                connection.rollback()

            messagebox.showerror(
                "Database Error",
                str(e)
            )

        finally:

            if connection:
                connection.close()

    # ==============================
    # Transfer Button
    # ==============================

    tk.Button(
        transfer_window,
        text="TRANSFER",
        width=25,
        height=2,
        font=("Arial", 11, "bold"),
        command=make_transfer
    ).pack(pady=35)


def transaction_history():

    history_window = tk.Toplevel(root)

    history_window.title("Transaction History")
    history_window.geometry("900x650")
    history_window.resizable(False, False)

    # ==============================
    # Title
    # ==============================

    tk.Label(
        history_window,
        text="TRANSACTION HISTORY",
        font=("Arial", 20, "bold")
    ).pack(pady=20)

    # ==============================
    # Account Number
    # ==============================

    tk.Label(
        history_window,
        text="Enter Account Number:",
        font=("Arial", 12)
    ).pack(pady=5)

    account_entry = tk.Entry(
        history_window,
        width=35
    )

    account_entry.pack(pady=5)

    # ==============================
    # Result Area
    # ==============================

    result_text = tk.Text(
        history_window,
        width=105,
        height=25,
        font=("Courier New", 10)
    )

    result_text.pack(pady=15)

    # ==============================
    # Search History
    # ==============================

    def search_history():

        account_number = account_entry.get().strip()

        # Validate account number
        if not account_number:

            messagebox.showerror(
                "Validation Error",
                "Please enter an account number."
            )

            account_entry.focus()

            return

        if not account_number.isdigit():

            messagebox.showerror(
                "Validation Error",
                "Account number must contain digits only."
            )

            account_entry.focus()

            return

        connection = None

        try:

            connection = get_connection()

            cursor = connection.cursor(
                dictionary=True
            )

            # ==============================
            # Check Account
            # ==============================

            account_query = """
                SELECT
                    account_number,
                    account_type,
                    balance,
                    status
                FROM accounts
                WHERE account_number = %s
            """

            cursor.execute(
                account_query,
                (account_number,)
            )

            account = cursor.fetchone()

            if not account:

                result_text.delete(
                    "1.0",
                    tk.END
                )

                messagebox.showerror(
                    "Account Not Found",
                    f"Account {account_number} "
                    f"does not exist."
                )

                return

            # ==============================
            # Get Transactions
            # ==============================

            transaction_query = """
                SELECT
                    transaction_id,
                    transaction_type,
                    amount,
                    transaction_date,
                    balance_after
                FROM transactions
                WHERE account_number = %s
                ORDER BY transaction_id ASC
            """

            cursor.execute(
                transaction_query,
                (account_number,)
            )

            transactions = cursor.fetchall()

            # Clear previous result
            result_text.delete(
                "1.0",
                tk.END
            )

            # ==============================
            # Account Information
            # ==============================

            result_text.insert(
                tk.END,
                "BANK ACCOUNT TRANSACTION HISTORY\n"
            )

            result_text.insert(
                tk.END,
                "=" * 100 + "\n\n"
            )

            result_text.insert(
                tk.END,
                f"Account Number : "
                f"{account['account_number']}\n"
            )

            result_text.insert(
                tk.END,
                f"Account Type   : "
                f"{account['account_type']}\n"
            )

            result_text.insert(
                tk.END,
                f"Status         : "
                f"{account['status']}\n"
            )

            result_text.insert(
                tk.END,
                f"Current Balance: "
                f"₹{float(account['balance']):.2f}\n\n"
            )

            # ==============================
            # No Transactions
            # ==============================

            if not transactions:

                result_text.insert(
                    tk.END,
                    "No transactions found for this account."
                )

                return

            # ==============================
            # Transaction Table
            # ==============================

            result_text.insert(
                tk.END,
                "-" * 100 + "\n"
            )

            result_text.insert(
                tk.END,
                f"{'ID':<6}"
                f"{'Type':<23}"
                f"{'Amount':<16}"
                f"{'Date':<24}"
                f"{'Balance':<16}\n"
            )

            result_text.insert(
                tk.END,
                "-" * 100 + "\n"
            )

            # ==============================
            # Display Transactions
            # ==============================

            for transaction in transactions:

                transaction_id = transaction[
                    "transaction_id"
                ]

                transaction_type = transaction[
                    "transaction_type"
                ]

                amount = float(
                    transaction["amount"]
                )

                transaction_date = transaction[
                    "transaction_date"
                ]

                balance_after = float(
                    transaction["balance_after"]
                )

                result_text.insert(
                    tk.END,
                    f"{transaction_id:<6}"
                    f"{transaction_type:<23}"
                    f"₹{amount:<15.2f}"
                    f"{str(transaction_date):<24}"
                    f"₹{balance_after:<15.2f}\n"
                )

            result_text.insert(
                tk.END,
                "-" * 100 + "\n"
            )

            result_text.insert(
                tk.END,
                f"\nTotal Transactions: "
                f"{len(transactions)}"
            )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

        finally:

            if connection:
                connection.close()

    # ==============================
    # View History Button
    # ==============================

    tk.Button(
        history_window,
        text="VIEW HISTORY",
        width=25,
        height=2,
        font=("Arial", 11, "bold"),
        command=search_history
    ).pack(pady=10)
    
# ==============================
# MAIN WINDOW
# ==============================

root = tk.Tk()

root.title("Bank Account Management System")
root.geometry("900x650")
root.resizable(False, False)

# ==============================
# Header
# ==============================

header_frame = tk.Frame(
    root,
    padx=20,
    pady=20
)

header_frame.pack(fill="x")

title = tk.Label(
    header_frame,
    text="BANK ACCOUNT MANAGEMENT SYSTEM",
    font=("Arial", 24, "bold")
)

title.pack(pady=(10, 5))

subtitle = tk.Label(
    header_frame,
    text="Secure • Simple • Reliable Banking",
    font=("Arial", 13)
)

subtitle.pack()

# ==============================
# Menu Title
# ==============================

menu_title = tk.Label(
    root,
    text="Banking Services",
    font=("Arial", 18, "bold")
)

menu_title.pack(pady=(20, 15))

# ==============================
# Button Frame
# ==============================

button_frame = tk.Frame(root)

button_frame.pack()

# Create Account

tk.Button(
    button_frame,
    text="CREATE ACCOUNT",
    width=28,
    height=3,
    font=("Arial", 11, "bold"),
    command=create_account
).grid(
    row=0,
    column=0,
    padx=15,
    pady=12
)

# View Account

tk.Button(
    button_frame,
    text="VIEW ACCOUNT",
    width=28,
    height=3,
    font=("Arial", 11, "bold"),
    command=view_account
).grid(
    row=0,
    column=1,
    padx=15,
    pady=12
)

# Deposit Money

tk.Button(
    button_frame,
    text="DEPOSIT MONEY",
    width=28,
    height=3,
    font=("Arial", 11, "bold"),
    command=deposit_money
).grid(
    row=1,
    column=0,
    padx=15,
    pady=12
)

# Withdraw Money

tk.Button(
    button_frame,
    text="WITHDRAW MONEY",
    width=28,
    height=3,
    font=("Arial", 11, "bold"),
    command=withdraw_money
).grid(
    row=1,
    column=1,
    padx=15,
    pady=12
)

# Transfer Money

tk.Button(
    button_frame,
    text="TRANSFER MONEY",
    width=28,
    height=3,
    font=("Arial", 11, "bold"),
    command=transfer_money
).grid(
    row=2,
    column=0,
    padx=15,
    pady=12
)

# Transaction History

tk.Button(
    button_frame,
    text="TRANSACTION HISTORY",
    width=28,
    height=3,
    font=("Arial", 11, "bold"),
    command=transaction_history
).grid(
    row=2,
    column=1,
    padx=15,
    pady=12
)

# ==============================
# Exit Button
# ==============================

tk.Button(
    root,
    text="EXIT",
    width=20,
    height=2,
    font=("Arial", 11, "bold"),
    command=root.destroy
).pack(pady=30)

# ==============================
# Start Application
# ==============================

root.mainloop()