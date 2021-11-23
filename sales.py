from sqlite3.dbapi2 import SQLITE_OK
from tkinter import*
from tkinter import font
from typing import Pattern
from PIL import Image, ImageTk  # sudo dnf install python3-pillow-tk
from tkinter import ttk, messagebox
import sqlite3
import os


class salesClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+240+140")
        self.root.title("Inventory Management System | Sales Window")
        self.root.config(bg="white")
        self.root.focus_force()

        # ============Variables===================
        self.var_invoice = StringVar()
        self.bill_list = []

        # ===========Title=============
        title = Label(self.root, text="Customer Bill Report", font=(
            "goudy old style", 22), bg="#0f4d7d", fg="white").place(x=0, y=10, width=1100, height=50)

        # =========Search=======================
        lbl_sales_invoice = Label(self.root, text="Invoice No.", font=(
            "goudy old style", 15), bg="white").place(x=50, y=90)

        self.txt_sales_invoice = Entry(self.root, textvariable=self.var_invoice, font=(
            "goudy old style", 15), bg="lightyellow")
        self.txt_sales_invoice.place(x=170, y=90, width=190)

        btn_Search = Button(self.root,  command=self.search, text="Search", cursor="hand2", font=(
            "goudy old style", 15), bg="#424949", fg="white").place(x=380, y=90, width=130, height=30)
        btn_clear = Button(self.root,  command=self.clear, text="Clear", cursor="hand2", font=(
            "goudy old style", 15), bg="#522920", fg="white").place(x=530, y=90, width=130, height=30)

        # =================Left Frame======================

        leftBox = Frame(self.root, bd=0,
                        relief=RIDGE, bg="lightblue")
        leftBox.place(x=50, y=140, width=300, height=350)
        scrolly = Scrollbar(leftBox, orient=VERTICAL)
        self.salesList = Listbox(leftBox, font=(
            "goudy old style", 15), bg="white", yscrollcommand=scrolly.set)
        scrolly.pack(side=RIGHT, fill=Y)
        scrolly.config(command=self.salesList.yview)
        self.salesList.pack(fill=BOTH, expand=1)
        self.salesList.bind("<ButtonRelease-1>", self.getBill)

        # =================Right Frame======================

        rightBox = Frame(self.root, bd=1,
                         relief=RIDGE, bg="white",)
        rightBox.place(x=400, y=140, width=360, height=350)
        lbl_rightBox = Label(rightBox, text="Customer Billing Area", font=(
            "Times New Roman", 18, "bold"), bg="lightgreen").pack(side=TOP, fill=X)

        scrolly2 = Scrollbar(rightBox, orient=VERTICAL)

        self.billArea = Text(rightBox, bg="lightyellow",
                             yscrollcommand=scrolly2.set)

        scrolly2.pack(side=RIGHT, fill=Y)
        scrolly2.config(command=self.billArea.yview)
        self.billArea.pack(fill=BOTH, expand=1)

        # ==================Image======================
        self.rightImage = Image.open("images/bill.jpg")
        self.rightImage = self.rightImage.resize(
            (270, 250), Image.ANTIALIAS)
        self.rightImage = ImageTk.PhotoImage(self.rightImage)

        lbl_image = Label(self.root, image=self.rightImage,
                          bd=0, relief=RIDGE).place(x=810, y=250)

        self.showBill()


# ====================Functions=============================

    def showBill(self):
        del self.bill_list[:]
        self.salesList.delete(0, END)
        for i in os.listdir('bill'):
            if i.split('.')[-1] == 'txt':
                self.salesList.insert(END, i)
                self.bill_list.append(i.split('.')[0])

    def getBill(self, ev):
        self.billArea.config(state=NORMAL)
        self.billArea.delete('1.0', END)
        index_ = self.salesList.curselection()
        file_name = self.salesList.get(index_)
        self.billArea.delete('1.0', END)
        fp = open(f'bill/{file_name}', 'r')
        for i in fp:
            self.billArea.insert(END, i)

        self.billArea.config(state="disabled")
        fp.close()

    def search(self):
        if self.var_invoice.get() == "":
            messagebox.showerror(
                "Error", "Invoice No Required!!", parent=self.root)
        else:
            if self.var_invoice.get() in self.bill_list:
                fp = open(f'bill/{self.var_invoice.get()}.txt', 'r')
                self.billArea.delete('1.0', END)
                for i in fp:
                    self.billArea.insert(END, i)
                fp.close()
            else:
                messagebox.showerror("Error", "Not Found")

    def clear(self):
        self.showBill(),
        self.billArea.delete('1.0', END),
        self.var_invoice.set("")


if __name__ == "__main__":
    root = Tk()
    obj = salesClass(root)
    root.mainloop()
