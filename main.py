import sys
from modules import interface

while True:
    # init windows
    main_window = interface.MainWindow()
    login_window = interface.LoginWindow()
    # login
    login_window.auto_login()
    if len(login_window.login_connection) == 0:
        login_window.login()
    # main
    main_window.show_main_window(login_window.login_connection, login_window.IMAP_keys)
    if not main_window.keep_work:
        sys.exit()

    if main_window.add_mail:
        login_window = interface.LoginWindow()
        login_window.login()




