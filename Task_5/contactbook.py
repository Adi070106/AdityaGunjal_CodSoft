import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

CONTACT_FILE = "contacts.json"

# ---------------------- DATA HANDLING ----------------------
def load_contacts():
    """Load contacts safely from JSON file."""
    if not os.path.exists(CONTACT_FILE):
        return []

    try:
        with open(CONTACT_FILE, "r") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            else:
                return []
    except json.JSONDecodeError:
        messagebox.showerror("Error", "contacts.json is corrupted. Fix or delete the file.")
        return []


def save_contacts(contacts):
    try:
        with open(CONTACT_FILE, "w") as f:
            json.dump(contacts, f, indent=4)
    except:
        messagebox.showerror("Error", "Unable to save contacts.")


# ---------------------- APP CLASS ----------------------
class ContactBook:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Book")
        self.root.geometry("850x500")
        self.root.configure(bg="#e9eef7")

        self.contacts = load_contacts()

        title = tk.Label(
            root, text="CONTACT BOOK", font=("Arial", 20, "bold"),
            bg="#4A6FA5", fg="white", pady=10
        )
        title.pack(fill=tk.X)

        main_frame = tk.Frame(root, bg="#e9eef7")
        main_frame.pack(pady=10)

        form_frame = tk.LabelFrame(main_frame, text="Add / Update Contact",
                                   font=("Arial", 12, "bold"), bg="#e9eef7")
        form_frame.grid(row=0, column=0, padx=20, pady=10)

        tk.Label(form_frame, text="Name:", bg="#e9eef7").grid(row=0, column=0, sticky="w")
        self.name_entry = tk.Entry(form_frame, width=30)
        self.name_entry.grid(row=0, column=1, pady=5)

        tk.Label(form_frame, text="Phone:", bg="#e9eef7").grid(row=1, column=0, sticky="w")
        self.phone_entry = tk.Entry(form_frame, width=30)
        self.phone_entry.grid(row=1, column=1, pady=5)

        tk.Label(form_frame, text="Email:", bg="#e9eef7").grid(row=2, column=0, sticky="w")
        self.email_entry = tk.Entry(form_frame, width=30)
        self.email_entry.grid(row=2, column=1, pady=5)

        tk.Label(form_frame, text="Address:", bg="#e9eef7").grid(row=3, column=0, sticky="w")
        self.address_entry = tk.Entry(form_frame, width=30)
        self.address_entry.grid(row=3, column=1, pady=5)

        tk.Button(form_frame, text="Add Contact", command=self.add_contact,
                  bg="#4A6FA5", fg="white", width=20).grid(row=4, column=0, columnspan=2, pady=10)

        tk.Button(form_frame, text="Update Selected", command=self.update_contact,
                  bg="#8E8FFA", fg="white", width=20).grid(row=5, column=0, columnspan=2, pady=5)

        tk.Button(form_frame, text="Delete Selected", command=self.delete_contact,
                  bg="#D9534F", fg="white", width=20).grid(row=6, column=0, columnspan=2, pady=5)

        # ---------------------- SEARCH ----------------------
        search_frame = tk.Frame(root, bg="#e9eef7")
        search_frame.pack()

        tk.Label(search_frame, text="Search:", bg="#e9eef7").grid(row=0, column=0)
        self.search_entry = tk.Entry(search_frame, width=40)
        self.search_entry.grid(row=0, column=1, padx=5)
        tk.Button(search_frame, text="Search", command=self.search_contact,
                  bg="#4A6FA5", fg="white").grid(row=0, column=2, padx=5)
        tk.Button(search_frame, text="Reset", command=self.reset_search,
                  bg="#6C757D", fg="white").grid(row=0, column=3)

        # ---------------------- CONTACT LIST ----------------------
        list_frame = tk.Frame(root, bg="#e9eef7")
        list_frame.pack(pady=10)

        self.tree = ttk.Treeview(list_frame, columns=("Name", "Phone", "Email", "Address"),
                                 show="headings", height=12)
        self.tree.pack()

        for col in ("Name", "Phone", "Email", "Address"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        self.load_list()

    # ---------------------- LOAD LIST ----------------------
    def load_list(self):
        """Load contacts into TreeView safely."""
        self.tree.delete(*self.tree.get_children())

        for c in self.contacts:
            name = c.get("name", "")
            phone = c.get("phone", "")
            email = c.get("email", "")
            address = c.get("address", "")

            self.tree.insert("", tk.END, values=(name, phone, email, address))

    # ---------------------- ADD CONTACT ----------------------
    def add_contact(self):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        address = self.address_entry.get().strip()

        if not name or not phone:
            messagebox.showerror("Error", "Name and Phone are mandatory!")
            return

        self.contacts.append({
            "name": name,
            "phone": phone,
            "email": email,
            "address": address
        })

        save_contacts(self.contacts)
        self.load_list()
        self.clear_entries()
        messagebox.showinfo("Success", "Contact added successfully!")

    # ---------------------- DELETE CONTACT ----------------------
    def delete_contact(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a contact to delete")
            return

        item_id = selected[0]
        index = self.tree.index(item_id)

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Delete '{self.contacts[index]['name']}'?"
        )
        if not confirm:
            return

        del self.contacts[index]

        save_contacts(self.contacts)
        self.load_list()
        self.clear_entries()
        messagebox.showinfo("Deleted", "Contact deleted successfully!")

    # ---------------------- UPDATE CONTACT ----------------------
    def update_contact(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a contact to update")
            return

        item_id = selected[0]
        index = self.tree.index(item_id)

        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        address = self.address_entry.get().strip()

        if not name or not phone:
            messagebox.showerror("Error", "Name and Phone are mandatory!")
            return

        self.contacts[index] = {
            "name": name,
            "phone": phone,
            "email": email,
            "address": address
        }

        save_contacts(self.contacts)
        self.load_list()
        messagebox.showinfo("Updated", "Contact updated successfully!")

    # ---------------------- SEARCH ----------------------
    def search_contact(self):
        keyword = self.search_entry.get().lower().strip()
        if not keyword:
            self.load_list()
            return

        results = [
            c for c in self.contacts
            if keyword in c.get("name", "").lower()
            or keyword in c.get("phone", "")
            or keyword in c.get("email", "").lower()
            or keyword in c.get("address", "").lower()
        ]

        self.tree.delete(*self.tree.get_children())

        for c in results:
            self.tree.insert("", tk.END,
                             values=(c["name"], c["phone"], c["email"], c["address"]))

    def reset_search(self):
        self.search_entry.delete(0, tk.END)
        self.load_list()
        self.clear_entries()

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        item_id = selected[0]
        values = self.tree.item(item_id, "values")

        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, values[0])
        self.phone_entry.delete(0, tk.END)
        self.phone_entry.insert(0, values[1])
        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, values[2])
        self.address_entry.delete(0, tk.END)
        self.address_entry.insert(0, values[3])


# ---------------------- MAIN APP ----------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = ContactBook(root)
    root.mainloop()
