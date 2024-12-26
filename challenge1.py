import tkinter as tk
from tkinter import messagebox, scrolledtext
import os

# Define the absolute file path for the text file
file_path = "data.txt"

# Ensure the text file exists
if not os.path.exists(file_path):
    open(file_path, "w").close()

# Function to add account details and write them to a text file
def add_account(entry_username, entry_password, entry_id, log_widget, account_listbox):
    username = entry_username.get()
    password = entry_password.get()
    user_id = entry_id.get()

    if username.strip() and password.strip() and user_id.strip():
        # Write the account to the text file
        with open(file_path, "a", encoding="utf-8") as file:
            file.write(f"Username: {username}, Password: {password}, ID: {user_id}\n")

        log_widget.insert(tk.END, f"Account added: {username}\n")
        log_widget.see(tk.END)

        # Clear the input fields
        entry_username.delete(0, tk.END)
        entry_password.delete(0, tk.END)
        entry_id.delete(0, tk.END)

        show_accounts(log_widget, account_listbox)  # Refresh the list of accounts after adding
    else:
        messagebox.showwarning("Warning", "All fields must be filled!")

# Function to show all accounts from the text file
def show_accounts(log_widget, account_listbox):
    log_widget.delete(1.0, tk.END)  # Clear the log area
    account_listbox.delete(0, tk.END)  # Clear the listbox

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
            if lines:
                log_widget.insert(tk.END, "Accounts in file:\n")
                for line in lines:
                    log_widget.insert(tk.END, line)
                    account_listbox.insert(tk.END, line.strip())
            else:
                log_widget.insert(tk.END, "No accounts in the file.\n")
    except FileNotFoundError:
        log_widget.insert(tk.END, "No data file found.\n")

# Function to delete selected account
def delete_account(account_listbox, log_widget):
    selected_account = account_listbox.curselection()
    if selected_account:
        account_to_delete = account_listbox.get(selected_account)
        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the account:\n{account_to_delete}?")

        if confirm:
            # Read all accounts and remove the selected one
            updated_accounts = []
            with open(file_path, "r", encoding="utf-8") as file:
                lines = file.readlines()
                updated_accounts = [line for line in lines if line.strip() != account_to_delete.strip()]

            # Write updated accounts back to the text file
            with open(file_path, "w", encoding="utf-8") as file:
                file.writelines(updated_accounts)

            log_widget.insert(tk.END, f"Account deleted: {account_to_delete}\n")
            log_widget.see(tk.END)
            show_accounts(log_widget, account_listbox)  # Refresh the list of accounts after deletion
    else:
        messagebox.showwarning("Warning", "Please select an account to delete!")

# Function to toggle password visibility
def toggle_password(entry_password, var):
    if var.get():
        entry_password.config(show="")
    else:
        entry_password.config(show="*")

# Create the main interface
def create_interface():
    # Initialize the main window
    root = tk.Tk()
    root.title("Account Manager")
    root.geometry("700x500")
    root.config(bg="#f0f0f0")  # Set background color

    # Create a frame for "nasro" at the top left
    top_frame = tk.Frame(root, bg="#f0f0f0")
    top_frame.pack(pady=10, padx=20, anchor="w")  # Align the frame to the top-left corner

    # Add "nasro" label in bold and italic in the top-left frame
    label_nasro = tk.Label(top_frame, text="nasro", font=("Helvetica", 36, "bold italic"), bg="#f0f0f0", anchor="w")
    label_nasro.pack(pady=10)

    # Create the frame for input fields
    frame = tk.Frame(root, bg="#f0f0f0")
    frame.pack(pady=10)

    # Input fields for account details
    tk.Label(frame, text="Username:", font=("Helvetica", 12), bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=5)
    entry_username = tk.Entry(frame, width=40, font=("Helvetica", 12))
    entry_username.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(frame, text="Password:", font=("Helvetica", 12), bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=5)
    entry_password = tk.Entry(frame, width=40, font=("Helvetica", 12), show="*")
    entry_password.grid(row=1, column=1, padx=10, pady=5)

    # Checkbox to toggle password visibility
    var_show_password = tk.BooleanVar()
    password_checkbox = tk.Checkbutton(frame, text="Show Password", variable=var_show_password, font=("Helvetica", 12), bg="#f0f0f0", command=lambda: toggle_password(entry_password, var_show_password))
    password_checkbox.grid(row=1, column=2, padx=10, pady=5)

    tk.Label(frame, text="ID:", font=("Helvetica", 12), bg="#f0f0f0").grid(row=2, column=0, padx=10, pady=5)
    entry_id = tk.Entry(frame, width=40, font=("Helvetica", 12))
    entry_id.grid(row=2, column=1, padx=10, pady=5)

    # Create the buttons and log area
    button_frame = tk.Frame(root, bg="#f0f0f0")
    button_frame.pack(pady=10)

    log_widget = scrolledtext.ScrolledText(root, width=70, height=15, font=("Courier New", 10), wrap=tk.WORD, state="normal")
    log_widget.pack(pady=5)

    tk.Button(button_frame, text="Add Account", command=lambda: add_account(entry_username, entry_password, entry_id, log_widget, account_listbox), font=("Helvetica", 12), bg="#4CAF50", fg="white", width=20, relief="solid").pack(side="left", padx=10, pady=5)
    tk.Button(button_frame, text="Show Accounts", command=lambda: show_accounts(log_widget, account_listbox), font=("Helvetica", 12), bg="#2196F3", fg="white", width=20, relief="solid").pack(side="left", padx=10, pady=5)
    
    # Listbox for displaying accounts and delete button
    account_listbox = tk.Listbox(root, width=70, height=10, font=("Courier New", 10), selectmode=tk.SINGLE)
    account_listbox.pack(pady=10)

    tk.Button(root, text="Delete Selected Account", command=lambda: delete_account(account_listbox, log_widget), font=("Helvetica", 12), bg="#FF5733", fg="white", width=20, relief="solid").pack(pady=10)

    # Show accounts on startup
    show_accounts(log_widget, account_listbox)

    # Run the application
    root.mainloop()

# Run the interface
if __name__ == "__main__":
    create_interface()
