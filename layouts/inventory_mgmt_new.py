from tkinter import *
from tkinter import ttk
from datetime import datetime
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

def fetch_data(query, params=None):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute(query, params or ())
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

def execute_query(query, params=None):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(query, params or ())
        connection.commit()
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

def clear_entries(entries, comboboxes=None):
    for entry in entries:
        entry.delete(0, END)
    if comboboxes:
        for combobox in comboboxes:
            combobox.set('')

def setup_frame(parent, title):
    frame = Frame(parent, width=800, height=600, bg=BG_COLOR, bd=8)
    frame.pack(fill=BOTH, expand=True)
    return frame

def setup_label(frame, text, x, y, font_size=FONT_SIZE):
    label = Label(frame, text=text, fg=FG_COLOR, bg=BG_COLOR, font=(PRIMARY_FONT, font_size, 'bold'))
    label.place(x=x, y=y)
    return label

def setup_combobox(frame, values, x, y):
    var = StringVar()
    combobox = ttk.Combobox(frame, textvariable=var, width=47, values=values)
    combobox.place(x=x, y=y)
    return combobox, var

def setup_entry(frame, x, y):
    entry = Entry(frame, width=50, borderwidth=2)
    entry.place(x=x, y=y)
    return entry

def setup_button(frame, text, x, y, command):
    button = Button(frame, text=text, bg=BTN_COLOR, width=23, font=(PRIMARY_FONT, FONT_SIZE, 'normal'), command=command)
    button.place(x=x, y=y)
    return button

# Main Application
def create_main_window():
    main_window = Tk()
    main_window.geometry('800x600')
    main_window.title('Spare Inventory Management System')
    main_window.resizable(False, False)

    notebook = ttk.Notebook(main_window)

    # Spare Entry Tab
    spare_entry_frame = setup_frame(notebook, 'Spare Entry')
    notebook.add(spare_entry_frame, text='Spare Entry')
    setup_label(spare_entry_frame, "Spare Entry", 250, 10, 24)
    labels = ['Spare Name:', 'Specification:', 'Location:', 'UOM:', 'Re-Order Level:']
    entries = []
    locations = [f"R{rack}-Bin{bin}" for rack in range(1, 6) for bin in range(1, 11)]

    for i, label in enumerate(labels):
        setup_label(spare_entry_frame, label, 10, 70 + 40 * i)
        if i in [0, 1, 4]:
            entries.append(setup_entry(spare_entry_frame, 200, 75 + 40 * i))
        elif i == 2:
            location_combobox, location_var = setup_combobox(spare_entry_frame, locations, 200, 155)
        elif i == 3:
            uom_combobox, uom_var = setup_combobox(spare_entry_frame, ['Piece', 'Box', 'Kg', 'Litre'], 200, 195)

    def submit_spare_entry():
        spare_name = entries[0].get()
        specification = entries[1].get()
        location = location_var.get()
        uom = uom_var.get()
        reorder_level = entries[2].get()

        if not all([spare_name, specification, location, uom, reorder_level]):
            messagebox.showerror("Error", "Please fill all the fields")
            return

        try:
            reorder_level = int(reorder_level)
        except ValueError:
            messagebox.showerror("Error", "Re-Order Level must be an integer")
            return

        query = """
        INSERT INTO spare_master (item_name, specification, location, uom, reorder_level)
        VALUES (%s, %s, %s, %s, %s)
        """
        execute_query(query, (spare_name, specification, location, uom, reorder_level))
        messagebox.showinfo("Success", "Item added successfully")
        clear_entries(entries, [location_combobox, uom_combobox])

    setup_button(spare_entry_frame, 'Submit', 30, 315, submit_spare_entry)
    setup_button(spare_entry_frame, 'Cancel', 310, 315, lambda: main_window.quit())

    # Spare Inward Tab
    spare_inward_frame = setup_frame(notebook, 'Spare Inward Entry')
    notebook.add(spare_inward_frame, text='Spare Inward Entry')
    setup_label(spare_inward_frame, "Spare Inward", 250, 10, 24)
    spare_names = fetch_data("SELECT spare_id, item_name, specification FROM spare_master")
    spare_name_combobox, spare_name_var = setup_combobox(spare_inward_frame, [f"{name} {spec}" for _, name, spec in spare_names],
                                                         250, 75)
    setup_label(spare_inward_frame, 'Spare Name:', 60, 70)
    setup_label(spare_inward_frame, 'Quantity:', 60, 110)
    quantity_entry = setup_entry(spare_inward_frame, 250, 115)

    setup_label(spare_inward_frame, 'Date:', 60, 150)
    date_var = StringVar()
    date_entry = Entry(spare_inward_frame, textvariable=date_var, width=50, borderwidth=2)
    date_var.set(datetime.now().strftime('%Y-%m-%d'))
    date_entry.place(x=250, y=155)

    def submit_spare_inward():
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

    setup_button(spare_inward_frame, 'Submit', 30, 200, submit_spare_inward)
    setup_button(spare_inward_frame, 'Cancel', 310, 200, lambda: main_window.quit())

    # Spare Consumption Tab
    spare_consumption_frame = setup_frame(notebook, 'Spare Consumption Entry')
    notebook.add(spare_consumption_frame, text='Spare Consumption Entry')
    setup_label(spare_consumption_frame, "Spare Consumption", 250, 10, 24)
    spare_names = fetch_data("SELECT spare_id, item_name, specification FROM spare_master")
    spare_name_combobox, spare_name_var = setup_combobox(spare_consumption_frame, [f"{name} {spec}" for _, name, spec in spare_names],
                                                         270, 75)
    setup_label(spare_consumption_frame, 'Spare Name:', 60, 70)
    setup_label(spare_consumption_frame, 'Quantity Consumed:', 60, 110)
    quantity_entry = setup_entry(spare_consumption_frame, 270, 115)

    setup_label(spare_consumption_frame, 'Date:', 60, 150)
    date_var = StringVar()
    date_entry = Entry(spare_consumption_frame, textvariable=date_var, width=50, borderwidth=2)
    date_var.set(datetime.now().strftime('%Y-%m-%d'))
    date_entry.place(x=270, y=155)

    def submit_spare_consumption():
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

        query = "INSERT INTO spare_consumption (spare_id, quantity, date) VALUES (%s, %s, %s)"
        execute_query(query, (spare_id, quantity, date))
        messagebox.showinfo("Success", "Spare consumption entry added successfully")
        clear_entries([quantity_entry, date_entry], [spare_name_combobox])

    setup_button(spare_consumption_frame, 'Submit', 30, 200, submit_spare_consumption)
    setup_button(spare_consumption_frame, 'Cancel', 310, 200, lambda: main_window.quit())

    # Stock Verification Tab
    stock_verification_frame = setup_frame(notebook, 'Stock Verification')
    notebook.add(stock_verification_frame, text='Stock Verification')
    setup_label(stock_verification_frame, "Stock Verification", 250, 10, 24)
    spare_names = fetch_data("SELECT spare_id, item_name, specification FROM spare_master")
    spare_name_combobox, spare_name_var = setup_combobox(stock_verification_frame, [f"{name} {spec}" for _, name, spec in spare_names],
                                                         270, 75)
    setup_label(stock_verification_frame, 'Spare Name:', 60, 70)

    def verify_stock():
        spare_name = spare_name_var.get()
        if not spare_name:
            messagebox.showerror("Error", "Please select a Spare Name")
            return

        spare_id = next((id for id, name, spec in spare_names if f"{name} {spec}" == spare_name), None)
        if not spare_id:
            messagebox.showerror("Error", "Invalid Spare Name")
            return

        query = """
        SELECT
            sm.item_name,
            sm.specification,
            COALESCE(si.total_quantity, 0) AS inward_quantity,
            COALESCE(sc.total_quantity, 0) AS consumed_quantity,
            COALESCE(si.total_quantity, 0) - COALESCE(sc.total_quantity, 0) AS available_quantity
        FROM
            spare_master sm
            LEFT JOIN (
                SELECT spare_id, SUM(quantity) AS total_quantity
                FROM spare_inward
                GROUP BY spare_id
            ) si ON sm.spare_id = si.spare_id
            LEFT JOIN (
                SELECT spare_id, SUM(quantity) AS total_quantity
                FROM spare_consumption
                GROUP BY spare_id
            ) sc ON sm.spare_id = sc.spare_id
        WHERE
            sm.spare_id = %s
        """
        result = fetch_data(query, (spare_id,))
        if not result:
            messagebox.showinfo("Info", "No data found for the selected Spare Name")
        else:
            item_name, specification, inward_qty, consumed_qty, available_qty = result[0]
            messagebox.showinfo("Stock Details", f"Item Name: {item_name}\nSpecification: {specification}\n"
                                                  f"Inward Quantity: {inward_qty}\nConsumed Quantity: {consumed_qty}\n"
                                                  f"Available Quantity: {available_qty}")

    setup_button(stock_verification_frame, 'Verify Stock', 30, 200, verify_stock)
    setup_button(stock_verification_frame, 'Cancel', 310, 200, lambda: main_window.quit())

    notebook.pack(fill=BOTH, expand=True)
    main_window.mainloop()

create_main_window()
