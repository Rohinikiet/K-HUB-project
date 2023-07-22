from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import random

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/expenses')
db = client['expense_tracker']
expenses_collection = db['expenses']


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        description = request.form['description']
        amount = float(request.form['amount'])

        # Insert the new expense to MongoDB
        expenses_collection.insert_one({
            'description': description,
            'amount': amount
        })

        # Redirect to the index page after adding the expense
        return redirect(url_for('index'))

    # Fetch all expenses from MongoDB
    expenses = list(expenses_collection.find())

    return render_template('index.html', expenses=expenses)


@app.route('/visualize', methods=['GET'])
def visualize():
    # Fetch all expenses from MongoDB
    expenses = list(expenses_collection.find())

    # Prepare data for visualization
    labels = [expense['description'] for expense in expenses]
    amounts = [expense['amount'] for expense in expenses]

    return render_template('visualize.html', labels=labels, amounts=amounts)


if __name__ == '__main__':
    app.run(debug=True)
