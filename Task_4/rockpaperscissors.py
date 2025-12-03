import tkinter as tk
import random

root = tk.Tk()
root.title("Rock Paper Scissors 🎮")
root.geometry("500x550")
root.config(bg="#f0f4f8")

CHOICES = ["Rock", "Paper", "Scissors"]
EMOJIS = {"Rock": "🪨", "Paper": "📄", "Scissors": "✂️"}

user_score = 0
computer_score = 0
tie_score = 0

# Logic
def determine_winner(user_choice, computer_choice):
    if user_choice == computer_choice:
        return "It's a tie!"
    elif (user_choice == "Rock" and computer_choice == "Scissors") or \
         (user_choice == "Paper" and computer_choice == "Rock") or \
         (user_choice == "Scissors" and computer_choice == "Paper"):
        return "You win!"
    else:
        return "Computer wins!"

def play(user_choice):
    global user_score, computer_score, tie_score

    computer_choice = random.choice(CHOICES)
    result = determine_winner(user_choice, computer_choice)

    # Result
    result_label.config(
        text=f"🧍 You: {EMOJIS[user_choice]} {user_choice}\n💻 Computer: {EMOJIS[computer_choice]} {computer_choice}\n\n➡️ {result}",
        fg="#333"
    )

    if result == "You win!":
        user_score += 1
    elif result == "Computer wins!":
        computer_score += 1
    else:
        tie_score += 1

    update_score_label()

    toggle_choice_buttons(state="disabled")
    play_again_btn.place(relx=0.5, rely=0.85, anchor="center")

def reset_game():
    global user_score, computer_score, tie_score
    user_score = computer_score = tie_score = 0
    update_score_label()
    result_label.config(text="Make your move!", fg="#555")
    toggle_choice_buttons(state="normal")
    play_again_btn.place_forget()

def play_again():
    result_label.config(text="Make your move!", fg="#555")
    toggle_choice_buttons(state="normal")
    play_again_btn.place_forget()

def toggle_choice_buttons(state):
    for btn in (rock_btn, paper_btn, scissors_btn):
        btn.config(state=state)

def update_score_label():
    score_label.config(
        text=f"🏆 You: {user_score}    💻 Computer: {computer_score}    🤝 Tie: {tie_score}"
    )

# UI 

gradient = tk.Canvas(root, width=500, height=550, highlightthickness=0)
gradient.place(x=0, y=0)
for i in range(550):
    color = f"#%02x%02x%02x" % (240 - i//4, 244 - i//6, 248 - i//5)
    gradient.create_line(0, i, 500, i, fill=color)

title_label = tk.Label(
    root,
    text="🎮 Rock - Paper - Scissors 🎮",
    font=("Segoe UI", 22, "bold"),
    bg="#f0f4f8",
    fg="#023047"
)
title_label.place(relx=0.5, y=40, anchor="center")

result_label = tk.Label(
    root,
    text="Make your move!",
    font=("Segoe UI", 15),
    bg="#f0f4f8",
    fg="#444",
    justify="center"
)
result_label.place(relx=0.5, rely=0.4, anchor="center")

# Button
def hover_in(event):
    event.widget.config(bg="#0077b6")

def hover_out(event):
    event.widget.config(bg="#219ebc")

btn_style = {
    "width": 12,
    "font": ("Segoe UI", 13, "bold"),
    "bg": "#219ebc",
    "fg": "white",
    "activebackground": "#0077b6",
    "activeforeground": "white",
    "relief": "flat",
    "bd": 0,
    "cursor": "hand2"
}

button_frame = tk.Frame(root, bg="#f0f4f8")
button_frame.place(relx=0.5, rely=0.6, anchor="center")

rock_btn = tk.Button(button_frame, text="🪨 Rock", command=lambda: play("Rock"), **btn_style)
paper_btn = tk.Button(button_frame, text="📄 Paper", command=lambda: play("Paper"), **btn_style)
scissors_btn = tk.Button(button_frame, text="✂️ Scissors", command=lambda: play("Scissors"), **btn_style)

rock_btn.grid(row=0, column=0, padx=10)
paper_btn.grid(row=0, column=1, padx=10)
scissors_btn.grid(row=0, column=2, padx=10)

for btn in (rock_btn, paper_btn, scissors_btn):
    btn.bind("<Enter>", hover_in)
    btn.bind("<Leave>", hover_out)

score_label = tk.Label(
    root,
    text="🏆 You: 0    💻 Computer: 0    🤝 Tie: 0",
    font=("Segoe UI", 13, "bold"),
    bg="#f0f4f8",
    fg="#023047"
)
score_label.place(relx=0.5, rely=0.75, anchor="center")

play_again_btn = tk.Button(
    root,
    text="🔁 Play Again",
    command=play_again,
    bg="#90be6d",
    fg="white",
    font=("Segoe UI", 12, "bold"),
    width=15,
    relief="flat",
    bd=0,
    cursor="hand2"
)

reset_btn = tk.Button(
    root,
    text="⏹ Reset Scores",
    command=reset_game,
    bg="#ef233c",
    fg="white",
    font=("Segoe UI", 12, "bold"),
    width=15,
    relief="flat",
    bd=0,
    cursor="hand2"
)
reset_btn.place(relx=0.5, rely=0.92, anchor="center")

root.mainloop()
