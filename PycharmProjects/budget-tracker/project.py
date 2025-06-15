import tkinter as tk
from tkinter import messagebox
import json

def setup_gui():
    root = tk.Tk()
    root.title("financially responsible")

    expenses = []
    budget = 0

    tk.Label(root, text="Set Budget:").grid(row=0, column=0)
    budget_entry = tk.Entry(root)
    budget_entry.grid(row=0, column=1)

    tk.Label(root, text="Category:").grid(row=1, column=0)
    category_entry = tk.Entry(root)
    category_entry.grid(row=1,column=1)

    tk.Label(root,text="Amount:").grid(row=2,column=0)
    amount_entry =tk.Entry(root)
    amount_entry.grid(row=2,column=1)

    tk.Label(root, text="Description:").grid(row=3,column=0)
    description_entry =tk.Entry(root)
    description_entry.grid(row=3,column=1)

    expense_listbox = tk.Listbox(root, width=50)
    expense_listbox.grid(row=4,column=0,columnspan=2)

    def set_budget():
        nonlocal budget
        try:
            budget = float(budget_entry.get())
            messagebox.showinfo("budget set",f"Your budget is set to ${budget}")
        except ValueError:
            messagebox.showerror("error","please enter a valid number for the budget!")

    def add_expense():
        category =category_entry.get()
        amount =amount_entry.get()
        description =description_entry.get()
        if not category or not amount or not description:
            messagebox.showerror("error","all fields are required")
            return
        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("error","amount must be a number")
            return
        expenses.append({"category": category,"amount": amount,"description": description})
        messagebox.showinfo("success","expense added successfully")

        category_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)
        description_entry.delete(0, tk.END)

        check_budget()
    def view_expenses():
        expense_listbox.delete(0,tk.END)
        index= 1
        for expense in expenses:
            expense_listbox.insert(
                tk.END,
                f"{index}. {expense['category']}-${expense['amount']}({expense['description']})")
            index+=1
    def analyze_trends():
        if not expenses:
            messagebox.showinfo("trends", "no expenses to analyze.")
            return
        category_totals={}
        for expense in expenses:
            category = expense['category']
            if category not in category_totals:
                category_totals[category] = 0
            category_totals[category] += expense['amount']
        highest_category = None
        highest_amount = 0
        for category, total in category_totals.items():
            if total > highest_amount:
                highest_category = category
                highest_amount = total
        highest_amount =category_totals[highest_category]

        messagebox.showinfo("trends",f"highest spending:{highest_category}-${highest_amount}")

    def delete_expense():
        selected = expense_listbox.curselection()
        if not selected:
            messagebox.showerror("error","no expense selected")
            return

        index=selected[0]
        del expenses[index]
        view_expenses()
        messagebox.showinfo("success","expense deleted successfully!")

    def save_to_file():
        filename ="expenses.json"
        try:
            with open(filename,'w') as file:
                json.dump(expenses,file)
            messagebox.showinfo("success",f"expenses saved to{filename}successfully")
        except :
            messagebox.showerror("error",f"failed to save to file:")

    def load_from_file():
        filename= "expenses.json"
        try:
            with open(filename, 'r') as file:
                expenses.clear()
                expenses.extend(json.load(file))
            view_expenses()
            messagebox.showinfo("success", f"expenses loaded from{filename}successfully")
        except:
            messagebox.showerror("error", f"failed to load from file:")

    def check_budget():
        total_spent = 0
        for expense in expenses:
            total_spent += expense['amount']
        if budget and total_spent >budget:
            messagebox.showwarning("budget exceeded","you have exceeded your budget")

    tk.Button(root,text="set budget",command=set_budget).grid(row=5,column=0,columnspan=2)
    tk.Button(root,text="add expense",command=add_expense).grid(row=6,column=0,columnspan=2)
    tk.Button(root,text="view expenses",command=view_expenses).grid(row=7,column=0,columnspan=2)
    tk.Button(root,text="analyze trends",command=analyze_trends).grid(row=8,column=0,columnspan=2)
    tk.Button(root,text="save to file",command=save_to_file).grid(row=9,column=0,columnspan=2)
    tk.Button(root,text="load from file",command=load_from_file).grid(row=10,column=0,columnspan=2)
    tk.Button(root,text="delete selected",command=delete_expense).grid(row=11,column=0,columnspan=2)

    root.mainloop()

setup_gui()
