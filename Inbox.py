import tkinter as tk
from Email import Email
import sqlite3
import sqlite3 as sql
import tkinter.messagebox
import smtplib
from sqlite3 import Error
from imbox import Imbox
from email.message import EmailMessage
import vlc



class Inbox:
    def __init__(self, master=None, app = None):
        self.master = master
        self.app = app
        self.frame = tk.Frame(self.master, padx=10, pady=20)
        self.email_obj = Email(master=self.master, app=self)

        self.label_to = tk.Label(self.frame, text="Inbox:")
        self.label_to.grid(row=0, column=0)

        self.music = tk.Label(self.frame, text="Music -->")
        self.music.grid(row=0, column=2)

        self.on = tk.PhotoImage(file="On_p.png")
        self.off = tk.PhotoImage(file="Off_p.png")

        self.is_off = True
        self.music_button = tk.Button(self.frame, image=self.off, command=self.switch)
        self.music_button.grid(row=0, column=3, sticky="W")

        list_scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL)
        list_scrollbar.grid(row=1, column=11, sticky="NS")

        self.list_of_mails = tk.Listbox(self.frame, yscrollcommand=list_scrollbar.set)
        self.list_of_mails.config(width=70, height=20)
        self.list_of_mails.grid(row=1, column=0, columnspan=10, ipadx=10,ipady=10)

        list_scrollbar.config(command=self.list_of_mails.yview)

        self.button_read = tk.Button(self.frame, text="Read mail",  bg="light pink", fg="white", command=self.read_email)
        self.button_read.grid(row=3, column=0, sticky='E')

        self.button_log_out = tk.Button(self.frame, text="Log out", bg="light pink", fg="white", command=self.log_out)
        self.button_log_out.grid(row=3, column=1, sticky="E")

        self.button_write_email = tk.Button(self.frame, text="Write email", bg="light pink", fg="white", command=self.go_to_email)
        self.button_write_email.grid(row=3, column=2, sticky="E")

        self.button_show_emails = tk.Button(self.frame, text="Show all emails", bg="light pink", fg="white",
                                        command=self.download_mails)
        self.button_show_emails.grid(row=3, column=3, sticky="E")

        self.button_forward_to = tk.Button(self.frame, text="Forward to", bg="light pink", fg="white",
                                            command=self.forward_to_button)
        self.button_forward_to.grid(row=3, column=4, sticky="E")

    def switch(self):
        if self.is_off:
            self.music_button.config(image=self.on)
            self.sound_file = vlc.MediaPlayer("music.mp3")
            self.sound_file.play()
            self.is_off = False
        else:
            self.music_button.config(image=self.off)
            self.sound_file.stop()
            self.is_off = True

    def go_to_inbox(self):
        self.frame.grid()

    def main_page(self):
        self.app.main_page()

    def go_to_email(self):
        self.frame.grid_forget()
        self.email_obj.frame.grid()

    def read_email(self):
        self.sel_idx = self.list_of_mails.curselection()
        value = self.list_of_mails.get(self.sel_idx)
        tk.messagebox.showinfo(message=value)

    def download_mails(self):
        self.connection = sql.connect('Emails.db')
        self.server = "imap.gmail.com"
        self.username = self.app.get_username()
        self.password = self.app.get_password()
        sql_add = 'INSERT into emails ("date", "from", "subject", "email_body") VALUES(?,?,?,?)'
        sql_remove = 'DELETE from emails'

        with self.connection:
            try:
                self.connection.execute(sql_remove)
            except:
                tk.messagebox.showerror("Unsuccessful removing")

        with Imbox(self.server, username=self.username, password=self.password) as imbox:
            self.all_messages = imbox.messages()

            for uid, message in self.all_messages:
                counter = 0
                email_date = message.date[:-11]
                email_from = message.sent_from[0]['email']
                email_subject = message.subject
                email_body = message.body['plain'][0]


                data = [email_date, email_from, email_subject, str(email_body)]

                self.data_in_str = f"{email_date}\n From: {email_from}\n Subject: {email_subject}\n Text: {str(email_body)}"
                self.list_of_mails.insert(counter, self.data_in_str)

                counter += 1

        with self.connection:
            try:
                self.connection.execute(sql_add, data)
            except sqlite3.Error:
                print("SQLite error!")

    def forward(self):
        self.message = EmailMessage()

        self.temp_forward_to = self.forward_to.get()
        self.sel_idx = self.list_of_mails.curselection()
        value = self.list_of_mails.get(self.sel_idx)

        username = self.app.get_username()
        password = self.app.get_password()

        to = self.temp_forward_to
        self.to = to

        self.subject = ""

        self.body = str(value)

        self.message['subject'] = self.subject
        self.message['from'] = username

        self.message['to'] = self.to
        self.message.set_content(self.body)
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(username, password)
        server.send_message(self.message)

        tkinter.messagebox.showinfo(message="The email is successfully sent!")



    def forward_to_button(self):
        self.temp_forward_to = tk.StringVar()
        self.forward_to = tk.Entry(self.frame, bg="white", width=50, textvariable=self.temp_forward_to)
        self.forward_to.grid(row=4, column=0, columnspan=5)

        forward_to_button = tk.Button(self.frame, text="Send", bg="light pink", fg="white", command = self.forward)
        forward_to_button.grid(row=4, column=5, sticky="W")

    def log_out(self):
        self.frame.grid_forget()
        self.app.main_page()

    def get_username(self):
        return self.app.get_username()

    def get_password(self):
        return self.app.get_password()