#!/bin/bash
cd ..
pyinstaller ./pyinstaller-spec-files/Block-That-Shit-Linux.spec --onefile --strip --clean --upx-dir="./upx/upx-3.91-amd64_linux/" Block-That-Shit.py
