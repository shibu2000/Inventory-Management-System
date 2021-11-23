from os import stat
from tkinter import*
from PIL import ImageTk, Image
from tkinter import messagebox


class forget:
    def __init__(self, root):
        self.root = root
        self.root.geometry("455x606+746+100")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")

        self.var_otp = StringVar()
        self.new_password = StringVar()
        self.confirm_password = StringVar()

        caption_forget = Label(
            self.root, text="Forget Password", bg="white", font=("Times New Roman", 35, "bold")).pack(side=TOP, fill=X, pady=10)

        lbl_otp = Label(self.root, text="Enter OTP send on Registered Email :", font=(
            "Times New Roman", 15, "bold"), bg="white").place(x=50, y=120)

        txt_otp = Entry(self.root, textvariable=self.var_otp, font=(
            "Times New Roman", 17, "bold"), bg="lightyellow")
        txt_otp.place(x=50, y=170, width=200, height=30)

        btn_confirm = Button(self.root, command=self.confirm, text="Confirm", cursor="hand2", font=(
            "Times New Roman", 15, "bold"), bg="#6166B3").place(x=290, y=170, height=30)

        lbl_div = Label(self.root, text="-------------------------------------------------", font=(
            "Times New Roman", 15, "bold"), bg="white", state=DISABLED).place(x=50, y=220)

        lbl_newPassword = Label(self.root,  text="Enter New Password :", font=(
            "Times New Roman", 15, "bold"), bg="white").place(x=50, y=270)

        txt_newPassword = Entry(self.root, show='*', textvariable=self.new_password, font=(
            "Times New Roman", 15, "bold"), bg="lightyellow")
        txt_newPassword.place(x=50, y=310, width=300, height=30)

        lbl_confirm_pass = Label(self.root, text="Confirm Password :", font=(
            "Times New Roman", 15, "bold"), bg="white").place(x=50, y=360)

        txt_confirm_pass = Entry(self.root, show='*', textvariable=self.confirm_password, font=(
            "Times New Roman", 15, "bold"), bg="lightyellow")
        txt_confirm_pass.place(x=50, y=400, width=300, height=30)

        self.btn_submit = Button(self.root, command=self.submit, text="Submit", cursor="hand2", font=(
            "Times New Roman", 15, "bold"), bg="#6166B3", state=DISABLED)
        self.btn_submit.place(x=50, y=460, width=150)

        self.forget_img = Image.open('images/forget.jpg')
        self.forget_img = self.forget_img.resize((160, 160), Image.ANTIALIAS)
        self.forget_img = ImageTk.PhotoImage(self.forget_img)

        lbl_forget_img = Label(
            self.root, image=self.forget_img, bd=0).place(x=280, y=440)

# ======================Functions============================================================

    def confirm(self):
        if self.var_otp.get() == "":
            messagebox.showerror("Error", "Enter OTP", parent=self.root)
        else:
            self.btn_submit.config(state=NORMAL)

    def submit(self):
        if self.new_password.get() == "" or self.confirm_password.get() == "":
            messagebox.showerror(
                "Error", "Enter New Password", parent=self.root)
        elif self.new_password.get() != self.confirm_password.get():
            messagebox.showwarning(
                "Mismatch", "Password Mismatch", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = forget(root)
    root.mainloop()
