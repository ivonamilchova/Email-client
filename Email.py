import tkinter as tk
import tkinter.messagebox
import smtplib
import imghdr
from tkinter import filedialog
from email.message import EmailMessage

attachments = []

class Email:
    def __init__(self, master=None, app=None):
        self.master = master
        self.app = app
        self.frame = tk.Frame(self.master, padx=10, pady=20)

        self.label_to = tk.Label(self.frame, text="To:")
        self.label_to.grid(row=0, column=0)

        self.text_to = tk.Entry(self.frame, bg="white", width=100)
        self.text_to.grid(row=0, column=1)

        self.label_subject = tk.Label(self.frame, text="Subject:")
        self.label_subject.grid(row=1, column=0)
        self.text_subject = tk.Entry(self.frame, bg="white", width=100)
        self.text_subject.grid(row=1, column=1)

        self.label_text = tk.Label(self.frame, text="Mail text:")
        self.label_text.grid(row=2, column=0)

        text_scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL)
        text_scrollbar.grid(row=2, column=2, sticky="NS")

        self.text = tk.Text(self.frame, bg="white", width=80, height=30, yscrollcommand=text_scrollbar.set)
        self.text.grid(row=2, column=1)
        text_scrollbar.config(command=self.text.yview)

        self.button_send = tk.Button(self.frame, text="Send", bg="light pink", fg="white", command=self.send_email)
        self.button_send.grid(row=3, column=2)

        self.button_add = tk.Button(self.frame, text="Add Attachments", bg="light pink", fg="white", command=self.attach_files)
        self.button_add.grid(row=3, column=0)

        self.label_add = tk.Label(self.frame)
        self.label_add.grid(row=3, column=1, sticky="W")

        self.button_log_out = tk.Button(self.frame, text="Log out", bg="light pink", fg="white", command=self.log_out)
        self.button_log_out.grid(row=3, column=1, sticky="E")

        self.button_log_out = tk.Button(self.frame, text="Back", bg="light pink", fg="white",
                                        command=self.go_to_inbox)
        self.button_log_out.grid(row=4, column=2, sticky="E")

    def go_to_inbox(self):
        self.frame.grid_forget()
        self.app.go_to_inbox()

    def log_out(self):
        self.frame.grid_forget()
        self.app.main_page()

    def send_email(self):
        try:
            self.message = EmailMessage()

            temp_receiver = tk.StringVar()
            temp_subject = tk.StringVar()
            temp_body = tk.StringVar()


            self.current_username = self.app.get_username()
            self.current_password = self.app.get_password()

            temp_receiver = self.text_to.get()
            self.to = temp_receiver.split(',')

            temp_subject = self.text_subject.get()
            self.subject = temp_subject

            temp_body = self.text.get("1.0", 'end')
            self.body = temp_body

            self.message['subject'] = self.subject
            self.message['from'] = self.current_username


            self.message['to'] = self.to
            self.message.set_content(self.body)

            for filename in attachments:
                filetype = filename.split('.')
                filetype = filetype[1]
                if (filetype == 'jpg' or filetype == 'JPG' or filetype == 'png' or filetype == 'PNG'):
                    with open(filename, 'rb') as f:
                        file_data = f.read()
                        image_type = imghdr.what(filename)
                    self.message.add_attachment(file_data, maintype='image', subtype=image_type, filename=f.name)
                else:
                    with open(filename, 'rb') as f:
                        file_data = f.read()
                    self.message.add_attachment(file_data, maintype='aplication', subtype='octet-stream',
                                                filename=f.name)


            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(self.current_username, self.current_password)
            server.send_message(self.message)
            tkinter.messagebox.showinfo(message="The email is successfully sent!")
        except :

            tkinter.messagebox.showerror(title="Error", message="Invalid email address!")

    def attach_files(self):
        filename = filedialog.askopenfilename(initialdir='C:/', title='Select a file')
        attachments.append(filename)

        short_filename = filename.split("/")

        self.label_add.config(text=self.label_add.cget("text") + str(short_filename[len(short_filename) - 1]) + ', ')



