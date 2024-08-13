from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from datetime import datetime

# Initialize main window
def create_spare_inward_window(root):
    spareInwardWindow = Toplevel(root)
    spareInwardWindow.geometry('600x300')
    bgColor = '#E7E8D8'
    fgColor = 'black'
    btnColor = '#BC9F8B'
    lblFontSize = 12
    spareInwardWindow.title('Spare Inward Entry')
    spareInwardWindow.resizable(False, False)
    primaryFont = 'century gothic'




    # Database connection
    def create_connection():
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="spare_inventory_db"
        )


    def get_spare_names():
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT spare_id, item_name, specification FROM spare_master")
        spare_names = cursor.fetchall()
        connection.close()
        return spare_names


    # Define callback functions
    def clear_entries():
        for entry in entries:
            entry.delete(0, END)
        spare_name_var.set('')
        date_var.set(datetime.now().strftime('%Y-%m-%d'))


    def submit():
        spare_name = spare_name_var.get()
        quantity = entries[0].get()
        date = date_var.get()

        if not spare_name or not quantity or not date:
            messagebox.showerror("Error", "Please fill all the fields")
            return

        try:
            quantity = int(quantity)
        except ValueError:
            messagebox.showerror("Error", "Quantity must be an integer")
            return

        spare_id = next((id for id, name, spec in spare_names if f"{name} {spec}" == spare_name), None)
        if not spare_id:
            messagebox.showerror("Error", "Invalid Spare Name")
            return

        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO spare_inward (spare_id, quantity, date) VALUES (%s, %s, %s)",
            (spare_id, quantity, date)
        )
        connection.commit()
        connection.close()

        messagebox.showinfo("Success", "Spare inward entry added successfully")
        clear_entries()


    def cancel():
        spareInwardWindow.destroy()


    # Load spare names into combobox
    spare_names = get_spare_names()
    spare_name_combobox_values = [f"{name} {spec}" for _, name, spec in spare_names]

    # Layout Section
    frame = Frame(spareInwardWindow, width=600, height=400, bg=bgColor, bd=8)
    frame.place(x=0, y=0)

    heading = Label(frame, text='Spare Inward Entry', fg=fgColor, bg=bgColor, font=(primaryFont, 20, 'bold', 'underline'))
    heading.place(x=150, y=3)

    # Labels and Entries
    labels = ['Spare Name:', 'Quantity:', 'Date:']
    entries = []
    y_positions = [70, 110, 150]

    # Spare Name Dropdown
    spare_name_var = StringVar()
    spare_name_combobox = ttk.Combobox(frame, textvariable=spare_name_var, width=47)
    spare_name_combobox['values'] = spare_name_combobox_values
    spare_name_combobox.place(x=200, y=75)

    for i, text in enumerate(labels):
        label = Label(frame, text=text, fg=fgColor, bg=bgColor, font=(primaryFont, lblFontSize, 'normal'))
        label.place(x=10, y=y_positions[i])
        if i == 1:  # Entry widget for Quantity
            entry = Entry(frame, width=50, borderwidth=2)
            entry.place(x=200, y=y_positions[i] + 5)
            entries.append(entry)
        elif i == 2:  # Date Entry
            date_var = StringVar()
            date_entry = Entry(frame, textvariable=date_var, width=50, borderwidth=2)
            date_var.set(datetime.now().strftime('%Y-%m-%d'))  # Set current date
            date_entry.place(x=200, y=y_positions[i] + 5)
            entries.append(date_entry)

    # Buttons
    submitBtn = Button(frame, text='Submit', bg=btnColor, width=14, font=(primaryFont, lblFontSize, 'normal'),
                       command=submit)
    submitBtn.place(x=150, y=200)

    cancelBtn = Button(frame, text='Cancel', bg=btnColor, width=14, font=(primaryFont, lblFontSize, 'normal'),
                       command=cancel)
    cancelBtn.place(x=310, y=200)

    # Start main loop
    spareInwardWindow.mainloop()
