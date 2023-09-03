import base64
import email
import email.header
import email.utils
import json
import os
import quopri
import re

from modules import tools

class MailProcessor:
    @staticmethod
    def get_messages_ids(mailbox, selected_mailbox):
        status = mailbox.select(selected_mailbox)[0]
        if status == 'OK':
            _, data = mailbox.search(None, 'ALL')
            messages_ids = data[0].split()
            return messages_ids
        else:
            print("mail.Mail.get_messages_ids(): Bad mail folder")
            return []

    @classmethod
    def decode_imap_text(cls, text):
        text = str(text)
        pattern = r"=\?[^?]{0,}\?.\?.{0,}?\?="
        try:
            to_decode = re.findall(pattern, text)
        except Exception as e:
            print(e)
            to_decode = ""
        if len(to_decode) != 0:
            for part in to_decode:
                decoded_part = cls.decode(part)
                text = text.replace(part+" ", decoded_part)
                text = text.replace(" " + part, decoded_part)
                text = text.replace(" " + part + " ", decoded_part)
                text = text.replace(part, decoded_part)
        text = re.sub(r"""[^\S ]""", "", text)
        return text

    @staticmethod
    def decode(text):
        try:
            pattern = r"=\?.{1,}?\?[bqBQ]\?"
            codec = re.findall(pattern, text)[0]
            if "?b?" in codec.lower():
                text = text[:-2].replace(codec, '', )
                return base64.b64decode(text).decode(codec[2:-3])
            elif "?q?" in codec.lower():
                text = text[:-2].replace(codec, '', )
                return quopri.decodestring(text).decode(codec[2:-3])

        except Exception as e:
            print("decode_imap_text: " + str(e))
            return text

    @classmethod
    def get_sender(cls, data):
        for response_part in data:
            if isinstance(response_part, tuple):
                message = email.message_from_bytes(response_part[1])
                sender_info = message['From']
                sender_mail = sender_info.split('<')[-1][:-1]
                sender_name = sender_info[:-len(sender_mail)-3]
                sender_name = cls.decode_imap_text(sender_name)
                if sender_name != '':
                    return sender_name + '  |  ' + sender_mail
                else:
                    return sender_mail

    @classmethod
    def get_title(cls, data):
        for response_part in data:
            if isinstance(response_part, tuple):
                message = email.message_from_bytes(response_part[1])
                title = message['Subject']
                title = cls.decode_imap_text(title)
                return title

    @staticmethod
    def get_body(data):
        body = {"text": "", "html": ""}
        for response_part in data:
            if isinstance(response_part, tuple):
                message = email.message_from_bytes(response_part[1])
                for part in message.walk():
                    content_type = part.get_content_type()
                    codec = part.get_content_charset()
                    disposition = part.get_content_disposition()
                    if content_type == 'text/plain' and disposition != "attachment":
                        text = part.get_payload()
                        if part["Content-Transfer-Encoding"] == "base64":
                            text = base64.b64decode(text).decode(codec)
                        elif part["Content-Transfer-Encoding"] == "quoted-printable":
                            text = quopri.decodestring(text).decode(codec)
                        body["text"] = text
                    elif content_type == 'text/html' and disposition != "attachment":
                        html = part.get_payload()
                        if part["Content-Transfer-Encoding"] == "base64":
                            html = base64.b64decode(html).decode(codec)
                        elif part["Content-Transfer-Encoding"] == "quoted-printable":
                            html = quopri.decodestring(html).decode(codec)
                        body["html"] = html
        return body

    @classmethod
    def get_attachments(cls, login, data, selected_mailbox, message_id):
        filenames = []
        for response_part in data:
            if isinstance(response_part, tuple):
                message = email.message_from_bytes(response_part[1])
                if message.is_multipart():
                    for part in message.walk():
                        filename = part.get_filename()
                        if filename is not None:
                            filename = cls.decode_imap_text(filename)
                            data_to_save = part.get_payload(decode=True)
                            tools.download_attachment(login, filename, data_to_save, selected_mailbox, message_id)
                            filenames.append(filename)
        return filenames

    @classmethod
    def get_message_content_by_id(cls, login, mailbox, selected_mailbox_coded, selected_mailbox, message_id):
        mailbox.select(selected_mailbox_coded)
        login_path = os.path.join(tools.put_path, login)
        mailbox_path = os.path.join(login_path, selected_mailbox)
        message_path = os.path.join(mailbox_path, str(message_id))
        message_info_path = os.path.join(message_path, "message_info.json")

        tools.mkdir(tools.put_path)
        tools.mkdir(login_path)
        tools.mkdir(mailbox_path)
        tools.mkdir(message_path)

        if os.path.exists(message_info_path):
            return cls.get_message_info_from_json(message_info_path)
        else:
            return cls.save_message_info_to_json(login, mailbox, selected_mailbox, message_id, message_info_path)

    @staticmethod
    def get_message_info_from_json(message_info_path):
        with open(message_info_path) as f:
            message_content = json.load(f)
        return message_content

    @classmethod
    def save_message_info_to_json(cls, login, mailbox, selected_mailbox, message_id, message_info_path):
        message_content = cls.assemble_message_info(login, mailbox, selected_mailbox, message_id)
        with open(message_info_path, 'w') as f:
            json.dump(message_content, f)
        return message_content

    @classmethod
    def assemble_message_info(cls, login, mailbox, selected_mailbox, message_id):
        status, data = mailbox.fetch(message_id, "RFC822")
        if status == 'OK':
            return {"sender": cls.get_sender(data),
                    "title": cls.get_title(data),
                    "body": cls.get_body(data),
                    "attachments": cls.get_attachments(login, data, selected_mailbox, message_id),
                    "id": str(message_id),
                    "mailbox": selected_mailbox}
        else:
            print("update_mail_folder: Bad ID")
    @staticmethod
    def get_message_data_by_id(mailbox, selected_mailbox, message_id):
        try:
            mailbox.select(selected_mailbox)
            return mailbox.fetch(message_id, "RFC822")
        except Exception as e:
            print(e)
            return False, None

