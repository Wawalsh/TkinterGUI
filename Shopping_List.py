import tkinter as tk
from tkinter import messagebox
from db import Database

# Instanciate databse object
db = Database('store.db')

# Main Application/GUI class


class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        master.title('Shopping List')
        # Width height
        master.geometry("700x350")
        # Create widgets/grid
        self.create_widgets()
        # Init selected item var
        self.selected_item = 0
        # Populate initial list
        self.populate_list()

    def create_widgets(self):
        # item
        self.item_text = tk.StringVar()
        self.item_label = tk.Label(
            self.master, text='Item:', font=('bold', 14), pady=20)
        self.item_label.grid(row=0, column=0, sticky=tk.W)
        self.item_entry = tk.Entry(self.master, textvariable=self.item_text)
        self.item_entry.grid(row=0, column=1)
        # Product Type
        self.type_text = tk.StringVar()
        self.type_label = tk.Label(
            self.master, text='Product Type:', font=('bold', 14))
        self.type_label.grid(row=0, column=2, sticky=tk.W)
        self.type_entry = tk.Entry(
            self.master, textvariable=self.type_text)
        self.type_entry.grid(row=0, column=3)
        # Store
        self.store_text = tk.StringVar()
        self.store_label = tk.Label(
            self.master, text='Store:', font=('bold', 14))
        self.store_label.grid(row=1, column=0, sticky=tk.W)
        self.store_entry = tk.Entry(
            self.master, textvariable=self.store_text)
        self.store_entry.grid(row=1, column=1)
        # Price
        self.price_text = tk.StringVar()
        self.price_label = tk.Label(
            self.master, text='Price:', font=('bold', 14))
        self.price_label.grid(row=1, column=2, sticky=tk.W)
        self.price_entry = tk.Entry(self.master, textvariable=self.price_text)
        self.price_entry.grid(row=1, column=3)

        # item list (listbox)
        self.item_list = tk.Listbox(self.master, height=8, width=50, border=0)
        self.item_list.grid(row=3, column=0, columnspan=3,
                             rowspan=6, pady=20, padx=20)
        # Create scrollbar
        self.scrollbar = tk.Scrollbar(self.master)
        self.scrollbar.grid(row=3, column=3)
        # Set scrollbar to items
        self.item_list.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.item_list.yview)

        # Bind select
        self.item_list.bind('<<ListboxSelect>>', self.select_item)

        # Buttons
        self.add_btn = tk.Button(
            self.master, text="Add", width=12, command=self.add_item)
        self.add_btn.grid(row=2, column=0, pady=20)

        self.remove_btn = tk.Button(
            self.master, text="Remove", width=12, command=self.remove_item)
        self.remove_btn.grid(row=2, column=1)

        self.update_btn = tk.Button(
            self.master, text="Edit", width=12, command=self.update_item)
        self.update_btn.grid(row=2, column=2)

        self.exit_btn = tk.Button(
            self.master, text="Clear", width=12, command=self.clear_text)
        self.exit_btn.grid(row=2, column=3)

    def populate_list(self):
        # Delete items before update. So when you keep pressing it doesnt keep getting (show example by calling this twice)
        self.item_list.delete(0, tk.END)
        # Loop through records
        for row in db.fetch():
            # Insert into list
            self.item_list.insert(tk.END, row)

    # Add new item
    def add_item(self):
        if self.item_text.get() == '' or self.type_text.get() == '' or self.store_text.get() == '' or self.price_text.get() == '':
            messagebox.showerror(
                "Required Fields", "Please include all fields")
            return
        print(self.item_text.get())
        # Insert into DB
        db.insert(self.item_text.get(), self.type_text.get(),
                  self.store_text.get(), self.price_text.get())
        # Clear list
        self.item_list.delete(0, tk.END)
        # Insert into list
        self.item_list.insert(tk.END, (self.item_text.get(), self.type_text.get(
        ), self.store_text.get(), self.price_text.get()))
        self.clear_text()
        self.populate_list()

    # Runs when item is selected
    def select_item(self, event):
        # # Create global selected item to use in other functions
        # global self.selected_item
        try:
            # Get index
            index = self.item_list.curselection()[0]
            # Get selected item
            self.selected_item = self.item_list.get(index)
            # print(selected_item) # Print tuple

            # Add text to entries
            self.item_entry.delete(0, tk.END)
            self.item_entry.insert(tk.END, self.selected_item[1])
            self.type_entry.delete(0, tk.END)
            self.type_entry.insert(tk.END, self.selected_item[2])
            self.store_entry.delete(0, tk.END)
            self.store_entry.insert(tk.END, self.selected_item[3])
            self.price_entry.delete(0, tk.END)
            self.price_entry.insert(tk.END, self.selected_item[4])
        except IndexError:
            pass

    # Remove item
    def remove_item(self):
        db.remove(self.selected_item[0])
        self.clear_text()
        self.populate_list()

    # Update item
    def update_item(self):
        db.update(self.selected_item[0], self.item_text.get(
        ), self.type_text.get(), self.store_text.get(), self.price_text.get())
        self.populate_list()

    # Clear all text fields
    def clear_text(self):
        self.item_entry.delete(0, tk.END)
        self.type_entry.delete(0, tk.END)
        self.store_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)


root = tk.Tk()
app = Application(master=root)
app.mainloop()