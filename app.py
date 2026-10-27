

from flask import Flask, request, redirect, url_for, render_template_string, flash
from decimal import Decimal, InvalidOperation
from threading import Lock

app = Flask(__name__)
app.secret_key = "demo-secret-change-before-deployment"

# Temporary demo storage. Data disappears when the server restarts.
accounts = {}
next_account_number = 1001
lock = Lock()

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Bank Account Management</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f1f5f9;
            padding: 20px;
            color: #172033;
        }
        main {
            max-width: 800px;
            margin: auto;
            background: white;
            padding: 24px;
            border-radius: 12px;
        }
        section {
            background: #f8fafc;
            padding: 16px;
            margin: 16px 0;
            border-radius: 8px;
        }
        input, select, button {
            width: 100%;
            box-sizing: border-box;
            padding: 10px;
            margin: 7px 0;
        }
        button {
            background: #174b80;
            color: white;
            border: none;
            cursor: pointer;
            border-radius: 6px;
        }
        .notice {
            background: #fff3cd;
            padding: 12px;
        }
        .message {
            background: #dcfce7;
            padding: 10px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            padding: 8px;
            border-bottom: 1px solid #ddd;
            text-align: left;
        }
    </style>
</head>
<body>
<main>
    <h1>Bank Account Management</h1>

    <p class="notice">
        Demo application only. Do not enter real customer information
        or use this application for actual financial transactions.
    </p>

    {% for message in get_flashed_messages() %}
        <p class="message">{{ message }}</p>
    {% endfor %}

    <section>
        <h2>Create Account</h2>
        <form action="/create" method="post">
            <label>Customer Name</label>
            <input name="name" required maxlength="80">

            <label>Opening Balance</label>
            <input name="balance" type="number"
                   min="0" step="0.01" value="0" required>

            <button type="submit">Create Account</button>
        </form>
    </section>

    <section>
        <h2>Deposit or Withdraw</h2>
        <form action="/transaction" method="post">
            <label>Account Number</label>
            <input name="account" type="number" required>

            <label>Amount</label>
            <input name="amount" type="number"
                   min="0.01" step="0.01" required>

            <label>Transaction Type</label>
            <select name="kind">
                <option value="deposit">Deposit</option>
                <option value="withdraw">Withdraw</option>
            </select>

            <button type="submit">Submit Transaction</button>
        </form>
    </section>

    <section>
        <h2>Account Details</h2>
        {% if accounts %}
        <table>
            <tr>
                <th>Account Number</th>
                <th>Customer</th>
                <th>Balance</th>
            </tr>
            {% for account in accounts %}
            <tr>
                <td>{{ account.number }}</td>
                <td>{{ account.name }}</td>
                <td>{{ "%.2f"|format(account.balance) }}</td>
            </tr>
            {% endfor %}
        </table>
        {% else %}
        <p>No accounts created yet.</p>
        {% endif %}
    </section>
</main>
</body>
</html>
"""


@app.get("/")
def home():
    with lock:
        rows = [
            {
                "number": number,
                "name": data["name"],
                "balance": data["balance"]
            }
            for number, data in sorted(accounts.items())
        ]

    return render_template_string(HTML, accounts=rows)


@app.post("/create")
def create_account():
    global next_account_number

    name = request.form.get("name", "").strip()

    try:
        balance = Decimal(request.form.get("balance", "0"))
        if not name or not balance.is_finite() or balance < 0:
            raise ValueError
    except (InvalidOperation, ValueError):
        flash("Enter a valid name and opening balance.")
        return redirect(url_for("home"))

    with lock:
        number = next_account_number
        next_account_number += 1
        accounts[number] = {
            "name": name,
            "balance": balance
        }

    flash(f"Demo account created. Account number: {number}")
    return redirect(url_for("home"))


@app.post("/transaction")
def transaction():
    try:
        number = int(request.form.get("account", ""))
        amount = Decimal(request.form.get("amount", ""))
        kind = request.form.get("kind")

        if (
            not amount.is_finite()
            or amount <= 0
            or kind not in ("deposit", "withdraw")
        ):
            raise ValueError

    except (ValueError, InvalidOperation):
        flash("Enter a valid account number and positive amount.")
        return redirect(url_for("home"))

    with lock:
        account = accounts.get(number)

        if account is None:
            flash("Account not found. Create an account first.")

        elif kind == "withdraw" and account["balance"] < amount:
            flash("Insufficient demo balance.")

        else:
            if kind == "deposit":
                account["balance"] += amount
            else:
                account["balance"] -= amount

            flash(
                f"Demo {kind} successful. "
                f"New balance: {account['balance']:.2f}"
            )

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
