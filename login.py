from tkinter import*
from tkinter import font
from PIL import ImageTk, Image
from tkinter import messagebox
import sqlite3
import os
# from forget import forget
import email_otp
import smtplib
import time
import sys


class login:
    def __init__(self, root):
        self.root = root
        # getting screen width and height of display
        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()
        # self.root.attributes("-fullscreen", True)
        # setting tkinter window size
        self.root.geometry("%dx%d+0+0" % (width, height))

        # if sys.platform == 'win32':
        #     self.root.geometry("1366x700+0+0")
        #     # messagebox.showinfo("", sys.platform())
        # else:
        #     self.root.geometry("1350x700+0+0")
        self.root.title("Inventory Management Login System | Developed By SD")
        self.root.config(bg="white")
        if self.is_firstTime():
            os.system('python employee.py')
            self.root.destroy()
        else:
            self.otp = StringVar()
            self.pass_expire = 0
            # ===================Body Background Image=================================
            self.body_img = Image.open('images/login.jpg')
            self.body_img = self.body_img.resize((1400, 710), Image.ANTIALIAS)
            self.body_img = ImageTk.PhotoImage(self.body_img)

            lbl_img = Label(self.root, image=self.body_img).place(x=0, y=0)

            # =================Login Frame============================
            self.var_employee_id = StringVar()
            self.var_password = StringVar()

            login_frame = Frame(self.root, bd=0, relief=RIDGE, bg="white")
            login_frame.place(x=746, y=39, width=455, height=636)

            caption_login_frame = Label(
                login_frame, text="Login to IMS", bg="white", font=("Times New Roman", 45, "bold")).pack(side=TOP, fill=X, pady=15)

            lbl_border_bottom = Label(
                login_frame, text="--------------------------------------------------", font=(
                    "Times New Roman", 17, "bold"), bg="white", state=DISABLED).pack(side=TOP, fill=X)

            lbl_employee_id = Label(login_frame, text="Employee Id", font=(
                "Times New Roman", 20, "bold"), bg="white").place(x=60, y=140)

            txt_employee_id = Entry(login_frame, textvariable=self.var_employee_id, font=(
                "Times New Roman", 17, "bold"), bg="lightyellow")
            txt_employee_id.place(x=60, y=190, width=300, height=30)

            lbl_password = Label(login_frame, text="Password", font=(
                "Times New Roman", 20, "bold"), bg="white").place(x=60, y=260)

            txt_password = Entry(login_frame, show='*', textvariable=self.var_password, font=(
                "Times New Roman", 17, "bold"), bg="lightyellow")
            txt_password.place(x=60, y=310, width=300, height=30)

            btn_login = Button(login_frame, command=self.login, text="Log In", cursor="hand2", font=(
                "Times New Roman", 17, "bold"), bg="#6166B3").place(x=60, y=390, width=300)

            lbl_or = Label(
                login_frame, text="-----------------OR----------------", font=(
                    "Times New Roman", 17, "bold"), bg="white", state=DISABLED).place(x=60, y=450)
            btn_forget = Button(login_frame, command=self.forget_window, text="Forget Password?", font=(
                "Times New Roman", 17, "bold"), bg="white", fg="#00759E", bd=0, relief=RIDGE, activebackground="white", activeforeground="#6166B3").place(x=60, y=490, width=300)

    def login(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_employee_id.get() == "" or self.var_password.get() == "":
                messagebox.showerror("Error", "All Fields are Required")
            else:
                cur.execute("SELECT UTYPE FROM EMPLOYEE WHERE EMPID=? AND PASSWORD=?", (
                    self.var_employee_id.get(),
                    self.var_password.get()
                ))
                user = cur.fetchone()
                if user == None:
                    messagebox.showerror(
                        "Incorrect", "Incorrect Employee_ID/Password")
                else:
                    if user[0] == 'Admin':
                        self.root.destroy()
                        os.system("python dashboard.py")
                    else:
                        self.root.destroy()
                        os.system("python billing.py")
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to : {str(ex)}")

    def forget_window(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_employee_id.get() == "":
                messagebox.showerror("Error", "Employee ID Required")
            else:
                cur.execute("SELECT EMAIL FROM EMPLOYEE WHERE EMPID=?", (
                    self.var_employee_id.get(),

                ))
                self.email = cur.fetchone()
                if self.email == None:
                    messagebox.showerror(
                        "Incorrect", "Invalid Employee_ID", parent=self.root)
                else:
                    self.var_otp = StringVar()
                    self.new_password = StringVar()
                    self.confirm_password = StringVar()
                    chk = self.send_email_fun(self.email[0])
                    if chk == 'f':
                        messagebox.showerror(
                            "Error", "Connection Error,Try Again", parent=self.root)
                    else:
                        messagebox.showinfo(
                            "Success", f"Email Send to\n{self.email[0]}", parent=self.root)

                        self.forget_win = Toplevel(self.root)
                        self.forget_win.geometry("455x606+746+100")
                        self.forget_win.title("Inventory Management System")
                        self.forget_win.config(bg="white")
                        self.forget_win.focus_force()
                        # =============================Variables======================

                        caption_forget = Label(
                            self.forget_win, text="Forget Password", bg="white", font=("Times New Roman", 35, "bold")).pack(side=TOP, fill=X, pady=10)

                        lbl_otp = Label(self.forget_win, text="Enter OTP send on Registered Email :", font=(
                            "Times New Roman", 15, "bold"), bg="white").place(x=50, y=120)

                        txt_otp = Entry(self.forget_win, textvariable=self.var_otp, font=(
                            "Times New Roman", 17, "bold"), bg="lightyellow")
                        txt_otp.place(x=50, y=170, width=200, height=30)

                        btn_confirm = Button(self.forget_win, command=self.confirm, text="Confirm", cursor="hand2", font=(
                            "Times New Roman", 15, "bold"), bg="#6166B3").place(x=290, y=170, height=30)

                        lbl_div = Label(self.forget_win, text="-------------------------------------------------", font=(
                            "Times New Roman", 15, "bold"), bg="white", state=DISABLED).place(x=50, y=220)

                        lbl_newPassword = Label(self.forget_win, text="Enter New Password :", font=(
                            "Times New Roman", 15, "bold"), bg="white").place(x=50, y=270)

                        txt_newPassword = Entry(self.forget_win, show='*', textvariable=self.new_password, font=(
                            "Times New Roman", 15, "bold"), bg="lightyellow")
                        txt_newPassword.place(
                            x=50, y=310, width=300, height=30)

                        lbl_confirm_pass = Label(self.forget_win, text="Confirm Password :", font=(
                            "Times New Roman", 15, "bold"), bg="white").place(x=50, y=360)

                        txt_confirm_pass = Entry(self.forget_win, show='*', textvariable=self.confirm_password, font=(
                            "Times New Roman", 15, "bold"), bg="lightyellow")
                        txt_confirm_pass.place(
                            x=50, y=400, width=300, height=30)

                        self.btn_submit = Button(self.forget_win, command=self.submit, text="Submit", cursor="hand2", font=(
                            "Times New Roman", 15, "bold"), bg="#6166B3", state=DISABLED)
                        self.btn_submit.place(x=50, y=460, width=150)

                        self.forget_img = Image.open('images/forget.jpg')
                        self.forget_img = self.forget_img.resize(
                            (160, 160), Image.ANTIALIAS)
                        self.forget_img = ImageTk.PhotoImage(self.forget_img)

                        lbl_forget_img = Label(
                            self.forget_win, image=self.forget_img, bd=0).place(x=280, y=440)

        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to : {str(ex)}\n\nInternet Connection Required")

    def send_email_fun(self, to_):
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        email_ = email_otp.email
        pass_ = email_otp.pass_

        s.login(email_, pass_)

        self.otp = int(time.strftime('%H%S%M'))+int(time.strftime('%S'))
        subj = 'IMS Reset Password OTP'
        msg = f'Dear Sir/Madam\n\nYout Reset OTP is {str(self.otp)}.\n\nWith Regards,\nIMS Team\nDeveloped By Shibu Dhara'
        msg = "Subject:{}\n\n{}".format(subj, msg)
        s.sendmail(email_, to_, msg)
        chk = s.ehlo()
        if chk[0] == 250:
            return 's'
        else:
            return 'f'

    def confirm(self):
        if self.var_otp.get() == "":
            messagebox.showerror("Error", "Enter OTP", parent=self.forget_win)
        else:
            if int(self.var_otp.get()) == self.otp:
                messagebox.showinfo(
                    "Success", "OTP Verified\Enter New Password", parent=self.forget_win)
                self.btn_submit.config(state=NORMAL)

    def submit(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.new_password.get() == "" or self.confirm_password.get() == "":
                messagebox.showerror(
                    "Error", "Enter New Password", parent=self.forget_win)
            elif self.new_password.get() != self.confirm_password.get():
                messagebox.showwarning(
                    "Mismatch", "Password Mismatch", parent=self.forget_win)
            else:
                if self.pass_expire == 0:
                    cur.execute("UPDATE EMPLOYEE SET PASSWORD=? WHERE EMAIL=?", (
                        self.confirm_password.get(),
                        self.email[0]
                    ))
                    con.commit()
                    messagebox.showinfo(
                        "Success", "Password Changed", parent=self.forget_win)
                    self.pass_expire += 1
                else:
                    messagebox.showerror(
                        'Expire', 'OTP Expire', parent=self.forget_win)
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to : {str(ex)}", parent=self.forget_win)

    def is_firstTime(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM EMPLOYEE")
            usr = cur.fetchone()
            if usr == None:
                return True
            else:
                return False
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to : {str(ex)}", parent=self.forget_win)
# ====================Check Internet Connection=================================================================================
    # def connect(self, host='http://google.com'):
    #     try:
    #         urllib.request.urlopen(host)  # Python 3.x
    #         return True
    #     except:
    #         return False
# # ====================================================================================================================


if __name__ == "__main__":
    root = Tk()
    obj = login(root)
    root.mainloop()
