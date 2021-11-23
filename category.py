# from os import WIFSTOPPED
from sqlite3.dbapi2 import SQLITE_OK
from tkinter import*
from tkinter import font
from typing import Pattern
from PIL import Image, ImageTk  # sudo dnf install python3-pillow-tk
from tkinter import ttk, messagebox
import sqlite3
import re


class categoryClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+240+140")
        self.root.title("Inventory Management System | Category Window")
        self.root.config(bg="white")
        self.root.focus_force()

        # ====================All variables===================
        self.var_category_name = StringVar()

        # ===========Title=============
        title = Label(self.root, text="Manage Product Category", font=(
            "goudy old style", 22), bg="#0f4d7d", fg="white").place(x=50, y=10, width=1000, height=60)

        # ===========Other Contents============
        lbl_category_name = Label(
            self.root, text="Enter Category Name :", font=("new times roman", 15), bg="white")
        lbl_category_name.place(x=80, y=110)

        txt_category = Entry(self.root, textvariable=self.var_category_name, font=(
            "goudy old style", 15), bg="lightyellow").place(x=80, y=170, width=270)

        btn_add = Button(self.root, command=self.add, text="ADD", cursor="hand2", font=(
            "goudy old style", 15), bg="#424949", fg="white").place(x=370, y=170, width=100, height=30)
        btn_delete = Button(self.root, command=self.delete, text="DELETE", cursor="hand2", font=(
            "goudy old style", 15), bg="#438949", fg="white").place(x=490, y=170, width=100, height=30)

        # =============Category Details=========
        categoryFrame = Frame(self.root, bd=1, relief=RIDGE, bg="lightblue")
        categoryFrame.place(x=690, y=90, width=360, height=400)

        scrolly = Scrollbar(categoryFrame, orient=VERTICAL)
        scrollx = Scrollbar(categoryFrame, orient=HORIZONTAL)

        self.categoryTable = ttk.Treeview(categoryFrame, columns=(
            "CID", "NAME"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)

        scrollx.config(command=self.categoryTable.xview)
        scrolly.config(command=self.categoryTable.yview)

        self.categoryTable.heading("CID", text="CID")
        self.categoryTable.heading("NAME", text="NAME")

        self.categoryTable["show"] = "headings"

        self.categoryTable.column("CID", width=90)
        self.categoryTable.column("NAME", width=100)

        self.categoryTable.pack(fill=BOTH, expand=1)
        self.categoryTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    # ================Images================
        self.image = Image.open("images/category22.jpg")
        self.image = self.image.resize((400, 250), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(self.image)

        self.lbl_image = Label(self.root, image=self.image, borderwidth=0,
                               compound="center", highlightthickness=0).place(x=100, y=220)

    # ========================================================================================================
    # ==============Add Category================================

    def add(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_category_name.get() == "":
                messagebox.showerror(
                    "Error", "Please Enter Category Name", parent=self.root)
            else:
                cur.execute("Select * from CATEGORY where NAME=?",
                            (self.var_category_name.get(),))
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror(
                        "Error", "This Category Already Listed, Try Different", parent=self.root)
                else:
                    cur.execute(
                        "INSERT INTO CATEGORY (NAME) values(?)", (self.var_category_name.get(),))
                    con.commit()
                    messagebox.showinfo(
                        "Success", "Category Added", parent=self.root)
                    self.show()
                    self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")

    # ===================Show details in Treeview=================

    def show(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM CATEGORY")
            rows = cur.fetchall()
            self.categoryTable.delete(*self.categoryTable.get_children())
            for row in rows:
                self.categoryTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")

    def get_data(self, ev):
        f = self.categoryTable.focus()
        content = (self.categoryTable.item(f))
        row = content['values']
        # self.var_supplier_invoice.set(row[0]),
        self.var_category_name.set(row[1])

    # ===============Delete details from database==================

    def delete(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_category_name.get() == "":
                messagebox.showerror(
                    "Error", "Please Select Any Category", parent=self.root)
            else:
                cur.execute("Select * from CATEGORY where NAME=?",
                            (self.var_category_name.get(),))
                row = cur.fetchone()
                if row != None:
                    op = messagebox.askyesno(
                        "Confirm", "Do You Really Want To Delete?", parent=self.root)
                    if op == True:
                        cur.execute("DELETE FROM CATEGORY WHERE NAME=?",
                                    (self.var_category_name.get(),))
                        con.commit()
                        messagebox.showinfo("Successful", "Category Deleted",
                                            parent=self.root)
                        self.clear()
                else:
                    messagebox.showerror(
                        "Error", "Category Not Found", parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")
    # ====================Clear Textbox================

    def clear(self):
        self.var_category_name.set(""),

        self.show()


if __name__ == "__main__":
    root = Tk()
    obj = categoryClass(root)
    root.mainloop()
