import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt

conn = sqlite3.connect('expenses.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses(
        id INTEGER PRIMARY KEY,
        amount REAl,
        category TEXT,
        date TEXT
    )
''')
conn.commit()
def add_expense(amount, category):
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('INSERT INTO expenses (amount, category, date) VALUES (?, ?, ?)', (amount, category, date))
    conn.commit()
    print('Expense added successfully!')

def view_expenses():
    cursor.execute('SELECT * FROM expenses')
    expenses = cursor.fetchall()
    for expense in expenses:
        print(f"ID: {expense[0]}, Amount: {expense[1]}, Category: {expense[2]}, Date: {expense[3]}")


def summarize_expenses():
    category = input('Enter category to summarize: ')
    cursor.execute('SELECT SUM(amount) FROM expenses WHERE category = ?', (category,))
    total = cursor.fetchone()[0]
    if total:
        print(f"Total expenses for category '{category}': {total}")
    else:
        print(f"No expenses found for category '{category}'")


def visualize_expenses_by_category():
    cursor.execute('SELECT category, SUM(amount) FROM expenses GROUP BY category')
    data = cursor.fetchall()

    categories = [item[0] for item in data]
    amounts = [item[1] for item in data]

    plt.bar(categories, amounts)
    plt.xlabel('Expense Categories')
    plt.ylabel('Total Amount')
    plt.title('Expense Distribution by Category')
    plt.xticks(rotation=45)
    plt.show()



while True:
    print("\nExpense Tracker Menu:")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Summarize Expenses")
    print("4. visualize Expenses")
    print("5. Exit")
    choice = input("Enter your choice: ")

    if choice == '1':
        amount = float(input("Enter expense amount: "))
        category = input("Enter expense category: ")
        add_expense(amount, category)
    elif choice == '2':
        view_expenses()
    elif choice == '3':
        summarize_expenses()
    
    elif choice == '4':
        visualize_expenses_by_category()
    elif choice == '5':
        print("Exiting the Expense Tracker. Goodbye!")
        break
    else:
        print("Invalid choice. Please select a valid option.")