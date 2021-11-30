# from os import WIFSTOPPED
from sqlite3.dbapi2 import SQLITE_OK, Row
from tkinter import*
from tkinter import font
from typing import Pattern
from PIL import Image, ImageTk  # sudo dnf install python3-pillow-tk
from tkinter import ttk, messagebox
import sqlite3
import re


class productClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+240+140")
        self.root.resizable(False, False)
        self.root.title("Inventory Management System | Product Window")
        self.root.config(bg="white")
        self.root.focus_force()

        # ====================All variables===================
        self.var_category = StringVar()
        self.var_supplier = StringVar()
        self.cat_list = []
        self.sup_list = []
        self.fetch_cat_sup()
        self.var_name = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_status = StringVar()

        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        # ===========Left Frame========================
        productFrame = Frame(self.root, bd=1, relief=RIDGE, bg="white")
        productFrame.place(x=10, y=10, width=400, height=480)

        # ===========Left Frame Title=============
        title = Label(productFrame, text="Manage Product Details", font=(
            "goudy old style", 15), bg="blue", fg="white").place(x=0, y=0, width=400, height=30)
        # =====================================================================================
        lbl_category = Label(productFrame, text="Category :", font=(
            "goudy old style", 15), bg="white").place(x=20, y=60)

        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        cur.execute("SELECT NAME FROM CATEGORY")
        row = cur.fetchall()

        cmb_category = ttk.Combobox(productFrame, textvariable=self.var_category, values=self.cat_list,
                                    state="readonly", justify=CENTER, font=("goudy old style", 15))
        cmb_category.place(x=150, y=60, width=170)
        cmb_category.current(0)
        # ======================================================================================
        lbl_supplier = Label(productFrame, text="Supplier :", font=(
            "goudy old style", 15), bg="white").place(x=20, y=110)

        cmb_supplier = ttk.Combobox(productFrame, textvariable=self.var_supplier, values=self.sup_list,
                                    state="readonly", justify=CENTER, font=("goudy old style", 15))
        cmb_supplier.place(x=150, y=110, width=170)
        cmb_supplier.current(0)
        # =====================================================================================
        lbl_name = Label(productFrame, text="Name :", font=(
            "goudy old style", 15), bg="white").place(x=20, y=160)
        txt_name = Entry(productFrame, textvariable=self.var_name, font=(
            "goudy old style", 15), bg="lightyellow").place(x=150, y=160, width=170)
        # =======================================================================================
        lbl_price = Label(productFrame, text="Price :", font=(
            "goudy old style", 15), bg="white").place(x=20, y=210)
        txt_price = Entry(productFrame, textvariable=self.var_price, font=(
            "goudy old style", 15), bg="lightyellow").place(x=150, y=210, width=170)
        # =======================================================================================
        lbl_qty = Label(productFrame, text="QTY :", font=(
            "goudy old style", 15), bg="white").place(x=20, y=260)
        txt_qty = Entry(productFrame, textvariable=self.var_qty, font=(
            "goudy old style", 15), bg="lightyellow").place(x=150, y=260, width=170)
        # =======================================================================================
        lbl_status = Label(productFrame, text="Status :", font=(
            "goudy old style", 15), bg="white").place(x=20, y=310)

        cmb_status = ttk.Combobox(productFrame, textvariable=self.var_status, values=("ACTIVE", "INACTIVE"),
                                  state="readonly", justify=CENTER, font=("goudy old style", 15))
        cmb_status.place(x=150, y=310, width=170)
        cmb_status.current(0)

        # ===========Buttons===================================================================
        btn_save = Button(self.root, text="Save", command=self.save, cursor="hand2", font=(
            "goudy old style", 12), bg="#C70039", fg="white").place(x=15, y=400, height=40, width=90)
        btn_update = Button(self.root, text="Update", command=self.update, cursor="hand2", font=(
            "goudy old style", 12), bg="#1E8449", fg="white").place(x=115, y=400, height=40, width=90)
        btn_delete = Button(self.root, command=self.delete, text="Delete", cursor="hand2", font=(
            "goudy old style", 12), bg="#34495E", fg="white").place(x=215, y=400, height=40, width=90)
        btn_Clear = Button(self.root, command=self.clear, text="Clear", cursor="hand2", font=(
            "goudy old style", 12), bg="#6C3483", fg="white").place(x=315, y=400, height=40, width=90)

        # =============================Search Frame===========================================
        SeacrhFrame = LabelFrame(self.root, text="Search Product", bg="white", font=(
            "goudy old style", 12, "bold"), bd=2, relief=RIDGE)
        SeacrhFrame.place(x=430, y=10, width=650, height=70)

        # =======options======
        cmbSupplier = ttk.Combobox(SeacrhFrame, textvariable=self.var_searchby, values=("Select", "Category", "Supplier", "Name"),
                                   state="readonly", justify=CENTER, font=("goudy old style", 15))
        cmbSupplier.place(x=10, y=10, width=180)
        cmbSupplier.current(0)

        txt_search = Entry(SeacrhFrame,  textvariable=self.var_searchtxt, font=(
            "goudy old style", 15), bg="lightyellow").place(x=200, y=9, width=290)
        btn_Search = Button(SeacrhFrame,  command=self.search, text="Search", cursor="hand2", font=(
            "goudy old style", 15), bg="#424949", fg="white").place(x=500, y=9, width=130, height=30)

        # =============Product Details=========
        prod_frame = Frame(self.root, bd=1, relief=RIDGE, bg="lightblue")
        prod_frame.place(x=430, y=100, width=650, height=390)

        scrolly = Scrollbar(prod_frame, orient=VERTICAL)
        scrollx = Scrollbar(prod_frame, orient=HORIZONTAL)

        self.productTable = ttk.Treeview(prod_frame, columns=(
            "P_ID", "CATEGORY", "SUPPLIER", "NAME", "PRICE", "QTY", "STATUS"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)

        scrollx.config(command=self.productTable.xview)
        scrolly.config(command=self.productTable.yview)

        self.productTable.heading("P_ID", text="Product ID")
        self.productTable.heading("CATEGORY", text="CATEGORY")
        self.productTable.heading("SUPPLIER", text="SUPPLIER")
        self.productTable.heading("NAME", text="NAME")
        self.productTable.heading("PRICE", text="PRICE")
        self.productTable.heading("QTY", text="QTY")
        self.productTable.heading("STATUS", text="STATUS")

        self.productTable["show"] = "headings"

        self.productTable.column("P_ID", width=90)
        self.productTable.column("CATEGORY", width=100)
        self.productTable.column("SUPPLIER", width=100)
        self.productTable.column("NAME", width=100)
        self.productTable.column("PRICE", width=100)
        self.productTable.column("QTY", width=100)
        self.productTable.column("STATUS", width=100)

        self.productTable.pack(fill=BOTH, expand=1)
        self.productTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()

        self.fetch_cat_sup()
# ======================fetch CATEGORY & SUPPLIER=======================

    def fetch_cat_sup(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT NAME FROM CATEGORY")
            cat = cur.fetchall()
            if len(cat) > 0:
                self.cat_list.append("Select")
                for i in cat:
                    self.cat_list.append(i[0])
            else:
                self.cat_list.append("Empty")

            cur.execute("SELECT NAME FROM SUPPLIER")
            sup = cur.fetchall()
            if len(sup) > 0:
                self.sup_list.append("Select")
                for i in sup:
                    self.sup_list.append(i[0])
            else:
                self.sup_list.append("Empty")

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")
# ==========================SAVE PRODUCT==========================================

    def save(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_category.get() == "Select" or self.var_supplier.get() == "Select" or self.var_name.get() == "":
                messagebox.showerror(
                    "Error", "All Fields Are required", parent=self.root)
            else:
                cur.execute("Select * from PRODUCT where NAME=?",
                            (self.var_name.get(),))
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror(
                        "Error", "Product Already Listed, try different", parent=self.root)
                else:
                    cur.execute(
                        "INSERT INTO PRODUCT (CATEGORY, SUPPLIER, NAME, PRICE, QTY,STATUS) values(?,?,?,?,?,?)", (
                            self.var_category.get(),
                            self.var_supplier.get(),
                            self.var_name.get(),
                            self.var_price.get(),
                            self.var_qty.get(),
                            self.var_status.get()
                        ))
                    con.commit()
                    messagebox.showinfo(
                        "Success", "Product Added", parent=self.root)
                    self.show()
                    self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")

# ===================Show details in Treeview=================

    def show(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM PRODUCT")
            rows = cur.fetchall()
            self.productTable.delete(*self.productTable.get_children())
            for row in rows:
                self.productTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")

# ===================Get Data from Database and show into textbox===============

    def get_data(self, ev):
        f = self.productTable.focus()
        content = (self.productTable.item(f))
        row = content['values']
        self.var_category.set(row[1]),
        self.var_supplier.set(row[2]),
        self.var_name.set(row[3]),
        self.var_price.set(row[4]),
        self.var_qty.set(row[5]),
        self.var_status.set(row[6]),

        # self.txt_supplier_invoice.configure(state='disabled')

# ========================Update details===========================

    def update(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_category.get() == "Select" or self.var_supplier.get() == "Select" or self.var_name.get() == "":
                messagebox.showerror(
                    "Error", "All Fields Are required", parent=self.root)
            else:
                cur.execute("Select * from PRODUCT where NAME=?",
                            (self.var_name.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror(
                        "Error", "Product Not Found", parent=self.root)
                else:
                    cur.execute(
                        "UPDATE PRODUCT set CATEGORY=?, SUPPLIER=?, PRICE=?, QTY=?, STATUS=? WHERE NAME=?", (
                            self.var_category.get(),
                            self.var_supplier.get(),
                            self.var_price.get(),
                            self.var_qty.get(),
                            self.var_status.get(),
                            self.var_name.get()

                        ))
                    con.commit()
                    messagebox.showinfo(
                        "Success", "Product Details Updated", parent=self.root)

                    self.show()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")

# ===============Delete details from database==================

    def delete(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_name.get() == "":
                messagebox.showerror(
                    "Error", "Please Select Product", parent=self.root)
            else:
                cur.execute("Select * from PRODUCT where NAME=?",
                            (self.var_name.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror(
                        "Error", "Product Not Found", parent=self.root)
                else:
                    op = messagebox.askyesno(
                        "Confirm", "Do You Really Want To Delete?", parent=self.root)
                    if op == True:
                        cur.execute("DELETE FROM PRODUCT WHERE NAME=?",
                                    (self.var_name.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Product Removed",
                                            parent=self.root)
                        self.clear()
                        self.show()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")

# ================Clear textboxes========================

    def clear(self):
        self.var_category.set("Select"),
        self.var_supplier.set("Select"),
        self.var_name.set(""),
        self.var_price.set(""),
        self.var_qty.set(""),
        self.var_status.set("ACTIVE"),

        self.var_searchtxt.set(""),
        self.var_searchby.set("Select")
        self.show()

        # self.txt_supplier_invoice.configure(state=NORMAL)

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
                cur.execute("SELECT * FROM PRODUCT WHERE " +
                            self.var_searchby.get()+" LIKE '%"+self.var_searchtxt.get()+"%'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.productTable.delete(
                        *self.productTable.get_children())
                    for row in rows:
                        self.productTable.insert('', END, values=row)
                else:
                    messagebox.showerror(
                        "Error", "No Record Found!!!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")


if __name__ == "__main__":
    root = Tk()
    obj = productClass(root)
    root.mainloop()
