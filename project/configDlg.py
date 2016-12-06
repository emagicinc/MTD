#!/usr/bin/env python
from PyQt4 import QtCore, QtGui
#import urllib.request, urllib.parse, urllib.error
#from collections import OrderedDict
#import PixmapCache
import codecs
import re
#from util.commonDlg import *
from util.common import getUserList, resetCombo, getCourse, getCourseInfo, getExistingDir, getOpenFileName, setItemId
#from UI.ui_customDict import Ui_CustomDict
from UI.Ui_configDlg import Ui_ConfigDlg
#from util import SMMessageBox
#from .dict import Dict
#import sqlite3
#from .exerciseDlg import *
#from .exerciseDlg import *
#import .jquery_rc

codec = QtCore.QTextCodec.codecForName("UTF-8")
settings = QtCore.QSettings("./option.ini", QtCore.QSettings.IniFormat)
settings.setIniCodec(codec)
settings1 = QtCore.QSettings("./option.ini", QtCore.QSettings.IniFormat)
settings1.setIniCodec(codec)
        
class ConfigDlg(QtGui.QDialog):
    def __init__(self, mw):
        super(ConfigDlg, self).__init__(mw)
        '''选项'''        
        self.ui = Ui_ConfigDlg()        
        self.ui.setupUi(self)
        self.common = None
        self.type = "/course/"
        self.shortCuts = "/ShortCuts/"
        self.mw = mw
        self.userList = None#用户列表
        self.userPath = None#路径
        self.mw.guidDict = None#guid字典[id] = guid
        self.mw.pathDict = None#路径字典[id] = path
        self.initialize()
        #题型:练习说明
        self.ui.spellCombo.lineEdit().editingFinished.connect(self.setSpell)
        self.ui.qaCombo.lineEdit().editingFinished.connect(self.setQa)
        self.ui.chooseCombo.lineEdit().editingFinished.connect(self.setChoose)
        self.ui.tfCombo.lineEdit().editingFinished.connect(self.setTf)
        self.ui.audPathCombo.lineEdit().editingFinished.connect(self.setAudPath)
        self.ui.dbCombo.lineEdit().editingFinished.connect(self.setDb)
        self.setWindowIcon(QtGui.QIcon(':/images/icon.png'))
        
    ################################################
    ###               新代码开始                 ### 
    ################################################  
    def setSpell(self):
        '''设置填空题练习说明'''
        settings1.setValue(self.type + "spellTxt", self.ui.spellCombo.currentText())
        
    def setQa(self):
        '''设置问答题练习说明'''
        settings1.setValue(self.type + "qaTxt", self.ui.qaCombo.currentText())

    def setChoose(self):
        '''设置选择题练习说明'''
        settings1.setValue(self.type + "chooseTxt", self.ui.chooseCombo.currentText())
        
    def setTf(self):
        '''设置是非题练习说明'''
        settings1.setValue(self.type + "tfTxt", self.ui.tfCombo.currentText())
        
    @QtCore.pyqtSlot(int)
    def on_userCombo_currentIndexChanged(self):
        '''用户名储存'''
        settings1.setValue(self.type + "user",self.ui.userCombo.currentText())
        if self.userList:
            self.ui.dbCombo.clear()
            for user in self.userList:
                self.ui.dbCombo.addItem( """%s%s/Repetitions.dat""" % (self.userPath, user))
            self.ui.dbCombo.setCurrentIndex(self.ui.userCombo.currentIndex())
            self.resetCourse(settings.value(self.type + "courseId"))#重置课程组合框
            self.mw.autoBackup()
    
    def setDb(self):
        '''手动设置数据库路径'''
        self.on_dbCombo_currentIndexChanged()
        db = self.ui.dbCombo.currentText()
        users = re.findall('UX/(.*?)/Repetitions.dat', db, re.S)
        if users:
            user = users[0]
            if user in self.userList:
                index = self.ui.userCombo.findText(user)
                if index > -1:
                    self.ui.userCombo.setCurrentIndex(index)
            else:
                self.ui.userCombo.addItem(user)
            settings1.setValue(self.type + "user", user)
            
        
    @QtCore.pyqtSlot(int)
    def on_dbCombo_currentIndexChanged(self):
        '''数据库名储存'''
        settings1.setValue(self.type + "db", self.ui.dbCombo.currentText())
        courseId = settings.value(self.type + "courseId")
        self.resetCourse(courseId)
        self.resetPath()

    @QtCore.pyqtSlot(int)
    def on_courseCombo_currentIndexChanged(self):
        """
        课程名称
        """
        txt = self.ui.courseCombo.currentText()
        courseId = self.ui.courseCombo.itemData(self.ui.courseCombo.currentIndex())
        settings1.setValue(self.type + "courseName", txt)
        settings1.setValue(self.type + "courseId", courseId)
        self.resetPath()
#        print(settings.value(self.type + "courseId"))
        
    def resetCourse(self, courseId):
        '''重置课程组合框,主要用于初始化及用户变更'''
        result = getCourse(self.ui.dbCombo.currentText())
        if result:
            self.guidDict, self.pathDict = getCourseInfo(result)
            resetCombo(self.ui.courseCombo, result, True, courseId, "findData")
  
    def resetPath(self):
        '''重置路径组合框,用于初始化和数据库/课程变动'''
        if self.pathDict:
            for k, v in self.pathDict.items():
                self.ui.coursePathCombo.addItem(v, k)
            self.ui.coursePathCombo.setCurrentIndex(
                    self.ui.coursePathCombo.findData(settings.value(self.type + "courseId")))
            #储存路径
            self.setCoursePath()

    @QtCore.pyqtSlot()
    def on_coursePathBtn_clicked(self):
        '''载入课程路径'''
        getOpenFileName("载入课程包", self.ui.coursePathCombo, "combo", self, "课程包文件 (*.smpak);;所有文件 (*)")
        self.setCoursePath()

    def setCoursePath(self):
        '''设置课程路径'''
        path = QtCore.QFileInfo(self.ui.coursePathCombo.currentText()).path()
        settings1.setValue(self.type + "coursePath", path.replace("/", "\\"))
        
    @QtCore.pyqtSlot()
    def on_audPathBtn_clicked(self):
        '''载入音频路径'''
        getExistingDir("载入语音库", self.ui.audPathCombo, "combo", self)
        self.setAudPath()
        
    def setAudPath(self):
        '''设置音频路径'''
        path = self.ui.audPathCombo.currentText()
        settings1.setValue(self.type + "audioPath", path)        

    @QtCore.pyqtSlot(bool)
    def on_autoSaveCB_toggled(self):
        '''自动储存'''
        if self.ui.autoSaveCB.isChecked():
            settings1.setValue(self.type + "autoSave", "1")
        else:
            settings1.setValue(self.type + "autoSave", "0")
            
    @QtCore.pyqtSlot(bool)
    def on_autoBackupCB_toggled(self):
        '''自动备份'''
        if self.ui.autoBackupCB.isChecked():
            settings1.setValue(self.type + "autoBackup", "1")
        else:
            settings1.setValue(self.type + "autoBackup", "0")

    ####快捷键
    @QtCore.pyqtSlot(bool)
    def on_snagQRB1_toggled(self):
        '''抓图Q_mod'''
        if self.ui.snagQRB1.isChecked():
            settings1.setValue(self.shortCuts + "snagQMod", "WIN")
            
    @QtCore.pyqtSlot(bool)
    def on_snagQRB2_toggled(self):
        '''抓图Q_mod'''
        if self.ui.snagQRB2.isChecked():
            settings1.setValue(self.shortCuts + "snagQMod", "CTRL")
            
    @QtCore.pyqtSlot(bool)
    def on_snagQRB3_toggled(self):
        '''抓图Q_mod'''
        if self.ui.snagQRB3.isChecked():
            settings1.setValue(self.shortCuts + "snagQMod", "Alt")
            
    @QtCore.pyqtSlot(bool)
    def on_snagQRB4_toggled(self):
        '''抓图Q_mod'''
        if self.ui.snagQRB4.isChecked():
            settings1.setValue(self.shortCuts + "snagQMod", "NONE")

    @QtCore.pyqtSlot(bool)
    def on_snagARB1_toggled(self):
        '''抓图A_mod'''
        if self.ui.snagARB1.isChecked():
            settings1.setValue(self.shortCuts + "snagAMod", "WIN")
            
    @QtCore.pyqtSlot(bool)
    def on_snagARB2_toggled(self):
        '''抓图A_mod'''
        if self.ui.snagARB2.isChecked():
            settings1.setValue(self.shortCuts + "snagAMod", "CTRL")
            
    @QtCore.pyqtSlot(bool)
    def on_snagARB3_toggled(self):
        '''抓图A_mod'''
        if self.ui.snagARB3.isChecked():
            settings1.setValue(self.shortCuts + "snagAMod", "Alt")

    @QtCore.pyqtSlot(bool)
    def on_snagARB4_toggled(self):
        '''抓图A_mod'''
        if self.ui.snagARB4.isChecked():
            settings1.setValue(self.shortCuts + "snagAMod", "NONE")
            
    @QtCore.pyqtSlot(bool)
    def on_captureQRB1_toggled(self):
        '''采集问题_mod'''
        if self.ui.captureQRB1.isChecked():
            settings1.setValue(self.shortCuts + "captureQMod", "WIN")
            
    @QtCore.pyqtSlot(bool)
    def on_captureQRB2_toggled(self):
        '''采集问题_mod'''
        if self.ui.captureQRB2.isChecked():
            settings1.setValue(self.shortCuts + "captureQMod", "CTRL")
            
    @QtCore.pyqtSlot(bool)
    def on_captureQRB3_toggled(self):
        '''采集问题_mod'''
        if self.ui.captureQRB3.isChecked():
            settings1.setValue(self.shortCuts + "captureQMod", "Alt")

    @QtCore.pyqtSlot(bool)
    def on_captureQRB4_toggled(self):
        '''采集问题_mod'''
        if self.ui.captureQRB4.isChecked():
            settings1.setValue(self.shortCuts + "captureQMod", "NONE")
            
    @QtCore.pyqtSlot(bool)
    def on_captureARB1_toggled(self):
        '''采集答案_mod'''
        if self.ui.captureARB1.isChecked():
            settings1.setValue(self.shortCuts + "captureAMod", "WIN")

    @QtCore.pyqtSlot(bool)
    def on_captureARB2_toggled(self):
        '''采集答案_mod'''
        if self.ui.captureARB2.isChecked():
            settings1.setValue(self.shortCuts + "captureAMod", "CTRL")
            
    @QtCore.pyqtSlot(bool)
    def on_captureARB3_toggled(self):
        '''采集答案_mod'''
        if self.ui.captureARB3.isChecked():
            settings1.setValue(self.shortCuts + "captureAMod", "Alt")
            
    @QtCore.pyqtSlot(bool)
    def on_captureARB4_toggled(self):
        '''采集答案_mod'''
        if self.ui.captureARB4.isChecked():
            settings1.setValue(self.shortCuts + "captureAMod", "NONE")
            
    @QtCore.pyqtSlot(int)
    def on_snagQCombo_currentIndexChanged(self):
        '''抓图Q:主键'''
        txt = self.ui.snagQCombo.currentText()
        settings1.setValue(self.shortCuts + "snagQ", txt)
        
    @QtCore.pyqtSlot(int)
    def on_snagACombo_currentIndexChanged(self):
        '''抓图A:主键'''
        txt = self.ui.snagACombo.currentText()
        settings1.setValue(self.shortCuts + "snagA", txt)
        
    @QtCore.pyqtSlot(int)
    def on_captureQCombo_currentIndexChanged(self):
        '''采集问题:主键'''
        txt = self.ui.captureQCombo.currentText()
        settings1.setValue(self.shortCuts + "captureQ", txt) 
        
    @QtCore.pyqtSlot(int)
    def on_captureACombo_currentIndexChanged(self):
        '''采集答案:主键'''
        txt = self.ui.captureACombo.currentText()
        settings1.setValue(self.shortCuts + "captureA", txt)
        
    def initialize(self):
        '''初始化'''
        '''获取用户数据,可同时为"写入数据库"和"课程同步"服务'''
        #MOD键
        #采集问题:辅键
        if settings.value(self.shortCuts + "captureAMod") == "WIN":
            self.ui.captureARB1.setChecked(True)
        elif settings.value(self.shortCuts + "captureAMod") == "CTRL":
            self.ui.captureARB2.setChecked(True)
        elif settings.value(self.shortCuts + "captureAMod") == "ALT":
            self.ui.captureARB3.setChecked(True) 
        #采集答案:辅键
        if settings.value(self.shortCuts + "captureQMod") == "WIN":
            self.ui.captureQRB1.setChecked(True)
        elif settings.value(self.shortCuts + "captureQMod") == "CTRL":
            self.ui.captureQRB2.setChecked(True)
        elif settings.value(self.shortCuts + "captureQMod") == "ALT":
            self.ui.captureQRB3.setChecked(True) 
        #抓图A:辅键
        if settings.value(self.shortCuts + "snagAMod") == "WIN":
            self.ui.snagARB1.setChecked(True)
        elif settings.value(self.shortCuts + "snagAMod") == "CTRL":
            self.ui.snagARB2.setChecked(True)
        elif settings.value(self.shortCuts + "snagAMod") == "ALT":
            self.ui.snagARB3.setChecked(True)    
         #抓图Q:辅键
        if settings.value(self.shortCuts + "snagQMod") == "WIN":
            self.ui.snagQRB1.setChecked(True)
        elif settings.value(self.shortCuts + "snagQMod") == "CTRL":
            self.ui.snagQRB2.setChecked(True)
        elif settings.value(self.shortCuts + "snagQMod") == "ALT":
            self.ui.snagQRB3.setChecked(True)              
        #采集问题&答案:主键
        try:
            self.ui.snagQCombo.setCurrentIndex(
                self.ui.snagQCombo.findText(settings.value(self.shortCuts + "snagQ")))
            self.ui.snagACombo.setCurrentIndex(
                self.ui.snagACombo.findText(settings.value(self.shortCuts + "snagA")))
            self.ui.captureQCombo.setCurrentIndex(
                self.ui.captureQCombo.findText(settings.value(self.shortCuts + "captureQ")))
            self.ui.captureACombo.setCurrentIndex(
                self.ui.captureACombo.findText(settings.value(self.shortCuts + "captureA")))
        except:
            pass
        #启用自动储存
        if settings.value(self.type + "autoSave") == "1":
            self.ui.autoSaveCB.setChecked(True)
        else:
            self.ui.autoSaveCB.setChecked(False)
        #启用自动备份
        if settings.value(self.type + "autoBackup") == "1":
            self.ui.autoBackupCB.setChecked(True)
        else:
            self.ui.autoBackupCB.setChecked(False)            
        #!!!重要:获取数据库用户名&路径
        self.userPath, self.userList = getUserList(self)
        courseId = settings.value(self.type + "courseId")
        resetCombo(self.ui.userCombo, self.userList, None, 
                settings.value(self.type + "user"), "findText") 
        self.resetCourse(courseId)#重置课程组合框
        self.resetPath()#重置路径组合框
        #语音库路径
        path = settings.value(self.type + "audioPath")
        self.ui.audPathCombo.setEditText(path)
        
        self.ui.pagesSpin.setValue(int(settings.value(self.type + "pagesPerChap")))
        self.ui.tempNumSpin.setValue(int(settings.value(self.type + "tempNum")))
        self.ui.tempImgSpin.setValue(int(settings.value(self.type + "tempImg")))
        #题型:练习说明
        self.ui.spellCombo.setEditText(str(settings.value(self.type + "spellTxt")))
        self.ui.qaCombo.setEditText(str(settings.value(self.type + "qaTxt")))
        self.ui.chooseCombo.setEditText(str(settings.value(self.type + "chooseTxt")))
        self.ui.tfCombo.setEditText(str(settings.value(self.type + "tfTxt")))
        
    @QtCore.pyqtSlot(int)
    def on_tempNumSpin_valueChanged(self):
        '''模板编号'''
        settings1.setValue(self.type + "tempNum", self.ui.tempNumSpin.value()) 

    @QtCore.pyqtSlot(int)
    def on_tempImgSpin_valueChanged(self):
        '''背景图编号'''
        settings1.setValue(self.type + "tempImg", self.ui.tempImgSpin.value()) 
  
    @QtCore.pyqtSlot(int)
    def on_pagesSpin_valueChanged(self):
        '''每章节页面数'''
        settings1.setValue(self.type + "pagesPerChap", self.ui.pagesSpin.value())   
    ################################################
    ###               新代码结束                 ### 
    ################################################  
    
    @QtCore.pyqtSlot()
    def on_okBtn_clicked(self):
        '''暂时与关闭按钮功能一样'''
        courseId = self.ui.courseCombo.itemData(self.ui.courseCombo.currentIndex())
        self.mw.resetCourse(courseId)
#        setItemId(self.mw, courseId)#设置itemId
#        try:
#            self.mw.setCoursePath()
#            self.mw.updateChapName()
#            self.mw.initChapTree()#重置章节树
#        except:
#            pass
#            self.mw.itemList = [] # 列表重置
        self.close()

    @QtCore.pyqtSlot()
    def on_closeBtn_clicked(self):
        '''退出'''  
        self.close()                               
