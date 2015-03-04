# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'about.ui'
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
        Dialog.resize(499, 423)
        self.pushButton_Close = QtGui.QPushButton(Dialog)
        self.pushButton_Close.setGeometry(QtCore.QRect(410, 380, 80, 23))
        self.pushButton_Close.setObjectName(_fromUtf8("pushButton_Close"))
        self.label_Version = QtGui.QLabel(Dialog)
        self.label_Version.setGeometry(QtCore.QRect(170, 80, 550, 16))
        self.label_Version.setObjectName(_fromUtf8("label_Version"))
        self.label_Platform = QtGui.QLabel(Dialog)
        self.label_Platform.setGeometry(QtCore.QRect(170, 100, 550, 16))
        self.label_Platform.setObjectName(_fromUtf8("label_Platform"))
        self.label_License = QtGui.QLabel(Dialog)
        self.label_License.setGeometry(QtCore.QRect(170, 120, 550, 16))
        self.label_License.setOpenExternalLinks(True)
        self.label_License.setObjectName(_fromUtf8("label_License"))
        self.label_Title = QtGui.QLabel(Dialog)
        self.label_Title.setGeometry(QtCore.QRect(160, 10, 311, 31))
        self.label_Title.setTextFormat(QtCore.Qt.RichText)
        self.label_Title.setObjectName(_fromUtf8("label_Title"))
        self.label_Image = QtGui.QLabel(Dialog)
        self.label_Image.setGeometry(QtCore.QRect(9, 9, 128, 128))
        self.label_Image.setText(_fromUtf8(""))
        self.label_Image.setPixmap(QtGui.QPixmap(_fromUtf8("icons/block_blue.png")))
        self.label_Image.setObjectName(_fromUtf8("label_Image"))
        self.tabWidget = QtGui.QTabWidget(Dialog)
        self.tabWidget.setGeometry(QtCore.QRect(9, 164, 481, 201))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.scrollArea_2 = QtGui.QScrollArea(self.tab)
        self.scrollArea_2.setGeometry(QtCore.QRect(0, 0, 475, 171))
        self.scrollArea_2.setFrameShape(QtGui.QFrame.NoFrame)
        self.scrollArea_2.setFrameShadow(QtGui.QFrame.Plain)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName(_fromUtf8("scrollArea_2"))
        self.scrollAreaWidgetContents_2 = QtGui.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 461, 275))
        self.scrollAreaWidgetContents_2.setObjectName(_fromUtf8("scrollAreaWidgetContents_2"))
        self.gridLayout_2 = QtGui.QGridLayout(self.scrollAreaWidgetContents_2)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_AboutText = QtGui.QLabel(self.scrollAreaWidgetContents_2)
        self.label_AboutText.setTextFormat(QtCore.Qt.RichText)
        self.label_AboutText.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_AboutText.setWordWrap(True)
        self.label_AboutText.setMargin(15)
        self.label_AboutText.setOpenExternalLinks(True)
        self.label_AboutText.setObjectName(_fromUtf8("label_AboutText"))
        self.gridLayout_2.addWidget(self.label_AboutText, 0, 0, 1, 1)
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.scrollArea = QtGui.QScrollArea(self.tab_2)
        self.scrollArea.setGeometry(QtCore.QRect(0, 0, 475, 171))
        self.scrollArea.setFrameShape(QtGui.QFrame.NoFrame)
        self.scrollArea.setFrameShadow(QtGui.QFrame.Plain)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 461, 479))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.gridLayout = QtGui.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_BTSLicenseHeader = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_BTSLicenseHeader.setWordWrap(True)
        self.label_BTSLicenseHeader.setMargin(15)
        self.label_BTSLicenseHeader.setOpenExternalLinks(True)
        self.label_BTSLicenseHeader.setObjectName(_fromUtf8("label_BTSLicenseHeader"))
        self.gridLayout.addWidget(self.label_BTSLicenseHeader, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.label_Author = QtGui.QLabel(Dialog)
        self.label_Author.setGeometry(QtCore.QRect(170, 50, 371, 16))
        self.label_Author.setObjectName(_fromUtf8("label_Author"))

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "About", None))
        self.pushButton_Close.setText(_translate("Dialog", "Close", None))
        self.label_Version.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-weight:600;\">Version: 1.0</span></p></body></html>", None))
        self.label_Platform.setText(_translate("Dialog", "<html><head/><body><p>Platform: Linux</p></body></html>", None))
        self.label_License.setText(_translate("Dialog", "License: <a href=\"https://github.com/joeylane/Block-That-Shit/blob/master/LICENSE\">GNU/GPLv3</a>", None))
        self.label_Title.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:22pt; font-weight:600; color:#767676;\">Block-That-Shit</span></p></body></html>", None))
        self.label_AboutText.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-weight:600;\">Block-That-Shit</span> is a free, cross platform domain blocker developed by Joey Lane. The source code is available on my <a href=\"https://github.com/joeylane\"><span style=\" text-decoration: underline; color:#0000ff;\">GitHub page</span></a>. I sincerely hope that you find this software useful!</p><p>Binaries are available for Microsoft Windows, MacOS X, and Linux.</p><p>All program logic is written in Python. The GUI was developed using Qt with bindings provided by PyQt. The binaries for each supported operating system are built using PyInstaller.</p><p>Python version: 2.7.9</p><p>Qt version: 4.8.6</p><p>PyQt version: 4.10.4</p><p>PyInstaller version: 2.1</p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Dialog", "About", None))
        self.label_BTSLicenseHeader.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-weight:600;\">Block-That-Shit</span> is released under the <a href=\"https://github.com/joeylane/Block-That-Shit/blob/master/LICENSE\"><span style=\" text-decoration: underline; color:#0000ff;\">GNU/GPLv3</span></a> license.</p><p>Copyright (C) 2015 Joey Lane</p><p>This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.</p><p>This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.</p><p>You should have received a copy of the GNU General Public License along with this program. If not, see http://www.gnu.org/licenses/.</p><p><span style=\" font-weight:600;\">Python®</span> is provided under the <a href=\"https://www.python.org/download/releases/2.7/license/\"><span style=\" text-decoration: underline; color:#0000ff;\">Python Software Foundation license version 2</span></a>. Python is a registered trademark of the Python Software Foundation.</p><p><span style=\" font-weight:600;\">Qt®</span> is offered under multiple licenses. The <a href=\"http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html\"><span style=\" text-decoration: underline; color:#0000ff;\">GNU/LGPL Version 2.1</span></a> license was chosen for this project. Qt is a registered trade mark of Digia Plc.</p><p><span style=\" font-weight:600;\">PyQt</span> is offered under multiple licenses. The <a href=\"http://www.gnu.org/licenses/gpl.html\"><span style=\" text-decoration: underline; color:#0000ff;\">GNU/GPLv3</span></a> license was chosen for this project. PyQt is provided by Riverbank Computing Limited.</p><p><span style=\" font-weight:600;\">PyInstaller</span> is provided under the <a href=\"http://www.gnu.org/licenses/old-licenses/gpl-2.0.html\"><span style=\" text-decoration: underline; color:#0000ff;\">GNU/GPL Version 2</span></a> license. It is created and maintained by several volunteers on GitHub.</p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "License Details", None))
        self.label_Author.setText(_translate("Dialog", "Author: Joey Lane", None))

