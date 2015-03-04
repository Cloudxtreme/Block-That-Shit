# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'update.ui'
#
# Created: Tue Mar  3 18:49:42 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(412, 92)
        self.pushButton_Download = QtGui.QPushButton(Dialog)
        self.pushButton_Download.setGeometry(QtCore.QRect(210, 60, 101, 23))
        self.pushButton_Download.setObjectName(_fromUtf8("pushButton_Download"))
        self.labelStatus = QtGui.QLabel(Dialog)
        self.labelStatus.setGeometry(QtCore.QRect(10, 20, 401, 16))
        self.labelStatus.setAlignment(QtCore.Qt.AlignCenter)
        self.labelStatus.setObjectName(_fromUtf8("labelStatus"))
        self.pushButton_Close = QtGui.QPushButton(Dialog)
        self.pushButton_Close.setGeometry(QtCore.QRect(320, 60, 80, 23))
        self.pushButton_Close.setObjectName(_fromUtf8("pushButton_Close"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.pushButton_Download.setText(_translate("Dialog", "Download", None))
        self.labelStatus.setText(_translate("Dialog", "You are already running the latest version!", None))
        self.pushButton_Close.setText(_translate("Dialog", "Close", None))

