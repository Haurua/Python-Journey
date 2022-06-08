# ***** Imported modules
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import sqlite3
import os.path
import wikipedia

# ***** Main window attributes
root = Tk()
root.title("Virtual Dossete Box")
root.geometry("1100x500")
root.resizable(False, False)
root.configure(padx=5, pady=5)

# ***** Main window geometry
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)


# ***** Function: populates tree view % notes widget with SQL database
def populate_tree_view():
    tree_view.delete(*tree_view.get_children())
    con = sqlite3.connect("med_db.db")
    cur = con.cursor()
    cur.execute("SELECT entry_id, med, weight, morn, noon, eve FROM medication")
    records = cur.fetchall()
    for record in records:
        tree_view.insert("", 0, values=record)
    notes_text.delete(1.0, END)
    con.commit()
    con.close()


# ***** Class: contains "Add Medication" top-level window
class AddMedication:
    def __init__(self):
        # ***** Method: allows user to search wikipedia for medication summary
        def wiki_notes():
            if add_med_entry.get() == "":
                messagebox.showerror(title="Error", message="Please enter a medication before searching Wiki.")
            else:
                confirm = messagebox.askquestion(title="Attention",
                                                 message="Searching Wiki will delete current notes, proceed?")
                if confirm == "yes":
                    try:
                        add_notes_text.delete(1.0, END)
                        add_notes_text.insert(1.0, wikipedia.summary(add_med_entry.get(), "4"))
                    except wikipedia.PageError:
                        messagebox.showerror(title="Error", message="Wiki not found, please check medication spelling.")

        # ***** Method: Adds new medication to database with user input
        def add_medication():
            # ***** Message Box: error message if medication name is not entered
            if add_med_entry.get() == "":
                messagebox.showerror(title="Error", message="Please enter the medication name.")
            elif add_med_entry.get() != "":
                # ***** SQL Query: adds new medication to database with the user input
                con = sqlite3.connect("med_db.db")
                cur = con.cursor()
                cur.execute(
                    """INSERT INTO medication (med, weight, morn, noon, eve, notes) VALUES (?, ?, ?, ?, ?, ?)""",
                    (add_med_entry.get(),
                     add_weight_entry.get(),
                     add_morn_chk.get(),
                     add_noon_chk.get(),
                     add_eve_chk.get(),
                     add_notes_text.get(1.0, "end-1c")
                     ))
                con.commit()
                con.close()
                # ***** Message Box: success message when medication is entered in to the SQL database
                success_msg = f"{add_med_entry.get()} has been added to the medication list."
                messagebox.showerror(title="Success", message=success_msg)
                # ***** Closes top level window after medication is added
                add_med_window.destroy()
                populate_tree_view()

        # ***** Top Level: "Add Medication" window attributes
        add_med_window = Toplevel()
        add_med_window.title("Add Medication Form")
        add_med_window.geometry("700x400")
        add_med_window.configure(padx=5, pady=5)
        add_med_window.resizable(False, False)

        # ***** "Add Medication" geometry
        add_med_window.rowconfigure(0, weight=1)
        add_med_window.rowconfigure(1, weight=1)
        add_med_window.columnconfigure(0, weight=1)
        add_med_window.columnconfigure(1, weight=1)

        # ***** Label Frame: add form frame contains form to ender new medication details
        add_form_frame = LabelFrame(add_med_window, text="Enter Details")
        add_form_frame.grid(row=0, column=0, padx=3, pady=3, sticky="nesw")

        # ***** Add form label frame geometry
        add_form_frame.rowconfigure(0, weight=1)
        add_form_frame.rowconfigure(1, weight=1)
        add_form_frame.rowconfigure(2, weight=1)
        add_form_frame.rowconfigure(3, weight=1)
        add_form_frame.rowconfigure(4, weight=1)
        add_form_frame.columnconfigure(0, weight=1)
        add_form_frame.columnconfigure(1, weight=1)

        # ***** Label: add form labels
        add_med_label = Label(add_form_frame, text="Medication:")
        add_med_label.grid(row=0, column=0)
        add_med_label = Label(add_form_frame, text="Weight (mg):")
        add_med_label.grid(row=1, column=0)
        add_med_label = Label(add_form_frame, text="Morning:")
        add_med_label.grid(row=2, column=0)
        add_med_label = Label(add_form_frame, text="Noon:")
        add_med_label.grid(row=3, column=0)
        add_med_label = Label(add_form_frame, text="Evening:")
        add_med_label.grid(row=4, column=0)

        # ***** Entry: add form entries
        add_med_entry = Entry(add_form_frame, width=28)
        add_med_entry.grid(row=0, column=1, sticky="w")
        add_weight_entry = Entry(add_form_frame, width=28)
        add_weight_entry.grid(row=1, column=1, sticky="w")

        # ***** Checkbutton: add form check buttons
        add_morn_chk = StringVar(value="No")
        Checkbutton(add_form_frame, variable=add_morn_chk, onvalue="Yes", offvalue="No").grid(row=2, column=1,
                                                                                              sticky="w")
        add_noon_chk = StringVar(value="No")
        Checkbutton(add_form_frame, variable=add_noon_chk, onvalue="Yes", offvalue="No").grid(row=3, column=1,
                                                                                              sticky="w")
        add_eve_chk = StringVar(value="No")
        Checkbutton(add_form_frame, variable=add_eve_chk, onvalue="Yes", offvalue="No").grid(row=4, column=1,
                                                                                             sticky="w")

        # ***** Label Frame: notes frame contains text box to ender new medication notes
        add_notes_frame = LabelFrame(add_med_window, text="Enter Notes")
        add_notes_frame.grid(row=0, column=1, padx=3, pady=3, sticky="nesw")

        # ***** Scrollbar: y-axis for notes box
        add_notes_scrollbar_y = Scrollbar(add_notes_frame, orient=VERTICAL)
        add_notes_scrollbar_y.pack(fill=Y, side=RIGHT)

        # ***** Text: text box for notes entry
        add_notes_text = Text(add_notes_frame, width=30, height=20, highlightthickness=0, wrap="word",
                              yscrollcommand=add_notes_scrollbar_y.set)
        add_notes_text.pack(fill=BOTH, expand=TRUE)

        # ***** Label Frame: commands frame containing buttons
        add_commands_frame = LabelFrame(add_med_window, text="Commands")
        add_commands_frame.grid(row=1, column=0, padx=3, pady=3, columnspan=2, sticky="nesw")

        # ***** Label Frame: commands frame geometry
        add_commands_frame.rowconfigure(0, weight=1)
        add_commands_frame.columnconfigure(0, weight=1)
        add_commands_frame.columnconfigure(1, weight=1)
        add_commands_frame.columnconfigure(2, weight=1)

        # ***** Button: add or cancel buttons for add new form
        add_add_med_btn = Button(add_commands_frame, text="Add Medication", width=13, command=add_medication)
        add_add_med_btn.grid(row=0, column=0)
        wiki_add_med_btn = Button(add_commands_frame, text="Search Wiki", width=13, command=wiki_notes)
        wiki_add_med_btn.grid(row=0, column=1)
        cnl_add_med_btn = Button(add_commands_frame, text="Cancel", width=13, command=add_med_window.destroy)
        cnl_add_med_btn.grid(row=0, column=2)

        # ***** Deactivates main window while top level is open
        add_med_window.grab_set()


# ***** Class: contains "Modify Medication" top-level window
class ModifyMedication:
    def __init__(self):
        # ***** Message Box: error message if there is no selection when modification is attempted
        if not tree_view.selection():
            messagebox.showerror(title="Attention", message="Please select a medication to modify.")
        else:
            # ***** Method: SQL query that populates modify window directly with SQL database information
            def populate_mod_entries():
                mod_med_selection = tree_view.item(tree_view.focus())
                mod_rowid_selection = mod_med_selection["values"][0]
                con = sqlite3.connect("med_db.db")
                cur = con.cursor()
                cur.execute("SELECT * "
                            "FROM medication "
                            f"WHERE rowid={mod_rowid_selection}")
                results = cur.fetchall()
                # ***** List Comprehension: finds elements inside tuple that is inside list then converts to string
                mod_med_entry.insert(0, "".join([item[1] for item in results]))
                mod_weight_entry.insert(0, "".join([item[2] for item in results]))
                mod_notes.insert(1.0, "".join([item[6] for item in results]))
                con.commit()
                con.close()

            # ***** Method: modifies selected medication and updates SQL database
            def modify_medication():
                # ***** Message Box: error message if there is no selection when modification is attempted
                if mod_med_entry.get() == "":
                    messagebox.showerror(title="Error", message="Please enter the medication name.")
                elif mod_med_entry.get() != "":
                    mod_med_selection = tree_view.item(tree_view.focus())
                    mod_rowid_selection = mod_med_selection["values"][0]
                    con = sqlite3.connect("med_db.db")
                    cur = con.cursor()
                    cur.execute("SELECT * "
                                "FROM medication "
                                f"WHERE rowid={mod_rowid_selection}")
                    cur.execute("UPDATE medication "
                                "SET "
                                f"med='{mod_med_entry.get()}',"
                                f"weight='{mod_weight_entry.get()}',"
                                f"morn='{mod_morn_chk.get()}',"
                                f"noon='{mod_noon_chk.get()}',"
                                f"eve='{mod_eve_chk.get()}',"
                                f"notes='{mod_notes.get(1.0, 'end-1c')}' WHERE rowid={mod_rowid_selection}")
                    con.commit()
                    con.close()
                    # ***** Message Box: success message when medication is entered in to the SQL database
                    success_msg = f"{mod_med_entry.get()} has been modified."
                    messagebox.showerror(title="Success", message=success_msg)
                    # ***** Closes top level window after medication is added
                    mod_med_window.destroy()
                    populate_tree_view()

            # ***** Method: allows user to search wikipedia for medication summary
            def wiki_notes():
                if mod_med_entry.get() == "":
                    messagebox.showerror(title="Error", message="Please enter a medication before searching Wiki.")
                else:
                    confirm = messagebox.askquestion(title="Attention",
                                                     message="Searching Wiki will delete current notes, proceed?")
                    if confirm == "yes":
                        try:
                            mod_notes.delete(1.0, END)
                            mod_notes.insert(1.0, wikipedia.summary(mod_med_entry.get(), "4"))
                        except wikipedia.PageError:
                            messagebox.showerror(title="Error",
                                                 message="Wiki not found, please check medication spelling.")

            # ***** SQL query to populate top level window with selected medication to modify
            med_selection = tree_view.item(tree_view.focus())
            rowid_selection = med_selection["values"][0]
            mod_con = sqlite3.connect("med_db.db")
            mod_cur = mod_con.cursor()
            mod_cur.execute("SELECT * "
                            "FROM medication "
                            f"WHERE rowid={rowid_selection}")
            notes_selection = mod_cur.fetchall()

            # ***** Top Level: "Modify Medication" window attributes
            mod_med_window = Toplevel()
            mod_med_window.title(f"Modifying {''.join([item[1] for item in notes_selection])}")
            mod_med_window.geometry("700x400")
            mod_med_window.resizable(False, False)
            mod_med_window.configure(padx=5, pady=5)

            # ***** "Modify Medication" geometry
            mod_med_window.rowconfigure(0, weight=1)
            mod_med_window.rowconfigure(1, weight=1)
            mod_med_window.columnconfigure(0, weight=1)
            mod_med_window.columnconfigure(1, weight=1)

            # ***** Label Frame: modify form frame contains form to ender modified medication details
            mod_form_frame = LabelFrame(mod_med_window, text="Enter Details")
            mod_form_frame.grid(row=0, column=0, padx=3, pady=3, sticky="nesw")

            # ***** Modify form label frame geometry
            mod_form_frame.rowconfigure(0, weight=1)
            mod_form_frame.rowconfigure(1, weight=1)
            mod_form_frame.rowconfigure(2, weight=1)
            mod_form_frame.rowconfigure(3, weight=1)
            mod_form_frame.rowconfigure(4, weight=1)
            mod_form_frame.columnconfigure(0, weight=1)
            mod_form_frame.columnconfigure(1, weight=1)

            # ***** Label: modify form labels
            mod_med_label = Label(mod_form_frame, text="Medication:")
            mod_med_label.grid(row=0, column=0)
            mod_med_label = Label(mod_form_frame, text="Weight (mg):")
            mod_med_label.grid(row=1, column=0)
            mod_med_label = Label(mod_form_frame, text="Morning:")
            mod_med_label.grid(row=2, column=0)
            mod_med_label = Label(mod_form_frame, text="Noon:")
            mod_med_label.grid(row=3, column=0)
            mod_med_label = Label(mod_form_frame, text="Evening:")
            mod_med_label.grid(row=4, column=0)

            # ***** Entry: modify form entries
            mod_med_entry = Entry(mod_form_frame, width=28)
            mod_med_entry.grid(row=0, column=1, sticky="w")
            mod_weight_entry = Entry(mod_form_frame, width=28)
            mod_weight_entry.grid(row=1, column=1, sticky="w")

            # ***** Checkbutton: modify form check buttons, state is set with above SQL query
            mod_morn = "".join([item[3] for item in notes_selection])
            mod_morn_chk = StringVar(value=f"{mod_morn}")
            Checkbutton(mod_form_frame, variable=mod_morn_chk, onvalue="Yes", offvalue="No").grid(row=2, column=1,
                                                                                                  sticky="w")
            mod_noon = "".join([item[4] for item in notes_selection])
            mod_noon_chk = StringVar(value=f"{mod_noon}")
            Checkbutton(mod_form_frame, variable=mod_noon_chk, onvalue="Yes", offvalue="No").grid(row=3, column=1,
                                                                                                  sticky="w")
            mod_eve = "".join([item[5] for item in notes_selection])
            mod_eve_chk = StringVar(value=f"{mod_eve}")
            Checkbutton(mod_form_frame, variable=mod_eve_chk, onvalue="Yes", offvalue="No").grid(row=4, column=1,
                                                                                                 sticky="w")

            # ***** Label Frame: notes frame contains text box to ender modified medication notes
            mod_notes_frame = LabelFrame(mod_med_window, text="Enter Notes")
            mod_notes_frame.grid(row=0, column=1, padx=3, pady=3, sticky="nesw")

            # ***** Scrollbar: y-axis for notes box
            mod_notes_scrollbar_y = Scrollbar(mod_notes_frame, orient=VERTICAL)
            mod_notes_scrollbar_y.pack(fill=Y, side=RIGHT)

            # ***** Text: text box for notes entry
            mod_notes = Text(mod_notes_frame, width=30, height=20, highlightthickness=0, wrap="word",
                             yscrollcommand=mod_notes_scrollbar_y.set)
            mod_notes.pack(fill=BOTH, expand=TRUE)

            # ***** Label Frame: commands frame containing buttons
            mod_commands_frame = LabelFrame(mod_med_window, text="Commands")
            mod_commands_frame.grid(row=1, column=0, padx=3, pady=3, columnspan=2, sticky="nesw")

            # ***** Label Frame: commands frame geometry
            mod_commands_frame.rowconfigure(0, weight=1)
            mod_commands_frame.columnconfigure(0, weight=1)
            mod_commands_frame.columnconfigure(1, weight=1)
            mod_commands_frame.columnconfigure(2, weight=1)

            # ***** Button: modify or cancel buttons for modification new form
            mod_med_btn = Button(mod_commands_frame, text="Modify Medication", width=13, command=modify_medication)
            mod_med_btn.grid(row=0, column=0)
            wiki_add_med_btn = Button(mod_commands_frame, text="Search Wiki", width=13, command=wiki_notes)
            wiki_add_med_btn.grid(row=0, column=1)
            cnl_mod_med_btn = Button(mod_commands_frame, text="Cancel", width=13, command=mod_med_window.destroy)
            cnl_mod_med_btn.grid(row=0, column=2)

            mod_con.commit()
            mod_con.close()
            populate_mod_entries()
            # ***** Deactivates main window while top level is open
            mod_med_window.grab_set()


# ***** Function: deletes selected medication from SQL database
def delete_medication():
    if not tree_view.selection():
        messagebox.showerror(title="Error", message="Please select a medication to delete.")
    else:
        med_selection = tree_view.item(tree_view.focus())
        med_name = med_selection["values"][1]
        confirm = messagebox.askquestion(title="Attention", message=f"Are you sure you want to delete {med_name}?")
        if confirm == "yes":
            selected = (tree_view.item(tree_view.focus()))
            rowid = selected["values"]
            con = sqlite3.connect("med_db.db")
            cur = con.cursor()
            cur.execute(f"DELETE FROM medication WHERE rowid={rowid[0]}")
            con.commit()
            con.close()
            populate_tree_view()
            notes_text.delete(1.0, END)


# ***** Tree View: main attributes
tree_view_frame = LabelFrame(root, text="Medication List")
tree_view_frame.grid(row=0, column=0, padx=3, pady=3, sticky="nesw")

# ***** Scrollbar: y-axis for tree view
tree_view_scrollbar_y = Scrollbar(tree_view_frame, orient=VERTICAL)
tree_view_scrollbar_y.pack(fill=Y, side=RIGHT)

# ***** Tree View: initial set up of columns
tree_view = Treeview(tree_view_frame, yscrollcommand=tree_view_scrollbar_y.set,
                     columns=("entry_id", "med", "weight", "morn", "noon", "eve"),
                     displaycolumns=("med", "weight", "morn", "noon", "eve"), show="headings", height=20)
tree_view.pack(fill=BOTH, expand=TRUE)

# ***** Tree View: set up of column displayed headings
tree_view.heading("med", text="Medication")
tree_view.heading("weight", text="Weight (mg)")
tree_view.heading("morn", text="Morning")
tree_view.heading("noon", text="Noon")
tree_view.heading("eve", text="Evening")

# ***** Tree View: column attributes
tree_view.column("med", width=230, anchor=CENTER)
tree_view.column("weight", width=25, anchor=CENTER)
tree_view.column("morn", width=5, anchor=CENTER)
tree_view.column("noon", width=5, anchor=CENTER)
tree_view.column("eve", width=5, anchor=CENTER)


# ***** Function: populates notes text box with relevant information when medication is clicked
def populate_notes(event):
    try:
        med_selection = tree_view.item(tree_view.focus())
        rowid_selection = med_selection["values"][0]
        notes_text.delete(1.0, END)
        con = sqlite3.connect("med_db.db")
        cur = con.cursor()
        cur.execute("SELECT * "
                    "FROM medication "
                    f"WHERE rowid={rowid_selection}")
        notes_selection = cur.fetchall()
        notes_list_to_string = "".join([item[6] for item in notes_selection])
        notes_text.insert(1.0, notes_list_to_string)
        con.commit()
        con.close()
    except IndexError:
        print("Treeview item not selected.")


# ***** Event: calls above function when user clicks and then releases on selected medication
tree_view.bind("<ButtonRelease-1>", populate_notes)

# ***** Label Frame: contains notes text box
notes_frame = LabelFrame(root, text="Notes")
notes_frame.grid(row=0, column=1, padx=3, pady=3, sticky="nesw")

# ***** Scrollbar: y-axis for notes text box
notes_scrollbar_y = Scrollbar(notes_frame, orient=VERTICAL)
notes_scrollbar_y.pack(fill=Y, side=RIGHT)

# ***** Text: text box for notes display
notes_text = Text(notes_frame, highlightthickness=0, width=1, wrap="word",
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
add_btn = Button(commands_frame, text="Add Medication", width=13, command=AddMedication)
add_btn.grid(row=0, column=0)
mod_btn = Button(commands_frame, text="Modify Medication", width=13, command=ModifyMedication)
mod_btn.grid(row=0, column=1)
del_btn = Button(commands_frame, text="Delete Medication", width=13, command=delete_medication)
del_btn.grid(row=0, column=2)


# ***** Function: creates SQL database if one does not already exist
def initialise_database():
    if os.path.isfile("med_db.db"):
        print("Database already exists.")
    else:
        con = sqlite3.connect("med_db.db")
        cur = con.cursor()
        cur.execute("""CREATE TABLE medication (
        entry_id INTEGER PRIMARY KEY,
        med TEXT,
        weight TEXT,
        morn TEXT,
        noon TEXT,
        eve TEXT,
        notes TEXT
        )""")
        con.commit()
        con.close()
        print("New database created.")


# ***** Calls functions to initialise application
initialise_database()
populate_tree_view()
root.mainloop()
