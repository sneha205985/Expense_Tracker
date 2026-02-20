import matplotlib.pyplot as plt
from api_client import get_all_expenses
from collections import defaultdict

def show_pie_chart():
    try:
        expenses = get_all_expenses()
        category_totals = defaultdict(float)

        for _, _, category, amount, _ in expenses:
            category_totals[category] += amount

        if not category_totals:
            import tkinter.messagebox as messagebox
            messagebox.showinfo("Info", "No expenses to display")
            return

        labels = category_totals.keys()
        sizes = category_totals.values()

        plt.figure(figsize=(6, 6))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%')
        plt.title("Expense Distribution by Category")
        plt.show()
    except Exception as e:
        import tkinter.messagebox as messagebox
        messagebox.showerror("Error", f"Failed to load expenses: {str(e)}")