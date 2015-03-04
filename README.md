Block-That-Shit
====================================
Block-That-Shit is a free, cross platform domain blocker designed with Qt and written in Python.  Block-That-Shit provides a user friendly way to block advertisements, malware serving domains, botnets, and much more.  Block-That-Shit is an open source project released under the [GNU/GPLv3](http://www.gnu.org/licenses/gpl.html) license.

![Block-That-Shit](https://raw.githubusercontent.com/joeylane/Block-That-Shit/master/screenshots/blockthatshit.jpg)

Unlike most ad blocking software (AdBlock Plus for example), Block-That-Shit requires NO browser extensions to install.  It works with ALL web browsers as well as any other software on your system.

Block-That-Shit is compatible with Windows, MacOS X, and most Linux distributions.  Ports for Android and iPhone are coming soon!

<h3>How it works</h3>
Block-That-Shit works by manipulating the hosts file of your operating system.  The hosts file is a core component of the Internet Protocol Suite, every device connected to an IP based network (such as the internet) has one.  The hosts file is there to assist your operating system with domain name resolution.  Block-That-Shit assembles a list of domains that are known to serve advertisements and malware.  It injects this list into your hosts file, forcing those domains to redirect to the loopback address on your network interface.

In other words, it prevents your computer from ever making a connection to a blacklisted domain.

This is a very different approach from traditional ad blocking software.  Most ad block software requires the installation of browser add ons.  Hosts file based ad blocking is browser independent.  Meaning once you activate domain blocking with Block-That-Shit, ads will be blocked in ALL web browsers on your system, for all users.  Ads will also be blocked in all applications that attempt to connect to an advertising server.  There are no browser extensions to install, and ads can always be re-enabled at the push of a button.

<h3>System requirements</h3>
Supported operating systems:
* Microsoft Windows Vista, 7, 8, 8.1 or higher (no XP or RT support, sorry.)
* MacOS X 10.6 or higher
* Linux (Too many to list, works with most distros.  Let me know if you find one it doesn't work with.)

Supported processors:
* Windows - x86 (32bit) or x86_64 (64bit) AMD or Intel processor
* Mac - x86_64 (64bit) AMD or Intel processor
* Linux - x86_64 (64bit) AMD or Intel processor

If you need ARM support, or x86 (32bit) support for OS X or Linux, you're going to have to build from source.

<h3>Where can I download Block-That-Shit?</h3>
You can download Block-That-Shit for Windows, MacOS X, and Linux right here:

* [Block-That-Shit for Windows](https://github.com/joeylane/Block-That-Shit/releases/download/v1.0/Block-That-Shit-Windows.exe)
* [Block-That-Shit for Mac](https://github.com/joeylane/Block-That-Shit/releases/download/v1.0/Block-That-Shit-Mac.app.zip)
* [Block-That-Shit for Linux](https://github.com/joeylane/Block-That-Shit/releases/download/v1.0/Block-That-Shit-Linux.tar.gz)

No installation is required, the binaries are designed to be completely portable.  Just download, and run!  Simple as that.  For MacOS X and Linux users, the binaries are compressed so you'll need to extract them first.  One of the cool benefits of single binary portability, is it allows you to use Block-That-Shit from a portable flash drive if you need to enable blocking on multiple computers.  This makes it a handy addition to your tech tool kit.

NOTE:  Technically, you can remove Block-That-Shit once you have enabled domain blocking and it will still continue to protect you, though I wouldnt recommend it.  Keeping Block-That-Shit handy on your PC allows you to continually update the block list, and also re-enable advertisements if need be.  The primary blacklist used by Block-That-Shit is updated every single day with new domains.  So its not a bad idea to keep Block-That-Shit handy just to stay up to date.

<h3>How should I use Block-That-Shit?</h3>
Open Block-That-Shit, and press the 'Download' button.  It really is that simple.  The block list is updated daily, so I would recommend you re-run Block-That-Shit every once in a while to keep your hosts file updated.  Run it as often as you like.  There are directions below on how to set up Block-That-Shit for automatic hosts file updates.

In addition to the downloaded block list, you can also specify any individual domains you wish to block under the 'Local Blacklist' tab.  This flexibility allows Block-That-Shit to block any domains/websites you wish.  You could hypothetically use this to prevent certain applications from sending data back to their authors, or possibly as basic parental control software.

Also provided is a 'Local Whitelist' feature for whitelisting domains.  This is useful if you encounter a situation where Block-That-Shit is blocking a domain that you need access to.  Simply put the domain name in the whitelist, and it will be ignored.

NOTE:  You will probably need to close all your browser windows before any changes will take effect.  If you want to be certain, just reboot your PC after updating the block list (though this is typically not necassary).

<h3>Can I use both Block-That-Shit AND AdBlock Plus together?</h3>
Absolutely!  In fact, Block-That-Shit should play nice with all software on your PC, including anti-virus software.  It is simply another layer of protection.

With that in mind, I personally do not like browser extensions of any kind (including AdBlock Plus).  Installing a browser extension can increase the attack surface for browser based exploits, and in some cases, can lead to additional security risks when browsing the web.  This is one of the reasons I wrote Block-That-Shit in the first place.

<h3>Does Block-That-Shit help prevent viruses and spyware?</h3>
Yes!  Malware is often spread through insecure advertising networks, and served to your browser when you visit a website serving the malicious advertisement.  Block-That-Shit prevents your computer from ever establishing a connection to these known ad servers, thus greatly reducing the risk of browser based exploitation.  In addition to blocking ad serving domains, Block-That-Shit also blocks domains that are known to be affiliated with several common botnets, and trojanized networks.  This means that even if your PC gets infected with a common trojan (such as Zeus, or Spyeye for example), your computer will NOT be able to talk to the command and control server, thus preventing the attacker from stealing your private data.

Block-That-Shit is NOT meant to replace traditional end point anti-virus software, it is designed to supplement it, and provide you with yet another layer of protection.

<h3>Can Block-That-Shit update my hosts file automatically?</h3>
Yes, although this requires some additional setup.  Block-That-Shit has a single command line parameter called --autorun.  If you run Block-That-Shit with this parameter and specify the path to your settings.cfg file, it will run without user interaction.  For example:

* Block-That-Shit.exe --autorun "C:\Users\YOUR USER NAME\AppData\Local\Joey Lane\Block-That-Shit\settings.cfg"

While this may seem complicated at first, using this command line parameter means you can use Block-That-Shit with ANY task scheduling system.  That means Task Scheduler for Windows is supported, Automator for MacOS X is supported, and Cron/Anacron for Linux is supported.  It also allows Block-That-Shit to be integrated into any maintenance scripts.  Please note that in order to use the autoupdate feature, Block-That-Shit MUST be run as Administrator on Windows, or root on MacOS X and Linux.

<h3>Can I view the main hosts file Block-That-Shit is using?</h3>
Absolutely.  I created a GitHub repo just for the hosts file to make it easier to keep track of the daily updates.  You can find it here:

* https://github.com/joeylane/hosts

Also note, that you can easily add additional hosts files to Block-That-Shit, if this list isn't comprehensive enough for you.

<h3>How do I build Block-That-Shit from source?</h3>
There are a few pre prerequisite software packages you will need to install if you wish to build Block-That-Shit from the source code.  The required packages are:

* Python 2.7.9
* appdirs 1.4.0 (installed via PIP)
* Qt 4.8.6
* PyQt 4.10.4
* PyInstaller 2.1

Once you have the required packages installed on your system, the easiest way to build is to simply use the provided build scripts for each OS.  Just clone this repo, run the approriate build script for your OS, and the final binary will be located in the "dist" folder inside your project folder.

<h3>License</h3>
Block-That-Shit is a cross platform domain blocker for Windows, MacOS X, and Linux.

Copyright (C) 2015 Joey Lane

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.