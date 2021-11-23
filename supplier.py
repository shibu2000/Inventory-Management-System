# from os import WIFSTOPPED
from sqlite3.dbapi2 import SQLITE_OK
from tkinter import*
from tkinter import font
from typing import Pattern
from PIL import Image, ImageTk  # sudo dnf install python3-pillow-tk
from tkinter import ttk, messagebox
import sqlite3
import re


class supplierClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+240+140")
        self.root.title("Inventory Management System | Supplier Window")
        self.root.config(bg="white")
        self.root.focus_force()
        # ====================All variables===================
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        self.var_supplier_invoice = StringVar()
        self.var_name = StringVar()
        self.var_contact = StringVar()

        # ====Title=====
        title = Label(self.root, text="Supplier Details", font=(
            "goudy old style", 20), bg="#0f4d7d", fg="white").place(x=50, y=10, width=1000, height=40)
        # =======options======
        lbl_search = Label(
            self.root, text="Search By Invoice No:", font=("new times roman", 15), bg="white")
        lbl_search.place(x=580, y=60)

        txt_search = Entry(self.root, textvariable=self.var_searchtxt, font=(
            "goudy old style", 15), bg="lightyellow").place(x=810, y=60, width=150)
        btn_Search = Button(self.root, command=self.search, text="Search", cursor="hand2", font=(
            "goudy old style", 15), bg="#424949", fg="white").place(x=970, y=60, width=100, height=30)

        # ====other contents
        # ====Row 1======
        lbl_supplier_invoice = Label(self.root, text="Invoice No.:", font=(
            "goudy old style", 15), bg="white").place(x=50, y=80)

        self.txt_supplier_invoice = Entry(self.root, textvariable=self.var_supplier_invoice, font=(
            "goudy old style", 15), bg="lightyellow")
        self.txt_supplier_invoice.place(x=200, y=80, width=180)

        # =========row2=================
        lbl_name = Label(self.root, text="Name:", font=(
            "goudy old style", 15), bg="white").place(x=50, y=140)

        txt_name = Entry(self.root, textvariable=self.var_name, font=(
            "goudy old style", 15), bg="lightyellow").place(x=200, y=140, width=180)

        # ================row3============

        lbl_contact = Label(self.root, text="Contact:", font=(
            "goudy old style", 15), bg="white").place(x=50, y=200)

        txt_contact = Entry(self.root, textvariable=self.var_contact, font=(
            "goudy old style", 15), bg="lightyellow").place(x=200, y=200, width=180)

        # ==========Row4===========
        lbl_desc = Label(self.root, text="Description:", font=(
            "goudy old style", 15), bg="white").place(x=50, y=260)

        self.txt_desc = Text(self.root, font=(
            "goudy old style", 15), bg="lightyellow")
        self.txt_desc.place(x=200, y=260, width=300, height=70)

        # ===========Buttons=========
        btn_save = Button(self.root, text="Save", command=self.save, cursor="hand2", font=(
            "goudy old style", 12), bg="#C70039", fg="white").place(x=50, y=400, height=40, width=110)
        btn_update = Button(self.root, text="Update", command=self.update, cursor="hand2", font=(
            "goudy old style", 12), bg="#1E8449", fg="white").place(x=170, y=400, height=40, width=110)
        btn_delete = Button(self.root, command=self.delete, text="Delete", cursor="hand2", font=(
            "goudy old style", 12), bg="#34495E", fg="white").place(x=290, y=400, height=40, width=110)
        btn_Clear = Button(self.root, command=self.clear, text="Clear", cursor="hand2", font=(
            "goudy old style", 12), bg="#6C3483", fg="white").place(x=410, y=400, height=40, width=110)

        # =============Employee Details=========
        emp_frame = Frame(self.root, bd=1, relief=RIDGE, bg="lightblue")
        emp_frame.place(x=580, y=100, width=500, height=400)

        scrolly = Scrollbar(emp_frame, orient=VERTICAL)
        scrollx = Scrollbar(emp_frame, orient=HORIZONTAL)

        self.supplierTable = ttk.Treeview(emp_frame, columns=(
            "INVOICE", "NAME", "CONTACT", "DESC"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)

        scrollx.config(command=self.supplierTable.xview)
        scrolly.config(command=self.supplierTable.yview)

        self.supplierTable.heading("INVOICE", text="INVOICE NO")
        self.supplierTable.heading("NAME", text="NAME")
        self.supplierTable.heading("CONTACT", text="CONTACT")
        self.supplierTable.heading("DESC", text="DESCRIPTION")

        self.supplierTable["show"] = "headings"

        self.supplierTable.column("INVOICE", width=90)
        self.supplierTable.column("NAME", width=100)
        self.supplierTable.column("CONTACT", width=100)
        self.supplierTable.column("DESC", width=100)

        self.supplierTable.pack(fill=BOTH, expand=1)
        self.supplierTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()

# =================================================================================================
# =========================Save Details=====================
    def save(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_supplier_invoice.get() == "":
                messagebox.showerror(
                    "Error", "Invoice must be required", parent=self.root)
            else:
                cur.execute("Select * from SUPPLIER where INVOICE=?",
                            (self.var_supplier_invoice.get(),))
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror(
                        "Error", "This Invoice number already assigned, try different", parent=self.root)
                else:
                    cur.execute(
                        "INSERT INTO SUPPLIER (INVOICE, NAME, CONTACT, DESCRIPTION) values(?,?,?,?)", (
                            self.var_supplier_invoice.get(),
                            self.var_name.get(),
                            self.var_contact.get(),
                            self.txt_desc.get(1.0, END),
                        ))
                    con.commit()
                    messagebox.showinfo(
                        "Success", "Supplier Details Saved", parent=self.root)
                    self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")

# ===================Show details in Treeview=================

    def show(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM SUPPLIER")
            rows = cur.fetchall()
            self.supplierTable.delete(*self.supplierTable.get_children())
            for row in rows:
                self.supplierTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")

# ===================Get Data from Database and show into textbox===============

    def get_data(self, ev):
        f = self.supplierTable.focus()
        content = (self.supplierTable.item(f))
        row = content['values']
        self.var_supplier_invoice.set(row[0]),
        self.var_name.set(row[1]),
        self.var_contact.set(row[2]),
        self.txt_desc.delete(1.0, END),
        self.txt_desc.insert(END, row[3])

        self.txt_supplier_invoice.configure(state='disabled')

# ========================Update details===========================

    def update(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_supplier_invoice.get() == "":
                messagebox.showerror(
                    "Error", "Invoice must be required", parent=self.root)
            else:
                cur.execute("Select * from SUPPLIER where INVOICE=?",
                            (self.var_supplier_invoice.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror(
                        "Error", "Invalid Invoice Number", parent=self.root)
                else:
                    cur.execute(
                        "UPDATE SUPPLIER set NAME=?, CONTACT=?, DESCRIPTION=? WHERE INVOICE=?", (
                            self.var_name.get(),
                            self.var_contact.get(),
                            self.txt_desc.get(1.0, END),
                            self.var_supplier_invoice.get()

                        ))
                    con.commit()
                    messagebox.showinfo(
                        "Success", "Supplier Details Updated", parent=self.root)

                    self.show()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")

# ===============Delete details from database==================

    def delete(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_supplier_invoice.get() == "":
                messagebox.showerror(
                    "Error", "Invoice Number must be required", parent=self.root)
            else:
                cur.execute("Select * from SUPPLIER where INVOICE=?",
                            (self.var_supplier_invoice.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror(
                        "Error", "Invalid Invoice Number", parent=self.root)
                else:
                    op = messagebox.askyesno(
                        "Confirm", "Do You Really Want To Delete?", parent=self.root)
                    if op == True:
                        cur.execute("DELETE FROM SUPPLIER WHERE INVOICE=?",
                                    (self.var_supplier_invoice.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "SUPPLIER Details Deleted",
                                            parent=self.root)
                        self.clear()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")

# ================Clear textboxes========================

    def clear(self):
        self.var_supplier_invoice.set(""),
        self.var_name.set(""),
        self.var_contact.set(""),
        self.txt_desc.delete(1.0, END),

        self.var_searchtxt.set("")
        self.show()

        self.txt_supplier_invoice.configure(state=NORMAL)

    def search(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_searchtxt.get() == "":
                messagebox.showerror(
                    "Error", "Invoice Number Required", parent=self.root)
            else:
                cur.execute("SELECT * FROM SUPPLIER WHERE INVOICE=?",
                            (self.var_searchtxt.get(),))
                row = cur.fetchall()
                if row != None:
                    self.supplierTable.delete(
                        *self.supplierTable.get_children())
                    for row in row:
                        self.supplierTable.insert('', END, values=row)
                else:
                    messagebox.showerror(
                        "Error", "No Record Found!!!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")


if __name__ == "__main__":
    root = Tk()
    obj = supplierClass(root)
    root.mainloop()
