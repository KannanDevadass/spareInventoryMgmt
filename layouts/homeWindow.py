# homeWindow.py

from tkinter import *
from spareEntry import create_spare_entry_window
from spareInward import create_spare_inward_window
from spareConsumption import create_spare_consumption_window
from stockVerification import create_stock_verification_window

# Define global window variables
homeWindow = None
spareEntryWindow = None
spareInwardWindow = None
spareConsumptionWindow = None
stockVerificationWindow = None


def create_home_window():
    global homeWindow
    homeWindow = Tk()
    homeWindow.geometry('800x600')
    bgColor = '#E7E8D8'
    fgColor = 'black'
    btnColor = '#BC9F8B'
    fontSize = 14
    primaryFont = 'century gothic'
    homeWindow.title('Spare Inventory Management System')
    homeWindow.resizable(False, False)

    frame = Frame(homeWindow, width=800, height=600, bg=bgColor, bd=8)
    frame.place(x=0, y=0)

    img = PhotoImage(file="logo.png")
    logo_label = Label(frame, image=img)
    logo_label.image = img
    logo_label.place(x = 15, y = 20)

    # logo_label = Label(frame, text="[LOGO]", font=(primaryFont, 20, 'bold'), fg=fgColor, bg=bgColor)
    # logo_label.place(x=20, y=20)

    title = Label(frame, text="Spare Inventory Management System", font=(primaryFont, 24, 'bold'), fg=fgColor,
                  bg=bgColor)
    title.place(x=120, y=50)

    spare_entry_button = Button(frame, text="Spare Entry", bg=btnColor, width=23,
                                font=(primaryFont, fontSize, 'normal'), command=open_spare_entry)
    spare_entry_button.place(x=120, y=150)

    spare_inward_button = Button(frame, text="Spare Inward Entry", bg=btnColor, width=23,
                                 font=(primaryFont, fontSize, 'normal'), command=open_spare_inward)
    spare_inward_button.place(x=400, y=150)

    spare_consumption_button = Button(frame, text="Spare Consumption Entry", bg=btnColor, width=23,
                                      font=(primaryFont, fontSize, 'normal'), command=open_spare_consumption)
    spare_consumption_button.place(x=120, y=200)

    stock_verification_button = Button(frame, text="Stock Verification", bg=btnColor, width=23,
                                       font=(primaryFont, fontSize, 'normal'), command=open_stock_verification)
    stock_verification_button.place(x=400, y=200)

    homeWindow.mainloop()


def open_spare_entry():
    global spareEntryWindow
    spareEntryWindow = create_spare_entry_window(homeWindow)
    # spareEntryWindow.deiconify()


def open_spare_inward():
    global spareInwardWindow
    spareInwardWindow = create_spare_inward_window(homeWindow)
    # spareInwardWindow.deiconify()


def open_spare_consumption():
    global spareConsumptionWindow
    spareConsumptionWindow = create_spare_consumption_window(homeWindow)
    # spareConsumptionWindow.deiconify()


def open_stock_verification():
    global stockVerificationWindow
    stockVerificationWindow = create_stock_verification_window(homeWindow)
    # stockVerificationWindow.deiconify()


# Start the application
create_home_window()
