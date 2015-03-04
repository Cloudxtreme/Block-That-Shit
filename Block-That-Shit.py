import socket
import subprocess
import tempfile
import datetime
import time
import ctypes
import urllib2
import argparse
import webbrowser

from os.path import expanduser
from collections import OrderedDict
from shutil import copyfile
from PyQt4 import QtGui, QtCore
from ConfigParser import SafeConfigParser

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from appdirs import *

from mainwindow import Ui_MainWindow
import about
import update
import progressdialog



#region "Global variables"


# define global variables
applicationName = "Block-That-Shit"
applicationAuthor = "Joey Lane"
versionNumber = "1.0"
osPlatform = ""
hostsPath = "" # will store the path to the hosts file
homeDir = "" # will store the path to the current users home directory

# the redirection IP to use when parsing downloaded hosts files
redirectionIP = "127.0.0.1"

# these 2 variables are to simplify some cross thread calls when restoring a hosts file
restorePath = "" # will store the path of the selected hosts file to restore
restoreMoveOn = False # will let the worker thread know once the file dialog has closed on the main thread

# this variable holds the latest version number when the user checks for updates
latestVersionNumber = float()


#endregion


#region "Global functions"


# Elevate permissions and perform the cp/copy command based on the os environment
def ElevatedCopy(source, destination):

    if osPlatform == "linux":
        # encapsulate the paths with double quotes just in case there is a space in either path
        source = "\"" + source + "\""
        destination = "\"" + destination + "\""
        if os.geteuid() != 0:
            # determine which graphical sudo interface to prompt with
            if os.path.exists("/usr/bin/kdesudo"):
                process = subprocess.Popen("/usr/bin/kdesudo cp " + source + " " + destination, shell=True, stdout=subprocess.PIPE)
                process.wait()
            elif os.path.exists("/usr/bin/gksudo"):
                process = subprocess.Popen("/usr/bin/gksudo cp " + source + " " + destination, shell=True, stdout=subprocess.PIPE)
                process.wait()
            else:
                # fall back on policykit if kdesudo and gksudo do not exist
                process = subprocess.Popen("pkexec cp " + source + " " + destination, shell=True, stdout=subprocess.PIPE)
                process.wait()
        else:
            # we are already root
            process = subprocess.Popen("cp " + source + " " + destination, shell=True, stdout=subprocess.PIPE)
            process.wait()
    elif osPlatform == "darwin":
        if os.geteuid() != 0:
            # build our privilege escalation applescript in the temp directory
            scriptPath = os.path.join(tempfile.gettempdir(), "osx_elevate.sh")
            privElevationScript = open(scriptPath, "w+")
            privElevationScript.write("#!/bin/sh\n")
            privElevationScript.write('osascript -e "do shell script \\"$*\\" with administrator privileges"\n')
            privElevationScript.close()
            cpCommand = "cp " + "'" + source + "'" + " " + "'" + destination + "'"
            process = subprocess.Popen("sh " + scriptPath + " " + "\"" + cpCommand + "\"", shell=True, stdout=subprocess.PIPE)
            process.wait()
            # remove the privilege escalation script
            os.remove(scriptPath)
        else:
            # we are already root
            process = subprocess.Popen("cp " + "'" + source + "'" + " " + "'" + destination + "'", shell=True, stdout=subprocess.PIPE)
            process.wait()
    elif osPlatform == "win32":
        # encapsulate the paths with double quotes just in case there is a space in either path
        source = "\"" + source + "\""
        destination = "\"" + destination + "\""
        # determine if the user is running the program as administrator
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        if is_admin == False:
            # use our external elevate binary to give the user a UAC prompt
            # set the path to the binary based on if we are running from a onefile exe
            # or directly from python
            elevateExePath = os.path.join("\"" + getattr(sys, '_MEIPASS', os.getcwd()) + os.sep + "permission-elevation\"", "elevate.exe")
            process = subprocess.Popen(elevateExePath + " copy " + source + " " + destination, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            process.wait()
        else:
            # we are already running as administrator
            process = subprocess.Popen("copy " + source + " " + destination, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            process.wait()
    else:
        print "Something went wrong!  Unknown OS."

    # get the results of the os copy command to verify the hosts file was replaced
    return process.returncode


# AutoRun is run ONLY when the program is started with the --autorun flag
def AutoRun(settingsfile):
    if osPlatform == "linux":
        if os.geteuid() != 0:
            sys.exit("The autorun feature can only be run as root!")
    elif osPlatform == "darwin":
        if os.geteuid() != 0:
            sys.exit("The autorun feature can only be run as root!")
    elif osPlatform == "win32":
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        if is_admin == False:
            sys.exit("The autorun feature can only be run as administrator!")

    # load our settings file
    settingsPath = settingsfile

    # check if settings path exists first
    if os.path.exists(settingsPath):

        print "Loading settings file from: " + settingsPath

        # make sure we are connected to the internet
        updateTimeout = 0
        while not is_connected():
            time.sleep(60)
            updateTimeout += 1
            if updateTimeout == 5:
                sys.exit("No internet connection.  Operation timed out after 5 minutes.")

        config = SafeConfigParser()
        config.read(settingsPath)

        # a list of URLS to pull our blacklisted host entries from
        urls = []
        for url in config.items('Online_Blacklists'):
            urls.append(url[1])

        # an empty list variable to store our parsed out host entries
        blacklistedHosts = []

        # define a temp file for storing the downloaded data
        tempFile = os.path.join(tempfile.gettempdir(), "tmphosts")

        # iterate through each URL, and parse out the host entries provided
        for url in urls:
            try:
                link = urllib2.urlopen(str(url))

                meta = link.info()
                file_size = int(meta.getheaders('Content-Length')[0])

                # if temp file doesnt exist, create it, otherwise append to it
                if not os.path.exists(tempFile):
                    tempFileWrite = open(tempFile, "w+")
                else:
                    tempFileWrite = open(tempFile, "a")

                # write a newline first to make sure that if we are aggregating multiple online hosts files,
                # we do not end up writing the beginning line at the end of the previously downloaded hosts file
                tempFileWrite.write("\n")

                downloaded_bytes = 0
                block_size = 1024*8 # not sure if *8 is needed

                # write the data to the temp file and update our progress bar
                while True:
                    buffer = link.read(block_size)
                    if not buffer:
                        break
                    tempFileWrite.write(buffer)
                    downloaded_bytes += block_size

                tempFileWrite.close()

                # read the data from the temp file and process it into our list variable
                tempFileRead = open(tempFile, "r")

                for line in tempFileRead:
                    if not line.strip() == "":
                        if not line.strip().startswith("#"):
                            if not line.strip().endswith(" # LOCAL-BLACKLIST"):
                                # make sure we are parsing valid hosts file entries
                                if line.strip().startswith("127.0.0.1") or line.strip().startswith("0.0.0.0"):
                                    # if there is a comment after the host entry, strip it out
                                    hostEntry = line.split("#", 1)[0]
                                    blacklistedHosts.append(hostEntry.strip())
                        elif line.strip().endswith(" # LOCAL-WHITELIST"):
                            # if there is a comment after the host entry, strip it out
                            hostEntry = line.split("#", 1)[1]
                            blacklistedHosts.append(hostEntry.strip())

                tempFileRead.close()

            except:
                # online hosts file is not valid, move along
                pass

        # set the IP redirection for the blacklisted hosts
        for n,item in enumerate(blacklistedHosts):
            blacklistedHosts[n] = redirectionIP + " " + item.split()[1]

        # replace any tabs with a single space
        # add our custom blacklist entries, ignore our whitelist entries
        # and strip out any common local entries, as we will add them on our own next
        fileOutput = []
        ignoreEntries = [" ip6-localhost", " ip6-loopback", " ip6-localnet", " ip6-mcastprefix", " ip6-allnodes", " ip6-allrouters", " localhost"] # we should check for tabs too, TO DO

        whiteList = []
        for whitelistDomain in config.items('Domain_Whitelist'):
            if not str(whitelistDomain[1]).strip() == "":
                if not str(whitelistDomain[1]).strip().startswith("#"):
                    whiteList.extend([str(" " + str(whitelistDomain[1]))])

        for outputLine in blacklistedHosts:
            if not str(outputLine).endswith(tuple(ignoreEntries)):
                if str(outputLine).endswith(tuple(whiteList)):
                    fileOutput.append("%s\n" % ' '.join(str("# " + outputLine + " # LOCAL-WHITELIST").split()))
                else:
                    fileOutput.append("%s\n" % ' '.join(str(outputLine).split()))

        for blacklistDomain in config.items('Domain_Blacklist'):
            if not str(blacklistDomain[1]).strip() == "":
                if not str(blacklistDomain[1]).strip().startswith("#"):
                    fileOutput.append(redirectionIP + " " + str(blacklistDomain[1]).strip()  + " # LOCAL-BLACKLIST\n")

        # remove any duplicates we may have parsed
        fileOutput = list(OrderedDict.fromkeys(fileOutput))

        # get the total count of blocked domains
        totalBlockCount = 0
        for entry in fileOutput:
            if not str(entry).startswith("#"):
                totalBlockCount +=1

        # overwrite our temp file in the temp directory with the aggregated hosts data
        thefile = open(tempFile, "w")

        thefile.write("# This hosts file was generated by " + applicationName + "\n")
        thefile.write("# Generated on: " + time.strftime("%x") + " at " + time.strftime("%X") + "\n")
        thefile.write("# Currently blocking " + str(totalBlockCount) + " domains\n")

        # write out any optional host entries selected with the checkboxes
        if config.get('Hosts_File_Settings', 'ipv4_localhost') == "True":
            thefile.write("127.0.0.1 localhost\n")
        if config.get('Hosts_File_Settings', 'ipv6_localhost') == "True":
            thefile.write("::1 ip6-localhost\n")
        if config.get('Hosts_File_Settings', 'ipv6_loopback') == "True":
            thefile.write("::1 ip6-loopback\n")
        if config.get('Hosts_File_Settings', 'ipv6_localnet') == "True":
            thefile.write("fe00::0 ip6-localnet\n")
        if config.get('Hosts_File_Settings', 'ipv6_mcastprefix') == "True":
            thefile.write("ff00::0 ip6-mcastprefix\n")
        if config.get('Hosts_File_Settings', 'ipv6_allnodes') == "True":
            thefile.write("ff02::1 ip6-allnodes\n")
        if config.get('Hosts_File_Settings', 'ipv6_allrouters') == "True":
            thefile.write("ff02::2 ip6-allrouters\n")

        # write our our aggregated black list
        for hostLine in fileOutput:
            thefile.write(hostLine)
        thefile.close()

        # print out the new stats, if we encountered an error, notify the user.
        if ElevatedCopy(tempFile, hostsPath) == 0:
            print "Hosts file updated successfully!  Currently blocking " + str(totalBlockCount) + " domains."
        else:
            print "Hosts file was not updated!"

        # remove the temp file
        os.remove(tempFile)

    else:
        print "No settings file was found!"


# tell us if we are connected to the internet or not
def is_connected():
    try:
        s = socket.create_connection(("8.8.8.8", 53), 2)
        s.close()
        return True
    except:
        pass
    return False


#endregion


class ControlMainWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(ControlMainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        global osPlatform
        global hostsPath
        global homeDir

        # configure our worker threads for making cross thread calls to the gui
        # this is so we can download/modify our files in a separate thread, and still
        # update our progress bar, and other gui controls on the main thread
        self.downloadworker = DownloadWorker(self)
        self.downloadworker.showProgress.connect(self.showProgress)
        self.downloadworker.updateProgress.connect(self.setProgress)
        self.downloadworker.buttonsEnabled.connect(self.buttonsenabled)
        self.downloadworker.statusBarChangeText.connect(self.statusBarChangeText)
        self.downloadworker.onOffSwitch.connect(self.onOffSwitch)

        self.saveblackandwhitelistsworker = SaveBlackAndWhitelistsWorker(self)
        self.saveblackandwhitelistsworker.showProgress.connect(self.showProgress)
        self.saveblackandwhitelistsworker.updateProgress.connect(self.setProgress)
        self.saveblackandwhitelistsworker.buttonsEnabled.connect(self.buttonsenabled)
        self.saveblackandwhitelistsworker.statusBarChangeText.connect(self.statusBarChangeText)
        self.saveblackandwhitelistsworker.onOffSwitch.connect(self.onOffSwitch)

        self.updateworker = UpdateWorker(self)
        self.updateworker.updateDialogChangeText.connect(self.updateDialogChangeText)
        self.updateworker.updateDialogShowDownloadButton.connect(self.updateDialogShowDownloadButton)

        self.updateDialog = QtGui.QDialog(self)
        self.updateUi = update.Ui_Dialog()
        self.updateUi.setupUi(self.updateDialog)
        self.updateUi.pushButton_Download.clicked.connect(self.openUpdatePage)
        self.updateUi.pushButton_Close.clicked.connect(self.updateDialog.close)
        self.updateDialog.setWindowTitle("Checking for updates")
        self.updateDialog.setFixedSize(self.updateDialog.size())

        self.restorehostsfileworker = RestoreHostsFileWorker(self)
        self.restorehostsfileworker.getFileToRestore.connect(self.restorehostsfiledialog)
        self.restorehostsfileworker.showProgress.connect(self.showProgress)
        self.restorehostsfileworker.updateProgress.connect(self.setProgress)
        self.restorehostsfileworker.buttonsEnabled.connect(self.buttonsenabled)
        self.restorehostsfileworker.statusBarChangeText.connect(self.statusBarChangeText)

        self.progressDialog = QtGui.QDialog(self)
        self.progressUi = progressdialog.Ui_Dialog()
        self.progressUi.setupUi(self.progressDialog)
        self.progressDialog.setWindowTitle("Progress")
        self.progressDialog.setFixedSize(self.progressDialog.size())

        self.setWindowIcon(QtGui.QIcon(os.path.join(getattr(sys, '_MEIPASS', os.getcwd()) + os.sep + "icons", "block_blue.png")))

        # make sure window is not resizeable
        self.setFixedSize(self.size())

        # center the window
        self.move(QtGui.QApplication.desktop().screen().rect().center()- self.rect().center())

        # initialize file menu
        self.ui.actionSave_Settings.triggered.connect(self.savesettings)
        self.ui.actionRestore_Default_Settings.triggered.connect(self.restoredefaulsettings)
        self.ui.actionBackup_Hosts_File.triggered.connect(self.backuphostsfile)
        self.ui.actionRestore_Hosts_File.triggered.connect(self.restorehostsfileworker.start)
        self.ui.actionExit.triggered.connect(self.appexit)

        # initialize help menu
        self.ui.actionWebsite.triggered.connect(self.showwebsite)
        self.ui.actionCheck_For_Updates.triggered.connect(self.checkupdates)
        self.ui.actionReport_A_Bug.triggered.connect(self.reportbug)
        self.ui.actionAbout.triggered.connect(self.about)

        # initialize buttons
        self.ui.pushButton_Update_Hosts_File.clicked.connect(self.downloadworker.start)
        self.ui.pushButton_SaveBlackList.clicked.connect(self.saveblackandwhitelistsworker.start)
        self.ui.pushButton_SaveWhiteList.clicked.connect(self.saveblackandwhitelistsworker.start)
        self.ui.pushButton_Add_Online_Blacklist.clicked.connect(self.addonlineblacklist)
        self.ui.pushButton_Remove_Online_Blacklist.clicked.connect(self.removeonlineblacklist)
        self.ui.pushButtonOnOff.clicked.connect(self.onOffSwitch)

        # create a label on the status bar
        self.statusText = QtGui.QLabel("")
        self.statusText.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.ui.statusbar.addPermanentWidget(self.statusText, 1)

        # load the current hosts file and update the status bar
        self.gethostsfile()

        # load our settings file if there is one
        self.loadsettings()


    #region "Buttons and menu item event handlers"


    # backup the current hosts file
    def backuphostsfile(self):
        global homeDir
        dateAndTime = datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')

        fileDialog = QFileDialog.getSaveFileName(None, "Save Backup", os.path.join(homeDir, dateAndTime + ".hostsbackup"), "Hosts Backups (*.hostsbackup)")
        if fileDialog != "":
            try:
                fileName = str(fileDialog)
                if not fileName.endswith(".hostsbackup"):
                    fileName = fileName + ".hostsbackup"
                copyfile(hostsPath, fileName)
                homeDir = os.path.dirname(fileName)
                self.statusBarChangeText("Hosts file was backed up successfully!", "green")
            except:
                self.statusBarChangeText("Hosts file was NOT backed up!", "red")


    # exit the program
    def appexit(self):
        self.close()


    # display the website
    def showwebsite(self):
        url = "https://github.com/joeylane/Block-That-Shit"
        webbrowser.open(url, new=0, autoraise=True)


    # check for updates
    def checkupdates(self):
        # make sure we are online first
        if not is_connected():
            self.statusBarChangeText("You are not connected to the internet!", "red")
            return
        self.updateUi.pushButton_Download.setVisible(False)
        self.updateworker.start()
        self.updateDialog.exec_()


    # report a bug
    def reportbug(self):
        url = "https://github.com/joeylane/Block-That-Shit/issues"
        webbrowser.open(url, new=0, autoraise=True)


    # display the about dialog
    def about(self):
        import platform
        aboutDialog = QtGui.QDialog(self)
        aboutUi = about.Ui_Dialog()
        aboutUi.setupUi(aboutDialog)
        aboutUi.pushButton_Close.clicked.connect(aboutDialog.close)

        aboutUi.label_Title.setText('<html><head/><body><p><span style=" font-size:22pt; font-weight:600; color:#767676;">' + applicationName + '</span></p></body></html>')
        aboutUi.label_Author.setText("Author: " + applicationAuthor)
        aboutUi.label_Version.setText('<html><head/><body><p><span style=" font-weight:600;">Version: ' + versionNumber + '</span></p></body></html>')
        aboutUi.label_Platform.setText("Platform: " + platform.system() + " " + platform.release())

        imagePath = os.path.join(getattr(sys, '_MEIPASS', os.getcwd()) + os.sep + "icons", "block_blue.png")
        aboutUi.label_Image.setPixmap(QtGui.QPixmap(imagePath))
        # make sure window is not resizeable
        aboutDialog.setFixedSize(aboutDialog.size())
        aboutDialog.exec_()


    # add an online blacklist link
    def addonlineblacklist(self):
        dlg =  QtGui.QInputDialog(self)
        dlg.setInputMode( QtGui.QInputDialog.TextInput)
        dlg.setLabelText("Enter the hosts file URL:")
        dlg.setWindowTitle("Add online blacklist")
        dlg.setFixedSize(500, 100)
        ok = dlg.exec_()
        if ok:
            url = str(dlg.textValue()).strip()
            if not url == "":
                if not " " in url:
                    self.ui.listWidget_Online_Blacklists.addItem(url)


    # remove selected online blacklists
    def removeonlineblacklist(self):
        for item in self.ui.listWidget_Online_Blacklists.selectedItems():
            self.ui.listWidget_Online_Blacklists.takeItem(self.ui.listWidget_Online_Blacklists.row(item))


    # restore default settings
    def restoredefaulsettings(self):
        dialog = QtGui.QMessageBox.information(self, 'Restore defaults?', 'Are you sure you want to restore the default settings?', buttons = QtGui.QMessageBox.Ok|QtGui.QMessageBox.Cancel)
        if dialog == QtGui.QMessageBox.Ok:
            self.ui.actionInclude_IPv4_localhost.setChecked(Qt.Checked)
            self.ui.actionInclude_IPv6_localhost.setChecked(Qt.Checked)
            self.ui.actionInclude_IPv6_loopback.setChecked(Qt.Checked)
            self.ui.actionInclude_IPv6_localnet.setChecked(Qt.Checked)
            self.ui.actionInclude_IPv6_mcastprefix.setChecked(Qt.Checked)
            self.ui.actionInclude_IPv6_allnodes.setChecked(Qt.Checked)
            self.ui.actionInclude_IPv6_allrouters.setChecked(Qt.Checked)
            self.ui.actionSave_Settings_When_Exiting.setChecked(Qt.Checked)

            self.ui.listWidget_Online_Blacklists.clear()
            self.ui.listWidget_Online_Blacklists.addItem("https://raw.githubusercontent.com/joeylane/hosts/master/hosts")


    # on/off push button
    def onOffSwitch(self, onOff=None):
        if self.ui.label_OnOff.text().contains("Off"):
            if onOff == "off":
                self.switchIsOff()
            else:
                # user is turning the switch on
                # check to see if a modified hosts file exists in the settings directory
                settingsPathNewHosts = os.path.join(user_data_dir(applicationName, applicationAuthor), "newhosts")
                if not os.path.exists(settingsPathNewHosts):
                    self.statusBarChangeText("No blacklist found, press the download button first!", "red")
                    return
                self.switchIsOn()
        elif self.ui.label_OnOff.text().contains("On"):
            if onOff == "on":
                self.switchIsOn()
            else:
                # user is turning the switch off
                self.switchIsOff()


    #endregion


    #region "Helper functions"


    # open the contents of the hosts file
    def gethostsfile(self):
        global hostsPath
        hosts = open(hostsPath,'r').read()

        # load the current hosts file, and determine how many entries we have
        mycount = 0
        fileHeader = []
        fileHeaderCount = 0

        ignoreEntries = [" ip6-localhost", " ip6-loopback", " ip6-localnet", " ip6-mcastprefix", " ip6-allnodes", " ip6-allrouters", " localhost"] # we should check for tabs too, TO DO
        for line in hosts.split("\n"):

            # grab the first 3 lines of the file as our 'header', which contains our stats
            fileHeaderCount += 1
            if fileHeaderCount <= 3:
                fileHeader.append(line)

            if not line.strip() == "":
                if not line.startswith("#"):
                    if not line.endswith(tuple(ignoreEntries)):
                        mycount += 1

        palette = QPalette()
        palette.setColor(QPalette.Text,Qt.darkGray)
        self.ui.plainTextEdit_View_Hosts_File.setPalette(palette)

        # populate the view hosts file plainTextEdit
        self.ui.plainTextEdit_View_Hosts_File.setPlainText(hosts)

        # determine if the switch should be enabled or not
        try:
            # read the 3rd line, and determine how many domains are being blocked
            if int(str(fileHeader[2]).split(" ")[3]) > 0:
                self.labelOnOff(True)
                self.pushButtonOnOffSetIcon(True)
            else:
                self.labelOnOff(False)
                self.pushButtonOnOffSetIcon(False)
        except:
            # this should only fire when we are dealing with a hosts file we didn't generate
            self.labelOnOff(False)
            self.pushButtonOnOffSetIcon(False)
            mycount = 0

        # update the DomainCount label to show how many current hosts entries we have
        self.ui.label_DomainsBlocked.adjustSize()
        self.ui.label_DomainCount.setTextFormat(Qt.RichText)
        self.ui.label_DomainCount.setText('<html><head/><body><p><span style="font-size:15px; font-weight:600; color:#1a9cff;">' + str("{:,}".format(mycount)) + '</span></p></body></html>')
        self.ui.label_DomainCount.adjustSize()

        # update our LastDownloadedDateTime label to show our date statistics
        try:
            settingsPathNewHosts = os.path.join(user_data_dir(applicationName, applicationAuthor), "newhosts")

            with open(settingsPathNewHosts) as myfile:
                head = [next((myfile)) for x in xrange(2)]
            lastDownload =  str(head[1]).split(" ")[3] + " at " + str(head[1]).split(" ")[5] + " " + str(head[1]).split(" ")[6]
            self.ui.label_LastDownloadedDateTime.setText("Last downloaded: " + lastDownload)
            self.ui.label_LastDownloadedDateTime.setTextFormat(Qt.RichText) # this make sure to vertical align the text
        except:
            self.ui.label_LastDownloadedDateTime.setText("Last downloaded: NEVER")
            self.ui.label_LastDownloadedDateTime.setTextFormat(Qt.RichText) # this make sure to vertical align the text


    # show progress dialog
    def showProgress(self, boolean):
        if boolean == True:
            self.progressDialog.exec_()
        else:
            self.progressDialog.close()


    # this helps us update the progress bar from the worker thread
    def setProgress(self, value, text):
        if value > 100:
            value = 100
        if not text == "":
            self.progressUi.label_Status.setText(text)
        self.progressUi.progressBar.setValue(value)


    # enable/disable the user controls
    def buttonsenabled(self, boolean):
        self.ui.pushButton_Update_Hosts_File.setEnabled(boolean)
        self.ui.tabWidget.setEnabled(boolean)
        self.ui.menubar.setEnabled(boolean)
        self.ui.pushButtonOnOff.setEnabled(boolean)


    # this allows us to retrieve user input from the gui from the worker thread
    def getVars(self):
        # a list of URLS to pull our blacklisted host entries from
        urls = []
        for index in xrange(self.ui.listWidget_Online_Blacklists.count()):
            urls.append(self.ui.listWidget_Online_Blacklists.item(index).text())

        return urls


    # save our settings
    def savesettings(self):

        # check if the app settings directory exists, and create it if not.
        if not os.path.exists(user_data_dir(applicationName, applicationAuthor)):
            os.makedirs(user_data_dir(applicationName, applicationAuthor))

        settingsPath = os.path.join(user_data_dir(applicationName, applicationAuthor), "settings.cfg")

        # remove old settings file before storing new one
        if os.path.exists(settingsPath):
            os.remove(settingsPath)

        config = SafeConfigParser()
        config.read(settingsPath)
        config.add_section('Hosts_File_Settings')
        config.add_section('Online_Blacklists')
        config.add_section('Domain_Blacklist')
        config.add_section('Domain_Whitelist')

        # save basic hosts file settings
        config.set('Hosts_File_Settings', 'ipv4_localhost', str(self.ui.actionInclude_IPv4_localhost.isChecked()))
        config.set('Hosts_File_Settings', 'ipv6_localhost', str(self.ui.actionInclude_IPv6_localhost.isChecked()))
        config.set('Hosts_File_Settings', 'ipv6_loopback', str(self.ui.actionInclude_IPv6_loopback.isChecked()))
        config.set('Hosts_File_Settings', 'ipv6_localnet', str(self.ui.actionInclude_IPv6_localnet.isChecked()))
        config.set('Hosts_File_Settings', 'ipv6_mcastprefix', str(self.ui.actionInclude_IPv6_mcastprefix.isChecked()))
        config.set('Hosts_File_Settings', 'ipv6_allnodes', str(self.ui.actionInclude_IPv6_allnodes.isChecked()))
        config.set('Hosts_File_Settings', 'ipv6_allrouters', str(self.ui.actionInclude_IPv6_allrouters.isChecked()))
        config.set('Hosts_File_Settings', 'save_settings_on_exit', str(self.ui.actionSave_Settings_When_Exiting.isChecked()))

        # save the online blacklists
        for i in range(self.ui.listWidget_Online_Blacklists.count()):
            config.set('Online_Blacklists', str(i), str(self.ui.listWidget_Online_Blacklists.item(i).text()))

        # save our custom blacklist entries
        blacklistLineCount = 0
        for line in self.ui.plainTextEdit_Domain_Blacklist.toPlainText().split("\n"):
            config.set('Domain_Blacklist', str(blacklistLineCount), str(line))
            blacklistLineCount += 1

        # save our custom whitelist entries
        whiteLineCount = 0
        for line in self.ui.plainTextEdit_Domain_Whitelist.toPlainText().split("\n"):
            config.set('Domain_Whitelist', str(whiteLineCount), str(line))
            whiteLineCount += 1

        # write the config file
        with open(settingsPath, 'w') as f:
            config.write(f)


    # load configuration settings
    def loadsettings(self):

        settingsPath = os.path.join(user_data_dir(applicationName, applicationAuthor), "settings.cfg")

        # check if settings path exists first
        if os.path.exists(settingsPath):
            config = SafeConfigParser()
            config.read(settingsPath)

            # load basic hosts file settings
            if config.get('Hosts_File_Settings', 'ipv4_localhost') == "True":
                self.ui.actionInclude_IPv4_localhost.setChecked(Qt.Checked)
            else:
                self.ui.actionInclude_IPv4_localhost.setChecked(Qt.Unchecked)
            if config.get('Hosts_File_Settings', 'ipv6_localhost') == "True":
                self.ui.actionInclude_IPv6_localhost.setChecked(Qt.Checked)
            else:
                self.ui.actionInclude_IPv6_localhost.setChecked(Qt.Unchecked)
            if config.get('Hosts_File_Settings', 'ipv6_loopback') == "True":
                self.ui.actionInclude_IPv6_loopback.setChecked(Qt.Checked)
            else:
                self.ui.actionInclude_IPv6_loopback.setChecked(Qt.Unchecked)
            if config.get('Hosts_File_Settings', 'ipv6_localnet') == "True":
                self.ui.actionInclude_IPv6_localnet.setChecked(Qt.Checked)
            else:
                self.ui.actionInclude_IPv6_localnet.setChecked(Qt.Unchecked)
            if config.get('Hosts_File_Settings', 'ipv6_mcastprefix') == "True":
                self.ui.actionInclude_IPv6_mcastprefix.setChecked(Qt.Checked)
            else:
                self.ui.actionInclude_IPv6_mcastprefix.setChecked(Qt.Unchecked)
            if config.get('Hosts_File_Settings', 'ipv6_allnodes') == "True":
                self.ui.actionInclude_IPv6_allnodes.setChecked(Qt.Checked)
            else:
                self.ui.actionInclude_IPv6_allnodes.setChecked(Qt.Unchecked)
            if config.get('Hosts_File_Settings', 'ipv6_allrouters') == "True":
                self.ui.actionInclude_IPv6_allrouters.setChecked(Qt.Checked)
            else:
                self.ui.actionInclude_IPv6_allrouters.setChecked(Qt.Unchecked)
            if config.get('Hosts_File_Settings', 'save_settings_on_exit') == "True":
                self.ui.actionSave_Settings_When_Exiting.setChecked(Qt.Checked)
            else:
                self.ui.actionSave_Settings_When_Exiting.setChecked(Qt.Unchecked)

            # load online blacklists
            self.ui.listWidget_Online_Blacklists.clear()
            for url in config.items('Online_Blacklists'):
                self.ui.listWidget_Online_Blacklists.addItem(url[1])

            # load our custom blacklist
            for domain in config.items('Domain_Blacklist'):
                self.ui.plainTextEdit_Domain_Blacklist.appendPlainText(domain[1])

            # load our custom whitelist
            for domain in config.items('Domain_Whitelist'):
                self.ui.plainTextEdit_Domain_Whitelist.appendPlainText(domain[1])


    # show the file dialog to select a hosts file to restore
    def restorehostsfiledialog(self):
        # this is called from the worker thread to display our file dialog.  once we change the restoreMoveOn variable
        # to True, the worker thread will continue operations.
        global homeDir
        global restorePath
        global restoreMoveOn
        fileDialog = QFileDialog.getOpenFileName(None, "Restore Backup", homeDir, "Hosts Backups (*.hostsbackup)")
        if fileDialog != "":
            if osPlatform == "win32":
                restorePath = str(fileDialog).replace("/", "\\")
            else:
                restorePath = str(fileDialog)
        else:
            restorePath = ""
        restoreMoveOn = True


    # update status bar text
    def statusupdate(self, text, color):
        self.statusText.setStyleSheet(' QLabel {color: ' + color + '}')
        self.statusText.setText(text)


    # change the text on the status bar
    def statusBarChangeText(self, message, color):
        self.updatestatusbarworker = UpdateStatusBarWorker(self, message, color)
        self.updatestatusbarworker.statusUpdate.connect(self.statusupdate)
        self.updatestatusbarworker.getHostsfile.connect(self.gethostsfile)
        self.updatestatusbarworker.start()


    # change the text on the update dialog
    def updateDialogChangeText(self, text):
        self.updateUi.labelStatus.setText(text)


    # choose which download page to show when updating
    def openUpdatePage(self, version):
        webbrowser.open("https://github.com/joeylane/Block-That-Shit/releases/tag/v" + str(latestVersionNumber), autoraise=True)
        self.updateDialog.close()


    # show download button on the update dialog
    def updateDialogShowDownloadButton(self, boolean):
        self.updateUi.pushButton_Download.setVisible(boolean)

    # change the text label by the on/off switch
    def labelOnOff(self, boolean):
        if boolean:
            self.ui.label_OnOff.setText('<html><head/><body><p><span style="font-size:16px; font-weight:600; color:#07b50d;">On</span></p></body></html>')
        else:
            self.ui.label_OnOff.setText('<html><head/><body><p><span style="font-size:16px; font-weight:600; color:#da0000;">Off</span></p></body></html>')


    # change the icon of the on/off switch
    def pushButtonOnOffSetIcon(self, boolean):
        if boolean:
            imagePath = os.path.join(getattr(sys, '_MEIPASS', os.getcwd()) + os.sep + "icons", "Switch-On-256.png")
            self.ui.pushButtonOnOff.setIcon(QtGui.QIcon(imagePath))
        else:
            imagePath = os.path.join(getattr(sys, '_MEIPASS', os.getcwd()) + os.sep + "icons", "Switch-Off-256.png")
            self.ui.pushButtonOnOff.setIcon(QtGui.QIcon(imagePath))


    # start onoffworker with the switch on
    def switchIsOn(self):
        self.onoffworker = OnOffWorker(self, True)
        self.onoffworker.showProgress.connect(self.showProgress)
        self.onoffworker.updateProgress.connect(self.setProgress)
        self.onoffworker.buttonsEnabled.connect(self.buttonsenabled)
        self.onoffworker.statusBarChangeText.connect(self.statusBarChangeText)
        self.onoffworker.labelOnOff.connect(self.labelOnOff)
        self.onoffworker.pushButtonOnOffSetIcon.connect(self.pushButtonOnOffSetIcon)
        self.onoffworker.start()


    # start onoffworker with the switch off
    def switchIsOff(self):
        self.onoffworker = OnOffWorker(self, False)
        self.onoffworker.showProgress.connect(self.showProgress)
        self.onoffworker.updateProgress.connect(self.setProgress)
        self.onoffworker.buttonsEnabled.connect(self.buttonsenabled)
        self.onoffworker.statusBarChangeText.connect(self.statusBarChangeText)
        self.onoffworker.labelOnOff.connect(self.labelOnOff)
        self.onoffworker.pushButtonOnOffSetIcon.connect(self.pushButtonOnOffSetIcon)
        self.onoffworker.start()


    #endregion


    # handle any events before the program closes
    def closeEvent(self, event):
        # save our settings if required
        if self.ui.actionSave_Settings_When_Exiting.isChecked():
            self.savesettings()


class DownloadWorker(QtCore.QThread):

    # This is the signal that will be emitted during the processing.
    showProgress = QtCore.pyqtSignal(bool)
    updateProgress = QtCore.pyqtSignal(int, str)
    buttonsEnabled = QtCore.pyqtSignal(bool)
    statusBarChangeText = QtCore.pyqtSignal(str, str)
    onOffSwitch = QtCore.pyqtSignal(str)

    def __init__(self, instance):
        QtCore.QThread.__init__(self)
        self.instance = instance


    def run(self):

        # make sure we are online first
        if not is_connected():
            self.statusBarChangeText.emit("You are not connected to the internet!", "red")
            return

        # show progress dialog
        self.showProgress.emit(True)

        # disable user controls while we update
        self.buttonsEnabled.emit(False)

        # get the online blacklist urls from the gui
        urls = ControlMainWindow.getVars(self.instance)

        # an empty list variable to store our parsed out host entries
        blacklistedHosts = []

        # define a temp file for storing the downloaded data
        tempFile = os.path.join(tempfile.gettempdir(), "tmphosts")

        # iterate through each URL, and parse out the host entries provided
        for url in urls:
            try:
                # reset progress bar
                self.updateProgress.emit(0, "Downloading: " + url)

                link = urllib2.urlopen(str(url))

                meta = link.info()
                file_size = int(meta.getheaders('Content-Length')[0])

                # if temp file doesnt exist, create it, otherwise append to it
                if not os.path.exists(tempFile):
                    tempFileWrite = open(tempFile, "w+")
                else:
                    tempFileWrite = open(tempFile, "a")

                # write a newline first to make sure that if we are aggregating multiple online hosts files,
                # we do not end up writing the beginning line at the end of the previously downloaded hosts file
                tempFileWrite.write("\n")

                downloaded_bytes = 0
                block_size = 1024*8 # not sure if *8 is needed

                # write the data to the temp file and update our progress bar
                while True:
                    buffer = link.read(block_size)
                    if not buffer:
                        break
                    tempFileWrite.write(buffer)
                    downloaded_bytes += block_size
                    self.updateProgress.emit(float(downloaded_bytes)/file_size*100, "")

                tempFileWrite.close()

                # read the data from the temp file and process it into our list variable
                tempFileRead = open(tempFile, "r")

                for line in tempFileRead:
                    if not line.strip() == "":
                        if not line.strip().startswith("#"):
                            if not line.strip().endswith(" # LOCAL-BLACKLIST"):
                                # make sure we are parsing valid hosts file entries
                                if line.strip().startswith("127.0.0.1") or line.strip().startswith("0.0.0.0"):
                                    # if there is a comment after the host entry, strip it out
                                    hostEntry = line.split("#", 1)[0]
                                    blacklistedHosts.append(hostEntry.strip())
                        elif line.strip().endswith(" # LOCAL-WHITELIST"):
                            # if there is a comment after the host entry, strip it out
                            hostEntry = line.split("#", 1)[1]
                            blacklistedHosts.append(hostEntry.strip())

                tempFileRead.close()

            except:
                # online hosts file is not valid, move along
                pass

        # set the IP redirection for the blacklisted hosts
        for n,item in enumerate(blacklistedHosts):
            blacklistedHosts[n] = redirectionIP + " " + item.split()[1]

        # replace any tabs with a single space
        # add our custom blacklist entries, ignore our whitelist entries
        # and strip out any common local entries, as we will add them on our own next
        fileOutput = []
        ignoreEntries = [" ip6-localhost", " ip6-loopback", " ip6-localnet", " ip6-mcastprefix", " ip6-allnodes", " ip6-allrouters", " localhost"] # we should check for tabs too, TO DO

        whiteList = []
        for whitelistDomain in self.instance.ui.plainTextEdit_Domain_Whitelist.toPlainText().split("\n"):
            if not str(whitelistDomain).strip() == "":
                if not str(whitelistDomain).strip().startswith("#"):
                    whiteList.extend([str(" " + str(whitelistDomain))])

        for outputLine in blacklistedHosts:
            if not str(outputLine).endswith(tuple(ignoreEntries)):
                if str(outputLine).endswith(tuple(whiteList)):
                    fileOutput.append("%s\n" % ' '.join(str("# " + outputLine + " # LOCAL-WHITELIST").split()))
                else:
                    fileOutput.append("%s\n" % ' '.join(str(outputLine).split()))

        for blacklistDomain in self.instance.ui.plainTextEdit_Domain_Blacklist.toPlainText().split("\n"):
            if not str(blacklistDomain).strip() == "":
                if not str(blacklistDomain).strip().startswith("#"):
                    fileOutput.append(redirectionIP + " " + str(blacklistDomain).strip()  + " # LOCAL-BLACKLIST\n")

        # remove any duplicates we may have parsed
        fileOutput = list(OrderedDict.fromkeys(fileOutput))

        # get the total count of blocked domains
        totalBlockCount = 0
        for entry in fileOutput:
            if not str(entry).startswith("#"):
                totalBlockCount +=1

        # overwrite our temp file in the temp directory with the aggregated hosts data
        thefile = open(tempFile, "w")

        thefile.write("# This hosts file was generated by " + applicationName + "\n")
        thefile.write("# Generated on: " + time.strftime("%x") + " at " + time.strftime("%I:%M:%S %p") + "\n")
        thefile.write("# Currently blocking " + str(totalBlockCount) + " domains\n")

        # write out any optional host entries selected with the checkboxes
        if self.instance.ui.actionInclude_IPv4_localhost.isChecked():
            thefile.write("127.0.0.1 localhost\n")
        if self.instance.ui.actionInclude_IPv6_localhost.isChecked():
            thefile.write("::1 ip6-localhost\n")
        if self.instance.ui.actionInclude_IPv6_loopback.isChecked():
            thefile.write("::1 ip6-loopback\n")
        if self.instance.ui.actionInclude_IPv6_localnet.isChecked():
            thefile.write("fe00::0 ip6-localnet\n")
        if self.instance.ui.actionInclude_IPv6_mcastprefix.isChecked():
            thefile.write("ff00::0 ip6-mcastprefix\n")
        if self.instance.ui.actionInclude_IPv6_allnodes.isChecked():
            thefile.write("ff02::1 ip6-allnodes\n")
        if self.instance.ui.actionInclude_IPv6_allrouters.isChecked():
            thefile.write("ff02::2 ip6-allrouters\n")

        # write our our aggregated black list
        for hostLine in fileOutput:
            thefile.write(hostLine)
        thefile.close()

        # copy the aggregated hosts file to our settings directory
        # check if the app settings directory exists, and create it if not.
        if not os.path.exists(user_data_dir(applicationName, applicationAuthor)):
            os.makedirs(user_data_dir(applicationName, applicationAuthor))
        settingsPathNewHosts = os.path.join(user_data_dir(applicationName, applicationAuthor), "newhosts")
        copyfile(tempFile, settingsPathNewHosts)

        # close progress dialog
        self.showProgress.emit(False)
        # re-enable the user controls
        self.buttonsEnabled.emit(True)

        # update statusbar text
        self.statusBarChangeText.emit("Hosts files downloaded and parsed successfully!", "green")

        # apply changes to hosts file by turning the switch on
        self.onOffSwitch.emit("on")

        # remove the temp file
        os.remove(tempFile)


class SaveBlackAndWhitelistsWorker(QtCore.QThread):

    # This is the signal that will be emitted during the processing.
    showProgress = QtCore.pyqtSignal(bool)
    updateProgress = QtCore.pyqtSignal(int, str)
    buttonsEnabled = QtCore.pyqtSignal(bool)
    statusBarChangeText = QtCore.pyqtSignal(str, str)
    onOffSwitch = QtCore.pyqtSignal(str)

    def __init__(self, instance):
        QtCore.QThread.__init__(self)
        self.instance = instance


    def run(self):

        # show progress dialog
        self.showProgress.emit(True)

        # disable user controls while we update
        self.buttonsEnabled.emit(False)

        # an empty list variable to store our parsed out host entries
        blacklistedHosts = []

        # load the hosts file from our settings directory
        settingsPathNewHosts = os.path.join(user_data_dir(applicationName, applicationAuthor), "newhosts")
        if os.path.exists(settingsPathNewHosts):

            tempFileRead = open(settingsPathNewHosts, "r")

            for line in tempFileRead:
                if not line.strip() == "":
                    if not line.strip().startswith("#"):
                        if not line.strip().endswith(" # LOCAL-BLACKLIST"):
                            # if there is a comment after the host entry, strip it out
                            hostEntry = line.split("#", 1)[0]
                            blacklistedHosts.append(hostEntry.strip())
                    elif line.strip().endswith(" # LOCAL-WHITELIST"):
                        # if there is a comment after the host entry, strip it out
                        hostEntry = line.split("#", 1)[1]
                        blacklistedHosts.append(hostEntry.strip())

            tempFileRead.close()

        # set the IP redirection for the blacklisted hosts
        for n,item in enumerate(blacklistedHosts):
            blacklistedHosts[n] = redirectionIP + " " + item.split()[1]

        # replace any tabs with a single space
        # add our custom blacklist entries, ignore our whitelist entries
        # and strip out any common local entries, as we will add them on our own next
        fileOutput = []
        ignoreEntries = [" ip6-localhost", " ip6-loopback", " ip6-localnet", " ip6-mcastprefix", " ip6-allnodes", " ip6-allrouters", " localhost"] # we should check for tabs too, TO DO

        whiteList = []
        for whitelistDomain in self.instance.ui.plainTextEdit_Domain_Whitelist.toPlainText().split("\n"):
            if not str(whitelistDomain).strip() == "":
                if not str(whitelistDomain).strip().startswith("#"):
                    whiteList.extend([str(" " + str(whitelistDomain))])

        for outputLine in blacklistedHosts:
            if not str(outputLine).endswith(tuple(ignoreEntries)):
                if str(outputLine).endswith(tuple(whiteList)):
                    fileOutput.append("%s\n" % ' '.join(str("# " + outputLine + " # LOCAL-WHITELIST").split()))
                else:
                    fileOutput.append("%s\n" % ' '.join(str(outputLine).split()))

        for blacklistDomain in self.instance.ui.plainTextEdit_Domain_Blacklist.toPlainText().split("\n"):
            if not str(blacklistDomain).strip() == "":
                if not str(blacklistDomain).strip().startswith("#"):
                    fileOutput.append(redirectionIP + " " + str(blacklistDomain).strip() + " # LOCAL-BLACKLIST\n")

        # remove any duplicates we may have parsed
        fileOutput = list(OrderedDict.fromkeys(fileOutput))

        # overwrite our temp file in the temp directory with the aggregated hosts data
        thefile = open(settingsPathNewHosts, "w")

        thefile.write("# This hosts file was generated by " + applicationName + "\n")
        thefile.write("# Generated on: " + time.strftime("%x") + " at " + time.strftime("%I:%M:%S %p") + "\n")
        thefile.write("# Currently blocking " + str(len(fileOutput)) + " domains\n")

        # write out any optional host entries selected with the checkboxes
        if self.instance.ui.actionInclude_IPv4_localhost.isChecked():
            thefile.write("127.0.0.1 localhost\n")
        if self.instance.ui.actionInclude_IPv6_localhost.isChecked():
            thefile.write("::1 ip6-localhost\n")
        if self.instance.ui.actionInclude_IPv6_loopback.isChecked():
            thefile.write("::1 ip6-loopback\n")
        if self.instance.ui.actionInclude_IPv6_localnet.isChecked():
            thefile.write("fe00::0 ip6-localnet\n")
        if self.instance.ui.actionInclude_IPv6_mcastprefix.isChecked():
            thefile.write("ff00::0 ip6-mcastprefix\n")
        if self.instance.ui.actionInclude_IPv6_allnodes.isChecked():
            thefile.write("ff02::1 ip6-allnodes\n")
        if self.instance.ui.actionInclude_IPv6_allrouters.isChecked():
            thefile.write("ff02::2 ip6-allrouters\n")

        # write our our aggregated black list
        for hostLine in fileOutput:
            thefile.write(hostLine)
        thefile.close()

        # close progress dialog
        self.showProgress.emit(False)
        # re-enable the user controls
        self.buttonsEnabled.emit(True)

        # update statusbar text
        self.statusBarChangeText.emit("Local blacklist saved successfully!", "green")

        # apply changes to hosts file by turning the switch on
        self.onOffSwitch.emit("on")

        # save settings
        self.instance.savesettings()


class UpdateWorker(QtCore.QThread):

    # This is the signal that will be emitted during the processing.
    updateDialogChangeText = QtCore.pyqtSignal(str)
    updateDialogShowDownloadButton = QtCore.pyqtSignal(bool)

    def __init__(self, instance):
        QtCore.QThread.__init__(self)
        self.instance = instance


    def run(self):

        global latestVersionNumber

        self.updateDialogChangeText.emit("checking for latest version...")

        versionLatest = urllib2.urlopen(str("https://raw.githubusercontent.com/joeylane/Block-That-Shit/master/VERSION")).read().strip()

        # if a new version is available, offer to send user to the download page
        if float(versionLatest) > float(versionNumber):
            self.updateDialogShowDownloadButton.emit(True)
            self.updateDialogChangeText.emit("A new version is available: v" + versionLatest)
            latestVersionNumber = versionLatest
        else:
            self.updateDialogChangeText.emit("You are already running the latest version.")


class OnOffWorker(QtCore.QThread):

    # This is the signal that will be emitted during the processing.
    showProgress = QtCore.pyqtSignal(bool)
    updateProgress = QtCore.pyqtSignal(int, str)
    buttonsEnabled = QtCore.pyqtSignal(bool)
    statusBarChangeText = QtCore.pyqtSignal(str, str)
    labelOnOff = QtCore.pyqtSignal(bool)
    pushButtonOnOffSetIcon = QtCore.pyqtSignal(bool)

    def __init__(self, instance, enabler):
        QtCore.QThread.__init__(self)
        self.instance = instance
        self.enabler = enabler


    def run(self):
        # show progress dialog
        self.showProgress.emit(True)
        self.buttonsEnabled.emit(False)

        # enable domain blocking
        if self.enabler == True:
            # user is turning the switch on
            # check if the app settings directory exists, and create it if not.
            if not os.path.exists(user_data_dir(applicationName, applicationAuthor)):
                os.makedirs(user_data_dir(applicationName, applicationAuthor))
            settingsPathNewHosts = os.path.join(user_data_dir(applicationName, applicationAuthor), "newhosts")

            # if we encountered an error, notify the user.  update the status bar text
            if ElevatedCopy(settingsPathNewHosts, hostsPath) == 0:
                self.statusBarChangeText.emit("Domain blocking was enabled successfully!", "green")
                # turn the switch on
                #self.labelOnOff.emit(True)
                #self.pushButtonOnOffSetIcon.emit(True)
            else:
                self.statusBarChangeText.emit("Domain blocking was NOT enabled!", "black")

        # diable domain blocking
        elif self.enabler == False:
            self.updateProgress.emit(0, "Clearing hosts file")

            tempFile = os.path.join(tempfile.gettempdir(), "tmphosts")

             # overwrite our temp file in the temp directory with the aggregated hosts data
            thefile = open(tempFile, "w")

            thefile.write("# This hosts file was generated by " + applicationName + "\n")
            thefile.write("# Generated on: " + time.strftime("%x") + " at " + time.strftime("%I:%M:%S %p") + "\n")
            thefile.write("# Currently blocking 0 domains\n")

            # write out any optional host entries selected with the checkboxes
            if self.instance.ui.actionInclude_IPv4_localhost.isChecked():
                thefile.write("127.0.0.1 localhost\n")
            if self.instance.ui.actionInclude_IPv6_localhost.isChecked():
                thefile.write("::1 ip6-localhost\n")
            if self.instance.ui.actionInclude_IPv6_loopback.isChecked():
                thefile.write("::1 ip6-loopback\n")
            if self.instance.ui.actionInclude_IPv6_localnet.isChecked():
                thefile.write("fe00::0 ip6-localnet\n")
            if self.instance.ui.actionInclude_IPv6_mcastprefix.isChecked():
                thefile.write("ff00::0 ip6-mcastprefix\n")
            if self.instance.ui.actionInclude_IPv6_allnodes.isChecked():
                thefile.write("ff02::1 ip6-allnodes\n")
            if self.instance.ui.actionInclude_IPv6_allrouters.isChecked():
                thefile.write("ff02::2 ip6-allrouters\n")

            thefile.close()

            self.updateProgress.emit(100, "")

            # update the View Hosts File tab and the status bar with the new stats
            # if we encountered an error, notify the user.
            if ElevatedCopy(tempFile, hostsPath) == 0:
                # update statusbar text
                self.statusBarChangeText.emit("Domain blocking has been disabled!", "red")
                # turn the switch off
                #self.labelOnOff.emit(False)
                #self.pushButtonOnOffSetIcon.emit(False)
            else:
                # update statusbar text
                self.statusBarChangeText.emit("Domain blocking was NOT disabled!", "black")

            # remove the temp file
            os.remove(tempFile)

        # close progress dialog
        self.showProgress.emit(False)
        # re-enable the user controls
        self.buttonsEnabled.emit(True)


class RestoreHostsFileWorker(QtCore.QThread):

    # This is the signal that will be emitted during the processing.
    showProgress = QtCore.pyqtSignal(bool)
    updateProgress = QtCore.pyqtSignal(int, str)
    buttonsEnabled = QtCore.pyqtSignal(bool)
    statusBarChangeText = QtCore.pyqtSignal(str, str)
    getFileToRestore = QtCore.pyqtSignal()

    def __init__(self, instance):
        QThread.__init__(self, None)
        self.instance = instance

    def run(self):

        # this global variable serves as a communication mechanism between this worker thread
        # and our file dialog on the main thread.
        global restoreMoveOn

        # show progress dialog
        self.showProgress.emit(True)

        self.buttonsEnabled.emit(False)
        self.updateProgress.emit(0, "Restoring hosts file")

        self.getFileToRestore.emit()

        while not restoreMoveOn:
            pass
        restoreMoveOn = False

        fileName = restorePath

        if fileName.endswith(".hostsbackup") and os.path.exists(fileName):
            self.updateProgress.emit(100, "")
            # update the View Hosts File tab and the status bar with the new stats
            # if we encountered an error, notify the user.
            if ElevatedCopy(fileName, hostsPath) == 0:
                self.statusBarChangeText.emit("Hosts file restored successfully!", "green")
            else:
                self.statusBarChangeText.emit("Hosts file was NOT restored!", "red")

        # close progress dialog
        self.showProgress.emit(False)
        # re-enable the user controls
        self.buttonsEnabled.emit(True)


class UpdateStatusBarWorker(QtCore.QThread):

    # This is the signal that will be emitted during the processing.
    statusUpdate = QtCore.pyqtSignal(str, str)
    getHostsfile = QtCore.pyqtSignal()

    def __init__(self, instance, message, color):
        QThread.__init__(self, instance)
        self.instance = instance
        self.message = message
        self.color = color

    def run(self):
        messageTimer = 5
        self.statusUpdate.emit(self.message, self.color)
        self.getHostsfile.emit()
        while messageTimer > 0:
            time.sleep(1)
            messageTimer -= 1
        self.statusUpdate.emit("", "black")


if __name__ == "__main__":

    # load the hosts file
    if sys.platform.startswith('win32'):
        # Windows
        osPlatform = "win32"
        hostsPath = "C:\Windows\System32\Drivers\etc\hosts"
    elif sys.platform.startswith('linux'):
        # Linux
        osPlatform = "linux"
        hostsPath = "/etc/hosts"
    elif sys.platform.startswith('darwin'):
        # Mac
        osPlatform = "darwin"
        hostsPath = "/private/etc/hosts"
    else:
        # couldnt determine OS, exit application
        sys.exit("ERROR: Unknown operating system...exiting.")

    # set home directory
    homeDir = expanduser("~")

    parser = argparse.ArgumentParser(description='Run ' + applicationName + ' with the --autorun flag and specify a user settings file '
                                                                            'to process a hosts file automatically.  This is intended to be used for facilitating '
                                                                            'native task scheduler processing.')
    parser.add_argument('-a','--autorun', help='Example: --autorun [PATH_TO_SETTINGS_FILE]', required=False)
    args = vars(parser.parse_args())

    if args["autorun"]:
        AutoRun(args["autorun"])

    # we are not using autorun.  launch the gui
    else:
        app = QtGui.QApplication(sys.argv)
        mySW = ControlMainWindow()
        mySW.show()
        # bring main window into foreground, this resolves an issue with OS X opening
        # the application behind other windows
        mySW.raise_()
        sys.exit(app.exec_())
