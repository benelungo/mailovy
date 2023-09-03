import smtplib
import imaplib
import poplib

class Connection:
    def __init__(self, login, imap_key):
        self.login = login
        self.IMAP_key = imap_key
        self.connect = None

    def imap(self):
        return 'imap.' + self.login.split('@')[-1]

    def connect_to_mail_server(self):
        try:
            self.connect = imaplib.IMAP4_SSL(self.imap(), timeout=600)
            self.connect.login(self.login, self.IMAP_key)
            return True
        except Exception as e:
            print(e)
            return False

    def close_connection(self):
        self.connect.logout()
