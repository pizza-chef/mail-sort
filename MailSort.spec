# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

added_files = [
				('images/*.png', 'images'),
				('article/*.xml', 'article'),
				('printpost/PrintPost.txt', 'printpost'),
				('labels/ServiceIndicators.xml', 'labels'),
				('styles.qss', '.'),
				('settings/settings.xml', 'settings')
			  ]
			  
a = Analysis(['main.py'],
             pathex=['C:\\Users\\Dylan\\Documents\\Twins 2.0\\MailSort'],
             binaries=[],
             datas=added_files,
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='MailSort',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='MailSort')
