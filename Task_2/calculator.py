import tkinter as tk

# ---------------- Logic ---------------- #

def click(btn_text):
    global expression

    # Convert UI 'x' into internal '*'
    if btn_text == "x":
        btn_text = "*"

    if btn_text == "C":
        expression = ""
        input_var.set("")
        return

    if btn_text == "=":
        try:
            result = str(eval(expression))
            input_var.set(result)
            expression = result
        except ZeroDivisionError:
            input_var.set("Cannot divide by zero")
            expression = ""
        except Exception:
            input_var.set("Error")
            expression = ""
        return

    if btn_text == "%":
        try:
            result = str(eval(expression) / 100)
            input_var.set(result)
            expression = result
        except:
            input_var.set("Error")
            expression = ""
        return

    expression += btn_text
    input_var.set(expression)

# ---------------- UI ---------------- #

root = tk.Tk()
root.title("Colorful Calculator")
root.geometry("330x440")
root.resizable(False, False)
root.configure(bg="#1c1c1c")

expression = ""
input_var = tk.StringVar()

# Display
entry = tk.Entry(
    root,
    textvariable=input_var,
    font=("Arial", 28),
    justify="right",
    bd=0,
    bg="#1c1c1c",
    fg="white",
    relief=tk.FLAT
)
entry.pack(fill="x", padx=15, pady=20, ipady=20)

# Buttons layout
buttons = [
    ["C", "%", "/", "x"],
    ["7", "8", "9", "-"],
    ["4", "5", "6", "+"],
    ["1", "2", "3", "="],
    ["0", ".", "(", ")"]
]

btn_frame = tk.Frame(root, bg="#1c1c1c")
btn_frame.pack(expand=True, fill="both")

# Colors
NUMBER_BG = "#2e2e2e"
OP_BG = "#5a5a5a"

NUMBER_FG = "white"
OP_FG = "white"

for r, row in enumerate(buttons):
    for c, text in enumerate(row):

        # Number buttons
        if text.isdigit():
            bg = NUMBER_BG
            fg = NUMBER_FG

        # Operator buttons
        else:
            bg = OP_BG
            fg = OP_FG

        btn = tk.Button(
            btn_frame,
            text=text,
            font=("Arial", 18),
            bd=0,
            bg=bg,
            fg=fg,
            activebackground="#777",
            command=lambda t=text: click(t)
        )
        btn.grid(row=r, column=c, sticky="nsew", padx=5, pady=5)

# Grid resize rules
for i in range(5):
    btn_frame.rowconfigure(i, weight=1)
for i in range(4):
    btn_frame.columnconfigure(i, weight=1)

root.mainloop()
