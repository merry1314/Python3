#!E:\pythonProject\weixin\wechat\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'PyInstaller==3.5.dev0+b54a15d72e','console_scripts','pyi-archive_viewer'
__requires__ = 'PyInstaller==3.5.dev0+b54a15d72e'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('PyInstaller==3.5.dev0+b54a15d72e', 'console_scripts', 'pyi-archive_viewer')()
    )
