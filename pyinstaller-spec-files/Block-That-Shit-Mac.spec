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
pyz = PYZ(a.pure,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Block-That-Shit',
          debug=False,
          strip=None,
          upx=True,
          console=False , icon='block_blue.icns')
app = BUNDLE(exe,
             name='Block-That-Shit.app',
             icon='./icons/block_blue.icns',
             bundle_identifier=None)
