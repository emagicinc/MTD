#!/usr/bin/env python
# A simple setup script to create an executable using PyQt4. This also
# demonstrates the method for creating a Windows executable that does not have
# an associated console.
#
# PyQt4app.py is a very simple type of PyQt4 application
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the application

import sys

from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"
    
buildOptions = dict(icon = "icon.ico",
                     build_exe = "smeditor",
                     create_shared_zip = False,
                     append_script_to_exe = True,
                     optimize = 2,
                     include_msvcr = True,
                     ) 
constantsOptions = dict(copyright = "舍得学苑",
                     )     
setup(
        name = "SMEDITOR",
        version = "1.1.1",
        description = "SuperMemo课程编辑器",
#        constants = dict(build_exe = constantsOptions),    
#        constants = {"copyright" : "舍得学苑"},            
        options = dict(build_exe = buildOptions), 
#        options = {"build_exe" : {"includes" : "atexit" }}, 
        executables = [Executable("smeditor.py", base = base, icon = "icon.ico", targetDir="SMEDITOR")])

