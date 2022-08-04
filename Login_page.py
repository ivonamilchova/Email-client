import tkinter as tk
from Inbox import Inbox
import smtplib
import tkinter.messagebox
root = tk.Tk()

class LoginPage:
    def __init__(self, root = None):
        self.root = root
        self.frame = tk.Frame(self.root, padx=10, pady=20)
        self.frame.grid()

        self.var = Inbox(master=self.root, app=self)

        self.label_email = tk.Label(self.frame, text="Email address:")
        self.label_email.grid(row=0, column=0)

        self.temp_username = tk.StringVar()
        self.email_address = tk.Entry(self.frame, bg="white", width=50, textvariable=self.temp_username)
        self.email_address.grid(row=0, column=1)
        self.temp_username.set('imilchova21test@gmail.com')


        self.label_password = tk.Label(self.frame, text="Password:")
        self.label_password.grid(row=1, column=0)

        self.temp_password = tk.StringVar()
        self.password = tk.Entry(self.frame, bg="white", width=50, textvariable=self.temp_password)
        self.password.config(show="*")
        self.password.grid(row=1, column=1)
        self.temp_password.set('orfwiflsruvvelid')

        self.button = tk.Button(self.frame, text="Log in", bg="light pink", fg="white", command=self.log_in)
        self.button.grid(row=3, column=1, sticky="E")

        self.button_reset = tk.Button(self.frame, text="Reset", bg="light pink", fg="white", command=self.reset)
        self.button_reset.grid(row=2, column=1, sticky="E")

    def go_to_inbox_page(self):
        self.frame.grid_forget()
        self.var.go_to_inbox()

    def main_page(self):
        self.frame.grid()

    def get_username(self):
        return self.email_address.get()

    def get_password(self):
        return self.password.get()

    def reset(self):
        self.email_address.delete('0', "end")
        self.password.delete('0', 'end')

    def log_in(self):
        try:

             self.temp_username = self.email_address.get()
             self.temp_password = self.password.get()

             if self.temp_username and self.temp_password:

                  server = smtplib.SMTP("smtp.gmail.com", 587)
                  server.starttls()
                  if server.login(self.temp_username, self.temp_password):
                    self.go_to_inbox_page()
             else:
                 tk.messagebox.showerror(title="Error", message="Input username and password!")
        except smtplib.SMTPAuthenticationError:
            tk.messagebox.showerror(title="Error", message="Invalid username and password!")



e = LoginPage(root)
root.mainloop()
