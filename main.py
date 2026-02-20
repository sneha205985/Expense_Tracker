import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from api_client import (
    init_db, insert_expense, get_all_expenses, delete_expense, update_expense_by_id,
    login, register, set_auth_token
)
from visualizer import show_pie_chart
from utils import today_date
import requests

selected_expense_id = None     # Global for edit/update
total_label=None

def refresh_table(tree, total_label=None):
    for row in tree.get_children():
        tree.delete(row)
    for row in get_all_expenses():
        tree.insert("", tk.END, values=row)
    if total_label:
        total_label.config(text=f"Total Expense: Rs{get_total_expense():.2f}")

def submit_expense(date, category, amount, notes, tree):
    if not category or not amount:
        messagebox.showerror("Error", "Category and Amount required!")
        return
    try:
        insert_expense(date, category, float(amount), notes)
        refresh_table(tree)
        update_total_label()
        clear_entries()
    except ValueError:
        messagebox.showerror("Error", "Invalid amount")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("API Error", f"Failed to add expense: {str(e)}")
    except Exception as e:
        messagebox.showerror("Error", f"Error: {str(e)}")

def delete_selected(tree):
    selected = tree.selection()
    if selected:
        item = tree.item(selected[0])
        expense_id = item['values'][0]
        try:
            delete_expense(expense_id)
            refresh_table(tree)
            update_total_label()
        except requests.exceptions.RequestException as e:
            messagebox.showerror("API Error", f"Failed to delete expense: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")

def edit_selected(tree):
    global selected_expense_id
    selected = tree.selection()
    if selected:
        item = tree.item(selected[0])
        data = item['values']
        selected_expense_id = data[0]
        date_entry.delete(0, tk.END)
        category_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)
        notes_entry.delete(0, tk.END)
        date_entry.insert(0, data[1])
        category_entry.insert(0, data[2])
        amount_entry.insert(0, data[3])
        notes_entry.insert(0, data[4])

def update_expense(date, category, amount, notes, tree):
    global selected_expense_id
    if selected_expense_id is None:
        messagebox.showwarning("Warning", "No row selected for update!")
        return
    try:
        update_expense_by_id(selected_expense_id, date, category, float(amount), notes)
        selected_expense_id = None
        refresh_table(tree)
        update_total_label()
        clear_entries()
    except ValueError:
        messagebox.showerror("Error", "Invalid amount entered.")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("API Error", f"Failed to update expense: {str(e)}")
    except Exception as e:
        messagebox.showerror("Error", f"Error: {str(e)}")

def clear_entries():
    date_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    notes_entry.delete(0, tk.END)
    date_entry.insert(0, today_date())

def get_total_expense(): #total expense
    try:
        return sum(float(row[3]) for row in get_all_expenses())
    except Exception:
        return 0.0

def update_total_label():
    total=get_total_expense()
    total_label.config(text=f"Total Expense: Rs{total:.2f}")

def show_login_dialog(root):
    """Show login/register dialog"""
    login_window = tk.Toplevel(root)
    login_window.title("Login / Register")
    login_window.geometry("400x250")
    login_window.transient(root)
    login_window.grab_set()
    
    tk.Label(login_window, text="Username:").pack(pady=5)
    username_entry = tk.Entry(login_window, width=30)
    username_entry.pack(pady=5)
    
    tk.Label(login_window, text="Email:").pack(pady=5)
    email_entry = tk.Entry(login_window, width=30)
    email_entry.pack(pady=5)
    
    tk.Label(login_window, text="Password:").pack(pady=5)
    password_entry = tk.Entry(login_window, width=30, show="*")
    password_entry.pack(pady=5)
    
    def do_login():
        username = username_entry.get()
        password = password_entry.get()
        if not username or not password:
            messagebox.showerror("Error", "Username and password required!")
            return
        try:
            login(username, password)
            login_window.destroy()
            messagebox.showinfo("Success", "Logged in successfully!")
        except Exception as e:
            messagebox.showerror("Login Failed", f"Error: {str(e)}")
    
    def do_register():
        username = username_entry.get()
        email = email_entry.get()
        password = password_entry.get()
        if not username or not email or not password:
            messagebox.showerror("Error", "All fields required!")
            return
        try:
            register(username, email, password)
            login_window.destroy()
            messagebox.showinfo("Success", "Registered and logged in successfully!")
        except Exception as e:
            messagebox.showerror("Registration Failed", f"Error: {str(e)}")
    
    button_frame = tk.Frame(login_window)
    button_frame.pack(pady=10)
    tk.Button(button_frame, text="Login", command=do_login, width=15).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Register", command=do_register, width=15).pack(side=tk.LEFT, padx=5)
    
    username_entry.focus()


def main():
    global date_entry, category_entry, amount_entry, notes_entry

    root = tk.Tk()
    root.title("Expense Tracker")
    root.geometry("950x550")
    
    # Show login dialog first
    show_login_dialog(root)
    
    # Initialize database (no-op for API mode)
    init_db()

    center_frame = tk.Frame(root)
    center_frame.pack(pady=10)

    tk.Label(center_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=10, pady=5, sticky='e')
    date_entry = tk.Entry(center_frame, width=25)
    date_entry.insert(0, today_date())
    date_entry.grid(row=0, column=1, pady=5)

    tk.Label(center_frame, text="Category:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
    category_entry = tk.Entry(center_frame, width=25)
    category_entry.grid(row=1, column=1, pady=5)

    tk.Label(center_frame, text="Amount:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
    amount_entry = tk.Entry(center_frame, width=25)
    amount_entry.grid(row=2, column=1, pady=5)

    tk.Label(center_frame, text="Notes:").grid(row=3, column=0, padx=10, pady=5, sticky='e')
    notes_entry = tk.Entry(center_frame, width=25)
    notes_entry.grid(row=3, column=1, pady=5)

    button_frame = tk.Frame(root)
    button_frame.pack(pady=5)

    tk.Button(button_frame, text="Add Expense", command=lambda: submit_expense(
        date_entry.get(), category_entry.get(), amount_entry.get(), notes_entry.get(), tree
    )).grid(row=0, column=0, padx=5)

    tk.Button(button_frame, text="Delete Selected", command=lambda: delete_selected(tree)).grid(row=0, column=1, padx=5)
    tk.Button(button_frame, text="Edit Selected", command=lambda: edit_selected(tree)).grid(row=0, column=2, padx=5)
    tk.Button(button_frame, text="Update Expense", command=lambda: update_expense(
        date_entry.get(), category_entry.get(), amount_entry.get(), notes_entry.get(), tree
    )).grid(row=0, column=3, padx=5)

    tk.Button(button_frame, text="Show Pie Chart", command=show_pie_chart).grid(row=0, column=4, padx=5)

    global total_label
    total_label=tk.Label(root, text=f"Total Expense: Rs{get_total_expense():.2f}", font=("Arial", 20, "bold"))
    total_label.pack(pady=5)


    tree = ttk.Treeview(root, columns=("ID", "Date", "Category", "Amount", "Notes"), show='headings', height=10)
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")
    tree.pack(pady=15)

    refresh_table(tree)
    root.mainloop()

if __name__ == "__main__":
    main()
