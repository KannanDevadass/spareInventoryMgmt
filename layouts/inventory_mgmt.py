from tkinter import *
from datetime import datetime
from tkinter import ttk
import mysql.connector
from tkinter import messagebox

# Global Constants
BG_COLOR = '#E7E8D8'
FG_COLOR = 'black'
BTN_COLOR = '#BC9F8B'
FONT_SIZE = 14
PRIMARY_FONT = 'century gothic'
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'database': 'spare_inventory_db'
}


# Utility Functions
def create_connection():
    return mysql.connector.connect(**DB_CONFIG)


def fetch_data(query, param=None):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute(query, param or ())
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

def execute_query(query, params=None):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(query, params or ())
        connection.commit()  # Commit changes to the database
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        connection.rollback()  # Rollback in case of error
    finally:
        cursor.close()
        connection.close()

def clear_entries(entries, comboboxes=None):
    for entry in entries:
        entry.delete(0, END)
    if comboboxes:
        for combobox in comboboxes:
            combobox.set('')


def setup_frame(window, title):
    window.geometry('800x400')
    window.title(title)
    window.resizable(False, False)
    frame = Frame(window, width=800, height=600, bg=BG_COLOR, bd=8)
    frame.place(x=0, y=0)
    return frame


def setup_label(frame, text, x, y, font_size=FONT_SIZE):
    label = Label(frame, text=text, fg=FG_COLOR, bg=BG_COLOR, font=(PRIMARY_FONT, font_size, 'bold'))
    label.place(x=x, y=y)
    return label

def setup_combobox(frame, values, x, y):
    var = StringVar()
    combobox = ttk.Combobox(frame, textvariable=var, width=47)
    combobox['values'] = values
    combobox.place(x=x, y=y)
    # combobox.current(0)  # Set the default selection

    # def on_select(event):
    #     print("Combobox value selected:", var.get())
    #
    # combobox.bind("<<ComboboxSelected>>", on_select)
    # return combobox, var


def setup_entry(frame, x, y):
    entry = Entry(frame, width=50, borderwidth=2)
    entry.place(x=x, y=y)
    return entry


def setup_button(frame, text, x, y, command):
    button = Button(frame, text=text, bg=BTN_COLOR, width=23, font=(PRIMARY_FONT, FONT_SIZE, 'normal'), command=command)
    button.place(x=x, y=y)
    return button


# Main Application
def create_home_window():
    homeWindow = Tk()
    frame = setup_frame(homeWindow, 'Spare Inventory Management System')

    img = PhotoImage(file="logo.png")
    logo_label = Label(frame, image=img)
    logo_label.image = img
    logo_label.place(x=15, y=20)

    setup_label(frame, "Spare Inventory Management System", 120, 50, 24)

    setup_button(frame, "Spare Entry", 120, 150, open_spare_entry)
    setup_button(frame, "Spare Inward Entry", 400, 150, open_spare_inward)
    setup_button(frame, "Spare Consumption Entry", 120, 200, open_spare_consumption)
    setup_button(frame, "Stock Verification", 400, 200, open_stock_verification)

    homeWindow.mainloop()


# Spare Entry Window
def create_spare_entry_window():
    spareMasterWindow = Toplevel()
    frame = setup_frame(spareMasterWindow, 'Spare Entry')
    setup_label(frame, "Spare Entry", 250, 10, 24)


    # Labels and entries for Spare Entry Form
    labels = ['Spare Name:', 'Specification:', 'Location:', 'UOM:', 'Re-Order Level:']
    entries = []
    locations = [f"R{rack}-Bin{bin}" for rack in range(1, 6) for bin in range(1, 11)]


    # Create labels and input fields dynamically
    for i, label in enumerate(labels):
        setup_label(frame, label, 60, 70 + 40 * i)
        if i in [0, 1, 4]:
            entries.append(setup_entry(frame, 250, 75 + 40 * i))
        elif i == 2:
            location_var, location_combobox = setup_combobox(frame, locations, 250, 75 + 40 * i)

        elif i == 3:
            uom_combobox, uom_var = setup_combobox(frame, ['Piece', 'Box', 'Kg', 'Litre'], 250, 75 + 40 * i)

    # Function to handle form submission
    def submit():
        spare_name = entries[0].get()
        specification = entries[1].get()
        location = location_var.get()
        uom = uom_var.get()
        reorder_level = entries[2].get()

        print(spare_name, specification, location, uom, reorder_level)

        # Ensure all fields are filled
        if not all([spare_name, specification, location, uom, reorder_level]):
            messagebox.showerror("Error", "Please fill all the fields in the entry")
            return

        # Validate that the Re-Order Level is an integer
        try:
            reorder_level = int(reorder_level)
        except ValueError:
            messagebox.showerror("Error", "Re-Order Level must be an integer")
            return

        # Database operation
        try:
            query = (
                "INSERT INTO spare_master (item_name, specification, location, uom, reorder_level) VALUES (%s, %s, %s, %s, %s)")
            execute_query(query, (spare_name, specification, location, uom, reorder_level))

            # Success message and clear entries
            messagebox.showinfo("Success", "Item added successfully")
            clear_entries(entries, [location_combobox, uom_combobox])
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database error: {err}")


    # Buttons
    setup_button(frame, 'Submit', 40, 315, submit)
    setup_button(frame, 'Cancel', 320, 315, spareMasterWindow.destroy)

    spareMasterWindow.mainloop()



# Spare Inward Window
def create_spare_inward_window():
    spareInwardWindow = Toplevel()
    frame = setup_frame(spareInwardWindow, 'Spare Inward Entry')
    setup_label(frame, "Spare Inward", 250, 10, 24)

    spare_names = fetch_data("SELECT spare_id, item_name, specification FROM spare_master")
    spare_name_combobox, spare_name_var = setup_combobox(frame, [f"{name} {spec}" for _, name, spec in spare_names],
                                                         250, 75)
    setup_label(frame, 'Spare Name:', 60, 70)
    setup_label(frame, 'Quantity:', 60, 110)
    quantity_entry = setup_entry(frame, 250, 115)

    setup_label(frame, 'Date:', 60, 150)
    date_var = StringVar()
    date_entry = Entry(frame, textvariable=date_var, width=50, borderwidth=2)
    date_var.set(datetime.now().strftime('%Y-%m-%d'))
    date_entry.place(x=250, y=155)

    def submit():
        spare_name = spare_name_var.get()
        quantity = quantity_entry.get()
        date = date_var.get()

        if not all([spare_name, quantity, date]):
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

        query = "INSERT INTO spare_inward (spare_id, quantity, date) VALUES (%s, %s, %s)"
        execute_query(query, (spare_id, quantity, date))
        messagebox.showinfo("Success", "Spare inward entry added successfully")
        clear_entries([quantity_entry, date_entry], [spare_name_combobox])

    setup_button(frame, 'Submit', 30, 200, submit)
    setup_button(frame, 'Cancel', 310, 200, spareInwardWindow.destroy)

    spareInwardWindow.mainloop()


# Spare Consumption Window
def create_spare_consumption_window():
    spareConsumptionWindow = Toplevel()
    frame = setup_frame(spareConsumptionWindow, 'Spare Consumption Entry')
    setup_label(frame, "Spare Consumption", 250, 10, 24)

    spare_names = fetch_data("SELECT spare_id, item_name, specification FROM spare_master")
    spare_name_combobox, spare_name_var = setup_combobox(frame, [f"{name} {spec}" for _, name, spec in spare_names],
                                                         270, 75)

    setup_label(frame, 'Spare Name:', 60, 70)
    setup_label(frame, 'Quantity Consumed:', 60, 110)
    quantity_entry = setup_entry(frame, 270, 115)

    setup_label(frame, 'Date:', 60, 150)
    date_var = StringVar()
    date_entry = Entry(frame, textvariable=date_var, width=50, borderwidth=2)
    date_var.set(datetime.now().strftime('%Y-%m-%d'))
    date_entry.place(x=270, y=155)

    def submit():
        spare_name = spare_name_var.get()
        quantity = quantity_entry.get()
        date = date_var.get()

        if not all([spare_name, quantity, date]):
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

        query = "SELECT spare_stock.current_stock, spare_master.reorder_level FROM spare_stock JOIN spare_master ON spare_stock.spare_id = spare_master.spare_id WHERE spare_stock.spare_id = %s"
        stock_data = fetch_data(query, (spare_id,))

        if stock_data:
            current_stock, reorder_level = stock_data[0]
            if current_stock < quantity:
                messagebox.showerror("Error", f"Insufficient stock. Available: {current_stock}")
                return

            query = "INSERT INTO spare_consumption (spare_id, quantity, date) VALUES (%s, %s, %s)"
            execute_query(query, (spare_id, quantity, date))

            new_stock = current_stock - quantity
            query = "UPDATE spare_stock SET current_stock = %s WHERE spare_id = %s"
            fetch_data(query, (new_stock, spare_id))

            if new_stock < reorder_level:
                messagebox.showwarning("Warning", f"Stock below reorder level: {reorder_level}")

            messagebox.showinfo("Success", "Spare consumption entry added successfully")
            clear_entries([quantity_entry, date_entry], [spare_name_combobox])
        else:
            messagebox.showerror("Error", "Spare not found in stock")

    setup_button(frame, 'Submit', 30, 200, submit)
    setup_button(frame, 'Cancel', 310, 200, spareConsumptionWindow.destroy)

    spareConsumptionWindow.mainloop()


# Stock Verification Window
def create_stock_verification_window():
    stockVerificationWindow = Toplevel()
    frame = setup_frame(stockVerificationWindow, 'Stock Verification')
    setup_label(frame, 'Spare Stock Verification', 220, 10, 24)
    setup_label(frame, 'Spare Name:', 80, 100)

    spare_names = fetch_data("SELECT spare_id, item_name, specification FROM spare_master")
    spare_name_combobox, spare_name_var = setup_combobox(frame, [f"{name} {spec}" for _, name, spec in spare_names],
                                                         280, 105)

    def display_stock_details():
        spare_name = spare_name_var.get()

        if not spare_name:
            messagebox.showerror("Error", "Please select a spare name")
            return

        spare_id = next((id for id, name, spec in spare_names if f"{name} {spec}" == spare_name), None)
        if not spare_id:
            messagebox.showerror("Error", "Invalid Spare Name")
            return

        query = "SELECT spare_stock.current_stock, spare_master.reorder_level, spare_master.location FROM spare_stock JOIN spare_master ON spare_stock.spare_id = spare_master.spare_id WHERE spare_stock.spare_id = %s"
        stock_data = fetch_data(query, (spare_id,))

        if stock_data:
            current_stock, reorder_level, location = stock_data[0]
            setup_label(frame,f"Spare Name: {spare_name}",250,250)
            setup_label(frame, f"Current Stock: {current_stock}", 250, 280)
            setup_label(frame, f"Re-Order Level: {reorder_level}", 250, 310)
            setup_label(frame,f'Location: {location}',250,340)
        else:
            messagebox.showerror("Error", "No stock details found for selected spare")

    setup_button(frame, 'Verify', 80, 200, display_stock_details)
    setup_button(frame, 'Cancel', 360, 200, stockVerificationWindow.destroy)

    stockVerificationWindow.mainloop()


# Callback Functions to Open Different Windows
def open_spare_entry():
    create_spare_entry_window()


def open_spare_inward():
    create_spare_inward_window()


def open_spare_consumption():
    create_spare_consumption_window()


def open_stock_verification():
    create_stock_verification_window()


# Main Entry Point
if __name__ == "__main__":
    create_home_window()
