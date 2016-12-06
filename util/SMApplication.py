#!/usr/bin/env python
#coding=utf-8
# This is only needed for Python v2 but is harmless for Python v3.
# -*- coding: utf-8 -*-
#include <QString>

"""
Class implementing a specialized application class.
"""

from PyQt4.QtCore import QCoreApplication
from PyQt4.QtGui import QApplication
#from PyQt4 import QtCore
#from PyQt4 import QtGui
#from UserInterface import MainWindow
##from PyQt4.QtCore import QSettings
#codec2 = QtCore.QTextCodec.codecForName("gbk")
#settings = QtCore.QSettings("./option.ini", QtCore.QSettings.IniFormat)
#settings.setIniCodec(codec2)
#WM_HOTKEY = 0x0312
##以下为实现全局快捷键所需调用的东东
#from ctypes import c_bool, c_int, WINFUNCTYPE, windll
#from ctypes.wintypes import UINT
#import config
#
#DEBUG = False
#def debug_out(str):
#    if DEBUG:
#        print(str)
#    else:
#        pass
#测试快捷键
import config
WM_HOTKEY = 0x0312

class SMApplication(QApplication):
    """
    Eric application class with an object registry.
    """
    def __init__(self, argv):
        """
        Constructor
        
        @param argv command line arguments
        """
        QApplication.__init__(self, argv)
        
        self.__objectRegistry = {}
        self.__pluginObjectRegistry = {}
        
    def registerObject(self, name, object):
        """
        Public method to register an object in the object registry.
        
        @param name name of the object (string)
        @param object reference to the object
        @exception KeyError raised when the given name is already in use
        """
        if name in self.__objectRegistry:
            raise KeyError('Object "{0}" already registered.'.format(name))
        else:
            self.__objectRegistry[name] = object
#        print(self.__objectRegistry)
        
    def getObject(self, name):
        """
        Public method to get a reference to a registered object.
        
        @param name name of the object (string)
        @return reference to the registered object
        @exception KeyError raised when the given name is not known
        """
        if name in self.__objectRegistry:
            return self.__objectRegistry[name]
        else:
            raise KeyError('Object "{0}" is not registered.'.format(name))
#        print(self.__objectRegistry)
        
    def registerPluginObject(self, name, object, pluginType = None):
        """
        Public method to register a plugin object in the object registry.
        
        @param name name of the plugin object (string)
        @param object reference to the plugin object
        @keyparam pluginType type of the plugin object (string)
        @exception KeyError raised when the given name is already in use
        """
        if name in self.__pluginObjectRegistry:
            raise KeyError('Pluginobject "{0}" already registered.'.format(name))
        else:
            self.__pluginObjectRegistry[name] = (object, pluginType)
        
    def unregisterPluginObject(self, name):
        """
        Public method to unregister a plugin object in the object registry.
        
        @param name name of the plugin object (string)
        """
        if name in self.__pluginObjectRegistry:
            del self.__pluginObjectRegistry[name]
        
    def getPluginObject(self, name):
        """
        Public method to get a reference to a registered plugin object.
        
        @param name name of the plugin object (string)
        @return reference to the registered plugin object
        @exception KeyError raised when the given name is not known
        """
        if name in self.__pluginObjectRegistry:
            return self.__pluginObjectRegistry[name][0]
        else:
            raise KeyError('Pluginobject "{0}" is not registered.'.format(name))
        
    def getPluginObjects(self):
        """
        Public method to get a list of (name, reference) pairs of all
        registered plugin objects.
        
        @return list of (name, reference) pairs
        """
        objects = []
        for name in self.__pluginObjectRegistry:
            objects.append((name, self.__pluginObjectRegistry[name][0]))
        return objects
        
    def getPluginObjectType(self, name):
        """
        Public method to get the type of a registered plugin object.
        
        @param name name of the plugin object (string)
        @return type of the plugin object (string)
        @exception KeyError raised when the given name is not known
        """
        if name in self.__pluginObjectRegistry:
            return self.__pluginObjectRegistry[name][1]
        else:
            raise KeyError('Pluginobject "{0}" is not registered.'.format(name))

    def winEventFilter(self, msg):
#        debug_out("Message: " + str(hex(msg.message)) )
#        mainWin = self.getObject("UserIF")
        if msg.message == WM_HOTKEY:
            import imp
            imp.reload(config)
            if  msg.wParam == 1:
                mainWin.addQuestion()
                mainWin.trayIcon.showMessage("复制成功","已添加:"+mainWin.qText[:20]+"...")
            elif msg.wParam == 2:
                mainWin.addAnswer()
                mainWin.trayIcon.showMessage("复制成功","已添加:"+mainWin.aText[:20]+"...")
            elif msg.wParam == 3:
                mainWin.undo()
            return True, 0
        return False, 0
        
smApp = QCoreApplication.instance
