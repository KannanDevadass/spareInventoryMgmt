from tkinter import *
from tkinter import ttk
import mysql.connector
from tkinter import messagebox


# Initialize main window
def create_spare_entry_window(root):
    spareMasterWindow = Toplevel(root)
    spareMasterWindow.geometry('600x400')
    bgColor = '#E7E8D8'
    fgColor = 'black'
    btnColor = '#BC9F8B'
    lblFontSize = 12
    spareMasterWindow.title('Spare Entry')
    spareMasterWindow.resizable(False, False)
    primaryFont = 'century gothic'

    # Database connection
    def create_connection():
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="spare_inventory_db"
        )

    # Define callback functions

    def clear_entries():
        for entry in entries:
            entry.delete(0, END)
        location_var.set('')
        uom_var.set('')

    def submit():
        spare_name = entries[0].get()
        specification = entries[1].get()
        location = location_var.get()
        uom = uom_var.get()
        reorder_level = entries[2].get()


        if not spare_name or not specification or not location or not uom or not reorder_level:
            messagebox.showerror("Error", "Please fill all the fields")
            return

        try:
            reorder_level = int(reorder_level)
        except ValueError:
            messagebox.showerror("Error", "Re-Order Level must be integer")
            return

        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO spare_master (item_name, specification, location, uom, reorder_level) VALUES (%s, %s, %s, %s, %s)",
            (spare_name, specification, location, uom, reorder_level)
        )
        connection.commit()
        connection.close()

        messagebox.showinfo("Success", "Item added successfully")
        clear_entries()

    def cancel():
        spareMasterWindow.destroy()

    # Generate locations
    locations = [f"R{rack}-Bin{bin}" for rack in range(1, 6) for bin in range(1, 11)]

    # Layout Section
    frame = Frame(spareMasterWindow, width=600, height=400, bg=bgColor, bd=8)
    frame.place(x=0, y=0)

    heading = Label(frame, text='Spare Entry', fg=fgColor, bg=bgColor, font=(primaryFont, 20, 'bold', 'underline'))
    heading.place(x=200, y=3)

    # Labels and Entries
    labels = ['Spare Name:', 'Specification:', 'Location:', 'UOM:', 'Re-Order Level:']
    entries = []
    y_positions = [70, 110, 150, 190, 230]

    for i, text in enumerate(labels):
        label = Label(frame, text=text, fg=fgColor, bg=bgColor, font=(primaryFont, lblFontSize, 'normal'))
        label.place(x=10, y=y_positions[i])
        if i in [0, 1, 4]:  # Entry widgets for Spare Name, Specification, Re-Order Level, and Re-Order Quantity
            entry = Entry(frame, width=50, borderwidth=2)
            entry.place(x=200, y=y_positions[i] + 5)
            entries.append(entry)
        elif i == 2:  # Combobox for Location
            location_var = StringVar()
            location_combobox = ttk.Combobox(frame, textvariable=location_var, width=47)
            location_combobox['values'] = locations
            location_combobox.place(x=200, y=y_positions[i] + 5)
        elif i == 3:  # Combobox for UOM
            uom_var = StringVar()
            uom_combobox = ttk.Combobox(frame, textvariable=uom_var, width=47)
            uom_combobox['values'] = ('Piece', 'Box', 'Kg', 'Litre')  # Example UOMs
            uom_combobox.place(x=200, y=y_positions[i] + 5)


    # Buttons
    submitBtn = Button(frame, text='Submit', bg=btnColor, width=14, font=(primaryFont, lblFontSize, 'normal'),
                       command=submit)
    submitBtn.place(x=150, y=315)

    cancelBtn = Button(frame, text='Cancel', bg=btnColor, width=14, font=(primaryFont, lblFontSize, 'normal'),
                       command=cancel)
    cancelBtn.place(x=310, y=315)

    # Start main loop
    spareMasterWindow.mainloop()
