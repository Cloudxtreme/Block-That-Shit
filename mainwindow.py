# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(583, 373)
        MainWindow.setFocusPolicy(QtCore.Qt.StrongFocus)
        MainWindow.setStyleSheet(_fromUtf8(""))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 60, 561, 271))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName(_fromUtf8("tab_4"))
        self.pushButton_Remove_Online_Blacklist = QtGui.QPushButton(self.tab_4)
        self.pushButton_Remove_Online_Blacklist.setGeometry(QtCore.QRect(440, 100, 111, 23))
        self.pushButton_Remove_Online_Blacklist.setObjectName(_fromUtf8("pushButton_Remove_Online_Blacklist"))
        self.pushButton_Add_Online_Blacklist = QtGui.QPushButton(self.tab_4)
        self.pushButton_Add_Online_Blacklist.setGeometry(QtCore.QRect(440, 70, 111, 23))
        self.pushButton_Add_Online_Blacklist.setObjectName(_fromUtf8("pushButton_Add_Online_Blacklist"))
        self.listWidget_Online_Blacklists = QtGui.QListWidget(self.tab_4)
        self.listWidget_Online_Blacklists.setGeometry(QtCore.QRect(10, 70, 421, 121))
        self.listWidget_Online_Blacklists.setObjectName(_fromUtf8("listWidget_Online_Blacklists"))
        item = QtGui.QListWidgetItem()
        self.listWidget_Online_Blacklists.addItem(item)
        self.label_LastDownloadedDateTime = QtGui.QLabel(self.tab_4)
        self.label_LastDownloadedDateTime.setGeometry(QtCore.QRect(20, 200, 291, 23))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_LastDownloadedDateTime.setFont(font)
        self.label_LastDownloadedDateTime.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label_LastDownloadedDateTime.setObjectName(_fromUtf8("label_LastDownloadedDateTime"))
        self.pushButton_Update_Hosts_File = QtGui.QPushButton(self.tab_4)
        self.pushButton_Update_Hosts_File.setGeometry(QtCore.QRect(440, 200, 111, 23))
        self.pushButton_Update_Hosts_File.setObjectName(_fromUtf8("pushButton_Update_Hosts_File"))
        self.label_OnlineBlacklists = QtGui.QLabel(self.tab_4)
        self.label_OnlineBlacklists.setGeometry(QtCore.QRect(10, 10, 541, 41))
        self.label_OnlineBlacklists.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_OnlineBlacklists.setWordWrap(True)
        self.label_OnlineBlacklists.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label_OnlineBlacklists.setObjectName(_fromUtf8("label_OnlineBlacklists"))
        self.tabWidget.addTab(self.tab_4, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.plainTextEdit_Domain_Blacklist = QtGui.QPlainTextEdit(self.tab_2)
        self.plainTextEdit_Domain_Blacklist.setGeometry(QtCore.QRect(10, 70, 541, 131))
        self.plainTextEdit_Domain_Blacklist.setLineWrapMode(QtGui.QPlainTextEdit.NoWrap)
        self.plainTextEdit_Domain_Blacklist.setPlainText(_fromUtf8(""))
        self.plainTextEdit_Domain_Blacklist.setTabStopWidth(80)
        self.plainTextEdit_Domain_Blacklist.setObjectName(_fromUtf8("plainTextEdit_Domain_Blacklist"))
        self.label_Blacklist_Tab_Descripton = QtGui.QLabel(self.tab_2)
        self.label_Blacklist_Tab_Descripton.setGeometry(QtCore.QRect(10, 10, 541, 41))
        self.label_Blacklist_Tab_Descripton.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_Blacklist_Tab_Descripton.setWordWrap(True)
        self.label_Blacklist_Tab_Descripton.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label_Blacklist_Tab_Descripton.setObjectName(_fromUtf8("label_Blacklist_Tab_Descripton"))
        self.pushButton_SaveBlackList = QtGui.QPushButton(self.tab_2)
        self.pushButton_SaveBlackList.setGeometry(QtCore.QRect(460, 210, 91, 23))
        self.pushButton_SaveBlackList.setObjectName(_fromUtf8("pushButton_SaveBlackList"))
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName(_fromUtf8("tab_3"))
        self.plainTextEdit_Domain_Whitelist = QtGui.QPlainTextEdit(self.tab_3)
        self.plainTextEdit_Domain_Whitelist.setGeometry(QtCore.QRect(10, 70, 541, 131))
        self.plainTextEdit_Domain_Whitelist.setLineWrapMode(QtGui.QPlainTextEdit.NoWrap)
        self.plainTextEdit_Domain_Whitelist.setObjectName(_fromUtf8("plainTextEdit_Domain_Whitelist"))
        self.label_Whitelist_Tab_Descripton = QtGui.QLabel(self.tab_3)
        self.label_Whitelist_Tab_Descripton.setGeometry(QtCore.QRect(10, 10, 541, 41))
        self.label_Whitelist_Tab_Descripton.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_Whitelist_Tab_Descripton.setWordWrap(True)
        self.label_Whitelist_Tab_Descripton.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label_Whitelist_Tab_Descripton.setObjectName(_fromUtf8("label_Whitelist_Tab_Descripton"))
        self.pushButton_SaveWhiteList = QtGui.QPushButton(self.tab_3)
        self.pushButton_SaveWhiteList.setGeometry(QtCore.QRect(460, 210, 91, 23))
        self.pushButton_SaveWhiteList.setObjectName(_fromUtf8("pushButton_SaveWhiteList"))
        self.tabWidget.addTab(self.tab_3, _fromUtf8(""))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.plainTextEdit_View_Hosts_File = QtGui.QPlainTextEdit(self.tab)
        self.plainTextEdit_View_Hosts_File.setGeometry(QtCore.QRect(10, 90, 541, 131))
        self.plainTextEdit_View_Hosts_File.setLineWrapMode(QtGui.QPlainTextEdit.NoWrap)
        self.plainTextEdit_View_Hosts_File.setReadOnly(True)
        self.plainTextEdit_View_Hosts_File.setObjectName(_fromUtf8("plainTextEdit_View_Hosts_File"))
        self.label_Hostsfile_Tab_Warning = QtGui.QLabel(self.tab)
        self.label_Hostsfile_Tab_Warning.setGeometry(QtCore.QRect(10, 10, 541, 51))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_Hostsfile_Tab_Warning.sizePolicy().hasHeightForWidth())
        self.label_Hostsfile_Tab_Warning.setSizePolicy(sizePolicy)
        self.label_Hostsfile_Tab_Warning.setMinimumSize(QtCore.QSize(0, 0))
        self.label_Hostsfile_Tab_Warning.setTextFormat(QtCore.Qt.AutoText)
        self.label_Hostsfile_Tab_Warning.setScaledContents(True)
        self.label_Hostsfile_Tab_Warning.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_Hostsfile_Tab_Warning.setWordWrap(True)
        self.label_Hostsfile_Tab_Warning.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label_Hostsfile_Tab_Warning.setObjectName(_fromUtf8("label_Hostsfile_Tab_Warning"))
        self.label = QtGui.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(10, 70, 91, 16))
        self.label.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label.setObjectName(_fromUtf8("label"))
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.label_DomainsBlocked = QtGui.QLabel(self.centralwidget)
        self.label_DomainsBlocked.setGeometry(QtCore.QRect(20, 20, 151, 21))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_DomainsBlocked.sizePolicy().hasHeightForWidth())
        self.label_DomainsBlocked.setSizePolicy(sizePolicy)
        self.label_DomainsBlocked.setScaledContents(True)
        self.label_DomainsBlocked.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label_DomainsBlocked.setObjectName(_fromUtf8("label_DomainsBlocked"))
        self.label_DomainCount = QtGui.QLabel(self.centralwidget)
        self.label_DomainCount.setGeometry(QtCore.QRect(180, 20, 51, 21))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_DomainCount.sizePolicy().hasHeightForWidth())
        self.label_DomainCount.setSizePolicy(sizePolicy)
        self.label_DomainCount.setScaledContents(True)
        self.label_DomainCount.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label_DomainCount.setObjectName(_fromUtf8("label_DomainCount"))
        self.pushButtonOnOff = QtGui.QPushButton(self.centralwidget)
        self.pushButtonOnOff.setGeometry(QtCore.QRect(490, 10, 71, 41))
        self.pushButtonOnOff.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButtonOnOff.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("icons/Switch-On-256.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonOnOff.setIcon(icon)
        self.pushButtonOnOff.setIconSize(QtCore.QSize(64, 64))
        self.pushButtonOnOff.setAutoDefault(False)
        self.pushButtonOnOff.setDefault(False)
        self.pushButtonOnOff.setFlat(True)
        self.pushButtonOnOff.setObjectName(_fromUtf8("pushButtonOnOff"))
        self.label_OnOff = QtGui.QLabel(self.centralwidget)
        self.label_OnOff.setGeometry(QtCore.QRect(440, 20, 41, 21))
        self.label_OnOff.setAlignment(QtCore.Qt.AlignCenter)
        self.label_OnOff.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label_OnOff.setObjectName(_fromUtf8("label_OnOff"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 583, 20))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        self.menuHosts_Settings = QtGui.QMenu(self.menubar)
        self.menuHosts_Settings.setObjectName(_fromUtf8("menuHosts_Settings"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setSizeGripEnabled(False)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionBackup_Hosts_File = QtGui.QAction(MainWindow)
        self.actionBackup_Hosts_File.setObjectName(_fromUtf8("actionBackup_Hosts_File"))
        self.actionRestore_Hosts_File = QtGui.QAction(MainWindow)
        self.actionRestore_Hosts_File.setObjectName(_fromUtf8("actionRestore_Hosts_File"))
        self.actionEdit_Hosts_File = QtGui.QAction(MainWindow)
        self.actionEdit_Hosts_File.setObjectName(_fromUtf8("actionEdit_Hosts_File"))
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.actionCheck_For_Updates = QtGui.QAction(MainWindow)
        self.actionCheck_For_Updates.setObjectName(_fromUtf8("actionCheck_For_Updates"))
        self.actionReport_A_Bug = QtGui.QAction(MainWindow)
        self.actionReport_A_Bug.setObjectName(_fromUtf8("actionReport_A_Bug"))
        self.actionWebsite = QtGui.QAction(MainWindow)
        self.actionWebsite.setObjectName(_fromUtf8("actionWebsite"))
        self.actionClear_Hosts_File = QtGui.QAction(MainWindow)
        self.actionClear_Hosts_File.setObjectName(_fromUtf8("actionClear_Hosts_File"))
        self.actionSave_Settings = QtGui.QAction(MainWindow)
        self.actionSave_Settings.setObjectName(_fromUtf8("actionSave_Settings"))
        self.actionRestore_Default_Settings = QtGui.QAction(MainWindow)
        self.actionRestore_Default_Settings.setObjectName(_fromUtf8("actionRestore_Default_Settings"))
        self.actionSave_Settings_When_Exiting = QtGui.QAction(MainWindow)
        self.actionSave_Settings_When_Exiting.setCheckable(True)
        self.actionSave_Settings_When_Exiting.setChecked(True)
        self.actionSave_Settings_When_Exiting.setObjectName(_fromUtf8("actionSave_Settings_When_Exiting"))
        self.actionInclude_IPv4_localhost = QtGui.QAction(MainWindow)
        self.actionInclude_IPv4_localhost.setCheckable(True)
        self.actionInclude_IPv4_localhost.setChecked(True)
        self.actionInclude_IPv4_localhost.setObjectName(_fromUtf8("actionInclude_IPv4_localhost"))
        self.actionInclude_IPv6_localhost = QtGui.QAction(MainWindow)
        self.actionInclude_IPv6_localhost.setCheckable(True)
        self.actionInclude_IPv6_localhost.setChecked(True)
        self.actionInclude_IPv6_localhost.setObjectName(_fromUtf8("actionInclude_IPv6_localhost"))
        self.actionInclude_IPv6_loopback = QtGui.QAction(MainWindow)
        self.actionInclude_IPv6_loopback.setCheckable(True)
        self.actionInclude_IPv6_loopback.setChecked(True)
        self.actionInclude_IPv6_loopback.setObjectName(_fromUtf8("actionInclude_IPv6_loopback"))
        self.actionInclude_IPv6_localnet = QtGui.QAction(MainWindow)
        self.actionInclude_IPv6_localnet.setCheckable(True)
        self.actionInclude_IPv6_localnet.setChecked(True)
        self.actionInclude_IPv6_localnet.setObjectName(_fromUtf8("actionInclude_IPv6_localnet"))
        self.actionInclude_IPv6_mcastprefix = QtGui.QAction(MainWindow)
        self.actionInclude_IPv6_mcastprefix.setCheckable(True)
        self.actionInclude_IPv6_mcastprefix.setChecked(True)
        self.actionInclude_IPv6_mcastprefix.setObjectName(_fromUtf8("actionInclude_IPv6_mcastprefix"))
        self.actionInclude_IPv6_allnodes = QtGui.QAction(MainWindow)
        self.actionInclude_IPv6_allnodes.setCheckable(True)
        self.actionInclude_IPv6_allnodes.setChecked(True)
        self.actionInclude_IPv6_allnodes.setObjectName(_fromUtf8("actionInclude_IPv6_allnodes"))
        self.actionInclude_IPv6_allrouters = QtGui.QAction(MainWindow)
        self.actionInclude_IPv6_allrouters.setCheckable(True)
        self.actionInclude_IPv6_allrouters.setChecked(True)
        self.actionInclude_IPv6_allrouters.setObjectName(_fromUtf8("actionInclude_IPv6_allrouters"))
        self.menuFile.addAction(self.actionSave_Settings)
        self.menuFile.addAction(self.actionSave_Settings_When_Exiting)
        self.menuFile.addAction(self.actionRestore_Default_Settings)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionBackup_Hosts_File)
        self.menuFile.addAction(self.actionRestore_Hosts_File)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionWebsite)
        self.menuHelp.addAction(self.actionCheck_For_Updates)
        self.menuHelp.addAction(self.actionReport_A_Bug)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout)
        self.menuHosts_Settings.addAction(self.actionInclude_IPv4_localhost)
        self.menuHosts_Settings.addAction(self.actionInclude_IPv6_localhost)
        self.menuHosts_Settings.addAction(self.actionInclude_IPv6_loopback)
        self.menuHosts_Settings.addAction(self.actionInclude_IPv6_localnet)
        self.menuHosts_Settings.addAction(self.actionInclude_IPv6_mcastprefix)
        self.menuHosts_Settings.addAction(self.actionInclude_IPv6_allnodes)
        self.menuHosts_Settings.addAction(self.actionInclude_IPv6_allrouters)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHosts_Settings.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Block That Shit", None))
        self.pushButton_Remove_Online_Blacklist.setText(_translate("MainWindow", "Remove", None))
        self.pushButton_Add_Online_Blacklist.setText(_translate("MainWindow", "Add", None))
        __sortingEnabled = self.listWidget_Online_Blacklists.isSortingEnabled()
        self.listWidget_Online_Blacklists.setSortingEnabled(False)
        item = self.listWidget_Online_Blacklists.item(0)
        item.setText(_translate("MainWindow", "https://raw.githubusercontent.com/joeylane/hosts/master/hosts", None))
        self.listWidget_Online_Blacklists.setSortingEnabled(__sortingEnabled)
        self.label_LastDownloadedDateTime.setText(_translate("MainWindow", "Last downloaded:  Never", None))
        self.pushButton_Update_Hosts_File.setText(_translate("MainWindow", "Download", None))
        self.label_OnlineBlacklists.setText(_translate("MainWindow", "<html><head/><body><p>Add any additional online hosts files you wish to download here.  Press the \'Download\' button to download, and parse the online lists into your hosts file.</p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "Online Blacklists", None))
        self.label_Blacklist_Tab_Descripton.setText(_translate("MainWindow", "Enter one domain per line.  Lines that start with the # sign will be treated as comments and ignored.  All domains entered here shall be blocked.", None))
        self.pushButton_SaveBlackList.setText(_translate("MainWindow", "Save", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Local Blacklist", None))
        self.label_Whitelist_Tab_Descripton.setText(_translate("MainWindow", "Enter one domain per line.  Lines that start with the # sign will be treated as comments and ignored.  Access will be permitted to any domains listed here.", None))
        self.pushButton_SaveWhiteList.setText(_translate("MainWindow", "Save", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Local Whitelist", None))
        self.label_Hostsfile_Tab_Warning.setText(_translate("MainWindow", "The hosts file is utilized by your operating system to assist with domain name resolution.  Block-That-Shit manipulates the hosts file, and forces any requests to blacklisted domains to redirect.", None))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600; color:#000000;\">READ ONLY:</span></p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "View Hosts File", None))
        self.label_DomainsBlocked.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:15px; font-weight:600;\">Domains Blocked: </span></p></body></html>", None))
        self.label_DomainCount.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:15px; font-weight:600; color:#1a9cff;\">0</span></p></body></html>", None))
        self.label_OnOff.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:16px; font-weight:600; color:#07b50d;\">On</span></p></body></html>", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuHelp.setTitle(_translate("MainWindow", "Help", None))
        self.menuHosts_Settings.setTitle(_translate("MainWindow", "Settings", None))
        self.actionBackup_Hosts_File.setText(_translate("MainWindow", "Backup Hosts File", None))
        self.actionRestore_Hosts_File.setText(_translate("MainWindow", "Restore Hosts File", None))
        self.actionEdit_Hosts_File.setText(_translate("MainWindow", "Edit Hosts File Manually", None))
        self.actionExit.setText(_translate("MainWindow", "Exit", None))
        self.actionAbout.setText(_translate("MainWindow", "About", None))
        self.actionCheck_For_Updates.setText(_translate("MainWindow", "Check For Updates", None))
        self.actionReport_A_Bug.setText(_translate("MainWindow", "Report A Bug", None))
        self.actionWebsite.setText(_translate("MainWindow", "Website", None))
        self.actionClear_Hosts_File.setText(_translate("MainWindow", "Clear Hosts File", None))
        self.actionSave_Settings.setText(_translate("MainWindow", "Save Settings", None))
        self.actionRestore_Default_Settings.setText(_translate("MainWindow", "Restore Default Settings", None))
        self.actionSave_Settings_When_Exiting.setText(_translate("MainWindow", "Save Settings When Exiting", None))
        self.actionInclude_IPv4_localhost.setText(_translate("MainWindow", "Include IPv4 localhost", None))
        self.actionInclude_IPv6_localhost.setText(_translate("MainWindow", "Include IPv6 localhost", None))
        self.actionInclude_IPv6_loopback.setText(_translate("MainWindow", "Include IPv6 loopback", None))
        self.actionInclude_IPv6_localnet.setText(_translate("MainWindow", "Include IPv6 localnet", None))
        self.actionInclude_IPv6_mcastprefix.setText(_translate("MainWindow", "Include IPv6 mcastprefix", None))
        self.actionInclude_IPv6_allnodes.setText(_translate("MainWindow", "Include IPv6 allnodes", None))
        self.actionInclude_IPv6_allrouters.setText(_translate("MainWindow", "Include IPv6 allrouters", None))

