# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'progressdialog.ui'
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
        Dialog.resize(479, 61)
        Dialog.setModal(True)
        self.progressBar = QtGui.QProgressBar(Dialog)
        self.progressBar.setGeometry(QtCore.QRect(10, 10, 461, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.label_Status = QtGui.QLabel(Dialog)
        self.label_Status.setGeometry(QtCore.QRect(10, 40, 461, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_Status.setFont(font)
        self.label_Status.setText(_fromUtf8(""))
        self.label_Status.setObjectName(_fromUtf8("label_Status"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))

