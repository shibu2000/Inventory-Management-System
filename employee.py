import os
# from os import WIFSTOPPED
from sqlite3.dbapi2 import SQLITE_OK
from tkinter import*
from tkinter import font
from typing import Pattern
from PIL import Image, ImageTk  # sudo dnf install python3-pillow-tk
from tkinter import ttk, messagebox
import sqlite3
import re


class employeeClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+240+140")
        self.root.resizable(False, False)
        self.root.title("Inventory Management System | Employee")
        self.root.config(bg="white")
        self.root.focus_force()
        # ====================All variables===================
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

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

        # style = ttk.Style()
        # style.configure("BW.TLabel", foreground="white", background="white",
        #                 insertbackground="black", fieldbackground='blue')

        # ====Search Frame======
        SeacrhFrame = LabelFrame(self.root, text="Search Employee", bg="white", font=(
            "goudy old style", 12, "bold"), bd=2, relief=RIDGE)
        SeacrhFrame.place(x=210, y=20, width=650, height=70)

        # =======options======
        combBox = ttk.Combobox(SeacrhFrame, textvariable=self.var_searchby, values=("Select", "Email", "Name", "Contact"),
                               state="readonly", justify=CENTER, font=("goudy old style", 15))
        combBox.place(x=10, y=10, width=180)
        combBox.current(0)

        txt_search = Entry(SeacrhFrame, textvariable=self.var_searchtxt, font=(
            "goudy old style", 15), bg="lightyellow").place(x=200, y=9, width=290)
        btn_Search = Button(SeacrhFrame, command=self.search, text="Search", cursor="hand2", font=(
            "goudy old style", 15), bg="#424949", fg="white").place(x=500, y=9, width=130, height=30)

        # ====Title=====
        title = Label(self.root, text="Employee Details", font=(
            "goudy old style", 15), bg="#0f4d7d", fg="white").place(x=50, y=100, width=1000)

        # ====other contents
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

        # =========row2=================
        lbl_name = Label(self.root, text="Name:", font=(
            "goudy old style", 15), bg="white").place(x=50, y=190)
        lbl_dob = Label(self.root, text="DOB:", font=(
            "goudy old style", 15), bg="white").place(x=400, y=190)
        lbl_doj = Label(self.root, text="DOJ:", font=(
            "goudy old style", 15), bg="white").place(x=750, y=190)

        txt_name = Entry(self.root, textvariable=self.var_name, font=(
            "goudy old style", 15), bg="lightyellow").place(x=200, y=190, width=180)
        txt_dob = Entry(self.root, textvariable=self.var_dob, font=(
            "goudy old style", 15), bg="lightyellow").place(x=520, y=190, width=180)
        txt_doj = Entry(self.root, textvariable=self.var_doj, font=(
            "goudy old style", 15), bg="lightyellow").place(x=870, y=190, width=180)

        # ================row3============

        lbl_email = Label(self.root, text="Email:", font=(
            "goudy old style", 15), bg="white").place(x=50, y=230)
        lbl_password = Label(self.root, text="Password:", font=(
            "goudy old style", 15), bg="white").place(x=400, y=230)
        lbl_utype = Label(self.root, text="User Type:", font=(
            "goudy old style", 15), bg="white").place(x=750, y=230)

        txt_email = Entry(self.root, textvariable=self.var_email, font=(
            "goudy old style", 15), bg="lightyellow").place(x=200, y=230, width=180)
        txt_password = Entry(self.root, textvariable=self.var_pass, font=(
            "goudy old style", 15), bg="lightyellow").place(x=520, y=230, width=180)
        cmb_utype = ttk.Combobox(self.root, textvariable=self.var_utype, values=("Admin", "Employee"),
                                 state="readonly", justify=CENTER, font=("goudy old style", 15))
        cmb_utype.place(x=870, y=230, width=180)
        cmb_utype.current(0)

        # ==========Row4===========
        lbl_address = Label(self.root, text="Address:", font=(
            "goudy old style", 15), bg="white").place(x=50, y=270)
        lbl_salary = Label(self.root, text="Salary:", font=(
            "goudy old style", 15), bg="white").place(x=520, y=270)

        self.txt_address = Text(self.root, font=(
            "goudy old style", 15), bg="lightyellow")
        self.txt_address.place(x=200, y=270, width=300, height=70)

        txt_salary = Entry(self.root, textvariable=self.var_salary, font=(
            "goudy old style", 15), bg="lightyellow").place(x=640, y=270, width=180)
        # ===========Buttons=========
        btn_save = Button(self.root, text="Save", command=self.save, cursor="hand2", font=(
            "goudy old style", 12), bg="#C70039", fg="white").place(x=520, y=309, height=30, width=110)
        btn_update = Button(self.root, text="Update", command=self.update, cursor="hand2", font=(
            "goudy old style", 12), bg="#1E8449", fg="white").place(x=640, y=309, height=30, width=110)
        btn_delete = Button(self.root, command=self.delete, text="Delete", cursor="hand2", font=(
            "goudy old style", 12), bg="#34495E", fg="white").place(x=760, y=309, height=30, width=110)
        btn_Clear = Button(self.root, command=self.clear, text="Clear", cursor="hand2", font=(
            "goudy old style", 12), bg="#6C3483", fg="white").place(x=880, y=309, height=30, width=110)

        # =============Employee Details=========
        emp_frame = Frame(self.root, bd=1, relief=RIDGE, bg="lightblue")
        emp_frame.place(x=0, y=350, relwidth=1, height=150)

        scrolly = Scrollbar(emp_frame, orient=VERTICAL)
        scrollx = Scrollbar(emp_frame, orient=HORIZONTAL)

        self.employeeTable = ttk.Treeview(emp_frame, columns=(
            "EMPID", "NAME", "EMAIL", "GENDER", "CONTACT", "DOB", "DOJ", "PASSWORD", "UTYPE", "ADDRESS", "SALARY"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)

        scrollx.config(command=self.employeeTable.xview)
        scrolly.config(command=self.employeeTable.yview)

        self.employeeTable.heading("EMPID", text="EMP_ID")
        self.employeeTable.heading("NAME", text="NAME")
        self.employeeTable.heading("EMAIL", text="EMAIL")
        self.employeeTable.heading("GENDER", text="GENDER")
        self.employeeTable.heading("CONTACT", text="CONTACT")
        self.employeeTable.heading("DOB", text="D.O.B")
        self.employeeTable.heading("DOJ", text="D.O.J")
        self.employeeTable.heading("PASSWORD", text="PASSWORD")
        self.employeeTable.heading("UTYPE", text="U_TYPE")
        self.employeeTable.heading("ADDRESS", text="ADDRESS")
        self.employeeTable.heading("SALARY", text="SALARY")

        self.employeeTable["show"] = "headings"

        self.employeeTable.column("EMPID", width=90)
        self.employeeTable.column("NAME", width=100)
        self.employeeTable.column("EMAIL", width=100)
        self.employeeTable.column("GENDER", width=100)
        self.employeeTable.column("CONTACT", width=100)
        self.employeeTable.column("DOB", width=100)
        self.employeeTable.column("DOJ", width=100)
        self.employeeTable.column("PASSWORD", width=100)
        self.employeeTable.column("UTYPE", width=100)
        self.employeeTable.column("ADDRESS", width=100)
        self.employeeTable.column("SALARY", width=100)
        self.employeeTable.pack(fill=BOTH, expand=1)
        self.employeeTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()

# =================================================================================================
# =========================Save Details=====================
    def save(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror(
                    "Error", "Employee ID must be required", parent=self.root)
            else:
                cur.execute("Select * from EMPLOYEE where EMPID=?",
                            (self.var_emp_id.get(),))
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror(
                        "Error", "This Employee ID already assigned, try different", parent=self.root)
                else:
                    if self.var_email.get() == "":
                        cur.execute(
                            "INSERT INTO EMPLOYEE (EMPID, NAME, EMAIL, GENDER, CONTACT, DOB, DOJ, PASSWORD, UTYPE, ADDRESS, SALARY) values(?,?,?,?,?,?,?,?,?,?,?)", (
                                self.var_emp_id.get(),
                                self.var_name.get(),
                                self.var_email.get(),
                                self.var_gender.get(),
                                self.var_contact.get(),
                                self.var_dob.get(),
                                self.var_doj.get(),
                                self.var_pass.get(),
                                self.var_utype.get(),
                                self.txt_address.get(1.0, END),
                                self.var_salary.get()

                            ))
                        con.commit()
                        messagebox.showinfo(
                            "Success", "Employee Details Saved", parent=self.root)
                        self.clear()
                    else:
                        status = self.checkEmail(self.var_email.get())
                        if status == 1:
                            cur.execute(
                                "INSERT INTO EMPLOYEE (EMPID, NAME, EMAIL, GENDER, CONTACT, DOB, DOJ, PASSWORD, UTYPE, ADDRESS, SALARY) values(?,?,?,?,?,?,?,?,?,?,?)", (
                                    self.var_emp_id.get(),
                                    self.var_name.get(),
                                    self.var_email.get(),
                                    self.var_gender.get(),
                                    self.var_contact.get(),
                                    self.var_dob.get(),
                                    self.var_doj.get(),
                                    self.var_pass.get(),
                                    self.var_utype.get(),
                                    self.txt_address.get(1.0, END),
                                    self.var_salary.get()

                                ))
                            con.commit()
                            messagebox.showinfo(
                                "Success", "Employee Details Saved", parent=self.root)
                            self.clear()
                        else:
                            messagebox.showerror(
                                "Error", "Enter A Valid Email ID")

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")

# ===================Show details in Treeview=================

    def show(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM EMPLOYEE")
            rows = cur.fetchall()
            self.employeeTable.delete(*self.employeeTable.get_children())
            for row in rows:
                self.employeeTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")

# ===================Get Data from Database and show into textbox===============

    def get_data(self, ev):
        f = self.employeeTable.focus()
        content = (self.employeeTable.item(f))
        row = content['values']
        self.var_emp_id.set(row[0]),
        self.var_name.set(row[1]),
        self.var_email.set(row[2]),
        self.var_gender.set(row[3]),
        self.var_contact.set(row[4]),
        self.var_dob.set(row[5]),
        self.var_doj.set(row[6]),
        self.var_pass.set(row[7]),
        self.var_utype.set(row[8]),
        self.txt_address.delete(1.0, END),
        self.txt_address.insert(END, row[9]),
        self.var_salary.set(row[10])

# ========================Update details===========================

    def update(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror(
                    "Error", "Employee ID must be required", parent=self.root)
            else:
                cur.execute("Select * from EMPLOYEE where EMPID=?",
                            (self.var_emp_id.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror(
                        "Error", "Invalid Employee ID", parent=self.root)
                else:
                    if self.var_email.get() == "":
                        cur.execute(
                            "UPDATE EMPLOYEE set NAME=?, EMAIL=?, GENDER=?, CONTACT=?, DOB=?, DOJ=?, PASSWORD=?, UTYPE=?, ADDRESS=?, SALARY=? WHERE EMPID=?", (
                                self.var_name.get(),
                                self.var_email.get(),
                                self.var_gender.get(),
                                self.var_contact.get(),
                                self.var_dob.get(),
                                self.var_doj.get(),
                                self.var_pass.get(),
                                self.var_utype.get(),
                                self.txt_address.get(1.0, END),
                                self.var_salary.get(),
                                self.var_emp_id.get()

                            ))
                        con.commit()
                        messagebox.showinfo(
                            "Success", "Employee Details Updated", parent=self.root)

                        self.show()
                    else:
                        status = self.checkEmail(self.var_email.get())
                        if status == 1:
                            cur.execute(
                                "UPDATE EMPLOYEE set NAME=?, EMAIL=?, GENDER=?, CONTACT=?, DOB=?, DOJ=?, PASSWORD=?, UTYPE=?, ADDRESS=?, SALARY=? WHERE EMPID=?", (
                                    self.var_name.get(),
                                    self.var_email.get(),
                                    self.var_gender.get(),
                                    self.var_contact.get(),
                                    self.var_dob.get(),
                                    self.var_doj.get(),
                                    self.var_pass.get(),
                                    self.var_utype.get(),
                                    self.txt_address.get(1.0, END),
                                    self.var_salary.get(),
                                    self.var_emp_id.get()

                                ))
                            con.commit()
                            messagebox.showinfo(
                                "Success", "Employee Details Updated", parent=self.root)

                            self.show()
                        else:
                            messagebox.showerror(
                                "Error", "Enter A Valid Email ID")

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")

# ===============Delete details from database==================

    def delete(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror(
                    "Error", "Employee ID must be required", parent=self.root)
            else:
                cur.execute("Select * from EMPLOYEE where EMPID=?",
                            (self.var_emp_id.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror(
                        "Error", "Invalid Employee ID", parent=self.root)
                else:
                    op = messagebox.askyesno(
                        "Confirm", "Do You Really Want To Delete?", parent=self.root)
                    if op == True:
                        cur.execute("DELETE FROM EMPLOYEE WHERE EMPID=?",
                                    (self.var_emp_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Employee Details Deleted",
                                            parent=self.root)
                        self.clear()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")

# ================Clear textboxes========================

    def clear(self):
        self.var_emp_id.set(""),
        self.var_name.set(""),
        self.var_email.set(""),
        self.var_gender.set("Select"),
        self.var_contact.set(""),
        self.var_dob.set(""),
        self.var_doj.set(""),
        self.var_pass.set(""),
        self.var_utype.set("Admin"),
        self.txt_address.delete(1.0, END),
        self.var_salary.set("")

        self.var_searchtxt.set("")
        self.var_searchby.set("Select")
        self.show()

    def search(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_searchby.get() == "Select":
                messagebox.showerror(
                    "Error", "Select Any Option to Search", parent=self.root)
            elif self.var_searchtxt.get() == "":
                messagebox.showerror(
                    "Error", "Search Input Required", parent=self.root)
            else:
                cur.execute("SELECT * FROM EMPLOYEE WHERE " +
                            self.var_searchby.get()+" LIKE '%"+self.var_searchtxt.get()+"%'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.employeeTable.delete(
                        *self.employeeTable.get_children())
                    for row in rows:
                        self.employeeTable.insert('', END, values=row)
                else:
                    messagebox.showerror(
                        "Error", "No Record Found!!!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")

    def checkEmail(self, email):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if(re.fullmatch(regex, email)):
            return 1


if __name__ == "__main__":
    root = Tk()
    obj = employeeClass(root)
    root.mainloop()
