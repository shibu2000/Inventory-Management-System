from tkinter import*
from tkinter import font
from tkinter.font import Font
# import PIL
from PIL import Image, ImageTk  # sudo dnf install python3-pillow-tk
from employee import employeeClass
from supplier import supplierClass
from category import categoryClass
from product import productClass
from sales import salesClass
import time
import sqlite3
import os


class IMS:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title("Inventory Management System | Developed By SD")
        self.root.config(bg="white")

        # ======Title=======
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

        # ===Left Menu===
        self.leftMenu_logo = Image.open("images/209460111.png")
        self.leftMenu_logo = self.leftMenu_logo.resize(
            (200, 200), Image.ANTIALIAS)
        self.leftMenu_logo = ImageTk.PhotoImage(self.leftMenu_logo)

        Left_Menu = Frame(self.root, bd=0, relief=RIDGE, bg="white")
        Left_Menu.place(x=0, y=102, width=200, height=565)

        Left_Menu_label_logo = Label(Left_Menu, image=self.leftMenu_logo)
        Left_Menu_label_logo.pack(side=TOP, fill=X)

        Left_Menu_label = Label(Left_Menu, text="MENU", font=(
            "times new roman", 15, "bold"), bg="#009699").pack(side=TOP, fill=X)

        # ===LEFT MENU BUTTONS==
        # self.leftMenu_icon = PhotoImage("images/double-chevron.png")
        self.leftMenu_icon = Image.open("images/double-chevron.png")
        self.leftMenu_icon = self.leftMenu_icon.resize(
            (20, 20), Image.ANTIALIAS)
        self.leftMenu_icon = ImageTk.PhotoImage(self.leftMenu_icon)
        btn_employee = Button(Left_Menu, text="Employee", command=self.employee, image=self.leftMenu_icon, compound=LEFT, anchor="w", font=(
            "times new roman", 20), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)
        btn_supplier = Button(Left_Menu, command=self.supplier, text="Supplier", image=self.leftMenu_icon, compound=LEFT, anchor="w", font=(
            "times new roman", 20), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)
        btn_category = Button(Left_Menu, command=self.category, text="Category", image=self.leftMenu_icon, compound=LEFT, anchor="w", font=(
            "times new roman", 20), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)
        btn_products = Button(Left_Menu, command=self.product, text="Products", image=self.leftMenu_icon, compound=LEFT, anchor="w", font=(
            "times new roman", 20), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)
        btn_sales = Button(Left_Menu, command=self.sales, text="Sales", image=self.leftMenu_icon, compound=LEFT, anchor="w", font=(
            "times new roman", 20), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)
        btn_exit = Button(Left_Menu, text="Exit", image=self.leftMenu_icon, compound=LEFT, anchor="w", font=(
            "times new roman", 20), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)
        # ===Main Contents====
        self.label_employee = Label(self.root, text="Total Employee\n[ 0 ]", bd=5, relief=RIDGE, bg="#33bbf9", fg="white", font=(
            "goudy old style", 20, "bold"))
        self.label_employee.place(x=300, y=120, height=150, width=300)

        self.label_supplier = Label(self.root, text="Total Supplier\n[ 0 ]", bd=5, relief=RIDGE, bg="#33bbf9", fg="white", font=(
            "goudy old style", 20, "bold"))
        self.label_supplier.place(x=650, y=120, height=150, width=300)

        self.label_category = Label(self.root, text="Total Category\n[ 0 ]", bd=5, relief=RIDGE, bg="#33bbf9", fg="white", font=(
            "goudy old style", 20, "bold"))
        self.label_category.place(x=1000, y=120, height=150, width=300)

        self.label_product = Label(self.root, text="Total Product\n[ 0 ]", bd=5, relief=RIDGE, bg="#33bbf9", fg="white", font=(
            "goudy old style", 20, "bold"))
        self.label_product.place(x=300, y=300, height=150, width=300)

        self.label_sales = Label(self.root, text="Total Sales\n[ 0 ]", bd=5, relief=RIDGE, bg="#33bbf9", fg="white", font=(
            "goudy old style", 20, "bold"))
        self.label_sales.place(x=650, y=300, height=150, width=300)

        # ===Footer===
        label_footer = Label(self.root, text="Inventory Management System | Developed By- CrabyTech\nFor any issue contact: 7407038247", font=(
            "times new roman", 12, "bold"), bg="#4d636d", fg="white").pack(side=BOTTOM, fill=X)

        self.get_total()
# =========================================================================================================================
# ===============================Functions==============================

    def get_total(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()

        cur.execute("SELECT EMPID FROM EMPLOYEE")
        employee_row = cur.fetchall()
        self.label_employee.config(
            text=f"Total Employee\n[ {str(len(employee_row))} ]")

        cur.execute("SELECT INVOICE FROM SUPPLIER")
        supplier_row = cur.fetchall()
        self.label_supplier.config(
            text=f"Total Supplier\n[ {str(len(supplier_row))} ]")

        cur.execute("SELECT CID FROM CATEGORY")
        category_row = cur.fetchall()
        self.label_category.config(
            text=f"Total Category\n[ {str(len(category_row))} ]")

        cur.execute("SELECT P_ID FROM PRODUCT")
        product_row = cur.fetchall()
        self.label_product.config(
            text=f"Total Product\n[ {str(len(product_row))} ]")

        self.label_sales.config(
            text=f"Total Sales\n[ {len(os.listdir('bill'))} ]")

        time_ = time.strftime("%I:%M:%S")
        date_ = time.strftime("%d-%m-%y")
        self.lbl_dateTime .config(
            text=f"Welcome to my First Project\t\t Date: {str(date_)}\t\t Time: {str(time_)}")

        self.lbl_dateTime.after(200, self.get_total)

    def logout(self):
        self.root.destroy()
        os.system("python login.py")


# ============================All Sub Windows==============================================================================

    def employee(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = employeeClass(self.new_win)

    def supplier(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = supplierClass(self.new_win)

    def category(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = categoryClass(self.new_win)

    def product(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = productClass(self.new_win)

    def sales(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = salesClass(self.new_win)


if __name__ == "__main__":
    root = Tk()
    obj = IMS(root)
    root.mainloop()
