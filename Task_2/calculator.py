import tkinter as tk
from tkinter import messagebox

# ---------------------- Helpers ----------------------

def trim_number(num):
    """Remove trailing zeros from float output"""
    s = ('{:.10f}'.format(num)).rstrip('0').rstrip('.')
    return s if s != '' else '0'


def safe_eval(expr):
    """Safe evaluation for simple calculator expressions"""
    allowed = "0123456789+-*/.()"
    if any(ch not in allowed for ch in expr):
        raise ValueError("Invalid characters")
    return eval(expr)

# ---------------------- Event Logic ----------------------

def click(event):
    global expression
    text = event.widget.cget("text")

    # Convert UI 'x' → '*' internally
    if text == "x":
        text = "*"

    if text == "=":
        try:
            result = safe_eval(expression)
            result = round(result, 10)
            result = trim_number(result)
            entry_var.set(result)
            expression = result
        except ZeroDivisionError:
            messagebox.showerror("Error", "Cannot divide by zero!")
            expression = ""
            entry_var.set("")
        except Exception:
            messagebox.showerror("Error", "Invalid input!")
            expression = ""
            entry_var.set("")
        return

    if text == "C":
        expression = ""
        entry_var.set("")
        return

    if text == "%":
        try:
            if not expression:
                return

            # Find last operator
            last_op = None
            for i in range(len(expression)-1, -1, -1):
                if expression[i] in "+-*/":
                    if i == 0:   # leading -
                        continue
                    last_op = i
                    break

            if last_op is None:
                # single number
                val = float(expression)
                val /= 100
                expression = trim_number(val)
                entry_var.set(expression)
                return

            # expression looks like A op B
            A = safe_eval(expression[:last_op])
            B = float(expression[last_op+1:])

            percent_val = (A * B) / 100

            expression = expression[:last_op+1] + trim_number(percent_val)
            entry_var.set(expression)

        except:
            messagebox.showerror("Error", "Invalid percentage operation!")
            expression = ""
            entry_var.set("")
        return

    # Prevent consecutive operators (except leading -)
    if text in "+-*/":
        if expression == "":
            if text != "-":
                return
        if expression and expression[-1] in "+-*/":
            expression = expression[:-1]

    expression += text
    entry_var.set(expression)

# ---------------------- UI ----------------------

root = tk.Tk()
root.title("iOS Style Calculator")
root.geometry("340x520")
root.resizable(False, False)
root.configure(bg="#000000")

expression = ""
entry_var = tk.StringVar()

# Display
entry = tk.Entry(
    root,
    textvariable=entry_var,
    font=("SF Pro Display", 38),
    justify="right",
    bg="#000000",
    fg="#ffffff",
    bd=0,
    relief=tk.FLAT
)
entry.pack(fill="x", padx=15, pady=20, ipady=20)

# Buttons layout
buttons = [
    ["C", "%", "/", "x"],
    ["7", "8", "9", "-"],
    ["4", "5", "6", "+"],
    ["1", "2", "3", "="],
    ["0", ".", ""]
]

btn_frame = tk.Frame(root, bg="#000000")
btn_frame.pack(fill="both", expand=True, padx=10, pady=10)

# iOS colors
OPERATOR_BG = "#ff9f0a"
LIGHT_BTN = "#d4d4d2"
DARK_BTN = "#505050"

for r, row in enumerate(buttons):
    for c, text in enumerate(row):
        if text == "":
            continue

        # Decide color theme
        if text in ["+", "-", "x", "/", "="]:
            bg = OPERATOR_BG
            fg = "#ffffff"
        elif text == "C":
            bg = LIGHT_BTN
            fg = "#000000"
        else:
            bg = DARK_BTN
            fg = "#ffffff"

        btn = tk.Button(
            btn_frame,
            text=text,
            font=("SF Pro Display", 26),
            bg=bg,
            fg=fg,
            bd=0,
            relief=tk.FLAT,
            activebackground="#737373",
            activeforeground="#ffffff"
        )
        btn.grid(row=r, column=c, sticky="nsew", padx=6, pady=6)
        btn.bind("<Button-1>", click)

# Grid responsiveness
for i in range(5):
    btn_frame.rowconfigure(i, weight=1)
for i in range(4):
    btn_frame.columnconfigure(i, weight=1)

# Make '0' span 2 columns
zero_btn = None
for widget in btn_frame.grid_slaves(row=4, column=0):
    zero_btn = widget
if zero_btn:
    zero_btn.grid_configure(columnspan=2)

root.mainloop()
