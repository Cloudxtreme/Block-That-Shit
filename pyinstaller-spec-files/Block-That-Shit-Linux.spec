# -*- mode: python -*-

block_cipher = None


a = Analysis(['Block-That-Shit.py'],
             pathex=[os.getcwd()],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None,
             excludes=None,
             cipher=block_cipher)
a.datas += [('/icons/block_blue.png', './icons/block_blue.png', 'DATA')]
a.datas += [('/icons/Switch-On-256.png', './icons/Switch-On-256.png', 'DATA')]
a.datas += [('/icons/Switch-Off-256.png', './icons/Switch-Off-256.png', 'DATA')]

a.binaries = [x for x in a.binaries if not
              os.path.basename(x[1]).__contains__('libicudata.so')]
a.binaries = [x for x in a.binaries if not
              os.path.basename(x[1]).__contains__('codecs')]
a.binaries = [x for x in a.binaries if not
              os.path.basename(x[1]).__contains__('audio')]
a.binaries = [x for x in a.binaries if not
              os.path.basename(x[1]).__contains__('libQt3Support.so')]
a.binaries = [x for x in a.binaries if not
              os.path.basename(x[1]).__contains__('libQtDeclarative.so')]
a.binaries = [x for x in a.binaries if not
              os.path.basename(x[1]).__contains__('libQtXmlPatterns.so')]
a.binaries = [x for x in a.binaries if not
              os.path.basename(x[1]).__contains__('libQtScript.so')]
a.binaries = [x for x in a.binaries if not
              os.path.basename(x[1]).__contains__('libicuuc.so')]
a.binaries = [x for x in a.binaries if not
              os.path.basename(x[1]).__contains__('libX11.so')]
a.binaries = [x for x in a.binaries if not
              os.path.basename(x[1]).__contains__('libglib-2.0.so')]
a.binaries = [x for x in a.binaries if not
              os.path.basename(x[1]).__contains__('libcrypto.so.1.0')]

pyz = PYZ(a.pure,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Block-That-Shit',
          debug=False,
          strip=True,
          upx=True,
          console=True )
