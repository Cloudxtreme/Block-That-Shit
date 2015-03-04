#!/bin/bash
cd ..
pyinstaller ./pyinstaller-spec-files/Block-That-Shit-Mac.spec --onefile --windowed --clean --icon=./icons/block_blue.icns Block-That-Shit.py --upx-dir="./upx/upx309mac/" -y
cd dist
zip -r Block-That-Shit.app.zip ./Block-That-Shit.app
