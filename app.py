from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    # Get form data
    num_friends = int(request.form['num_friends'])
    names = [request.form[f'name_{i+1}'] for i in range(num_friends)]
    expenses = [float(request.form[f'expense_{i+1}']) for i in range(num_friends)]

    # Calculate total expenses and average per person
    total_expenses = sum(expenses)
    avg_expense = total_expenses / num_friends

    # Determine who owes whom
    transactions = []

    for i in range(num_friends):
        if expenses[i] > avg_expense:
            for j in range(num_friends):
                if expenses[j] < avg_expense:
                    amount_to_transfer = min(expenses[i] - avg_expense, avg_expense - expenses[j])
                    if amount_to_transfer > 0:
                        transactions.append((names[j], names[i], round(amount_to_transfer, 2)))
                        expenses[i] -= amount_to_transfer
                        expenses[j] += amount_to_transfer
                    if expenses[i] <= avg_expense:
                        break

    # Generate result with transactions
    results = []
    for transaction in transactions:
        results.append(f"{transaction[0]} needs to pay {transaction[1]} ₹{transaction[2]:.2f}.")

    return render_template('result.html', results=results, total_expenses=total_expenses, avg_expense=avg_expense)

if __name__ == '__main__':
    app.run()
