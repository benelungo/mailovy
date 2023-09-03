import base64
import os
import sys
import time

from PyQt5 import QtWidgets, QtGui, QtCore
from modules.files_processor import FilesProcessor
from modules.mail_processor import MailProcessor
from modules import tools, connection
from modules.interface_parts.login_form import UiLoginWindow
from modules.interface_parts.main_form import UiMainWindow
from modules.interface_parts.message_form import UiMessageWindow
from threading import Thread, Lock, Event


class MainWindow:
    def __init__(self):
        self.add_mail = False
        self.messages_shift = 0
        self.cell_index = 0
        self.IMAP_keys = {}
        self.senders = []
        self.titles = []
        self.login = None
        self.mailbox = None
        self.mail_ids = None
        self.keep_work = None
        self.mail_mailbox = {}
        self.radioButtons = []
        self.mailbox_names = {}
        self.refresh_process = None
        self.selected_mailbox = None
        self.message_content_folder = {}

        self.lock = Lock()
        self.stop_refresh_thread = False
        self.refresh_thread = Thread()

        self.app = QtWidgets.QApplication(sys.argv)
        self.main = QtWidgets.QMainWindow()
        self.main_ui = UiMainWindow()
        self.main_ui.setupUi(self.main)
        self.init_label_styles()
        self.hide_senders_and_titles()

    def show_main_window(self, login_connection: dict, IMAP_keys: dict):
        self.IMAP_keys = IMAP_keys
        self.mail_mailbox = login_connection
        self.login = list(self.mail_mailbox.keys())[0]
        self.change_mail()
        self.keep_work = False
        self.main.show()
        self.app.exec()

    def init_data(self):
        self.init_mail_folders()
        self.init_message_cells()
        self.init_radioButtons()
        self.init_buttons_functions()
        self.mail_ids = MailProcessor.get_messages_ids(self.mailbox, self.selected_mailbox)

    def init_comboBox(self):
        current_index = 0
        for login in self.mail_mailbox.keys():
            self.main_ui.comboBox.addItem(login)
            current_index += 1
            if self.login == login:
                self.main_ui.comboBox.setCurrentIndex(current_index)
                self.main_ui.comboBox.setCurrentText(login)

    def init_label_styles(self):
        self.sender_on = "QLabel{ \n" \
                         "border: 1px solid;\n" \
                         "border-radius: 4px;\n" \
                         "border-color: #b5b5b5;\n" \
                         "background-color: #b5b5b5;\n" \
                         "margin: 0px;\n" \
                         "padding: 2px;\n" \
                         "}\n" \
                         "QLabel:hover {\n" \
                         "    border-color: #a5a5a5;\n" \
                         "    background-color: #a5a5a5;\n" \
                         "}\n" \
                         ""
        self.sender_off = "QPushButton{ \n" \
                          "color: transparent;" \
                          "border: 1px solid;\n" \
                          "border-radius: 4px;\n" \
                          "border-color: transparent;\n" \
                          "background-color: transparent;\n" \
                          "margin: 0px;\n" \
                          "padding: 2px;\n" \
                          "}\n" \
                          "QPushButton:hover {\n" \
                          "    border-color: transparent;\n" \
                          "    background-color: transparent;\n" \
                          "}\n" \
                          ""
        self.title_on = "QLabel{ \n" \
                        "margin: 0px;\n" \
                        "padding: 0px 1px 0px 5px;\n" \
                        "}"

        self.title_off = "QLabel{ \n" \
                         "color: transparent;" \
                         "margin: 0px;\n" \
                         "padding: 0px 1px 0px 2px;\n" \
                         "}"

        self.radioButton_isChecked = "QRadioButton{ \n" \
                                     "background-color: #c9c9c9" \
                                     "}" \
                                     "QRadioButton:hover{" \
                                     "background-color: #b5b5b5;" \
                                     "}"

    def init_buttons_functions(self):
        self.main_ui.refresh_pushButton.clicked.connect(self.refresh)
        self.main_ui.logout_pushButton.clicked.connect(self.logout)
        self.main_ui.left_pushButton.clicked.connect(lambda: self.set_message_shift(self.messages_shift - 10))
        self.main_ui.left_pushButton.clicked.connect(self.refresh)
        self.main_ui.right_pushButton.clicked.connect(lambda: self.set_message_shift(self.messages_shift + 10))
        self.main_ui.right_pushButton.clicked.connect(self.refresh)
        self.main_ui.open_mail_pushButton.clicked.connect(lambda: os.startfile("temp"))
        self.main_ui.comboBox.currentTextChanged.connect(self.combobox_changed)
        self.main_ui.add_mail_pushButton.clicked.connect(self.add_new_mail)

    def init_mail_folders(self):
        possible_mail_folders = ["Inbox", "Flagged", "Important", "Sent", "Drafts", "Junk", "Spam", "Trash", "Deleted"]
        for possible_folder in possible_mail_folders:
            for i in self.mailbox.list()[1]:
                full_folder = i.decode('utf-8')
                folder = full_folder.split(' "/" ')[-1][1:-1]
                if possible_folder.lower() in full_folder.lower():
                    self.mailbox_names[possible_folder] = folder

    def init_radioButtons(self):
        for folder in self.mailbox_names.keys():
            radioButton = QtWidgets.QRadioButton(self.main_ui.verticalLayoutWidget)
            font = QtGui.QFont()
            font.setFamily("Koulen,cursive")
            font.setPointSize(10)
            font.setStyleStrategy(QtGui.QFont.PreferDefault)
            radioButton.setFont(font)
            radioButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            radioButton.setLayoutDirection(QtCore.Qt.LeftToRight)
            radioButton.setText(folder)
            radioButton.setIcon(QtGui.QIcon("data/images/" + folder.lower() + ".png"))
            radioButton.setAutoExclusive(True)
            radioButton.clicked.connect(self.refresh)
            radioButton.clicked.connect(lambda: self.set_message_shift(0))
            self.radioButtons.append(radioButton)
            self.main_ui.verticalLayout.addWidget(radioButton)

        self.radioButtons[0].setChecked(True)
        self.selected_mailbox = list(self.mailbox_names.keys())[0]
        spacerItem = QtWidgets.QSpacerItem(20, 319, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.main_ui.verticalLayout.addItem(spacerItem)

    def init_message_cells(self):
        font = QtGui.QFont()
        font.setFamily("Koulen,cursive")
        font.setPointSize(10)

        for i in range(10):
            message_verticalLayout = QtWidgets.QVBoxLayout()
            sender_label = QtWidgets.QLabel(self.main_ui.verticalLayoutWidget_2)
            sender_label.setFont(font)
            message_verticalLayout.addWidget(sender_label)
            title_label = QtWidgets.QLabel(self.main_ui.verticalLayoutWidget_2)
            title_label.setFont(font)
            message_verticalLayout.addWidget(title_label)
            self.main_ui.messages_verticalLayout.addLayout(message_verticalLayout)
            self.senders.append(sender_label)
            self.titles.append(title_label)

    def open_message_window(self, cell_index):
        MessageWindow(self.message_content_folder[cell_index], self.login)

    def put_message_in_cell(self, message_content):
        cell_index = self.cell_index
        self.senders[cell_index].setText(message_content['sender'])
        self.titles[cell_index].setText(message_content['title'])
        self.senders[cell_index].setStyleSheet(self.sender_on)
        self.titles[cell_index].setStyleSheet(self.title_on)
        self.senders[cell_index].setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.senders[cell_index].mousePressEvent = lambda a: self.open_message_window(cell_index)
        self.message_content_folder[cell_index] = message_content
        self.cell_index += 1

    def hide_senders_and_titles(self):
        for sender in self.senders:
            sender.setText('')
            sender.setStyleSheet(self.sender_off)
            sender.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
            sender.mousePressEvent = None
        for title in self.titles:
            title.setText('')
            title.setStyleSheet(self.title_off)
        self.message_content_folder = {}
        self.cell_index = 0

    def find_checked_radioButton(self):
        button_text = ""
        for button in self.radioButtons:
            if button.isChecked():
                self.selected_mailbox = self.mailbox_names[button.text()]
                button.setStyleSheet(self.radioButton_isChecked)
                button_text = button.text()
            else:
                button.setStyleSheet('')
        return button_text

    def refresh(self):
        self.hide_senders_and_titles()
        self.find_checked_radioButton()
        self.break_refresh_thread()
        self.mail_ids = MailProcessor.get_messages_ids(self.mailbox, self.selected_mailbox)
        self.mail_ids.reverse()
        self.clean_absent_ids()
        # self.get_dataset()
        self.refresh_thread = Thread(target=self.update_cell_info)
        self.refresh_thread.start()

    def clean_absent_ids(self):
        path = os.path.join("temp", self.login, self.find_checked_radioButton())
        if os.path.exists(path):
            existent = os.listdir(path)
            for saved_id in existent:
                rm_id = True
                for real_id in self.mail_ids:
                    if saved_id == str(real_id):
                        rm_id = False
                        break
                if rm_id:
                    tools.rm(os.path.join(path, saved_id))

    def update_cell_info(self):
        self.stop_refresh_thread = False
        first_message_index = self.messages_shift
        last_message_index = self.messages_shift + 10
        selected_mailbox_decoded = self.find_checked_radioButton()
        if last_message_index > len(self.mail_ids):
            last_message_index = len(self.mail_ids)
        for mail_id in self.mail_ids[first_message_index:last_message_index]:
            if self.stop_refresh_thread:
                break

            message_content = MailProcessor.get_message_content_by_id(self.login, self.mailbox,
                                                             self.selected_mailbox,
                                                             selected_mailbox_decoded,
                                                             mail_id)
            self.put_message_in_cell(message_content)

    def set_message_shift(self, shift):
        mail_ids_num = len(self.mail_ids)
        if 0 <= shift <= mail_ids_num:
            max_num = shift + 10
            if mail_ids_num < max_num:
                max_num = mail_ids_num
            self.main_ui.page_label.setText(str(shift + 1) + "-" + str(max_num))
            self.messages_shift = shift

    def break_refresh_thread(self):
        self.stop_refresh_thread = True
        if self.refresh_thread.is_alive():
            self.refresh_thread.join()
        self.cell_index = 0

    def logout(self):
        self.keep_work = True
        self.break_refresh_thread()
        tools.rm(os.path.join(tools.put_path, self.login))
        LoginWindow().remove_from_auto_login(self.login, self.IMAP_keys[self.login])
        self.mailbox.logout()
        self.main.close()

    def change_mail(self):
        self.break_refresh_thread()
        self.clean_main_window()
        self.init_comboBox()
        self.mailbox = self.mail_mailbox[self.login]
        self.init_data()
        self.refresh()
        self.refresh()

    def combobox_changed(self, value):
        print("combobox changed", value)
        self.login = value
        self.change_mail()

    def remove_mail(self):
        self.main_ui.comboBox.removeItem(self.main_ui.comboBox.currentIndex())
        self.change_mail()

    def clean_main_window(self):
        self.main_ui = UiMainWindow()
        self.main_ui.setupUi(self.main)
        self.senders = []
        self.titles = []
        self.radioButtons = []
        self.mailbox_names = {}
        self.message_content_folder = {}

    def add_new_mail(self):
        self.add_mail = True
        self.keep_work = True
        self.break_refresh_thread()
        self.main.close()
        self.mailbox.logout()

    def get_dataset(self):
        if self.find_checked_radioButton() == "Flagged":
            dataset_name = "promotion"
            path = "data/datasets/"
            path = os.path.join(path, dataset_name)
            titles_path = os.path.join(path, "titles")
            bodies_path = os.path.join(path, "bodies")
            tools.mkdir(path)
            tools.mkdir(titles_path)
            tools.mkdir(bodies_path)
            for mail_id in self.mail_ids:
                status, data = MailProcessor.get_message_data_by_id(self.mailbox, self.selected_mailbox, mail_id)
                if status:
                    filename = str(mail_id) + ".txt"
                    try:
                        title = MailProcessor.get_title(data)
                        body = MailProcessor.get_body(data)["text"]
                        with open(os.path.join(titles_path, filename), "w") as f:
                            f.write(title)
                        with open(os.path.join(bodies_path, filename), "w") as f:
                            f.write(body)
                        print(filename + "  -  " + "writen")
                    except Exception as e:
                        print(e)
                        print(filename + "  -  " + "error")

class LoginWindow:
    def __init__(self):
        self.IMAP_keys = {}
        self.login_connection = {}
        self.auto_login_path = "data/login_info"
        self.dialog = QtWidgets.QDialog()
        self.keep_work = None
        self.dialog_ui = UiLoginWindow()
        self.dialog_ui.setupUi(self.dialog)
        self.dialog_ui.Login_Button.clicked.connect(self.hide_login_window)

    def show_login_window(self):
        self.keep_work = False
        self.dialog.show()
        self.dialog.exec_()

    def hide_login_window(self):
        self.keep_work = True
        self.dialog.hide()

    def get_login_window_info(self):
        login = self.dialog_ui.Login_LineEdit.text()
        IMAP_key = self.dialog_ui.IMAP_key_LineEdit.text()
        return login, IMAP_key

    def get_auto_login_info(self):
        with open(self.auto_login_path, 'r') as fp:
            lines = fp.readlines()
        logins_IMAP_keys = {}
        for i in range(0, len(lines), 2):
            logins_IMAP_keys[lines[i].strip()] = lines[i + 1].strip()
        return logins_IMAP_keys

    def save_to_auto_login(self, login, IMAP_key):
        if os.path.exists(self.auto_login_path):
            logins_IMAP_keys = self.get_auto_login_info()

            if login in logins_IMAP_keys.keys() and IMAP_key in logins_IMAP_keys.values():
                return False
            elif login in logins_IMAP_keys.keys() and IMAP_key not in logins_IMAP_keys.values():
                self.remove_from_auto_login(login, logins_IMAP_keys[login])

        with open(self.auto_login_path, 'a') as fp:
            fp.writelines([login, "\n", IMAP_key, "\n"])

    def remove_from_auto_login(self, login, IMAP_key):
        with open(self.auto_login_path, 'r') as fp:
            lines = fp.readlines()
        with open(self.auto_login_path, 'w') as fp:
            fp.writelines([line for line in lines if line.strip() != login and line.strip() != IMAP_key])

    def remove_auto_login(self):
        if os.path.exists(self.auto_login_path):
            os.remove(self.auto_login_path)

    def login(self):
        while True:
            self.show_login_window()
            login, IMAP_key = self.get_login_window_info()
            connect = connection.Connection(login, IMAP_key)
            status = connect.connect_to_mail_server()
            if not self.keep_work:
                sys.exit()
            elif status:
                self.IMAP_keys[login] = IMAP_key
                self.save_to_auto_login(login, IMAP_key)
                self.login_connection[login] = connect.connect
                return True

    def auto_login(self):
        if os.path.exists(self.auto_login_path):
            logins_IMAP_keys = self.get_auto_login_info()
            for login, IMAP_key in logins_IMAP_keys.items():
                connect = connection.Connection(login, IMAP_key)
                status = connect.connect_to_mail_server()
                if status:
                    self.IMAP_keys[login] = IMAP_key
                    self.login_connection[login] = connect.connect
                else:
                    self.remove_from_auto_login(login, IMAP_key)


class MessageWindow:
    def __init__(self, message_content, login):
        self.login = login
        self.message_content = message_content
        self.path = ""
        self.raw_folder_path = ""
        self.processed_folder_path = ""
        self.init_paths()
        self.process_thread = Thread()
        self.dialog = QtWidgets.QDialog()
        self.dialog_ui = UiMessageWindow()
        self.dialog_ui.setupUi(self.dialog, len(self.message_content["attachments"])*13)
        self.set_title()
        self.set_sender()
        self.set_body()
        self.set_button_functions()
        self.dialog.show()
        self.dialog.exec_()

    def set_title(self):
        self.dialog_ui.title_label.setText(self.message_content["title"])

    def set_sender(self):
        self.dialog_ui.sender_label.setText(self.message_content["sender"])

    def set_body(self):
        self.dialog_ui.body_textBrowser.setText(self.message_content["body"]["text"])
        self.dialog_ui.body_textBrowser.setHtml(self.message_content["body"]["html"])

    def set_button_functions(self):
        status = self.set_raw_button()
        if status:
            self.set_processed_button()

    def set_raw_button(self):
        if os.path.exists(self.raw_folder_path):
            self.dialog_ui.raw_pushButton.clicked.connect(lambda: os.startfile(self.raw_folder_path))
            self.process_attachments()
            return True
        else:
            self.hide_attachments_section()
            return False

    def set_processed_button(self):
        if os.path.exists(self.raw_folder_path):
            if not os.path.exists(self.processed_folder_path):
                os.mkdir(self.processed_folder_path)
            self.dialog_ui.processed_pushButton.clicked.connect(lambda: os.startfile(self.processed_folder_path))

    def process_attachments(self):
        event = Event()
        analise_list = []
        self.process_thread = Thread(target=FilesProcessor.process_files, args=(self.raw_folder_path,
                                                                                self.processed_folder_path,
                                                                                self.message_content["attachments"],
                                                                                event,
                                                                                analise_list,
                                                                                ))
        status_thread = Thread(target=self.status_label_function, args=(event, analise_list,))
        status_thread.start()
        self.process_thread.start()

    def status_label_function(self, event, analise_list):
        self.dialog_ui.processing_status_label.setStyleSheet("QLabel{ color: green; background-color: transparent;}")
        while not event.isSet():
            self.dialog_ui.processing_status_label.setText("Processing.")
            time.sleep(0.5)
            self.dialog_ui.processing_status_label.setText("Processing..")
            time.sleep(0.5)
            self.dialog_ui.processing_status_label.setText("Processing...")
            time.sleep(0.5)
        result = ''
        for item in analise_list:
            result += item + "\n"
            self.dialog_ui.attachments_processing_result_textBrowser.setText(result)
            self.dialog_ui.attachments_processing_result_textBrowser.setStyleSheet(
                "QLabel{background-color: lightgrey; padding: 0px; padding-left: 2px; padding-top: -5px}")
        self.dialog_ui.processing_status_label.setStyleSheet("QLabel{ color: blue; background-color: transparent;}")
        self.dialog_ui.processing_status_label.setText("Done!")

    def init_paths(self):
        mailbox = self.message_content["mailbox"]
        message_id = self.message_content["id"]
        self.path = os.path.join("temp", os.path.join(self.login, os.path.join(mailbox, os.path.join(str(message_id),
                                                                                                     "attachments"))))
        self.raw_folder_path = os.path.join(self.path, "raw")
        self.processed_folder_path = os.path.join(self.path, "processed")

    def hide_attachments_section(self):
        self.dialog_ui.raw_pushButton.hide()
        self.dialog_ui.attachments_label.hide()
        self.dialog_ui.processed_pushButton.hide()
        self.dialog_ui.attachments_processing_result_textBrowser.hide()
        self.dialog_ui.processing_status_label.hide()
        self.dialog.setMinimumSize(QtCore.QSize(750, 350))
        self.dialog.setMaximumSize(QtCore.QSize(750, 350))
        self.dialog.resize(750, 350)
