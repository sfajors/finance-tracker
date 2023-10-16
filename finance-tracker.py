import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter import ttk
import json

import datetime
import json

class Transaction:
    def __init__(self, description, amount, category, date=None):
        self.description = description
        self.amount = amount
        self.category = category
        self.date = date if date else datetime.datetime.now().strftime('%Y-%m-%d')

class Expense(Transaction):
    def __init__(self, description, amount, category, date=None):
        super().__init__(description, -abs(amount), category, date)

class Income(Transaction):
    def __init__(self, description, amount, category="Income", date=None):
        super().__init__(description, abs(amount), category, date)

class Budget:
    def __init__(self):
        self.categories = {}

    def set_budget(self, category, amount):
        self.categories[category] = amount

    def get_budget(self, category):
        return self.categories.get(category, 0)

class FinanceTracker(Budget):
    def __init__(self):
        super().__init__()
        self.expenses = []
        self.incomes = []
        self.load_data()

    def add_expense(self, description, amount, category, date=None):
        expense = Expense(description, amount, category, date)
        self.expenses.append(expense)
        self.save_data()

    def add_income(self, description, amount, category="Income", date=None):
        income = Income(description, amount, category, date)
        self.incomes.append(income)
        self.save_data()

    def check_budget_status(self, category):
        budget = self.get_budget(category)
        expenses = sum(exp.amount for exp in self.expenses if exp.category == category)
        return budget + expenses

    def get_transactions_by_category(self, category):
        return [trans for trans in self.expenses + self.incomes if trans.category == category]

    def get_transactions_by_date(self, date):
        date_str = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m-%d')
        return [trans for trans in self.expenses + self.incomes if trans.date == date_str]

    def load_data(self):
        try:
            with open("finance_data.json", "r") as file:
                data = json.load(file)
                self.categories = data["categories"]
                self.expenses = [Expense(e["description"], e["amount"], e["category"], e["date"]) for e in data["expenses"]]
                self.incomes = [Income(i["description"], i["amount"], i["category"], i["date"]) for i in data["incomes"]]
        except FileNotFoundError:
            pass

    def save_data(self):
        data = {
            "categories": self.categories,
            "expenses": [{'description': e.description, 'amount': e.amount, 'category': e.category, 'date': e.date} for e in self.expenses],
            "incomes": [{'description': i.description, 'amount': i.amount, 'category': i.category, 'date': i.date} for i in self.incomes]
        }
        with open("finance_data.json", "w") as file:
            json.dump(data, file, indent=4)

import json

class FinanceTracker:
    def __init__(self):
        self.categories = {}
        self.expenses = []
        self.incomes = []
        self.load_data()

    def set_budget(self, category, amount):
        self.categories[category] = amount
        self.save_data()

    def get_budget(self, category):
        return self.categories.get(category, 0)

    def add_expense(self, description, amount, category):
        expense = Expense(description, amount, category)
        self.expenses.append(expense)
        self.save_data()

    def add_income(self, description, amount, category="Income"):
        income = Income(description, amount, category)
        self.incomes.append(income)
        self.save_data()

    def check_budget_status(self, category):
        budget = self.get_budget(category)
        expenses = sum(exp.amount for exp in self.expenses if exp.category == category)
        return budget + expenses

    def load_data(self):
        try:
            with open("finance_data.json", "r") as file:
                data = json.load(file)
                self.categories = data["categories"]
                self.expenses = [Expense(e["description"], e["amount"], e["category"]) for e in data["expenses"]]
                self.incomes = [Income(i["description"], i["amount"], i["category"]) for i in data["incomes"]]
        except FileNotFoundError:
            pass  # File does not exist yet, starting with an empty state

    def save_data(self):
        data = {
            "categories": self.categories,
            "expenses": [{"description": e.description, "amount": e.amount, "category": e.category} for e in self.expenses],
            "incomes": [{"description": i.description, "amount": i.amount, "category": i.category} for i in self.incomes]
        }
        with open("finance_data.json", "w") as file:
            json.dump(data, file, indent=4)

def run_application():
    finance_tracker = FinanceTracker()
    app = FinanceTrackerApp(finance_tracker)
    app.mainloop()

# GUI Implementation

class FinanceTrackerApp(tk.Tk):
    def __init__(self, finance_tracker):
        super().__init__()
        self.finance_tracker = finance_tracker
        self.title("Finance Tracker")
        self.geometry("1040x660")
        self.configure(bg="#F5F5F5")

        # Buttons
        self.add_expense_button = tk.Button(self, text="Add Expense", command=self.add_expense, bg="white", fg="#9CAFB7", highlightbackground='#9CAFB7', highlightthickness=10)
        self.add_expense_button.grid(row=0, column=0, pady=20, padx=10, sticky="nsew", ipady=10, ipadx=10)

        self.add_income_button = tk.Button(self, text="Add Income", command=self.add_income, bg="white", fg="#9CAFB7", highlightbackground='#9CAFB7', highlightthickness=10)
        self.add_income_button.grid(row=0, column=1, pady=20, padx=10, sticky="nsew", ipady=10, ipadx=10)

        self.set_budget_button = tk.Button(self, text="Set Budget", command=self.set_budget, bg="white", fg="#9CAFB7", highlightbackground='#9CAFB7', highlightthickness=10)
        self.set_budget_button.grid(row=1, column=0, pady=20, padx=10, sticky="nsew", ipady=10, ipadx=10)

        self.check_budget_status_button = tk.Button(self, text="Check Budget Status", command=self.check_budget_status, bg="white", fg="#9CAFB7", highlightbackground='#9CAFB7', highlightthickness=10)
        self.check_budget_status_button.grid(row=1, column=1, pady=20, padx=10, sticky="nsew", ipady=10, ipadx=10)

        self.view_transactions_button = tk.Button(self, text="View Transactions", command=self.view_transactions, bg="white", fg="#9CAFB7", highlightbackground='#9CAFB7', highlightthickness=10)
        self.view_transactions_button.grid(row=2, column=0, columnspan=2, pady=20, sticky="nsew", ipady=0, ipadx=0)

        # Treeview for transactions
        style = ttk.Style()
        style.configure("Custom.Treeview", background="#5E7782", foreground="white")
        style.map("Custom.Treeview", background=[('selected', 'blue')])
        self.tree = ttk.Treeview(self, style="Custom.Treeview", columns=("Description", "Amount", "Category", "Date", "Type"), show="headings")

        self.tree.heading("Description", text="Description")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Type", text="Type")
        self.tree.grid(row=3, column=0, columnspan=2, pady=20, padx=20, ipadx=8, sticky="nsew")

        # Edit and Delete buttons for transactions
        self.edit_button = tk.Button(self, text="Edit Transaction", command=self.edit_transaction, bg="white", fg="#9CAFB7", highlightbackground='#9CAFB7', highlightthickness=10)
        self.edit_button.grid(row=4, column=0, pady=10, padx=20, ipady=10, ipadx=10, sticky="nsew")

        self.delete_button = tk.Button(self, text="Delete Transaction", command=self.delete_transaction, bg="white", fg="#9CAFB7", highlightbackground='#9CAFB7', highlightthickness=10)
        self.delete_button.grid(row=4, column=1, pady=10, padx=20, ipady=10, ipadx=10, sticky="nsew")

        self.refresh_transactions()

    def refresh_transactions(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Load transactions into the treeview
        for expense in self.finance_tracker.expenses:
            self.tree.insert("", "end", values=(expense.description, expense.amount, expense.category, expense.date, "Expense"))

        for income in self.finance_tracker.incomes:
            self.tree.insert("", "end", values=(income.description, income.amount, income.category, income.date, "Income"))

    def delete_transaction(self):
        selected_item = self.tree.selection()[0]
        details = self.tree.item(selected_item, "values")
        description, _, category, date, transaction_type = details
        if messagebox.askyesno("Confirm", f"Are you sure you want to delete the transaction: {description} on {date}?"):
            success = self.finance_tracker.delete_transaction(description, date, transaction_type)
            if success:
                messagebox.showinfo("Info", "Transaction deleted successfully!")
                self.refresh_transactions()
            else:
                messagebox.showerror("Error", "Failed to delete transaction!")

    def edit_transaction(self):
        selected_item = self.tree.selection()[0]
        details = self.tree.item(selected_item, "values")
        old_description, old_amount, old_category, old_date, transaction_type = details

        new_description = simpledialog.askstring("Edit Transaction", "Description:", initialvalue=old_description)
        new_amount = simpledialog.askfloat("Edit Transaction", "Amount:", initialvalue=old_amount)
        new_category = simpledialog.askstring("Edit Transaction", "Category:", initialvalue=old_category)
        new_date = simpledialog.askstring("Edit Transaction", "Date (YYYY-MM-DD):", initialvalue=old_date)

        if new_description and new_amount and new_category and new_date:
            success = self.finance_tracker.edit_transaction(old_description, old_date, new_description, new_amount, new_category, new_date, transaction_type)
            if success:
                messagebox.showinfo("Info", "Transaction edited successfully!")
                self.refresh_transactions()
            else:
                messagebox.showerror("Error", "Failed to edit transaction!")

    # Existing methods from the original GUI

    def view_transactions(self):
        transactions_window = tk.Toplevel(self)
        transactions_window.title("Transactions")
        
        for expense in self.finance_tracker.expenses:
            expense_label = tk.Label(transactions_window, text=f"{expense.description} - ${-expense.amount} - {expense.category}")
            expense_label.pack(pady=5)

        for income in self.finance_tracker.incomes:
            income_label = tk.Label(transactions_window, text=f"{income.description} - ${income.amount} - {income.category}")
            income_label.pack(pady=5)

    def add_expense(self):
        description = simpledialog.askstring("Add Expense", "Description:")
        amount = simpledialog.askfloat("Add Expense", "Amount:")
        category = simpledialog.askstring("Add Expense", "Category:")
        if description and amount and category:
            self.finance_tracker.add_expense(description, amount, category)
            messagebox.showinfo("Info", "Expense added successfully!")
            self.refresh_transactions()

    def add_income(self):
        description = simpledialog.askstring("Add Income", "Description:")
        amount = simpledialog.askfloat("Add Income", "Amount:")
        if description and amount:
            self.finance_tracker.add_income(description, amount)
            messagebox.showinfo("Info", "Income added successfully!")
            self.refresh_transactions()

    def set_budget(self):
        category = simpledialog.askstring("Set Budget", "Category:")
        amount = simpledialog.askfloat("Set Budget", "Budget Amount:")
        if category and amount:
            self.finance_tracker.set_budget(category, amount)
            messagebox.showinfo("Info", f"Budget for {category} set to ${amount}")

    def check_budget_status(self):
        category = simpledialog.askstring("Check Budget Status", "Category:")
        if category:
            status = self.finance_tracker.check_budget_status(category)
            if status < 0:
                messagebox.showwarning("Warning", f"You are over budget by ${-status} for {category}.")
            else:
                messagebox.showinfo("Info", f"You are under budget by ${status} for {category}.")

# Run the GUI
if __name__ == "__main__":
    finance_tracker = FinanceTracker()
    app = FinanceTrackerApp(finance_tracker)
    app.mainloop()