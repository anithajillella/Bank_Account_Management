
from flask import Flask, render_template_string

app = Flask(__name__)

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
            text-align: center;
            padding: 40px 15px;
        }
        .container {
            max-width: 650px;
            margin: auto;
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 15px #ccd3dd;
        }
        h1 { color: #123b68; }
        .item {
            background: #eaf2ff;
            margin: 12px 0;
            padding: 15px;
            border-radius: 8px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Bank Account Management</h1>
        <p>Welcome to our banking application demo!</p>
        <div class="item">Create a bank account</div>
        <div class="item">View account details</div>
        <div class="item">Deposit and withdraw money</div>
        <div class="item">Transfer money</div>
        <div class="item">View transaction history</div>
        <p>Website deployment test successful.</p>
    </div>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
