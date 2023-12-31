# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\message.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class UiMessageWindow(object):
    def setupUi(self, MessageWindow, y_processing_buttons_shift):
        self.y_processing_buttons_shift = y_processing_buttons_shift
        MessageWindow.setObjectName("Message_Form")
        MessageWindow.resize(750, 400 + self.y_processing_buttons_shift)
        MessageWindow.setMinimumSize(QtCore.QSize(750, 400 + self.y_processing_buttons_shift))
        MessageWindow.setMaximumSize(QtCore.QSize(750, 400 + self.y_processing_buttons_shift))

        MessageWindow.setStyleSheet("@import url(\'https://fonts.googleapis.com/css2?family=Koulen&display=swap\');\n"
"\n"
"QDialog{ \n"
"    background-color: #dedede;\n"
"    font-family: \'Koulen\', cursive;\n"
"}\n"
"\n"
"QLabel {\n"
"    padding: 2px;\n"
"    background-color: #c7c7c7;\n"
"    border-radius: 3px;\n"
"}\n"
"\n"
"QTextBrowser {\n"
"    background-color: #f9f9f9;\n"
"    border: 1px solid #c9c9c9;\n"
"    border-radius: 2px;\n"
"}\n"
"\n"
"QPushButton{\n"
"    border: 1px solid;\n"
"    border-radius: 3px;\n"
"    border-color: #b5b5b5;\n"
"    background-color: #b5b5b5;\n"
"}\n"
"QPushButton:hover{\n"
"    border-radius: 3px;\n"
"    border-color: #a5a5a5;\n"
"    background-color: #a5a5a5;\n"
"}")

        font = QtGui.QFont()
        font.setFamily("Koulen,cursive")
        font.setPointSize(10)

        self.sender_label = QtWidgets.QLabel(MessageWindow)
        self.sender_label.setFont(font)
        self.sender_label.setGeometry(QtCore.QRect(10, 10, 730, 30))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sender_label.sizePolicy().hasHeightForWidth())
        self.sender_label.setSizePolicy(sizePolicy)
        self.sender_label.setObjectName("title_label")
        self.title_label = QtWidgets.QLabel(MessageWindow)
        font.setPointSize(8)
        self.title_label.setFont(font)
        self.title_label.setGeometry(QtCore.QRect(10, 45, 730, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.title_label.sizePolicy().hasHeightForWidth())
        self.title_label.setSizePolicy(sizePolicy)
        self.title_label.setStyleSheet("QLabel {\n"
"    background-color: transparent;\n"
"}")
        self.title_label.setObjectName("sender_label")

        self.body_textBrowser = QtWidgets.QTextBrowser(MessageWindow)
        self.body_textBrowser.setGeometry(QtCore.QRect(10, 70, 730, 270))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.body_textBrowser.sizePolicy().hasHeightForWidth())
        self.body_textBrowser.setSizePolicy(sizePolicy)
        self.body_textBrowser.setOpenExternalLinks(True)
        self.body_textBrowser.setObjectName("body_textBrowser")

        self.attachments_label = QtWidgets.QLabel(MessageWindow)
        self.attachments_label.setGeometry(QtCore.QRect(10, 345, 75, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.attachments_label.sizePolicy().hasHeightForWidth())
        self.attachments_label.setSizePolicy(sizePolicy)
        self.attachments_label.setObjectName("label_2")

        self.processing_status_label = QtWidgets.QLabel(MessageWindow)
        self.processing_status_label.setGeometry(QtCore.QRect(95, 345, 75, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.processing_status_label.sizePolicy().hasHeightForWidth())
        self.processing_status_label.setSizePolicy(sizePolicy)
        self.processing_status_label.setObjectName("label_2")

        self.attachments_processing_result_textBrowser = QtWidgets.QLabel(MessageWindow)
        self.attachments_processing_result_textBrowser.setGeometry(QtCore.QRect(10, 370, 730, self.y_processing_buttons_shift))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.attachments_processing_result_textBrowser.sizePolicy().hasHeightForWidth())
        self.attachments_processing_result_textBrowser.setSizePolicy(sizePolicy)
        self.attachments_processing_result_textBrowser.setObjectName("body_textBrowser")
        self.attachments_processing_result_textBrowser.setStyleSheet("QLabel{background-color: lightgrey; padding: 0px; padding-left: 2px;}")

        self.raw_pushButton = QtWidgets.QPushButton(MessageWindow)
        self.raw_pushButton.setGeometry(QtCore.QRect(10, 375 + self.y_processing_buttons_shift, 75, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.raw_pushButton.sizePolicy().hasHeightForWidth())
        self.raw_pushButton.setSizePolicy(sizePolicy)
        self.raw_pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.raw_pushButton.setObjectName("raw_pushButton")
        self.processed_pushButton = QtWidgets.QPushButton(MessageWindow)
        self.processed_pushButton.setGeometry(QtCore.QRect(95, 375 + self.y_processing_buttons_shift, 75, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.processed_pushButton.sizePolicy().hasHeightForWidth())
        self.processed_pushButton.setSizePolicy(sizePolicy)
        self.processed_pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.processed_pushButton.setObjectName("processed_pushButton")

        self.retranslateUi(MessageWindow)
        QtCore.QMetaObject.connectSlotsByName(MessageWindow)

    def retranslateUi(self, MessageWindow):
        _translate = QtCore.QCoreApplication.translate
        MessageWindow.setWindowTitle(_translate("Message_Form", "Dialog"))
        self.sender_label.setText(_translate("Message_Form", "Title"))
        self.title_label.setText(_translate("Message_Form", "Sender"))
        self.body_textBrowser.setHtml(_translate("Message_Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">BODY</p></body></html>"))
        self.attachments_label.setText(_translate("Message_Form", "Attachments:"))
        self.raw_pushButton.setText(_translate("Message_Form", "Raw"))
        self.processed_pushButton.setText(_translate("Message_Form", "Processed"))
