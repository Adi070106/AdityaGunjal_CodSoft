import tkinter as tk
from tkinter import messagebox
import random
import string

# Function to generate password
def generate_password():
    try:
        length = int(length_entry.get())
        if length < 6:
            messagebox.showerror("Error", "Password length must be at least 6")
            return

        # Include selected character types
        characters = ""
        if var_upper.get():
            characters += string.ascii_uppercase
        if var_lower.get():
            characters += string.ascii_lowercase
        if var_digits.get():
            characters += string.digits
        if var_symbols.get():
            characters += string.punctuation

        if not characters:
            messagebox.showerror("Error", "Please select at least one character type!")
            return

        # Generate password
        password = "".join(random.choice(characters) for _ in range(length))
        result_entry.delete(0, tk.END)
        result_entry.insert(0, password)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number!")

# Function to copy password
def copy_password():
    password = result_entry.get()
    if password:
        root.clipboard_clear()
        root.clipboard_append(password)
        messagebox.showinfo("Copied", "Password copied to clipboard!")
    else:
        messagebox.showwarning("Warning", "No password to copy!")

# ---- GUI ----
root = tk.Tk()
root.title("🔐 Password Generator")
root.geometry("500x500")
root.config(bg="#1e1e2f")

title_label = tk.Label(root, text="Secure Password Generator", font=("Arial Rounded MT Bold", 16), fg="white", bg="#1e1e2f")
title_label.pack(pady=15)

# Password length input
frame_length = tk.Frame(root, bg="#1e1e2f")
frame_length.pack(pady=5)
tk.Label(frame_length, text="Password Length:", font=("Arial", 12), fg="white", bg="#1e1e2f").pack(side=tk.LEFT, padx=5)
length_entry = tk.Entry(frame_length, width=10, font=("Arial", 12))
length_entry.pack(side=tk.LEFT)
length_entry.insert(0, "12")

# Character options
options_frame = tk.LabelFrame(root, text="Character Options", fg="white", bg="#292945", font=("Arial", 11, "bold"), bd=3, labelanchor='n')
options_frame.pack(pady=15, padx=10, fill="x")

var_upper = tk.BooleanVar(value=True)
var_lower = tk.BooleanVar(value=True)
var_digits = tk.BooleanVar(value=True)
var_symbols = tk.BooleanVar(value=True)

tk.Checkbutton(options_frame, text="Uppercase (A-Z)", variable=var_upper, font=("Arial", 10), bg="#292945", fg="white", selectcolor="#444").pack(anchor="w", padx=20)
tk.Checkbutton(options_frame, text="Lowercase (a-z)", variable=var_lower, font=("Arial", 10), bg="#292945", fg="white", selectcolor="#444").pack(anchor="w", padx=20)
tk.Checkbutton(options_frame, text="Digits (0-9)", variable=var_digits, font=("Arial", 10), bg="#292945", fg="white", selectcolor="#444").pack(anchor="w", padx=20)
tk.Checkbutton(options_frame, text="Symbols (!@#$%)", variable=var_symbols, font=("Arial", 10), bg="#292945", fg="white", selectcolor="#444").pack(anchor="w", padx=20)

# Generate button
generate_btn = tk.Button(root, text="Generate Password", command=generate_password, font=("Arial", 12, "bold"), bg="#3b82f6", fg="white", activebackground="#2563eb", relief="flat", padx=10, pady=5)
generate_btn.pack(pady=15)

# Result display
result_entry = tk.Entry(root, width=35, font=("Consolas", 12), justify="center")
result_entry.pack(pady=5)

# Copy button
copy_btn = tk.Button(root, text="Copy to Clipboard", command=copy_password, font=("Arial", 11), bg="#10b981", fg="white", relief="flat", padx=10, pady=5)
copy_btn.pack(pady=10)

footer = tk.Label(root, text="© CodSoft Internship - Task 3", font=("Arial", 9), bg="#1e1e2f", fg="gray")
footer.pack(side="bottom", pady=5)

root.mainloop()
