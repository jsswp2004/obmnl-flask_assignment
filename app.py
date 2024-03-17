# Import libraries
from flask import Flask, request, url_for, redirect, render_template
from flask import render_template
# Instantiate Flask functionality
app = Flask(__name__)
# Sample data
# Sample data
transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]
# Read operation: List all transactions
# @app.route("/")
# def get_transactions():
#    return render_template("transactions.html", transactions=transactions)

# Create operation
@app.route("/add", methods=["GET", "POST"])
def add_transaction():
    if request.method == "GET":
        return render_template("form.html")
    elif request.method == "POST":
        amount = float(request.form.get("amount"))
        description = request.form.get("description")

        new_transaction = {"id": len(transactions) + 1, "amount": amount, "description": description}
        transactions.append(new_transaction)

        return redirect(url_for("get_transactions"))

# Update operation: Display edit transaction form
@app.route("/edit/<int:transaction_id>", methods=["GET", "POST"])
def edit_transaction(transaction_id):
    if request.method == 'POST':
        # Extract the updated values from the form fields
        date = request.form['date']
        amount = float(request.form['amount'])

        # Find the transaction with the matching ID and update its values
        for transaction in transactions:
            if transaction['id'] == transaction_id:
                transaction['date'] = date
                transaction['amount'] = amount
                break

        # Redirect to the transactions list page
        return redirect(url_for("get_transactions"))
    
    # Find the transaction with the matching ID and render the edit form
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            return render_template("edit.html", transaction=transaction)

# Delete operation: Delete a transaction
@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
    # Find the transaction with the matching ID and remove it from the list
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            transactions.remove(transaction)
            break

    # Redirect to the transactions list page
    return redirect(url_for("get_transactions"))

@app.route("/search", methods=["GET", "POST"])
def search_transactions():
    if request.method == "POST":
        min_amount = float(request.form.get("min_amount"))
        max_amount = float(request.form.get("max_amount"))

        filtered_transactions = [
            transaction for transaction in transactions
            if min_amount <= transaction["amount"] <= max_amount
        ]

        return render_template("transactions.html", transactions=filtered_transactions)
    else:
        return render_template("search.html")
    
@app.route("/balance")
def total_balance():
    return str(sum(transaction["amount"] for transaction in transactions))

@app.route("/")
def get_transactions():
    total_balance_value = total_balance()  # Calculate total balance
    return render_template("transactions.html", transactions=transactions, total_balance=total_balance_value)

# Run the Flask app

if __name__ == "__main__":
    app.run(debug=True)
