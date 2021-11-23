from tkinter import*
from PIL import Image, ImageTk  # sudo dnf install python3-pillow-tk
from tkinter import ttk, messagebox
import sqlite3
import re


class first_time:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title(
            "Inventory Management Login System|First Time UserWindow| Developed By SD")
        self.root.config(bg="white")
        # =================All Variables==================================
        self.var_emp_id = StringVar()
        self.var_gender = StringVar()
        self.var_contact = StringVar()
        self.var_name = StringVar()
        self.var_email = StringVar()
        self.var_dob = StringVar()
        self.var_doj = StringVar()
        self.var_name = StringVar()
        self.var_pass = StringVar()
        self.var_utype = StringVar()
        self.var_salary = StringVar()
        # ================All Tkinter Widz================================
        title = Label(self.root, text="First Time User Registration", font=(
            "goudy old style", 20), bg="#0f4d7d", fg="white").pack(side=TOP, fill=X, ipady=10)

        # ====Row 1======
        lbl_emp_id = Label(self.root, text="Employee ID:", font=(
            "goudy old style", 15), bg="white").place(x=50, y=150)
        lbl_gender = Label(self.root, text="Gender:", font=(
            "goudy old style", 15), bg="white").place(x=400, y=150)
        lbl_contact = Label(self.root, text="Contact:", font=(
            "goudy old style", 15), bg="white").place(x=750, y=150)

        txt_emp_id = Entry(self.root, textvariable=self.var_emp_id, font=(
            "goudy old style", 15), bg="lightyellow")
        txt_emp_id.place(x=200, y=150, width=180)

        cmb_gender = ttk.Combobox(self.root, textvariable=self.var_gender, values=("Select", "Male", "Female", "Other"),
                                  state="readonly", justify=CENTER, font=("goudy old style", 15))
        cmb_gender.place(x=520, y=150, width=180)
        cmb_gender.current(0)
        txt_contact = Entry(self.root, textvariable=self.var_contact, font=(
            "goudy old style", 15), bg="lightyellow").place(x=870, y=150, width=180)


if __name__ == "__main__":
    root = Tk()
    obj = first_time(root)
    root.mainloop()
