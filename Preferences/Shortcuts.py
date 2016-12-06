#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2004 - 2010 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing functions dealing with keyboard shortcuts.
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore
#from E5Application import e5App
#import E5MessageBox
#
from Preferences import Prefs, syncPreferences
#
#from E5XML.ShortcutsReader import ShortcutsReader
#from E5XML.ShortcutsWriter import ShortcutsWriter
#from .SMApplication import smApp
#
#codec2 = QtCore.QTextCodec.codecForName("UTF-8")
#settings = QtCore.QSettings("./option.ini", QtCore.QPrefs.settings.IniFormat)
#Prefs.settings.setIniCodec(codec2)

def __readShortcut(act, category=None):
    """
    Private function to read a single keyboard shortcut from the Prefs.settings.
    
    @param act reference to the action object (E5Action)
    @param category category the action belongs to (string)
    @param prefClass preferences class used as the storage area
    """
    if act.objectName():
#        print(act.objectName())
        accel = Prefs.settings.value(
            "Shortcuts/{0}".format(act.objectName()))
#        print(accel)
        if accel is not None:
            act.setShortcut(QKeySequence(accel))
#        accel = Prefs.settings.value(
#            "Shortcuts/{0}/{1}/AltAccel".format(category, act.objectName()))
#        if accel is not None:
#            act.setAlternateShortcut(QKeySequence(accel))

def readShortcuts(mw):
    """
    Module function to read the keyboard shortcuts for the defined QActions.
    
    @keyparam prefClass preferences class used as the storage area
    @keyparam helpViewer reference to the help window object
    @keyparam pluginName name of the plugin for which to load shortcuts (string)
    """
#    if helpViewer is None and pluginName is None:
    for act in mw.getActions('evaluate'):
        __readShortcut(act)
    
'''注意,储存功能暂不使用,直接在wm.py中用__saveSettings'''
def __saveShortcut(act, category=None):
    """
    Private function to write a single keyboard shortcut to the Prefs.settings.
    
    @param act reference to the action object (E5Action)
    @param category category the action belongs to (string)
    @param prefClass preferences class used as the storage area
    """
    if act.objectName():
        Prefs.settings.setValue(
            "Shortcuts/{0}".format(act.objectName()), 
            act.shortcut().toString())
#        Prefs.settings.setValue(
#            "Shortcuts/{0}/{1}/AltAccel".format(category, act.objectName()), 
#            act.alternateShortcut().toString())

def saveShortcuts(mw, actDict):
    """
    Module function to write the keyboard shortcuts for the defined QActions.
    
    @param prefClass preferences class used as the storage area
    """
    # step 1: clear all previously saved shortcuts
    Prefs.settings.beginGroup("Shortcuts")
    Prefs.settings.remove("")
    Prefs.settings.endGroup()
    
    # step 2: save the various shortcuts
    for act in mw.getActions('evaluate'):
        key = actDict.get(act.objectName())
        if key:
#            print(key)
            act.setShortcut(QKeySequence(key))#先设置快捷键,再储存
            __saveShortcut(act)            
#
#
#    
#        if act.objectName():
#            Prefs.settings.setValue(
#                "Shortcuts/{0}".format(act.objectName()), 
#                act.shortcut().toString())
                

def __setAction(actions, sdict):
    """
    Private function to write a single keyboard shortcut to the settings.
    
    @param actions list of actions to set (list of E5Action)
    @param sdict dictionary containg accelerator information for one category
    """
    for act in actions:
        if act.objectName():
            try:
                accel, altAccel = sdict[act.objectName()]
                act.setShortcut(QKeySequence(accel))
                act.setAlternateShortcut(QKeySequence(altAccel))
            except KeyError:
                pass


def setActions(shortcuts):
    """
    Module function to set actions based on new format shortcuts file.
    
    @param shortcuts dictionary containing the accelerator information
        read from a XML file
    """
    if "Project" in shortcuts:
        __setAction(e5App().getObject("Project").getActions(),
            shortcuts["Project"])
    

