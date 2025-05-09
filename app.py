from flask import Flask, render_template, request, redirect
import csv
import os
from datetime import datetime


app = Flask(__name__)
FILENAME = "transactions.csv"

# Initialize CSV if not exists
if not os.path.exists(FILENAME):
    with open(FILENAME, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Type", "Category", "Amount", "Description"])

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/add', methods=['POST'])
def add_transaction():
    transaction_type = request.form['type']
    category = request.form['category']
    amount = request.form['amount']
    description = request.form['description']
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(FILENAME, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, transaction_type, category, amount, description])
    
    return redirect('/')

@app.route('/view')
def view_transactions():
    with open(FILENAME, mode='r') as file:
        reader = csv.reader(file)
        transactions = list(reader)[1:]  # skip header
    return render_template("view.html", transactions=transactions)

@app.route('/summary')
def summary():
    total_income = 0
    total_expense = 0

    with open(FILENAME, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                amount = float(row['Amount'])
                if row['Type'] == 'Income':
                    total_income += amount
                elif row['Type'] == 'Expense':
                    total_expense += amount
            except ValueError:
                continue

    balance = total_income - total_expense
    return render_template("summary.html", income=total_income, expense=total_expense, balance=balance)

@app.route('/clear', methods=['POST'])
def clear():
    with open(FILENAME, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Type", "Category", "Amount", "Description"])
    return redirect('/view')

if __name__ == '__main__':
    app.run(debug=True)
