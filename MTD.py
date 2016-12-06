#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sip

sip.setapi('QVariant', 2)

from PyQt4 import QtCore, QtGui, QtXml, QtNetwork, QtWebKit
from PyQt4.QtWebKit import QWebSettings
import codecs, zlib, struct, binascii, shutil, os, random, sqlite3, chardet, win32con, \
    win32api, json, re, time
from ctypes import c_bool, c_int, WINFUNCTYPE, windll, cdll, CDLL
from ctypes.wintypes import UINT
import win32com.client
from datetime import datetime
from PIL import Image
from bs4 import BeautifulSoup
import pandas as pd
from UI.Ui_mainWindow import Ui_MainWindow
# from UI.Ui_dbPathDlg import Ui_DbPathDlg
from util.common import copyTree, copyTemplate, initCourseList, readFile, strippedPath, correctCodec, getSelTxt, \
    outTxt, resultToId, getGuid, getFlds, date_uxStamp, execSql, makeImageList, makeAudioList, getMediaFile, \
    parseCourseList, getEmptyItem, writeCourseList, writeItemFile, writeDb, getOpenFileName, \
    copyFile, gotoQASection, saveEditItem, updateChapTree, verifyCourseName, outputStream, getCourse, getCourseInfo, \
    resetCombo, setItemId, getCourseList, getId, getExistingDir, deleteItemFile, getItemIdFromDb, \
    connectDb, closeDb, parseDbCourse, writeColDb, dbToQASection, saveEditData, warn, \
    getUserList, toList, getModelId, loadConf, resetModelCombo, getOnlineId
# from project.preview import RenderItem
# from project.produceDlg import ProduceDlg
from util.keyMap import getKey
from util import SMMessageBox
import Preferences as Prefs
from project.models import *
from util.db import DB

WM_HOTKEY = 0x0312


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent,
                                         QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowSystemMenuHint)

        self.ui = Ui_MainWindow()
        #        self.setPostition()
        self.ui.setupUi(self)
        #        self.styleDict = {
        #            "系统":"windows",
        #            "清新":"cleanlooks",
        #            "塑质":"plastique",
        #            "Motif":"Motif",
        #            "通用":"CDE"
        #            }
        self.curFile = None
        self.setWindowIcon(QtGui.QIcon(':/images/icon.png'))
        self.progName = "MTD"
        # TODO: 名称需要改为白色
        self.ver = "V 1.0.0"
        self.setWindowTitle('''%s   %s''' % (self.progName, self.ver))

        #######新参数#######
        self.itemId = None  # 表示新增item
        self.audioList = None
        self.imageList = None
        self.allItems = {}  # 将练习ID存入以章节ID为key的字典
        self.curChap = None  # 用来储存当前章节Item
        self.curChapId = Prefs.getCourse("curChap")  # 用来储存当前章节ID,为空时将页面添加到文档末
        self.itemList = []  # 用来储存当前课程章节树中点击过的item
        self.posList = []  # 第3列章节ID值,用于重载时判断是否选中
        self.selItems = []  # 选中的页面列表,以Item的方式,这是准备用来删除或移动操作的
        # 尝试启用新的参数
        self.chapDict = None  # 储存章节的父ID信息,此ID并非页面ID,如果此值不为0,则表示不是顶层章节
        self.chapIdDict = None  # 储存页面ID和章节ID的对应关系,用于课程列表编辑器
        self.chapOrder = []  # 章节顺序,用于排列章节,以便输出时遵循
        self.allItems = None  # 以ID为Key,id/name对列表为value的字典,用于展开,可看作练习id总表
        self.childDict = None  # 以父章节为key,子章节列表为value的字典,主要用于校验chapDict
        self.chapInfoDict = {}  # 150108新增,键为章节ID,值为Item,用于数据库模式章节初始化/课程制作模块章节初始化
        self.chapElemDict = {}  # 150110新增,键为章节ID,值为courseList的elem,用于创建课程列表时定位父节点
        # 原属configDlg的
        self.guidDict = None  # guid字典[id] = guid
        self.pathDict = None  # 路径字典[id] = path

        self.ac = None  # 用于SuperMemo划词助手连接
        self.confDict = {}  # 划词助手的模型参数

        self.cxn = None  # 数据库连接
        self.cur = None  # 数据库指针，cursor
        self.curDb = None  # 当前使用的DB类型,system, user，用来判断是否要重连数据库
        self.curCourseId = None
        self.today = QtCore.QDate.currentDate().toString("yyyy-MM-dd")  # 主要用于数据库LastRep数据
        '''信号，表示初始化完成，根据此信号初始化模式，连接数据库,置为None是为了防止初始化控件时执行refreshMode代码'''
        self.INITIALIZED = None

        self.settingsStyle = self.loadStyleSheet(':/qss/emagic.settings.qss')  # TODO:临时修改
        self.topStyle = self.loadStyleSheet(':/qss/emagic.top.qss')
        self.leftStyle = self.loadStyleSheet(':/qss/emagic.left.qss')
        self.mainStyle = self.loadStyleSheet(':/qss/emagic.main.qss')
        #        self.dlgStyle = self.loadStyleSheet(':/qss/emagic.dlg.qss')#各设置窗口 #TODO:临时修改,需要修改路径,重新编译
        self.centralStyle = self.loadStyleSheet(':/qss/emagic.central.qss')  # 主体部分
        self.ui.configWidget.setStyleSheet(self.settingsStyle)
        self.ui.topWidget.setStyleSheet(self.topStyle)
        self.ui.leftWidget.setStyleSheet(self.leftStyle)
        self.ui.mainWidget.setStyleSheet(self.mainStyle)
        self.ui.centralwidget.setStyleSheet(self.centralStyle)  # 这个级别最高，位于顶层
        self.moveable = False

        self.initialize()

    ################################################
    ###            新代码开始                    ### 
    ################################################  
    def setPostition(self):
        '''设置窗口位置'''
        desktop = QtGui.QApplication.desktop()
        rect = desktop.screenGeometry()
        self.move(rect.width() / 2 - 430, rect.height() / 4)

    def loadStyleSheet(self, qssFile):
        '''载入样式表'''
        file = QtCore.QFile(qssFile)
        file.open(QtCore.QFile.ReadOnly)
        styleSheet = file.readAll()
        file.close()
        try:
            # Python v2.
            styleSheet = unicode(styleSheet, encoding='utf8')
        except NameError:
            # Python v3.
            styleSheet = str(styleSheet, encoding='utf8')
        return styleSheet

    @QtCore.pyqtSlot()
    def on_inboxBtn_clicked(self):
        for i in self.se.query(Subtask).order_by(Subtask.id):
            print(i.title)
        for i in self.se.query(Task).order_by(Task.id):
            print(i.title)
        for i in self.se.query(List).order_by(List.id):
            print(i.title)

    @QtCore.pyqtSlot()
    def on_starListBtn_clicked(self):
        query = self.se.query(List).filter(List.title != 'inbox')
        res = query.all()

    @QtCore.pyqtSlot()
    def on_addListBtn_clicked(self):
        '''添加清单'''
        # 先弹出一个命名窗口
        print('addlist')

    #        title = self.ui.addSubtaskLE.text()
    #        #TODO: 最好做一个重名检查
    #        item = QtGui.QListWidgetItem(self.ui.subtaskLW)
    #        sid = None
    #        while True:
    #            sid = """13%s""" % getOnlineId()
    #            if sid not in self.subtasks.keys():
    #                break
    #        item.setText(title)
    #        item.setData(32, sid)
    #        subtask = Subask(onlineId=sid, title=title, parentId=self.curTaskId)
    #        self.se.add(subtask)
    #        self.se.commit()
    #        self.subtasks[sid] = title #更新self.tasks

    @QtCore.pyqtSlot()
    def on_manageListBtn_clicked(self):
        '''添加清单'''
        print('manage')
        # 切到清单页
        # 双击进入清单
        # 对清单进行重命名
        # 可对清单进行转换(转成任务,子任务,注意考虑清单下已有任务的情况),转移(到另一个清单下)

    def initialize(self):
        self.db = DB("./mtdo.db")  # 以下测试全部通过
        self.se = self.db.se
        # 获取当前任务ID:title的字典
        self.curListId = "278927047"
        self.curTaskId = None
        self.curSubtaskId = None
        self.hour = 0
        self.min = 0
        self.ui.mainStk.setCurrentIndex(0)
        self.timer = QtCore.QTimer(self)  # 用来计时
        self.timer.timeout.connect(self.showTime)  # 显示时间
        #        print(self.tasks)
        self.tasks = self.db.dic(Task)
        self.records = self.db.dic(Record)
        self.subtasks = self.db.dic(Subtask)
        self.lists = self.db.dic(List)
        for k, v in self.tasks.items():
            self.__setItem(k, v, self.ui.taskLW)
        for k, v in self.lists.items():
            self.__setItem(k, v, self.ui.listLW)

    def __setItem(self, id, title, obj):
        '''根据item列表对ListWidget进行设置;'''
        # TODO: 此方法暂未使用
        # TODO:151102修改元件库DRAG区规则,itemList不再是单一值的列表,而是变成以元组为值的列表,其它地方要视情况逐渐转变过来!
        item = QtGui.QListWidgetItem(obj)
        item.setText(title)
        item.setData(32, id)  # 编号

    #    @QtCore.pyqtSlot(QtGui.QListWidgetItem)
    #    def on_taskLW_itemClicked(self):
    #        """
    #        taskLW中item单击;
    #        """
    #        item = self.ui.taskLW.currentItem()
    #        #TODO:切换到子任务界面
    #        print(item.text(), item.data(32))

    @QtCore.pyqtSlot(QtGui.QListWidgetItem)
    def on_listLW_itemClicked(self, item):
        """
        listLW中item单击;
        """
        # 转到专用的页面
        self.ui.mainStk.setCurrentIndex(4)
        self.curListId = item.data(32)
        tasks = self.db.dic(Task, item.data(32))
        self.ui.listTaskLW.clear()
        for k, v in tasks.items():
            self.__setItem(k, v, self.ui.listTaskLW)
        #        print(item.text(), item.data(32))

    def addTask(self, le, lw, name=None):
        '''添加任务的公用方法'''
        # le为LineEdit控件
        # lw为ListWidget控件
        title = name
        if not name:
            title = le.text()
        # TODO: 最好做一个重名检查
        # TODO: 增加任务移动功能
        if title not in self.tasks.values():
            item = QtGui.QListWidgetItem(lw)
            # TODO: id应做成一个通用的方法
            id = None
            while True:
                id = """23%s""" % getOnlineId()
                if id not in self.tasks.keys():
                    break
            item.setText(title)
            item.setData(32, id)
            task = Task(
                onlineId=id,
                title=title,
                parentId=self.curListId,
            )
            self.se.add(task)
            self.tasks[id] = title  # 更新self.tasks
            if not name:  # 传入title的话,表示要批量处理
                self.se.commit()
                le.clear()

    @QtCore.pyqtSlot()
    def on_addListTaskLE_returnPressed(self):
        '''listPage下的添加任务'''
        self.addTask(self.ui.addListTaskLE, self.ui.listTaskLW)

    @QtCore.pyqtSlot()
    def on_addTaskLE_returnPressed(self):
        print("in")
        # TODO: 添加清单、任务、子任务
        # TODO:添加时setData
        # TODO:添加时更新数据库
        # TODO:读取数据库指定的任务和清单的控件
        self.addTask(self.ui.addTaskLE, self.ui.taskLW)

    @QtCore.pyqtSlot()
    def on_importBtn_clicked(self):
        '''导入任务@指定清单'''
        #        file = './import_test.txt'
        file = getOpenFileName('打开文件', None, 'file', self)
        df = pd.read_table(file)
        for i in df.values:
            self.addTask(self.ui.addListTaskLE, self.ui.listTaskLW, i[0])
        self.se.commit()

    @QtCore.pyqtSlot()
    def on_addListTaskBtn_clicked(self):
        '''新增任务@指定清单'''
        self.on_addListTaskLE_returnPressed()

    @QtCore.pyqtSlot()
    def on_addTaskBtn_clicked(self):
        '''新增任务'''
        self.on_addTaskLE_returnPressed()

    @QtCore.pyqtSlot(QtGui.QListWidgetItem)
    def on_taskLW_itemDoubleClicked(self, item):
        """
        taskLW 中item双击;
        """
        self.gotoTaskPage(item)

    @QtCore.pyqtSlot(QtGui.QListWidgetItem)
    def on_listTaskLW_itemDoubleClicked(self, item):
        """
        listTaskLW 中item双击;
        """
        self.gotoTaskPage(item)

    def gotoTaskPage(self, item):
        '''转到任务页面,公共方法'''
        self.curTaskId = item.data(32)
        self.ui.mainStk.setCurrentIndex(1)
        self.ui.taskLbl.setText(item.text())
        subtasks = self.db.dic(Subtask, item.data(32))
        self.ui.subtaskLW.clear()
        for k, v in subtasks.items():
            self.__setItem(k, v, self.ui.subtaskLW)

    @QtCore.pyqtSlot()
    def on_addSubtaskLE_returnPressed(self):
        print("in")
        # TODO: 添加清单、任务、子任务
        # TODO:添加时setData
        # TODO:添加时更新数据库
        # TODO:读取数据库指定的任务和清单的控件
        title = self.ui.addSubtaskLE.text()
        # TODO: 最好做一个重名检查
        item = QtGui.QListWidgetItem(self.ui.subtaskLW)
        id = None
        while True:
            id = """13%s""" % getOnlineId()
            if id not in self.subtasks.keys():
                break
        item.setText(title)
        item.setData(32, id)
        subtask = Subask(onlineId=id, title=title, parentId=self.curTaskId)
        self.se.add(subtask)
        self.se.commit()
        self.subtasks[id] = title  # 更新self.tasks

    @QtCore.pyqtSlot()
    def on_addSubtaskBtn_clicked(self):
        '''新增子任务'''
        self.on_addSubtaskLE_returnPressed()

    #    @QtCore.pyqtSlot(QtGui.QListWidgetItem)
    #    def on_subtaskLW_itemDoubleClicked(self, item):
    #        """
    #        subtaskLW 中item双击;
    #        """
    #        #转到第3页
    #        #时钟，开始按钮（可切换成暂停），终止按钮
    #        self.ui.mainStk.setCurrentIndex(2)
    #        self.curSubtaskId = item.data(32)
    #        self.ui.timerTitleLbl.setText(item.text())
    #        self.ui.lcdLN.display("00:00:00")
    @QtCore.pyqtSlot()
    def on_onManualBtn_clicked(self):
        '''进入手动记录界面'''
        self.ui.mainStk.setCurrentIndex(3)
        title = self.tasks.get(self.curTaskId)
        self.ui.recordTitleLbl.setText(title)
        today = QtCore.QDate.currentDate()
        self.ui.todayDE.setDate(today)
        self.ui.hourSpin.setValue(0)
        self.ui.minuteSpin.setValue(0)
        self.ui.minCountSpin.setValue(0)
        self.ui.maxCountSpin.setValue(0)

    @QtCore.pyqtSlot()
    def on_timerBtn_clicked(self):
        '''进入计时界面'''
        self.ui.mainStk.setCurrentIndex(2)
        #        self.curSubtaskId = item.data(32)
        title = self.tasks.get(self.curTaskId)
        self.ui.timerTitleLbl.setText(title)
        self.ui.lcdLN.display("00:00:00")

    @QtCore.pyqtSlot()
    def on_startBtn_clicked(self):
        '''开始计时'''
        if self.ui.startBtn.text() in ['开始', '继续']:
            if self.ui.startBtn.text() == '开始':
                self.hour = 0
                self.min = 0
                self.sec = 0
            self.ui.startBtn.setText('暂停')
            self.timer.start(1000)
            self.showTime()
        else:  # 暂停
            self.ui.startBtn.setText('继续')
            self.timer.stop()
        #            self.showTime()

    @QtCore.pyqtSlot()
    def on_rangeCB_toggled(self):
        '''范围CB是否选中'''
        active = self.ui.rangeCB.isChecked()
        self.ui.maxCountSpin.setVisible(active)
        self.ui.slashLbl.setVisible(active)

    @QtCore.pyqtSlot()
    def on_stopBtn_clicked(self):
        '''停止计时'''
        self.ui.startBtn.setText('开始')
        self.timer.stop()
        self.ui.mainStk.setCurrentIndex(3)
        title = self.tasks.get(self.curTaskId)
        self.ui.recordTitleLbl.setText(title)
        today = QtCore.QDate.currentDate()
        self.ui.todayDE.setDate(today)
        self.ui.hourSpin.setValue(self.hour)
        self.ui.minuteSpin.setValue(self.min)
        # TODO: 要控制单位的显示
        # TODO: 增加倒计时的功能

    @QtCore.pyqtSlot()
    def on_saveBtn_clicked(self):
        # 储存
        # 注意,如果从任务一级就开始记录,就必须指定是储存任务还是子任务
        # 注意,还是应该做成一个记录表来储存.
        # 这样也便于统计

        # TODO: 要可以修改记录
        # TODO: 点击后转到记录汇总页面
        # TODO: listPage内增加一个随机挑选任务的按钮
        # TODO: listPage内增加按星级/标签/常用等方式筛选,任务表要添加星级字段
        # TODO: 增加weekPlan表,用来随机挑选任务用,任务界面增加星期选项
        # TODO: 可以增加40-50秒以上算作一分钟的设置
        # 不足一分钟提示
        text = self.ui.recordTitleLbl.text()
        id = None
        while True:
            id = """33%s""" % getOnlineId()
            if id not in self.records.keys():
                break
            #        today = datetime.now()
        # 计算时间
        usageTime = self.hour * 60 + self.min  # 记录分钟数
        # 计算工作量
        minCount = None
        maxCount = None
        workLoad = self.ui.minCountSpin.value()
        date = self.ui.todayDE.dateTime()
        date = date.toPyDateTime()
        if self.ui.rangeCB.isChecked():
            minCount = self.ui.minCountSpin.value()
            maxCount = self.ui.maxCountSpin.value()
            workLoad = maxCount - minCount
        record = Record(
            onlineId=id,
            title=text,
            createdAt=date,
            updatedAt=date,
            parentId=self.curTaskId,
            usageTime=usageTime,
            workLoad=workLoad,
            minCount=minCount,
            maxCount=maxCount
        )
        self.se.add(record)
        self.se.commit()
        self.records[id] = text

    @QtCore.pyqtSlot()
    def on_resetBtn_clicked(self):
        '''重置计时'''
        self.ui.startBtn.setText('开始')
        self.timer.stop()
        self.hour = 0
        self.min = 0
        self.sec = 0

    def showTime(self):
        #        time = QtCore.QTime.currentTime()
        def cv(s):
            '''在数字前补0,并转成字符'''
            s = """0%s""" % s
            return s[-2:]

        self.sec += 1
        if self.sec == 60:
            self.min += 1
            self.sec = 0
        if self.min == 60:
            self.hour += 1
            self.min = 0
        #        text = time.toString('hh:mm:ss')
        #        if (self.sec % 2) == 0: #每秒更新一次
        #            text = text[:2] + ' ' + text[3:]
        #        curTime = QtCore.QTime.setHMS(self.hour, self.min, self.sec)
        text = """%s:%s:%s""" % (cv(self.hour), cv(self.min), cv(self.sec))
        #        text = QtCore.QTime.toString(curTime, "hh:mm:ss")

        self.ui.lcdLN.display(text)


        # 加上判断：if txt in self.tasks.values()
        # 要加一个生成onlineId的方法

    #    onlineId = Column(Integer)
    #    title = Column(String)
    #    createdAt = Column(Text)
    #    updatedAt = Column(Text)
    #    parentId = Column(Text)
    #    dueDate = Column(Text)
    #    starred = Column(Boolean)
    #    completed = Column(Boolean)
    #    completedAt = Column(Text)
    #    usageTime = Column(Time)
    #    workLoad = Column(Float)
    #    lastPos = Column(Integer)
    #    unit = Column(Integer)

    #    def setItem(self, itemList, widget):
    #        '''根据item列表对ListWidget进行设置;'''
    #        if len(itemList) < 1:
    #            return
    #        for i in itemList:
    #            item = QtGui.QListWidgetItem(widget)
    #            if isinstance(i, str):
    #                item.setText(i)
    #            else:
    #                item.setText("""[%s]%s""" % (i[1], i[0]))
    #                item.setData(32, i[1]) #编号
    #                item.setData(3, i[1]) #显示类型（设置为toolTipRole）
    #                item.setData(11, i[1]) #显示类型（设置为toolTipRole）
    #
    #            widget.addItem(item)

    def getTime(self, start):
        '''获取时间差'''
        now = time.time()
        interval = int((now - start) / 60)
        sec = int((now - start - interval * 60))
        return """%s分%s秒""" % (interval, sec)

    @QtCore.pyqtSlot()
    def on_closeBtn_clicked(self):
        '''退出'''
        self.quit()

    @QtCore.pyqtSlot()
    def on_exitBtn_clicked(self):
        '''退出'''
        self.quit()

    @QtCore.pyqtSlot()
    def on_minimizeBtn_clicked(self):
        '''最小化@顶部'''
        self.showMinimized()

    def quit(self):
        '''退出'''
        self.close()

    def closeEvent(self, event):
        '''响应关闭事件,注意,这里实际上是被self.quit调用'''
        sys.exit()

    def eventFilter(self, watched, event):
        """
        基本思路:给快捷键LE安装eventFilter,然后调用keyPressEvent
        Method called to filter the event queue.
        
        @param watched the QObject being watched
        @param event the event that occurred
        @return always False
        """
        if event.type() == QtCore.QEvent.KeyPress:
            self.keyPressEvent(event)
            return True

        return False

    def mousePressEvent(self, event):
        '''实现标题栏拖动：1'''
        if event.buttons() == QtCore.Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            rect = self.ui.topWidget.rect()
            if rect.contains(event.pos()):
                self.moveable = True
        event.accept()

    def mouseMoveEvent(self, event):
        '''实现标题栏拖动：2'''
        if event.buttons() == QtCore.Qt.LeftButton and self.moveable:
            self.move(event.globalPos() - self.dragPosition)
        event.accept()

    def mouseReleaseEvent(self, event):
        '''实现标题栏拖动：3'''
        if self.moveable:
            self.moveable = False

        #    def catureQustion(self):
        #        '''响应全局快捷键'''
        ##        from project.collectorDlg import CollectorDlg
        #        dlg = CollectorDlg(self)
        #        dlg.exec_()

    def writeNotes(self, pr):
        '''响应来自collectorWgtOK按钮点击'''
        file = './knowledge.txt'
        qtxt = pr.ui.questionLE.text()
        atxt = pr.ui.answerLE.text()
        if atxt != "" and qtxt != "":
            content = """%s\t%s\n""" % (qtxt, atxt)
            outputStream(self, content, file, 'append2')


class GlobalHotKeyApp(QtGui.QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.keyMap = {
            "ALT": 0x0001,
            "NONE": 0x000,
            "CONTROL": 0x0002,
            "SHIFT": 0x0004,
            "WIN": 0x0008,
            "F11": win32con.VK_F11,
            "F12": win32con.VK_F12,
            "R": ord("R"),
            "S": ord("S"),
            "A": ord("A"),
        }
        prototype = WINFUNCTYPE(c_bool, c_int, c_int, UINT, UINT)
        # paramflags: 1.窗口句柄; 2.热键序号；3.MOD键，4，热键
        paramflags = (1, 'hWnd', 0), (1, 'id', 0), (1, 'fsModifiers', 0), (1, 'vk', 0)
        self.RegisterHotKey = prototype(('RegisterHotKey', windll.user32), paramflags)

    def register(self):
        '''热键注册'''
        # 检查有无设置数据库
        #        db = Prefs.getCourse("db")
        #        if not QtCore.QFile.exists(db):
        #            dlg = DbPathDlg()
        #            dlg.exec_()
        #        else:
        self.mw = MainWindow()
        #            captureQModKey = Prefs.getShortcut("captureQMod")
        #            captureQMod = getKey(captureQModKey)
        #            captureQKey = Prefs.getShortcut("captureQ")
        #            captureQ = getKey(captureQKey)
        self.mw.show()

    #            if captureQMod and captureQ:
    #                r1 = self.RegisterHotKey(c_int(self.mw.winId()), 1, captureQMod, captureQ)
    #                if not r1:#全局捕捉问题
    #                    QtGui.QMessageBox.critical(self.mw, '热键冲突', """<p>无法注册全局热键 %s + %s.</p>\
    #                        <p>请重新选择热键!</p>""" % (captureQModKey, captureQKey))
    #            snagQModKey = Prefs.getShortcut("snagQMod")
    #            snagQMod = getKey(snagQModKey)
    #            snagAModKey = Prefs.getShortcut("snagAMod")
    #            snagAMod = getKey(snagAModKey)

    #            captureAModKey = Prefs.getShortcut("captureAMod")
    #            captureAMod = getKey(captureAModKey)
    #            snagQKey = Prefs.getShortcut("snagQ")
    #            snagQ = getKey(snagQKey)
    #            snagAKey = Prefs.getShortcut("snagA")
    #            snagA = getKey(snagAKey)


    #            captureAKey = Prefs.getShortcut("captureA")
    #            captureA = getKey(captureAKey)
    #            if snagQMod and snagQ:
    #                r1 = self.RegisterHotKey(c_int(self.winId()), 1, snagQMod, snagQ)
    #                if not r1:#问题区抓图
    #                    QtGui.QMessageBox.critical(self, '热键冲突', """<p>无法注册全局热键 %s + %s.</p>\
    #                        <p>请重新选择热键!</p>""" % (snagQModKey, snagQKey))
    #            if snagAMod and snagA:
    #                r2 = self.RegisterHotKey(c_int(self.winId()), 2, snagAMod, snagA)
    #                if not r2:#答案区抓图
    #                    QtGui.QMessageBox.critical(self, '热键冲突', """<p>无法注册全局热键 %s + %s.</p>\
    #                        <p>请重新选择热键!</p>""" % (snagAModKey, snagAKey))

    #            if captureAMod and captureA:
    #                r4 = self.RegisterHotKey(c_int(self.winId()), 4, captureAMod, captureA)
    #                if not r4:#全局捕捉答案
    #                    QtGui.QMessageBox.critical(self, '热键冲突', """<p>无法注册全局热键 %s + %s.</p>\
    #                        <p>请重新选择热键!</p>""" % (captureAModKey, captureAKey))

    def winEventFilter(self, msg):
        #        print(msg.message)
        if msg.message == WM_HOTKEY:
            #            import imp
            #            imp.reload(globalKey)
            #            if msg.wParam in (1, 2):#表示抓图到Q/区
            ##                self.snagit()
            #                self.grabImage(msg.wParam)
            if msg.wParam == 1:  # 全局抓Q
                self.mw.catureQustion()
            #            elif msg.wParam == 4: #全局抓A
            #                self.captureAnswer()
            else:
                pass  # 后期可改为增加从其它软件取文本快捷键
            return True, 0

        return False, 0


if __name__ == '__main__':
    import sys

    app = GlobalHotKeyApp(sys.argv)
    app.register()

    QtGui.QApplication.setQuitOnLastWindowClosed(False)

    r = app.exec_()

    sys.exit(r)
