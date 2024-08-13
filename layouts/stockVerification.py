from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector

def create_stock_verification_window(root):
    stock_verification_window = Toplevel(root)
    stock_verification_window.geometry('600x300')
    stock_verification_window.title('Stock Verification')
    stock_verification_window.resizable(False, False)

    bgColor = '#E7E8D8'
    fgColor = 'black'
    fontColor = 'black'
    btnColor = '#BC9F8B'
    lblFontSize = 12
    primaryFont = 'century gothic'
    def create_connection():
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="spare_inventory_db"
        )


    def fetch_stock_details():
        selected_spare = spare_name_var.get()
        spare_id = next((id for id, name, spec in spare_names if f"{name} {spec}" == selected_spare), None)

        if not spare_id:
            messagebox.showerror("Error", "Invalid Spare Name")
            location_var.set("N/A")
            stock_var.set("N/A")
            return

        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT location, current_stock
            FROM spare_master
            JOIN spare_stock ON spare_master.spare_id = spare_stock.spare_id
            WHERE spare_master.spare_id = %s
        """, (spare_id,))
        result = cursor.fetchone()
        connection.close()

        if result:
            location, current_stock = result
            location_var.set(location)
            stock_var.set(current_stock)
        else:
            location_var.set("N/A")
            stock_var.set("N/A")


    def submit_action():
        selected_spare = spare_name_var.get()
        if selected_spare:
            fetch_stock_details()
        else:
            messagebox.showerror("Error", "Please select a spare name.")
            location_var.set("N/A")
            stock_var.set("N/A")


    def cancel_action():
        # Clear all entries and reset the form
        spare_name_var.set('')
        location_var.set('')
        stock_var.set('')
        stock_verification_window.destroy()

    # GUI Setup


    frame = Frame(stock_verification_window, width=610, height=640, bg=bgColor, bd=8)
    frame.place(x=0, y=0)

    heading = Label(frame, text='Stock Verification', fg=fgColor, bg=bgColor, font=(primaryFont, 20, 'bold', 'underline'))
    heading.place(x=200, y=3)

    # Spare Name Selection
    spare_name_lbl = Label(frame, text='Spare Name:', fg=fgColor, bg=bgColor, font=(primaryFont, lblFontSize, 'normal'))
    spare_name_lbl.place(x=10, y=70)

    spare_name_var = StringVar()
    spare_name_combo = ttk.Combobox(frame, textvariable=spare_name_var, width=47)
    spare_name_combo.place(x=200, y=75)

    # Fetch spare names and specs from the database
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT spare_id, item_name, specification FROM spare_master")
    spare_names = cursor.fetchall()
    connection.close()

    spare_name_combo['values'] = [f"{name} {spec}" for id, name, spec in spare_names]

    # Display Location
    location_lbl = Label(frame, text='Location:', fg=fgColor, bg=bgColor, font=(primaryFont, lblFontSize, 'normal'))
    location_lbl.place(x=10, y=110)

    location_var = StringVar()
    location_entry = Entry(frame, textvariable=location_var, width=50, borderwidth=2, state='readonly')
    location_entry.place(x=200, y=115)

    # Display Current Stock
    stock_lbl = Label(frame, text='Current Stock:', fg=fgColor, bg=bgColor, font=(primaryFont, lblFontSize, 'normal'))
    stock_lbl.place(x=10, y=150)

    stock_var = StringVar()
    stock_entry = Entry(frame, textvariable=stock_var, width=50, borderwidth=2, state='readonly')
    stock_entry.place(x=200, y=155)

    # Submit and Cancel Buttons
    submit_btn = Button(frame, text='Submit', bg=btnColor, width=14, font=(primaryFont, lblFontSize, 'normal'),
                        command=submit_action)
    submit_btn.place(x=150, y=200)

    cancel_btn = Button(frame, text='Cancel', bg=btnColor, width=14, font=(primaryFont, lblFontSize, 'normal'),
                        command=cancel_action)
    cancel_btn.place(x=310, y=200)

    stock_verification_window.mainloop()
