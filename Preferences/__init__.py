# -*- coding: utf-8 -*-

# Copyright (c) 2002 - 2013 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Package implementing the preferences interface.

The preferences interface consists of a class, which defines the default
values for all configuration items and stores the actual values. These
values are read and written to the eric5 preferences file by module
functions. The data is stored in a file in a subdirectory of the users home
directory. The individual configuration data is accessed by accessor functions
defined on the module level. The module is simply imported wherever it is needed
with the statement 'import Preferences'. Do not use 'from Preferences import *'
to import it.
"""

import os
#import fnmatch
import shutil

from PyQt4.QtCore import QDir, QPoint, QLocale, QSettings, QTextCodec, QFileInfo, QCoreApplication, \
    QByteArray, QSize, QUrl, Qt, QLibraryInfo
from PyQt4.QtGui import QColor, QFont, QInputDialog, QPalette, QApplication
#from PyQt4.QtNetwork import QNetworkRequest
#from PyQt4.QtWebKit import QWebSettings
#from PyQt4.Qsci import QsciScintilla

#from E5Gui import E5FileDialog
#
#from E5Network.E5Ftp import E5FtpProxyType
#
#import QScintilla.Lexers

from Globals import settingsNameOrganization, settingsNameGlobal, settingsNameRecent, \
    isWindowsPlatform, findPython2Interpreters, getPythonModulesDirectory

#from Project.ProjectBrowserFlags import SourcesBrowserFlag, FormsBrowserFlag, \
#    ResourcesBrowserFlag, TranslationsBrowserFlag, InterfacesBrowserFlag, \
#    OthersBrowserFlag, AllBrowsersFlag


class Prefs(object):
    """
    A class to hold all configuration items for the application.
    """
    # 快捷键
    Shortcuts = {
        "answerKey": "Enter",
        "levelKey5": 5, 
        "levelKey4": 4, 
        "levelKey3": 3, 
        "levelKey2": 2, 
        "levelKey1": 1, 
        "levelKey0": 0 
    }


    # 项目设置
    Project = {
        "db": ".\\wordMaster.dat",
        "exportPath": ".\\output",
        "soundBankPath": "",
        "sentBankPath": "",
        "imagePath": "",
        "bgImage": 6, 
        "fontSizeQ": 20, 
        "fontSizeA": 18, 
        "font": "Microsoft YaHei UI",
        "exerciseType": 3, 
        "curExerciseType": 1, 
        "analyzeDoc": "analyze",
        "newWordDoc": "newWord",
        "reportDoc": "report",
        "exportDoc": "export",
        "dateMark1": "true",
        "dateMark2": "true",
        "useAudioQ": "true",
        "useAudioA": "true",
        "audioQ": "true",
        "audioA": "true",
        "useImage": "true",
        "useSentence": "true"
    }
    # 课程模型设置
    Course = {
        "0": "释义|图片,单词|例句|例句译文", 
        "0/audioQ": 0,
        "0/audioA": 2,
        "0/lessonTitle": "我的课程",
        "0/chapterTitle": "回想词汇",
        "0/questionTitle": "根据释义,回想词汇",
        "1":"单词拼写,释义|例句|例句译文", 
        "1/audioQ": 1,
        "1/audioA": 2,
        "1/lessonTitle": "我的课程",
        "1/chapterTitle": "单词听写",
        "1/questionTitle": "聆听录音,拼出单词",        
        "2":"单词,释义|图片|例句|例句译文",
        "2/audioQ": 1,
        "2/audioA": 2,
        "2/lessonTitle": "我的课程",
        "2/chapterTitle": "回想释义",
        "2/questionTitle": "根据单词,回想释义",
        "3":"例句语音|直觉造句",
        "3/audioQ": 0,
        "3/audioA": 2,
        "3/lessonTitle": "我的课程",
        "3/chapterTitle": "直觉造句",
        "3/questionTitle": "将当前词汇组成句子",
        "4":"选择单词,例句语音|例句|例句译文",
        "4/audioQ": 0,
        "4/audioA": 1,
        "4/lessonTitle": "我的课程",
        "4/chapterTitle": "选择单词",
        "4/questionTitle": "根据释义选择单词",
        "5":"选择释义,例句语音|例句|例句译文",
        "5/audioQ": 1,
        "5/audioA": 1,
        "5/lessonTitle": "我的课程",
        "5/chapterTitle": "选择释义",
        "5/questionTitle": "根据单词选择释义",
        "6":"词义匹配",
        "6/audioQ": 0,
        "6/audioA": 0,
        "6/lessonTitle": "我的课程",
        "6/chapterTitle": "词义匹配",
        "6/questionTitle": "将单词和释义一一配对"
    }

def initPreferences():
    """
    Module function to initialize the central configuration store.
    """
#    Prefs.settings = QSettings(
#        QSettings.IniFormat, QSettings.UserScope,
#        settingsNameOrganization, settingsNameGlobal)
#    QCoreApplication.setOrganizationName(settingsNameOrganization)
#    QCoreApplication.setApplicationName(settingsNameGlobal)
    Prefs.settings = QSettings("./option.ini", QSettings.IniFormat)
    codec = QTextCodec.codecForName("UTF-8")
    Prefs.settings.setIniCodec(codec)
#    Prefs.settings = QSettings(
#        QSettings.IniFormat, QSettings.SystemScope,
#        settingsNameOrganization, settingsNameGlobal)
#    QCoreApplication.setOrganizationName(settingsNameOrganization)
#    QCoreApplication.setApplicationName(settingsNameGlobal)
    
def syncPreferences(prefClass=Prefs):
    """
    Module function to sync the preferences to disk.
    
    In addition to syncing, the central configuration store is reinitialized as well.
    
    @param prefClass preferences class used as the storage area
    """
    prefClass.settings.setValue("General/Configured", True)
    prefClass.settings.sync()
    

def exportPreferences(prefClass=Prefs):
    """
    Module function to export the current preferences.
    
    @param prefClass preferences class used as the storage area
    """
    filename, selectedFilter = E5FileDialog.getSaveFileNameAndFilter(
        None,
        QCoreApplication.translate("Preferences", "Export Preferences"),
        "",
        QCoreApplication.translate("Preferences",
            "Properties File (*.ini);;All Files (*)"),
        None,
        E5FileDialog.Options(E5FileDialog.DontConfirmOverwrite))
    if filename:
        ext = QFileInfo(filename).suffix()
        if not ext:
            ex = selectedFilter.split("(*")[1].split(")")[0]
            if ex:
                filename += ex
        settingsFile = prefClass.settings.fileName()
        prefClass.settings = None
        shutil.copy(settingsFile, filename)
        initPreferences()


def importPreferences(prefClass=Prefs):
    """
    Module function to import preferences from a file previously saved by
    the export function.
    
    @param prefClass preferences class used as the storage area
    """
    filename = E5FileDialog.getOpenFileName(
        None,
        QCoreApplication.translate("Preferences", "Import Preferences"),
        "",
        QCoreApplication.translate("Preferences",
            "Properties File (*.ini);;All Files (*)"))
    if filename:
        settingsFile = prefClass.settings.fileName()
        shutil.copy(filename, settingsFile)
        initPreferences()


def isConfigured(prefClass=Prefs):
    """
    Module function to check, if the the application has been configured.
    
    @param prefClass preferences class used as the storage area
    @return flag indicating the configured status (boolean)
    """
    return toBool(prefClass.settings.value("General/Configured", False))

def initRecentSettings():
    """
    Module function to initialize the central configuration store for recently
    opened files and projects.
    
    This function is called once upon import of the module.
    """
    Prefs.rsettings = QSettings(
        QSettings.IniFormat, QSettings.UserScope,
        settingsNameOrganization, settingsNameRecent)
   
def initSettings(prefClass=Prefs):
    '''恢复默认设置'''   
    '''快捷键设置恢复默认后,重启后生效,应该重做一次Shortcuts.readShortcuts(self)'''
    prefClass.settings.beginGroup("Shortcuts")
    prefClass.settings.remove("")
    prefClass.settings.endGroup()
    for k, v in prefClass.Shortcuts.items():
        setShortcut(k, v)
    '''恢复Project默认设置'''
    prefClass.settings.beginGroup("Project")
    prefClass.settings.remove("")
    prefClass.settings.endGroup()
    for k, v in prefClass.Project.items():
        setProject(k, v)    
    '''恢复 Course 默认设置'''
    prefClass.settings.beginGroup("Course")
    prefClass.settings.remove("")
    prefClass.settings.endGroup()
    for k, v in prefClass.Course.items():
        setCourse(k, v)          
    syncPreferences()#此句貌似没起作用;
        
'''下面是一组组get和set,仅留几组供参考'''
'''每一组用来处理ini中不同的'文件夹' '''
    
def getShortcut(key, prefClass=Prefs):
    """
    读取配置文件中的快捷键
    """
    return str(prefClass.settings.value("Shortcuts/" + key))
    
def setShortcut(key, value, prefClass=Prefs):
    """
    储存快捷键设置到配置文件中
    """
    prefClass.settings.setValue("Shortcuts/" + key, value)

def getProject(key, prefClass=Prefs):
    """
    读取配置文件中除快捷键外的其它设置
    """
    if key in ['bgImage', 'fontSizeQ', 'fontSizeA']:
        value = prefClass.settings.value("Project/" + key)
        if value:#防止出现空值
            return int(value)
    elif key in ['font']:#词汇&释义字体
        font = prefClass.settings.value("Project/" + key)
        if font:
            f = QFont()
            f.fromString(font)
            return f
    elif key in ['audioQ','audioA','useAudioQ','useAudioA', 'dateMark1', 'dateMark2', 'useImage', 'useSentence']:
        #问题区&答案区音频/输出文档添加日期后缀/启用图片/启用例句
        return toBool(prefClass.settings.value("Project/" + key))
    else:
        return prefClass.settings.value("Project/" + key)
        
def setProject(key, value, prefClass=Prefs):
    """
    储存除快捷键外的其它设置到配置文件中
    """
    if key in ['font']:
        fontFamily = value
        if type(value) != str:
            fontFamily = value.family()
        prefClass.settings.setValue("Project/" + key, fontFamily)
    else:
        prefClass.settings.setValue("Project/" + key, value)

def getCourse(key, prefClass=Prefs):
    """
    读取配置文件中的课程设置
    """
    if "audio" in str(key) or key in ['curExerciseType']:
        value = prefClass.settings.value("Course/" + str(key))
        if value:#防止出现空值
            return int(value)
    elif key in ['lessonTitle', 'chapterTitle', 'questionTitle']:
        title = prefClass.settings.value("Course/" + str(key))
        if not title:#不要返回None值
            title = ""
        return title
    else:
        return prefClass.settings.value("Course/" + str(key))

def setCourse(key, value, prefClass=Prefs):
    """
    将课程设置保存到配置
    """
    prefClass.settings.setValue("Course/" + str(key), value)
        
###########以下还未用到#############
def getVarFilters(prefClass=Prefs):
    """
    Module function to retrieve the variables filter settings.
    
    @param prefClass preferences class used as the storage area
    @return a tuple defing the variables filter
    """
    localsFilter = eval(prefClass.settings.value("Variables/LocalsFilter",
        prefClass.varDefaults["LocalsFilter"]))
    globalsFilter = eval(prefClass.settings.value("Variables/GlobalsFilter",
        prefClass.varDefaults["GlobalsFilter"]))
    return (localsFilter, globalsFilter)
    

def setVarFilters(filters, prefClass=Prefs):
    """
    Module function to store the variables filter settings.
    
    @param prefClass preferences class used as the storage area
    """
    prefClass.settings.setValue("Variables/LocalsFilter", str(filters[0]))
    prefClass.settings.setValue("Variables/GlobalsFilter", str(filters[1]))
    

def getDebugger(key, prefClass=Prefs):
    """
    Module function to retrieve the debugger settings.
    
    @param key the key of the value to get
    @param prefClass preferences class used as the storage area
    @return the requested debugger setting
    """
    if key in ["RemoteDbgEnabled", "PassiveDbgEnabled",
                "CustomPython3Interpreter",
                "AutomaticReset", "DebugEnvironmentReplace",
                "PythonRedirect", "PythonNoEncoding",
                "Python3Redirect", "Python3NoEncoding",
                "RubyRedirect",
                "ConsoleDbgEnabled", "PathTranslation",
                "Autosave", "ThreeStateBreakPoints",
                "SuppressClientExit", "BreakAlways",
                "AutoViewSourceCode",
              ]:
        return toBool(prefClass.settings.value("Debugger/" + key,
            prefClass.debuggerDefaults[key]))
    elif key in ["PassiveDbgPort"]:
        return int(
            prefClass.settings.value("Debugger/" + key, prefClass.debuggerDefaults[key]))
    elif key in ["AllowedHosts"]:
        return toList(
            prefClass.settings.value("Debugger/" + key, prefClass.debuggerDefaults[key]))
    elif key == "PythonInterpreter":
        interpreter = \
            prefClass.settings.value("Debugger/" + key, prefClass.debuggerDefaults[key])
        if not interpreter:
            interpreters = findPython2Interpreters()
            if interpreters:
                if len(interpreters) == 1:
                    interpreter = interpreters[0]
                else:
                    selection, ok = QInputDialog.getItem(
                        None,
                        QCoreApplication.translate("Preferences",
                            "Select Python2 Interpreter"),
                        QCoreApplication.translate("Preferences",
                            "Select the Python2 interpreter to be used:"),
                        interpreters,
                        0, False)
                    if ok and selection != "":
                        interpreter = selection
                if interpreter:
                    setDebugger("PythonInterpreter", interpreter)
        return interpreter
    else:
        return \
            prefClass.settings.value("Debugger/" + key, prefClass.debuggerDefaults[key])
    

def setDebugger(key, value, prefClass=Prefs):
    """
    Module function to store the debugger settings.
    
    @param key the key of the setting to be set
    @param value the value to be set
    @param prefClass preferences class used as the storage area
    """
    prefClass.settings.setValue("Debugger/" + key, value)


def getSystem(key, prefClass=Prefs):
    """
    Module function to retrieve the various system settings.
    
    @param key the key of the value to get
    @param prefClass preferences class used as the storage area
    @return the requested system setting
    """
    from Utilities import supportedCodecs
    if key in ["StringEncoding", "IOEncoding"]:
        encoding = prefClass.settings.value("System/" + key,
            prefClass.sysDefaults[key])
        if encoding not in supportedCodecs:
            encoding = prefClass.sysDefaults[key]
        return encoding
    

def setSystem(key, value, prefClass=Prefs):
    """
    Module function to store the various system settings.
    
    @param key the key of the setting to be set
    @param value the value to be set
    @param prefClass preferences class used as the storage area
    """
    prefClass.settings.setValue("System/" + key, value)
    
def getTemplates(key, prefClass=Prefs):
    """
    Module function to retrieve the Templates related settings.
    
    @param key the key of the value to get
    @param prefClass preferences class used as the storage area
    @return the requested user setting
    """
    if key in ["SeparatorChar"]:
        return prefClass.settings.value("Templates/" + key,
            prefClass.templatesDefaults[key])
    else:
        return toBool(prefClass.settings.value("Templates/" + key,
            prefClass.templatesDefaults[key]))
    

def setTemplates(key, value, prefClass=Prefs):
    """
    Module function to store the Templates related settings.
    
    @param key the key of the setting to be set
    @param value the value to be set
    @param prefClass preferences class used as the storage area
    """
    prefClass.settings.setValue("Templates/" + key, value)
    

def getGeometry(key, prefClass=Prefs):
    """
    Module function to retrieve the display geometry.
    
    @param key the key of the value to get
    @param prefClass preferences class used as the storage area
    @return the requested geometry setting
    """
    if key in ["MainMaximized"]:
        return toBool(prefClass.settings.value("Geometry/" + key,
            prefClass.geometryDefaults[key]))
    else:
        v = prefClass.settings.value("Geometry/" + key)
        if v is not None:
            return v
        else:
            return prefClass.geometryDefaults[key]


def setGeometry(key, value, prefClass=Prefs):
    """
    Module function to store the display geometry.
    
    @param key the key of the setting to be set
    @param value the geometry to be set
    @param prefClass preferences class used as the storage area
    """
    if key in ["MainMaximized"]:
        prefClass.settings.setValue("Geometry/" + key, value)
    else:
        if prefClass.resetLayout:
            v = prefClass.geometryDefaults[key]
        else:
            v = value
        prefClass.settings.setValue("Geometry/" + key, v)


def toBool(value):
    """
    Module function to convert a value to bool.
    
    @param value value to be converted
    @return converted data
    """
    if value in ["true", "1", "True"]:
        return True
    elif value in ["false", "0", "False"]:
        return False
    else:
        return bool(value)


def toList(value):
    """
    Module function to convert a value to a list.
    
    @param value value to be converted
    @return converted data
    """
    if value is None:
        return []
    elif not isinstance(value, list):
        return [value]
    else:
        return value


def toByteArray(value):
    """
    Module function to convert a value to a byte array.
    
    @param value value to be converted
    @return converted data
    """
    if value is None:
        return QByteArray()
    else:
        return value


def toDict(value):
    """
    Module function to convert a value to a dictionary.
    
    @param value value to be converted
    @return converted data
    """
    if value is None:
        return {}
    else:
        return value


def convertPasswords(oldPassword, newPassword, prefClass=Prefs):
    """
    Module function to convert all passwords.
    
    @param oldPassword current master password (string)
    @param newPassword new master password (string)
    @param prefClass preferences class used as the storage area
    """
    from Utilities.crypto import pwRecode
    for key in ["ProxyPassword/Http", "ProxyPassword/Https",
                "ProxyPassword/Ftp", ]:
        prefClass.settings.setValue("UI/" + key, pwRecode(
            prefClass.settings.value("UI/" + key, prefClass.uiDefaults[key]),
            oldPassword,
            newPassword))
    for key in ["MailServerPassword"]:
        prefClass.settings.setValue("User/" + key, pwRecode(
            prefClass.settings.value("User/" + key, prefClass.userDefaults[key]),
            oldPassword,
            newPassword))
    for key in ["SyncFtpPassword", "SyncEncryptionKey"]:
        prefClass.settings.setValue("Help/" + key, pwRecode(
            prefClass.settings.value("Help/" + key, prefClass.helpDefaults[key]),
            oldPassword,
            newPassword))


initPreferences()
#initRecentSettings()
