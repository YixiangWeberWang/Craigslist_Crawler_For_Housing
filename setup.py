'''
Author: Yixiang Wang Email: yixiang.wang@yale.edu Wechat: tsinghuawyx
version: .02	Date: 04/12/2018
WARNING: THIS IS NOT FOR COMMERCIAL USE
Some comments are from http://cx-freeze.readthedocs.io/en/latest/distutils.html
This script is for building an executable from the .py file
'''
import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
includefiles = [] # include any files here that you wish
includes = []
excludes = []
packages = []
#build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
#base = None
#if sys.platform == "win32":
#    base = "Win32GUI"

exe = Executable(
 # what to build
   script = "cragCraw_v3.py", # the name of your main python script goes here 
   initScript = None,
   base = None, # if creating a GUI instead of a console app, type "Win32GUI"
   targetName = "cragCraw_v3.exe", # this is the name of the executable file
   icon = None # if you want to use an icon file, specify the file name here
)


setup(  name = "cragCraw_v3",
        version = "0.1",
        description = "Console app test",
        options = {"build_exe": {"excludes":excludes,"packages":packages,"include_files":includefiles}},
        executables = [exe]
)