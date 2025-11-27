import tkinter as tk
from tkinter import messagebox
import json
import os

TASK_FILE = "tasks.json"

def load_tasks():
    """Load tasks from file if it exists"""
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    """Save tasks to file"""
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")
        self.root.geometry("520x620")
        self.root.config(bg="#e9ecef")

        self.tasks = load_tasks()

        # ----- Header -----
        header = tk.Label(
            self.root,
            text="To-Do List",
            font=("Poppins", 22, "bold"),
            bg="#0d6efd",
            fg="white",
            pady=12
        )
        header.pack(fill="x")

        # ----- Entry Section -----
        entry_frame = tk.Frame(self.root, bg="#f8f9fa", bd=2, relief="ridge")
        entry_frame.pack(pady=20, padx=20, fill="x")

        self.task_entry = tk.Entry(
            entry_frame, font=("Arial", 14), width=28, bd=0, relief="flat", bg="#ffffff"
        )
        self.task_entry.grid(row=0, column=0, padx=10, pady=10, ipady=5)

        add_btn = tk.Button(
            entry_frame,
            text="Add Task",
            font=("Arial", 12, "bold"),
            bg="#198754",
            fg="white",
            width=12,
            relief="flat",
            activebackground="#157347",
            cursor="hand2",
            command=self.add_task
        )
        add_btn.grid(row=0, column=1, padx=5, pady=5)

        # ----- Task List -----
        list_frame = tk.Frame(self.root, bg="#f8f9fa", bd=2, relief="ridge")
        list_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(list_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(
            list_frame,
            font=("Segoe UI", 13),
            width=45,
            height=15,
            bd=0,
            relief="flat",
            bg="#ffffff",
            fg="#212529",
            selectmode=tk.SINGLE,
            selectbackground="#cfe2ff",
            activestyle="none",
            yscrollcommand=self.scrollbar.set
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.listbox.yview)

        # ----- Buttons -----
        btn_frame = tk.Frame(self.root, bg="#e9ecef")
        btn_frame.pack(pady=15)

        buttons = [
            ("Mark Done", "#198754", "#157347", self.mark_done),
            ("Delete Task", "#dc3545", "#bb2d3b", self.delete_task),
            ("Clear All", "#fd7e14", "#e96b0c", self.clear_all),
            ("Exit", "#6c757d", "#5c636a", self.root.destroy)
        ]

        for i, (text, color, active, cmd) in enumerate(buttons):
            btn = tk.Button(
                btn_frame,
                text=text,
                font=("Arial", 11, "bold"),
                bg=color,
                fg="white",
                activebackground=active,
                width=12,
                relief="flat",
                cursor="hand2",
                command=cmd
            )
            btn.grid(row=0, column=i, padx=7, pady=5)

        # Footer
        footer = tk.Label(
            self.root,
            text="Stay organized and productive.",
            bg="#e9ecef",
            fg="#495057",
            font=("Poppins", 10, "italic")
        )
        footer.pack(side="bottom", pady=8)

        self.refresh_listbox()

    def refresh_listbox(self):
        """Refresh the Listbox"""
        self.listbox.delete(0, tk.END)
        for task in self.tasks:
            status = "[✓]" if task["completed"] else "[ ]"
            self.listbox.insert(tk.END, f"{status}  {task['title']}")

    def add_task(self):
        """Add a new task"""
        title = self.task_entry.get().strip()
        if not title:
            messagebox.showwarning("Warning", "Please enter a task!")
            return
        self.tasks.append({"title": title, "completed": False})
        save_tasks(self.tasks)
        self.task_entry.delete(0, tk.END)
        self.refresh_listbox()

    def mark_done(self):
        """Mark selected task as complete"""
        try:
            index = self.listbox.curselection()[0]
            self.tasks[index]["completed"] = True
            save_tasks(self.tasks)
            self.refresh_listbox()
        except IndexError:
            messagebox.showinfo("Info", "Select a task to mark as done.")

    def delete_task(self):
        """Delete selected task"""
        try:
            index = self.listbox.curselection()[0]
            deleted = self.tasks.pop(index)
            save_tasks(self.tasks)
            self.refresh_listbox()
            messagebox.showinfo("Deleted", f"Deleted: {deleted['title']}")
        except IndexError:
            messagebox.showinfo("Info", "Select a task to delete.")

    def clear_all(self):
        """Clear all tasks"""
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all tasks?"):
            self.tasks.clear()
            save_tasks(self.tasks)
            self.refresh_listbox()


if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
