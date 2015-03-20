#to install: 
#python setup.py py2exe
#2015 03 20 
#Jeremy Xue
#Jeremy.xzm@gmail.com

from distutils.core import setup
import py2exe, sys, os

sys.argv.append('py2exe')

setup(
    options = {'py2exe': {'bundle_files': 1, 'compressed': True}},
    console = [{
                'script': "File_Diff.py",
                'icon_resources':[(1, 'FILEDIFF_icon.ico')]
                }],
    zipfile = None,
)