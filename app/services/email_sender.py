import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


class EmailSender:

    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

    def send(self, to_email, subject, html_content):

        msg = MIMEMultipart()
        msg["From"] = EMAIL_USER
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(html_content, "html"))

        server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        try:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.send_message(msg)
        finally:
            server.quit()