from datetime import date
from sqlite3.dbapi2 import Date, paramstyle, version
from tkinter import*
from tkinter import font
from tkinter.font import Font
from typing import Sized
# import PIL
from PIL import Image, ImageTk  # sudo dnf install python3-pillow-tk
from tkinter import ttk, messagebox
import sqlite3
import time
import os
import sys
import subprocess
import tempfile


class billing:
    def __init__(self, root):
        self.root = root
        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()
        # self.root.attributes("-fullscreen", True)
        # setting tkinter window size
        self.root.geometry("%dx%d+0+0" % (width, height))
        self.root.title("Inventory Management System | Developed By SD")
        self.root.config(bg="white")

        # =================================Variables==================================
        self.cart_list = []
        self.chk_print = 0

        self.icon_title = Image.open('images/logo1.png')
        resize_image = self.icon_title.resize((60, 50), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(resize_image)

        title = Label(self.root, text="Inventory Management System", image=self.img, compound=LEFT, font=(
            "times new roman", 40, "bold"), bg="#010c48", fg="white", anchor="w", padx=20).place(x=0, y=0, relwidth=1, height=70)
        # ====Button Logout====
        btn_logout = Button(self.root, command=self.logout, text="Logout", font=(
            "times new roman", 15, "bold"), bg="yellow", cursor="hand2").place(x=1200, y=10, height=50, width=150)

        # ===Second Label===
        self.lbl_dateTime = Label(self.root, text="Welcome to my First Project\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS", font=(
            "times new roman", 15, "bold"), bg="#4d636d", fg="white")
        self.lbl_dateTime.place(x=0, y=70, relwidth=1, height=30)
        # ===================Frame 1===================================================
        productFrame1 = Frame(self.root, bd=0, relief=RIDGE, bg="white")
        productFrame1.place(x=10, y=105, width=420, height=555)

        lbl_allProduct = Label(productFrame1, text="All Products", bg="ORANGE", font=(
            "New Times Roman", 15, "bold")).pack(side=TOP, fill=X)

        productFrame2 = Frame(productFrame1, bd=2, relief=RIDGE,
                              bg="#CAB8FF")
        productFrame2.place(x=0, y=30, width=420, height=80)

        self.var_searchName = StringVar()  # Search Entry Variable

        lbl1_name = Label(productFrame2,  text="Search Product | By Name", bg="#CAB8FF", fg="green", font=(
            "New Times Roman", 12, "bold",)).place(x=5, y=5)

        btn1_showALL = Button(productFrame2,  command=self.show, text="Show All", font=(
            "times new roman", 12), bg="#334756", fg="white", bd=2, cursor="hand2").place(x=320, y=5, width=90, height=30)

        lbl2_productName = Label(productFrame2, text="Product Name", bg="#CAB8FF", font=(
            "New Times Roman", 12, "bold",)).place(x=5, y=40)
        entry_productName = Entry(
            productFrame2, textvariable=self.var_searchName, bg="lightyellow").place(x=150, y=40, width=150, height=30)
        btn2_productFrame2 = Button(productFrame2, command=self.search, text="Search", font=(
            "times new roman", 12), bg="#055052", fg="white", bd=2, cursor="hand2").place(x=320, y=40, width=90, height=30)

        # =============Product Details Treeview=========
        prod_frame = Frame(productFrame1, bd=0, relief=RIDGE, bg="lightblue")
        prod_frame.place(x=0, y=120, width=420, height=430)

        scrolly = Scrollbar(prod_frame, orient=VERTICAL)
        scrollx = Scrollbar(prod_frame, orient=HORIZONTAL)

        self.productTable = ttk.Treeview(prod_frame, columns=(
            "P_ID", "NAME", "PRICE", "QTY", "STATUS"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)

        scrollx.config(command=self.productTable.xview)
        scrolly.config(command=self.productTable.yview)

        self.productTable.heading("P_ID", text="PID")
        self.productTable.heading("NAME", text="NAME")
        self.productTable.heading("PRICE", text="PRICE")
        self.productTable.heading("QTY", text="QTY")
        self.productTable.heading("STATUS", text="STATUS")

        self.productTable["show"] = "headings"

        self.productTable.column("P_ID", width=50)
        self.productTable.column("NAME", width=100)
        self.productTable.column("PRICE", width=90)
        self.productTable.column("QTY", width=70)
        self.productTable.column("STATUS", width=80)

        self.productTable.pack(fill=BOTH, expand=1)
        self.productTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()

        # ===========ProductFrame1 Footer Label=====================

        # ===============Frame 2==============================================
        self.cust_name = StringVar()
        self.cust_contact = StringVar()

        productFrame3 = Frame(self.root, bd=0, relief=RIDGE, bg="white")
        productFrame3.place(x=440, y=105, width=550, height=555)

        sub_productFrame3 = Frame(
            productFrame3, bd=2, relief=RIDGE, bg="#87AAAA")
        sub_productFrame3.place(x=0, y=0, width=547, height=70)

        lbl_customer = Label(sub_productFrame3, text="Customer Details", bg="#89B5AF", font=(
            "New Times Roman", 15, "bold")).pack(side=TOP, fill=X)
        lbl_name = Label(sub_productFrame3, text="Name :", bg="#87AAAA", font=(
            "New Times Roman", 12))
        lbl_name.place(x=5, y=35)

        txt_name = Entry(
            productFrame3, textvariable=self.cust_name, bg="#FFF9B6")
        txt_name.place(x=80, y=35, width=150)

        lbl_contact = Label(sub_productFrame3, text="Contact No :", bg="#87AAAA", font=(
            "New Times Roman", 12))
        lbl_contact.place(x=250, y=35)

        txt_contact = Entry(
            sub_productFrame3, textvariable=self.cust_contact, bg="#FFF9B6")
        txt_contact.place(x=370, y=35, width=150)

        # ================================Calculator Frame=========================================
        calcFrame = Frame(
            productFrame3, bd=4, relief=RIDGE, bg="white")
        calcFrame.place(x=0, y=80, width=265, height=360)
        self.var_calcInput = StringVar()

        txt_calcInput = Entry(
            calcFrame, textvariable=self.var_calcInput, font=('arial', 15, 'bold'), width=22, bd=7, relief=GROOVE, state='readonly', justify=RIGHT)
        txt_calcInput.grid(row=0, columnspan=4, ipady=20)

        btn7 = Button(calcFrame, text="7", command=lambda: self.get_input(7), font=(
            "arial", 15, "bold"), bd=2, width=4, pady=14,  cursor="hand2").grid(row=1, column=0)
        btn8 = Button(calcFrame, text="8", command=lambda: self.get_input(8), font=(
            "arial", 15, "bold"), bd=2, width=4, pady=14,  cursor="hand2").grid(row=1, column=1)
        btn9 = Button(calcFrame, text="9", command=lambda: self.get_input(9), font=(
            "arial", 15, "bold"), bd=2, width=4, pady=14,  cursor="hand2").grid(row=1, column=2)
        btn_sum = Button(calcFrame, text="+", command=lambda: self.get_input('+'), font=(
            "arial", 15, "bold"), bd=2, width=4, pady=14,  cursor="hand2").grid(row=1, column=3)

        btn4 = Button(calcFrame, command=lambda: self.get_input(4), text="4", font=(
            "arial", 15, "bold"), bd=2, width=4, pady=14, cursor="hand2").grid(row=2, column=0)
        btn5 = Button(calcFrame, command=lambda: self.get_input(5), text="5", font=(
            "arial", 15, "bold"), bd=2, width=4, pady=14, cursor="hand2").grid(row=2, column=1)
        btn6 = Button(calcFrame, command=lambda: self.get_input(6), text="6", font=(
            "arial", 15, "bold"), bd=2, width=4, pady=14, cursor="hand2").grid(row=2, column=2)
        btn_sub = Button(calcFrame, command=lambda: self.get_input('-'), text="-", font=(
            "arial", 15, "bold"), bd=2, width=4, pady=14, cursor="hand2").grid(row=2, column=3)

        btn1 = Button(calcFrame, command=lambda: self.get_input(1), text="1", font=(
            "arial", 15, "bold"), bd=2, width=4, pady=14, cursor="hand2").grid(row=3, column=0)
        btn2 = Button(calcFrame, command=lambda: self.get_input(2), text="2", font=(
            "arial", 15, "bold"), bd=2, width=4, pady=14, cursor="hand2").grid(row=3, column=1)
        btn3 = Button(calcFrame, command=lambda: self.get_input(3), text="3", font=(
            "arial", 15, "bold"), bd=2, width=4, pady=14, cursor="hand2").grid(row=3, column=2)
        btn_mul = Button(calcFrame, command=lambda: self.get_input('*'), text="*", font=(
            "arial", 15, "bold"), bd=2, width=4, pady=14, cursor="hand2").grid(row=3, column=3)

        btn0 = Button(calcFrame, command=lambda: self.get_input(0), text="0", font=(
            "arial", 15, "bold"), bd=2, width=4, pady=13, cursor="hand2").grid(row=4, column=0)
        btn_c = Button(calcFrame, command=self.calcClear, text="C", font=(
            "arial", 15, "bold"), bd=2, width=4, pady=13, cursor="hand2").grid(row=4, column=1)
        btn_eq = Button(calcFrame,  command=self.calc_Operations, text='=', font=(
            "arial", 15, "bold"), bd=2, width=4, pady=13, cursor="hand2").grid(row=4, column=2)
        btn_div = Button(calcFrame, command=lambda: self.get_input('/'), text="/", font=(
            "arial", 15, "bold"), bd=2, width=4, pady=13, cursor="hand2").grid(row=4, column=3)

        # ===================Cart Frame==========================================
        cartFrame = Frame(productFrame3, bd=0, relief=RIDGE,
                          bg="white")
        cartFrame.place(x=270, y=80, width=275, height=365)
        self.lbl_cartFrame = Label(
            cartFrame, text="Cart\tTotal Product: [0]", font=("arial", 12, "bold"))
        self.lbl_cartFrame.pack(side=TOP, fill=X)

        # =============Cart Details Treeview=========
        cartFrame_tree = Frame(cartFrame, bd=0, bg="lightblue")
        cartFrame_tree.place(x=0, y=30, width=274, height=330)

        scrolly = Scrollbar(cartFrame_tree, orient=VERTICAL)
        scrollx = Scrollbar(cartFrame_tree, orient=HORIZONTAL)

        self.productTable2 = ttk.Treeview(cartFrame_tree, columns=(
            "P_ID", "NAME", "PRICE", "QTY"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)

        scrollx.config(command=self.productTable2.xview)
        scrolly.config(command=self.productTable2.yview)

        self.productTable2.heading("P_ID", text="PID")
        self.productTable2.heading("NAME", text="NAME")
        self.productTable2.heading("PRICE", text="PRICE")
        self.productTable2.heading("QTY", text="QTY")

        self.productTable2["show"] = "headings"

        self.productTable2.column("P_ID", width=50)
        self.productTable2.column("NAME", width=100)
        self.productTable2.column("PRICE", width=100)
        self.productTable2.column("QTY", width=70)

        self.productTable2.pack(fill=BOTH, expand=1)
        self.productTable2.bind("<ButtonRelease-1>", self.cart_get_data)

        # ============================Cart Frame 2===============================
        self.var_pid = StringVar()
        self.var_ProdName = StringVar()
        self.var_PPQty = StringVar()
        self.var_qty = StringVar()
        self.var_stock = StringVar()

        cartFrame2 = Frame(productFrame3, bd=1, relief=RIDGE, bg="#CDF2CA")
        cartFrame2.place(x=0, y=450, width=547, height=100)

        lbl_ProdName = Label(cartFrame2, text="Product Name", bg="#CDF2CA", font=(
            "New Times Roman", 12)).place(x=10, y=10)

        lbl_PPQty = Label(cartFrame2, text="Price Per QTY", bg="#CDF2CA", font=(
            "New Times Roman", 12)).place(x=200, y=10)

        lbl_name = Label(cartFrame2, text="Quantity", bg="#CDF2CA", font=(
            "New Times Roman", 12))
        lbl_name.place(x=380, y=10)

        txt_ProdName = Entry(
            cartFrame2, textvariable=self.var_ProdName, bg="#FFF9B6", state='disabled')
        txt_ProdName.place(x=10, y=35, width=150)

        txt_PPQty = Entry(
            cartFrame2, textvariable=self.var_PPQty, bg="#FFF9B6", state='disabled')
        txt_PPQty.place(x=200, y=35, width=150)

        txt_qty = Entry(
            cartFrame2, textvariable=self.var_qty, bg="#FFF9B6")
        txt_qty.place(x=380, y=35, width=150)

        self.lbl_stock = Label(cartFrame2,  bg="#CDF2CA", font=(
            "New Times Roman", 12))
        self.lbl_stock.place(x=10, y=70)

        btn1_cart_clear = Button(cartFrame2, command=self.cart_clear, text="Clear", font=(
            "times new roman", 12), bg="#66806A", bd=3, cursor="hand2").place(x=180, y=65, width=100, height=30)
        btn2_remove = Button(cartFrame2, command=self.remove_cart, text="Remove", font=(
            "times new roman", 12), bg="#66806A", bd=3, cursor="hand2").place(x=280, y=65, width=100, height=30)
        btn2_add_update_cart = Button(cartFrame2, command=self.add_update_cart, text="Add/Update Cart", font=(
            "times new roman", 12), bg="#66806A", bd=3, cursor="hand2").place(x=380, y=65, width=150, height=30)

        # ===========================Product Frame 4/Billing Area===================================

        productFrame4 = Frame(self.root, bd=0, relief=RIDGE, bg="white")
        productFrame4.place(x=1000, y=105, width=360, height=555)

        lbl_productFrame4 = Label(productFrame4, text="Customer Billing Area", font=(
            "Times New Roman", 16, "bold"), bg="red").pack(side=TOP, fill=X)
        sub_productFrame4 = Frame(
            productFrame4, bd=2, relief=RIDGE, bg="lightblue")
        sub_productFrame4.place(x=0, y=30, height=410, width=360)
        scrolly = Scrollbar(sub_productFrame4, orient=VERTICAL)
        scrolly.pack(side=RIGHT, fill=Y)
        self.txt_billArea = Text(sub_productFrame4, yscrollcommand=scrolly.set)
        self.txt_billArea.pack(fill=BOTH, expand=1)

        scrolly.config(command=self.txt_billArea.yview)
        sub_productFrame4_2 = Frame(
            productFrame4, bd=0, relief=RIDGE, bg="white")

        sub_productFrame4_2.place(x=0, y=445, width=360, height=105)

        self.lbl_billAmnt = Label(sub_productFrame4_2, text="Bill Amount\n0", font=(
            "Times New Roman", 11, "bold"), bg="#C85C5C")
        self.lbl_billAmnt.place(x=0, y=0, width=125, height=55)
        self.lbl_discount = Label(sub_productFrame4_2, text="Discount\n5%", font=(
            "Times New Roman", 11, "bold"), width=12, bg="#34BE82")
        self.lbl_discount.place(x=130, y=0, width=100, height=55)
        self.lbl_netPay = Label(sub_productFrame4_2, text="Net Pay\n0", font=(
            "Times New Roman", 11, "bold"), width=13, bg="#9D84B7")
        self.lbl_netPay.place(x=235, y=0, width=125, height=55)

        btn_print = Button(sub_productFrame4_2, command=self.print_bill, bd=4, text="Print", font=(
            "Times New Roman", 12, "bold"), width=9, bg="#181D31", fg="white").place(x=0, y=60, width=115, height=45)

        btn_clear_all = Button(sub_productFrame4_2, command=self.clear_all, bd=4, text="Clear All", font=(
            "Times New Roman", 12, "bold"), width=9, bg="#105652", fg="white").place(x=120, y=60, width=115, height=45)
        btn_generate = Button(sub_productFrame4_2, command=self.generate_bill, bd=4, text="Generate\nSave Bill", font=(
            "Times New Roman", 12, "bold"), width=9, bg="#181D31", fg="white").place(x=240, y=60, width=120, height=45)

        # ===Footer===
        label_footer = Label(self.root, text="Inventory Management System | Developed By- CrabyTech\nFor any issue contact: 7407038247", font=(
            "times new roman", 12, "bold"), bg="#4d636d", fg="white").pack(side=BOTTOM, fill=X)

        self.update_dateTime()

# ==================All Functions==================================
# =====================Product Frame Functions======================
# ==============Search product=====================================

    def search(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_searchName.get() == "":
                messagebox.showerror("Error", "Name Required")
            else:
                cur.execute("SELECT P_ID,NAME,PRICE,QTY,STATUS FROM PRODUCT WHERE STATUS='ACTIVE' AND NAME LIKE'%" +
                            self.var_searchName.get()+"%'")
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
# ============Get Data From Treeview and add to cart===================

    def get_data(self, ev):
        f = self.productTable.focus()
        content = (self.productTable.item(f))
        row = content['values']
        self.var_pid.set(row[0]),
        self.var_ProdName.set(row[1]),
        self.var_PPQty.set(row[2]),
        self.var_qty.set("1")
        if row[3] > 0:
            self.lbl_stock.config(text=f"In Stock[{str(row[3])}]")
            self.var_stock.set(row[3])
            # messagebox.showinfo("", self.var_stock.get())
        else:
            self.var_stock.set('0')
            self.lbl_stock["text"] = "Out Of Stock"

            # =====================Show Data from Database in TREEVIEW 1===================

    def show(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute(
                "SELECT P_ID, NAME, PRICE,QTY,STATUS FROM PRODUCT WHERE STATUS='ACTIVE'")
            rows = cur.fetchall()
            self.productTable.delete(*self.productTable.get_children())
            for row in rows:
                self.productTable.insert('', END, values=row)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")

# ==============Calculator Functions===================================
    def get_input(self, num):
        xnum = self.var_calcInput.get()+str(num)
        self.var_calcInput.set(xnum)

    def calcClear(self):
        self.var_calcInput.set("")

    def calc_Operations(self):
        result = self.var_calcInput.get()
        self.var_calcInput.set(eval(result))

# ===================Add/Update cart============================
    def add_update_cart(self):
        try:
            if self.var_PPQty.get() == "":
                messagebox.showerror(
                    "Error", "Please Select any Product", parent=self.root)
            elif self.var_qty.get() == "" or self.var_qty.get() == "0":
                messagebox.showerror(
                    "Error", "Please Enter Quantity", parent=self.root)
            elif self.var_stock.get() == '0':
                messagebox.showerror(
                    "Out Of Stock", "Product Not Available!!", parent=self.root)
            elif int(self.var_stock.get()) < int(self.var_qty.get()):
                messagebox.showerror(
                    "Error", "Invalid Quantity!!", parent=self.root)
            else:
                price_cal = float(int(self.var_qty.get()) *
                                  float(self.var_PPQty.get()))
                cart_data = [self.var_pid.get(), self.var_ProdName.get(),
                             price_cal, self.var_qty.get(), self.var_stock.get()]

                # ============Update Cart============
                present = 'no'
                index_ = 0
                for row in self.cart_list:
                    if self.var_pid.get() == row[0]:
                        present = 'yes'
                        break
                    index_ += 1
                if present == 'yes':  # outside the for loop
                    op = messagebox.askyesno(
                        'Confirm', 'Product Already Present\nProceed to update', parent=self.root)
                    if op == True:
                        self.cart_list[index_][2] = price_cal
                        self.cart_list[index_][3] = self.var_qty.get()
                else:
                    self.cart_list.append(cart_data)
                self.cart_show()
                self.bill_updates()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")

    def remove_cart(self):
        if self.var_ProdName.get() == "":
            messagebox.showerror("Error", "Please Select Product From Cart!!")
        else:
            present = 'no'
            index_ = 0
            for row in self.cart_list:
                if self.var_ProdName.get() == row[1]:
                    present = 'yes'
                    break
                index_ += 1

            if present == 'yes':
                op = messagebox.askyesno("Confirm", "Want to Remove?")
                if op == True:
                    self.cart_list.pop(index_)
            else:
                messagebox.showerror(
                    "Error", "Product Not in The Cart\nPlease Select Product from Cart")

            self.cart_show()
            self.bill_updates()

    def cart_clear(self):
        self.var_ProdName.set(""),
        self.var_PPQty.set(""),
        self.var_qty.set(""),
        self.cust_name.set(""),
        self.cust_contact.set("")

    def bill_updates(self):
        self.billAmnt = 0
        self.netPay = 0
        for row in self.cart_list:
            self.billAmnt = self.billAmnt+row[2]

        self.discount = (self.billAmnt*5)/100
        self.netPay = self.billAmnt-self.discount
        self.lbl_billAmnt.config(
            text=f'Bill Amount\nRs.{str(self.billAmnt)}')
        self.lbl_netPay.config(text=f'Net Pay\nRs.{str(self.netPay)}')
        self.lbl_cartFrame.config(
            text=f"Cart\tTotal Product: [{str(len(self.cart_list))}]")

    def cart_show(self):
        try:
            self.productTable2.delete(*self.productTable2.get_children())
            for row in self.cart_list:
                self.productTable2.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")

    def cart_get_data(self, ev):
        f = self.productTable2.focus()
        content = (self.productTable2.item(f))
        row = content['values']
        self.var_pid.set(row[0])
        self.var_ProdName.set(row[1])
        self.var_PPQty.set(str(int((int(float(row[2]))/(int(row[3]))))))
        self.var_qty.set(row[3])
        # messagebox.showinfo
        self.lbl_stock.config(text=f"In Stock[{row[4]}]")

    def generate_bill(self):
        if self.cust_name.get() == "" or self.cust_contact.get() == "":
            messagebox.showinfo(
                "Error", "Customer Details are Required!", parent=self.root)
        elif len(self.cart_list) == 0:
            messagebox.showinfo("Error", "Please Add Product to The Cart")
        else:
            # ====Bill Top=====
            self.bill_top()

            # ====Bill Middle=====
            self.bill_middle()

            # ====Bill Bottom=====
            self.bill_bottom()

            fp = open(f'bill/{str(self.invoice)}.txt', 'w')
            fp.write(self.txt_billArea.get('1.0', END))
            fp.close()
            messagebox.showinfo(
                "Saved", "Bill Generated\n-File Saved-", parent=self.root)

            self.cart_clear()
            del self.cart_list[:]
            self.productTable2.delete(*self.productTable2.get_children())
            self.lbl_cartFrame['text'] = "Cart\tTotal Product: [0]"

            self.chk_print = 1

# =====================Bill Top=======================================

    def bill_top(self):
        self.invoice = int(time.strftime("%H%M%S")) + \
            int(time.strftime("%d%m%y"))
        bill_top_temp = f'''
\t\tInventory
   Phone No: 7407038247, Khirpai - 721232
{str('='*41)}
   Customer Name: {self.cust_name.get()}
   Phone No: {self.cust_contact.get()}
\t{str('-'*30)}
   Bill No: {str(self.invoice)} || Date: {str(time.strftime("%d/%m/%y"))}
{str('='*41)}
  Product Name\t\tQTY\tPrice
{str('='*41)}
        '''

        self.txt_billArea.delete('1.0', END)
        self.txt_billArea.insert('1.0', bill_top_temp)
# ===========================Bill Bottom======================================

    def bill_bottom(self):
        bill_bottom_temp = f'''
{str('='*40)}
   Bill Ammount\t\t\tRs.{self.billAmnt}
   Discount\t\t\tRs.{self.discount}
   Net Pay\t\t\tRs.{self.netPay}
{str('='*40)}
        '''
        self.txt_billArea.insert(END, bill_bottom_temp)

    def bill_middle(self):
        try:
            con = sqlite3.connect(database=r'ims.db')
            cur = con.cursor()
            for row in self.cart_list:
                pid = row[0]
                name = row[1]
                update_qty = int(row[4])-int(row[3])
                qty = row[3]
                if int(qty) == int(row[4]):
                    status = 'INACTIVE'
                else:
                    status = 'ACTIVE'
                # price = float(row[3])*int(row[2])
                price = str(row[2])
                self.txt_billArea.insert(
                    END, "\n  "+name+"\t\t"+qty+"\tRs."+price)
                # =========Update Quantity in product table=================
                cur.execute("UPDATE PRODUCT SET QTY=?,STATUS=? WHERE P_ID=?", (
                    update_qty,
                    status,
                    pid
                ))
                con.commit()
            con.close()
            self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")

    def clear_all(self):
        self.txt_billArea.delete('1.0', END)
        self.cart_clear()
        del self.cart_list[:]
        self.productTable2.delete(*self.productTable2.get_children())
        self.lbl_cartFrame['text'] = "Cart\tTotal Product: [0]"
        self.calcClear()
        self.lbl_stock["text"] = ""
        self.lbl_billAmnt["text"] = "Bill Amount"
        self.lbl_netPay["text"] = "Net Pay"
        self.var_searchName.set("")
        self.show()
        self.chk_print = 0

    def update_dateTime(self):
        time_ = time.strftime("%I:%M:%S")
        date_ = time.strftime("%d-%m-%y")
        self.lbl_dateTime .config(
            text=f"Welcome to my First Project\t\t Date: {str(date_)}\t\t Time: {str(time_)}")

        self.lbl_dateTime.after(200, self.update_dateTime)

    def print_bill(self):
        if self.chk_print == 1:
            messagebox.showinfo('Print', 'Please Wait', parent=self.root)
            new_file = tempfile.mktemp('.txt')
            open(new_file, 'w').write(self.txt_billArea.get('1.0', END))
            if sys.platform == 'win32':
                os.startfile(new_file, 'print')
            else:
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, new_file])
            # lpr =  subprocess.Popen("/usr/bin/lpr", stdin=subprocess.PIPE)
            # lpr.stdin.write(new_file)
        else:
            messagebox.showerror('Print', 'Please Generate Bill to Print')

    def logout(self):
        self.root.destroy()
        os.system("python login.py")


if __name__ == "__main__":
    root = Tk()
    obj = billing(root)
    root.mainloop()
