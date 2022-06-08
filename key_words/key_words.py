# ***** Imported modules
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import sqlite3
import os.path


# ***** Function: creates SQL database if one does not already exist
def initialise_database():
    if os.path.isfile("keywords_db.db"):
        print("Database already exists.")
    else:
        con = sqlite3.connect("keywords_db.db")
        cur = con.cursor()
        cur.execute("""CREATE TABLE keywords (
        entry_id INTEGER PRIMARY KEY,
        key TEXT,
        value TEXT
        )""")
        con.commit()
        con.close()
        print("New database created.")


# ***** Class: contains "Add Keyword" top-level window
class Add:
    def __init__(self):
        # ***** Method: Adds new keyword to database with user input
        def add_key():
            # ***** Message Box: error message if keyword is not entered
            if add_key_entry.get() == "":
                messagebox.showerror(title="Error", message="Please enter the new keyword.")
            elif add_key_entry.get() != "":
                # ***** SQL Query: adds new keyword to database with the user input
                con = sqlite3.connect("keywords_db.db")
                cur = con.cursor()
                cur.execute(
                    """INSERT INTO keywords (key, value) VALUES (?, ?)""",
                    (add_key_entry.get(),
                     add_value_text.get(1.0, "end-1c")
                     ))
                con.commit()
                con.close()
                # ***** Message Box: success message when keyword is entered in to the SQL database
                success_msg = f"{add_key_entry.get()} has been added to the keyword list."
                messagebox.showerror(title="Success", message=success_msg)
                # ***** Closes top level window after keyword is added
                add_key_window.destroy()
                populate_tree_view()

        # ***** Top Level: "Add keyword" window attributes
        add_key_window = Toplevel()
        add_key_window.title("Add Keyword")
        add_key_window.geometry("400x420")
        add_key_window.configure(padx=5, pady=5)
        add_key_window.resizable(False, False)

        # ***** New keyword window geometry
        add_key_window.rowconfigure(0, weight=1)
        add_key_window.rowconfigure(1, weight=1)
        add_key_window.rowconfigure(2, weight=1)
        add_key_window.columnconfigure(0, weight=1)

        # ***** Label Frame: add keyword frame contains keyword entry
        add_key_frame = LabelFrame(add_key_window, text="Enter Keyword")
        add_key_frame.grid(row=0, column=0, padx=3, pady=3, sticky="w")

        # ***** Add keyword label frame geometry
        add_key_frame.rowconfigure(0, weight=1)
        add_key_frame.columnconfigure(0, weight=1)

        # ***** Entry: add keyword entry
        add_key_entry = Entry(add_key_frame, width=28)
        add_key_entry.grid(row=0, column=0)

        # ***** Label Frame: notes frame contains text box to ender new keyword notes
        add_value_frame = LabelFrame(add_key_window, text="Enter Notes")
        add_value_frame.grid(row=1, column=0, padx=3, pady=3, sticky="nesw")

        # ***** Scrollbar: y-axis for notes box
        add_value_scrollbar_y = Scrollbar(add_value_frame, orient=VERTICAL)
        add_value_scrollbar_y.pack(fill=Y, side=RIGHT)

        # ***** Text: text box for notes entry
        add_value_text = Text(add_value_frame, height=20, highlightthickness=0, wrap="word",
                              yscrollcommand=add_value_scrollbar_y.set)
        add_value_text.pack(fill=BOTH, expand=TRUE)

        # ***** Label Frame: commands frame containing buttons
        add_commands_frame = LabelFrame(add_key_window, text="Commands")
        add_commands_frame.grid(row=2, column=0, padx=3, pady=3, sticky="nesw")

        # ***** Label Frame: commands frame geometry
        add_commands_frame.rowconfigure(0, weight=1)
        add_commands_frame.columnconfigure(0, weight=1)
        add_commands_frame.columnconfigure(1, weight=1)

        # ***** Button: add or cancel buttons for add new form
        add_key_btn = Button(add_commands_frame, text="Add Keyword", width=13, command=add_key)
        add_key_btn.grid(row=0, column=0)
        cnl_add_key_btn = Button(add_commands_frame, text="Cancel", width=13, command=add_key_window.destroy)
        cnl_add_key_btn.grid(row=0, column=1)

        # ***** Deactivates main window while top level is open
        add_key_window.grab_set()


# ***** Class: contains "Modify keyword" top-level window
class Mod:
    def __init__(self):
        # ***** Message Box: error message if there is no selection when modification is attempted
        if not tree_view.selection():
            messagebox.showerror(title="Attention", message="Please select a keyword to modify.")
        else:
            # ***** Method: SQL query that populates modify window directly with SQL database information
            def populate_mod_entries():
                mod_key_selection = tree_view.item(tree_view.focus())
                mod_rowid_selection = mod_key_selection["values"][0]
                con = sqlite3.connect("keywords_db.db")
                cur = con.cursor()
                cur.execute("SELECT * "
                            "FROM keywords "
                            f"WHERE rowid={mod_rowid_selection}")
                results = cur.fetchall()
                # ***** List Comprehension: finds elements inside tuple that is inside list then converts to string
                mod_key_entry.insert(0, "".join([item[1] for item in results]))
                mod_value_text.insert(1.0, "".join([item[2] for item in results]))
                con.commit()
                con.close()

            # ***** Method: modifies selected keyword and updates SQL database
            def mod_key():
                # ***** Message Box: error message if there is no selection when modification is attempted
                if mod_key_entry.get() == "":
                    messagebox.showerror(title="Error", message="Please select a keyword to modify.")
                elif mod_key_entry.get() != "":
                    mod_key_selection = tree_view.item(tree_view.focus())
                    mod_rowid_selection = mod_key_selection["values"][0]
                    con = sqlite3.connect("keywords_db.db")
                    cur = con.cursor()
                    cur.execute("SELECT * "
                                "FROM keywords "
                                f"WHERE rowid={mod_rowid_selection}")
                    cur.execute("UPDATE keywords "
                                "SET "
                                f"key='{mod_key_entry.get()}',"
                                f"value='{mod_value_text.get(1.0, 'end-1c')}' WHERE rowid={mod_rowid_selection}")
                    con.commit()
                    con.close()
                    # ***** Message Box: success message when keyword is entered in to the SQL database
                    success_msg = f"{mod_key_entry.get()} has been modified."
                    messagebox.showerror(title="Success", message=success_msg)
                    # ***** Closes top level window after keyword is added
                    mod_key_window.destroy()
                    populate_tree_view()

            # ***** SQL query to populate top level window with selected keyword to modify
            key_selection = tree_view.item(tree_view.focus())
            rowid_selection = key_selection["values"][0]
            mod_con = sqlite3.connect("keywords_db.db")
            mod_cur = mod_con.cursor()
            mod_cur.execute("SELECT * "
                            "FROM keywords "
                            f"WHERE rowid={rowid_selection}")
            notes_selection = mod_cur.fetchall()

            # ***** Top Level: "Modify keyword" window attributes
            mod_key_window = Toplevel()
            mod_key_window.title(f"Modifying '{''.join([item[1] for item in notes_selection])}'")
            mod_key_window.geometry("400x420")
            mod_key_window.resizable(False, False)
            mod_key_window.configure(padx=5, pady=5)

            # ***** New keyword window geometry
            mod_key_window.rowconfigure(0, weight=1)
            mod_key_window.rowconfigure(1, weight=1)
            mod_key_window.rowconfigure(2, weight=1)
            mod_key_window.columnconfigure(0, weight=1)

            # ***** Label Frame: add keyword frame contains keyword entry
            mod_key_frame = LabelFrame(mod_key_window, text="Enter Keyword")
            mod_key_frame.grid(row=0, column=0, padx=3, pady=3, sticky="w")

            # ***** Add keyword label frame geometry
            mod_key_frame.rowconfigure(0, weight=1)
            mod_key_frame.columnconfigure(0, weight=1)

            # ***** Entry: add keyword entry
            mod_key_entry = Entry(mod_key_frame, width=28)
            mod_key_entry.grid(row=0, column=0)

            # ***** Label Frame: notes frame contains text box to ender new keyword notes
            mod_value_frame = LabelFrame(mod_key_window, text="Enter Notes")
            mod_value_frame.grid(row=1, column=0, padx=3, pady=3, sticky="nesw")

            # ***** Scrollbar: y-axis for notes box
            mod_value_scrollbar_y = Scrollbar(mod_value_frame, orient=VERTICAL)
            mod_value_scrollbar_y.pack(fill=Y, side=RIGHT)

            # ***** Text: text box for notes entry
            mod_value_text = Text(mod_value_frame, height=20, highlightthickness=0, wrap="word",
                                  yscrollcommand=mod_value_scrollbar_y.set)
            mod_value_text.pack(fill=BOTH, expand=TRUE)

            # ***** Label Frame: commands frame containing buttons
            mod_commands_frame = LabelFrame(mod_key_window, text="Commands")
            mod_commands_frame.grid(row=2, column=0, padx=3, pady=3, sticky="nesw")

            # ***** Label Frame: commands frame geometry
            mod_commands_frame.rowconfigure(0, weight=1)
            mod_commands_frame.columnconfigure(0, weight=1)
            mod_commands_frame.columnconfigure(1, weight=1)

            # ***** Button: add or cancel buttons for add new form
            mod_key_btn = Button(mod_commands_frame, text="Add Keyword", width=13, command=mod_key)
            mod_key_btn.grid(row=0, column=0)
            cnl_mod_key_btn = Button(mod_commands_frame, text="Cancel", width=13, command=mod_key_window.destroy)
            cnl_mod_key_btn.grid(row=0, column=1)

            mod_con.commit()
            mod_con.close()
            populate_mod_entries()
            # ***** Deactivates main window while top level is open
            mod_key_window.grab_set()


# ***** Function: deletes selected keyword from SQL database
def delete():
    if not tree_view.selection():
        messagebox.showerror(title="Error", message="Please enter the new keyword.")
    else:
        key_selection = tree_view.item(tree_view.focus())
        key_name = key_selection["values"][1]
        confirm = messagebox.askquestion(title="Attention", message=f"Are you sure you want to delete {key_name}?")
        if confirm == "yes":
            selected = (tree_view.item(tree_view.focus()))
            rowid = selected["values"]
            con = sqlite3.connect("keywords_db.db")
            cur = con.cursor()
            cur.execute(f"DELETE FROM keywords WHERE rowid={rowid[0]}")
            con.commit()
            con.close()
            populate_tree_view()
            notes_text.delete(1.0, END)


# ***** Main window attributes
root = Tk()
root.title("Python Keyword Learning Tool")
root.geometry("700x420")
root.resizable(False, False)
root.configure(padx=5, pady=5)

# ***** Main window geometry
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

# ***** Frame: contains tree view
tree_view_frame = LabelFrame(root, text="Keyword")
tree_view_frame.grid(row=0, column=0, padx=3, pady=3, sticky="nesw")

# ***** Scrollbar: y-axis for tree view
tree_view_scrollbar_y = Scrollbar(tree_view_frame, orient=VERTICAL)
tree_view_scrollbar_y.pack(fill=Y, side=RIGHT)

# ***** Tree View: initial set up of columns
tree_view = Treeview(tree_view_frame, yscrollcommand=tree_view_scrollbar_y.set,
                     columns=("entry_id", "keyword", "value"),
                     displaycolumns="keyword", show="headings", height=10)
tree_view.pack(fill=BOTH, expand=TRUE)

# ***** Tree View: set up of column displayed headings
tree_view.heading("keyword", text="Keyword")

# ***** Tree View: column attributes
tree_view.column("keyword", width=50)

# ***** Label Frame: contains notes text box
notes_frame = LabelFrame(root, text="Notes")
notes_frame.grid(row=0, column=1, padx=3, pady=3, sticky="nesw")

# ***** Scrollbar: y-axis for notes text box
notes_scrollbar_y = Scrollbar(notes_frame, orient=VERTICAL)
notes_scrollbar_y.pack(fill=Y, side=RIGHT)

# ***** Text: text box for notes display
notes_text = Text(notes_frame, highlightthickness=0, width=50, wrap="word",
                  yscrollcommand=notes_scrollbar_y.set)
notes_text.pack(fill=BOTH, expand=TRUE)

# ***** Label Frame: commands frame that contains buttons
commands_frame = LabelFrame(root, text="Commands")
commands_frame.grid(row=1, column=0, padx=3, pady=3, columnspan=2, sticky="nesw")

# ***** Label Frame: commands frame geometry
commands_frame.rowconfigure(0, weight=1)
commands_frame.columnconfigure(0, weight=1)
commands_frame.columnconfigure(1, weight=1)
commands_frame.columnconfigure(2, weight=1)

# ***** Button: add, modify or cancel buttons
add_btn = Button(commands_frame, text="Add Keyword", width=13, command=Add)
add_btn.grid(row=0, column=0)
mod_btn = Button(commands_frame, text="Modify Keyword", width=13, command=Mod)
mod_btn.grid(row=0, column=1)
del_btn = Button(commands_frame, text="Delete Keyword", width=13, command=delete)
del_btn.grid(row=0, column=2)


# ***** Function: populates notes text box with relevant information when keyword is clicked
def populate_notes(event):
    try:
        key_selection = tree_view.item(tree_view.focus())
        rowid_selection = key_selection["values"][0]
        notes_text.delete(1.0, END)
        con = sqlite3.connect("keywords_db.db")
        cur = con.cursor()
        cur.execute("SELECT * "
                    "FROM keywords "
                    f"WHERE rowid={rowid_selection}")
        notes_selection = cur.fetchall()
        notes_list_to_string = "".join([item[2] for item in notes_selection])
        notes_text.insert(1.0, notes_list_to_string)
        con.commit()
        con.close()
    except IndexError:
        print("Treeview item not selected.")


# ***** Event: calls above function when user clicks and then releases on selected keyword
tree_view.bind("<ButtonRelease-1>", populate_notes)


# ***** Function: populates tree view
def populate_tree_view():
    tree_view.delete(*tree_view.get_children())
    con = sqlite3.connect("keywords_db.db")
    cur = con.cursor()
    cur.execute("SELECT entry_id, key, value FROM keywords")
    records = cur.fetchall()
    for record in records:
        tree_view.insert("", 0, values=record)
    notes_text.delete(1.0, END)
    con.commit()
    con.close()


initialise_database()
populate_tree_view()
root.mainloop()
