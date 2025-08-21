import json
from datetime import datetime

# Structure of a transaction
# {'type': 'income'/'expense', 'amount': float, 'category': str, 'date': 'YYYY-MM-DD', 'description': str}

transactions = []
savings_goals = []

# Add a transaction
def add_transaction(t_type, amount, category, date, description=""):
    transactions.append({
        'type': t_type,
        'amount': amount,
        'category': category,
        'date': date,
        'description': description
    })

# Sort transactions by amount or date
def sort_transactions(by='date', reverse=False):
    if by not in ['date', 'amount']:
        print("Can only sort by 'date' or 'amount'")
        return
    key_func = (lambda x: datetime.strptime(x['date'], '%Y-%m-%d')) if by == 'date' else (lambda x: x['amount'])
    return sorted(transactions, key=key_func, reverse=reverse)

# Search transactions by category or description keyword
def search_transactions(keyword):
    keyword = keyword.lower()
    return [t for t in transactions if keyword in t['category'].lower() or keyword in t['description'].lower()]

# Filter expenses over a certain amount
def filter_expenses(min_amount):
    return [t for t in transactions if t['type'] == 'expense' and t['amount'] > min_amount]

# Save data to file
def save_to_file(filename='finance_data.json'):
    data = {'transactions': transactions, 'savings_goals': savings_goals}
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Data saved to {filename}")

# Load data from file
def load_from_file(filename='finance_data.json'):
    global transactions, savings_goals
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        transactions = data.get('transactions', [])
        savings_goals = data.get('savings_goals', [])
        print(f"Data loaded from {filename}")
    except FileNotFoundError:
        print(f"No saved data found at {filename}")

# Add savings goal
def add_savings_goal(name, target_amount, current_amount=0):
    savings_goals.append({'name': name, 'target': target_amount, 'current': current_amount})

# Update savings goal progress
def update_savings_goal(name, amount):
    for goal in savings_goals:
        if goal['name'] == name:
            goal['current'] += amount
            if goal['current'] > goal['target']:
                goal['current'] = goal['target']
