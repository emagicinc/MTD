#!/usr/bin/env python
from PyQt4 import QtCore, QtGui, QtXml
#import zlib
#import struct
#import urllib.request, urllib.parse, urllib.error
#from collections import OrderedDict
#import PixmapCache
import codecs
import os
import re
#from util.commonDlg import *
from util.common import writeCourseList, getItemFile, removeMedia, deleteRecord, moveRecord
#from UI.ui_customDict import Ui_CustomDict
from UI.Ui_chaps import Ui_ChapsDlg
from util import SMMessageBox
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
#scriptSettings = QtCore.QSettings("./script.ini", QtCore.QSettings.IniFormat)
#scriptSettings.setIniCodec(codec)
#        
class ChapsDlg(QtGui.QDialog):
    def __init__(self, mw):
        super(ChapsDlg, self).__init__(mw)
        '''
        课程列表编辑器;
        '''        
        self.ui = Ui_ChapsDlg()        
        self.ui.setupUi(self)
        self.type = "/smeditor/"
        mw.chapIdDict = {}#储存每章节对应的父ID
        self.mw = mw
        self.xmlTree = XmlTree(self, mw) 
  
        self.initialize()

#        print("""列表为:%s""" % str(self.mw.deSelItems))        
#        self.setWindowTitle("课程预览")
        self.setWindowIcon(QtGui.QIcon(':/images/icon.png'))

    @QtCore.pyqtSlot(bool)
    def on_linkageCB_toggled(self):
        '''
         勾选以启用联动选择,对父章节的操作将直接影响子章节.
         '''
        if self.ui.linkageCB.isChecked():
            settings1.setValue(self.type + "linkage", "1")
        else:
            settings1.setValue(self.type + "linkage", "0")

    @QtCore.pyqtSlot(bool)
    def on_byNameRB_toggled(self):
        '''
        勾选以启用按名称过滤.
         '''
        if self.ui.byNameRB.isChecked():
            settings1.setValue(self.type + "filterMode", "1")
            
    @QtCore.pyqtSlot(bool)
    def on_byIDRB_toggled(self):
        '''
        勾选以启用按ID过滤.
         '''
        if self.ui.byIDRB.isChecked():
            settings1.setValue(self.type + "filterMode", "2")
            
    @QtCore.pyqtSlot()
    def on_deSelBtn_clicked(self):
        '''去选按钮'''
        if not self.ui.chapTree.selectedItems():
            self.ui.chapTree.selectAll()
        items = self.ui.chapTree.selectedItems()     
        for item in items:
            item.setCheckState(0, QtCore.Qt.Unchecked)
        
    @QtCore.pyqtSlot()
    def on_selHLBtn_clicked(self):
        '''选中按钮'''
#        self.mw.chapElemDict[id(item)] = element 
        for item in self.ui.chapTree.selectedItems():
            item.setCheckState(0, QtCore.Qt.Checked)
#            if id(item) in self.mw.deSelItems:
#                self.mw.deSelItems.remove(id(item))#ID从列表中移除
#        print(self.mw.deSelItems)
 
    @QtCore.pyqtSlot()
    def on_selInvBtn_clicked(self):
        '''反选按钮'''
#        self.mw.chapElemDict[id(item)] = element 
        self.mw.deSelItems = []#重置
        selected = self.ui.chapTree.selectedItems()
        self.ui.chapTree.selectAll()
        allItems = self.ui.chapTree.selectedItems()
        for item in allItems:
            item.setCheckState(0, QtCore.Qt.Checked)
        for item in selected:
            item.setCheckState(0, QtCore.Qt.Unchecked)
#            self.mw.deSelItems.append(id(item))#ID添加到列表中

    @QtCore.pyqtSlot()
    def on_selAllBtn_clicked(self):
        '''全选按钮'''
#        self.mw.chapElemDict[id(item)] = element 
#        print('all')
#        self.mw.deSelItems = []#列表归零
#        selected = self.ui.chapTree.selectedItems()
        self.ui.chapTree.selectAll()
        allItems = self.ui.chapTree.selectedItems()
        for item in allItems:
            item.setCheckState(0, QtCore.Qt.Checked)

    def invert_dict(self, chapDict):
        '''将传来的章节字典反转'''
        childDict = {}
        parentList = [v for k, v in chapDict.items()]
        parentList = list(set(parentList))
        for parent in parentList:
            childList = []
            for k, v in chapDict.items():
                if v == parent:
                    childList.append(k)
            childDict[parent] = childList
        return childDict
                
#    def checkDeSelItmBAK(self):
#        '''在按确定键前,统计被排除掉的章节列表,以及它们的pos列表'''
#        self.mw.deSelItems = []#先重置
#        self.mw.posList = []#先重置
#        for i in range(self.ui.chapTree.topLevelItemCount()):
#            item = self.ui.chapTree.topLevelItem(i)
#            self.checkItemState(item)
#            self.parseItem(item)
#        self.mw.childDict = self.invert_dict(self.mw.chapDict)#生成childDict
#        self.verifyChapDict()#根据deSelItems校验chapDict

    def checkDeSelItm(self):
        '''在按确定键前,统计被排除掉的章节列表,以及它们的pos列表'''
        '''启动前总检查,更新重要变量'''#注意,在本程序中,将使用checkSelItm
        self.mw.chapDict = {}#用来储存新的章节关系
        self.mw.deSelItems = []#先重置
        self.mw.posList = []#先重置
        self.mw.chapOrder = []#先重置
        for i in range(self.ui.chapTree.topLevelItemCount()):
            item = self.ui.chapTree.topLevelItem(i)
            self.mw.chapDict[id(item)] = 0#将0(根)作为值
            self.mw.chapOrder.append(id(item))#存入列表,以便输入时参照此顺序
            self.checkItemState(item)
            self.parseItem(item)
#        print(self.mw.chapDict)
        self.mw.childDict = self.invert_dict(self.mw.chapDict)#生成childDict
        self.verifyChapDict()#根据deSelItems校验chapDict
#        print(self.mw.chapOrder)

    def checkSelItm(self):
        '''在按确定键前,统计被排除掉的章节列表,以及它们的pos列表'''
        '''启动前总检查,更新重要变量'''
        self.mw.chapDict = {}#用来储存新的章节关系
        self.mw.selItems = []#先重置
        self.mw.posList = []#先重置
        self.mw.chapOrder = []#先重置
        for i in range(self.ui.chapTree.topLevelItemCount()):
            item = self.ui.chapTree.topLevelItem(i)
            self.mw.chapDict[id(item)] = 0#将0(根)作为值
            self.mw.chapOrder.append(id(item))#存入列表,以便输入时参照此顺序
            self.checkItemState(item)
            self.parseItem(item)
#        print(self.mw.chapDict)
        self.mw.childDict = self.invert_dict(self.mw.chapDict)#生成childDict
        self.verifyChapDict()#根据deSelItems校验chapDict
        
    def parseItem(self, item):
        '''将item层层剥皮,直到没有子Item'''
        if item.childCount() > 0:
            for i in range(item.childCount()):
                child = item.child(i)
                self.mw.chapDict[id(child)] = id(item)#将父item的id作为值
                self.mw.chapOrder.append(id(child))#存入列表,以便输入时参照此顺序
                self.checkItemState(child)
                if child.childCount() > 0:#如果大于0,就再执行本程序
                    self.parseItem(child)
                    
    def verifyChapDict(self):
        '''校验ChapDict,确认父章节ID'''
#        print(self.mw.deSelItems)
#        print(self.mw.childDict)
        for item in self.mw.selItems:
            prarentId = self.mw.chapDict.get(id(item))#取父ID
            self.checkParentId(prarentId, id(item))
#        print(self.mw.chapDict)
    
    def checkParentId(self, prarentId, id):
        if prarentId not in self.mw.selItems:
            childList = self.mw.childDict.get(id)#取id的子集
            if childList:
                for childId in childList:
                     self.mw.chapDict[childId] = prarentId#更新章节字典中的父ID
        else:#父ID也被排除,则尝试取上一层
            self.checkParentId(self.mw.chapDict.get(prarentId), id)

    def checkItemState(self, item):
        '''根据STATE的条件来决定取舍,值为0或2'''
        if item.checkState(0) == 2:
            self.mw.selItems.append(item)#被选中的列表,用于对选中页面进行删除或移动操作
            self.mw.posList.append(item.text(2))#将章节ID存入posList,在重载时将把相应的checkbox选中
        
    @QtCore.pyqtSlot()
    def on_moveBtn_clicked(self):
        '''移动页面到指定章节'''
        #清理
        self.checkSelItm()
        if len(self.mw.selItems) > 0:
            targetItem = self.ui.targetTree.selectedItems()
            parentId = '0'#未在右侧章节树中选择,则移到根章节下
            #移动页面
            if targetItem:
                if len(targetItem) > 0:
                    #确定目标章节ID
                    parentId = targetItem[0].text(1)
                
            for item in self.mw.selItems:
                name = item.text(1)
                id, type = item.data(1, 32)
                #修改课程列表文件
                writeCourseList(self, id, name, type, "move", item, parentId)
        #更新数据库
        moveRecord(self.mw.selItems, parentId)               
        #根据新course.xml重载当前树
        self.reloadChapTree()

    @QtCore.pyqtSlot()
    def on_removeBtn_clicked(self):
        '''删除选中页面:从课程列表中清除;更新数据库;删除Item文件;删除媒体文件;更新当前树,关闭本窗口后重载主窗口树'''
        self.checkSelItm()
        for item in self.mw.selItems:
            name = item.text(1)
            id, type = item.data(1, 32)
            #更新当前树
            parent = item.parent()
            if parent:#有父节点
                index = parent.indexOfChild(item)
                parent.takeChild(index)
            else:
                index = self.ui.chapTree.indexOfTopLevelItem(item)
                self.ui.chapTree.takeTopLevelItem(index)

            #移除媒体文件
            try:
                removeMedia(id)
            except:
                pass
            #修改课程列表文件
#            print(id, name, type, "remove", item)
#            print(item.parent())
            writeCourseList(self.mw, id, name, type, "remove", item)
            #删除Item文件
            itemFile = getItemFile(id)
            if os.path.isfile(itemFile): 
                os.remove(itemFile)
        #移除数据库指定行
        #貌似还未更新主窗口课程列表？
        deleteRecord(self.mw.selItems)            
                        
    @QtCore.pyqtSlot()
    def on_closeBtn_clicked(self):
        '''点取消键,开始统计选中的页面章节列表'''
        self.checkSelItm()
        self.mw.initChapTree()#初始化主窗口章节树
        self.close()
        
#        print("""列表为:%s""" % str(self.mw.deSelItems))
#        print("""章节ID列表为:%s""" % str(self.mw.posList))
        
    def closeEvent(self, event):
        '''响应关闭事件,统计选中的页面列表'''
        self.checkSelItm()
        self.mw.initChapTree()#初始化主窗口章节树
    
    def reloadChapTree(self):
        '''重新载入章节树'''
        coursePath = settings.value("/course/coursePath")
        self.mw.courseXML = """%s/override/course.xml""" % coursePath  
        try:
            self.mw.courseXML = courseListFile.replace("//", "/")
        except:
            pass
        #mw.courseXML在initialize中初始化
        if self.xmlTree.read(self.mw.courseXML):
            self.mw.statusBar().showMessage("课程列表重载成功", 2000)        
        
    @QtCore.pyqtSlot()        
    def on_filterLE_editingFinished(self):
        '''过滤:重新读xml'''
#        if self.ui.filterLE.text() != "":
        self.reloadChapTree()

        
    def initialize(self):
        """
        初始化;
        """
        '''131115新增'''
        self.ui.chapTree.setColumnWidth(0, 81)
        self.ui.chapTree.setColumnWidth(1, 121)
        self.ui.chapTree.setColumnWidth(2, 48)
        self.ui.targetTree.setColumnWidth(0, 111)
        self.ui.targetTree.setColumnWidth(1, 48)
        #启用联动选择
        if settings.value(self.type + "linkage") == "1":
            self.ui.linkageCB.setChecked(True)
        else:
            self.ui.linkageCB.setChecked(False)
        if settings.value(self.type + "filterMode") == "1":
            self.ui.byNameRB.setChecked(True)
        else:
            self.ui.byIDRB.setChecked(True)    
        self.reloadChapTree()#载入章节树
        #恢复勾选状态,此方法仅针对顶层
        count = self.ui.chapTree.topLevelItemCount()
        for i in range(count):
            if i in self.mw.posList:                
                item = self.ui.chapTree.topLevelItem(i)
                item.setCheckState(0, QtCore.Qt.Unchecked)             

class XmlTree(object):
    def __init__(self, parent, mw):
        '''利用传入的string,生成章节树'''

        self.domDocument = QtXml.QDomDocument()
        mw.chapElemDict = {}#储存章节列表
        mw.allItems = {}#储存每章节下面的excercise列表
        mw.chapDict = {}#储存每章节对应的父ID
        mw.childDict = {}#以父章节为key,子章节列表为value的字典,主要用于校验chapDict
        self.pr = parent
        self.tree = self.pr.ui.chapTree
        self.targetTree = self.pr.ui.targetTree
        self.mw = mw
        
    def read(self, courseXML):
        '''核心程序,此程序解析xml,并将其写入到章节树中'''
        self.filter = self.pr.ui.filterLE.text()
        xml_file = QtCore.QFile(courseXML)
        ok, errorStr, errorLine, errorColumn = \
                self.domDocument.setContent(xml_file, False)#这里是True的话,就会多出xmlns命名空间的定义
       
        root = self.domDocument.documentElement()
        self.tree.clear()
        self.targetTree.clear()##
        # It might not be connected.这个是否可以去除
        try:
            self.tree.itemChanged.disconnect(self.updateDomElement)
        except:
            pass
        child = root.firstChildElement('element')#遍历第一层章节
        while not child.isNull():
            self.parseFolderElement(child)#遍历各层子章节,未往里传parentItem表示这是第一层
            self.parseFolderElement(child, None, True)#设置targetTree
            child = child.nextSiblingElement('element')
        self.tree.itemChanged.connect(self.updateDomElement)
        return True
        
    def write(self, device):
        indentSize = 4
        out = QtCore.QTextStream(device)
        self.domDocument.save(out, indentSize)
        return True

    def updateDomElement(self, item, column):
        '''此处可修改章节名称,暂不考虑支持章节排序'''
        element = self.mw.chapElemDict.get(id(item))
#        print(id(item))
#        print(column)
        if not element.isNull():
            if column == 1:#第2栏
#                oldTitleElement = element.firstChildElement('element')
#                newTitleElement = self.domDocument.createElement('element')
#                print(item.text(1))
#                newTitleText = self.domDocument.createTextNode(item.text(1))#应该修改第2栏
#                newTitleElement.appendChild(newTitleText)
#                element.replaceChild(newTitleElement, oldTitleElement)
                element.setAttribute("name", item.text(1))
                self.mw.chapElemDict[id(item)] = element
#                print(element.attribute('id'))
#                print(self.mw.chapElemDict[id(item)].attribute('name'))
            elif column == 0:
                if self.pr.ui.linkageCB.isChecked():
                    self.linkage(item, item.checkState(0))
                    
    def linkage(self, item, checkState):
        '''联动选择'''
        for i in range(item.childCount()):
            child = item.child(i)
            child.setCheckState(0, checkState)
#            item.setCheckState(0, QtCore.Qt.Checked)
#            self.mw.chapDict[id(child)] = id(item)#将父item的id作为值
#            self.checkItemState(child)
            if child.childCount() > 0:#如果大于0,就再执行本程序
                self.linkage(child, checkState)        
#            else:
#                if element.tagName() == 'element':
#                    element.setAttribute('type', item.text(1))

    def setItem(self, elem, parent, id, type, name, TARGET=None):
        '''设置item,用于parseFolderElement'''
        item = self.createItem(elem, parent, TARGET)
        
        if parent is not None:#有父章节
#            print(id, parent.text(2))
            self.mw.chapIdDict[id] = parent.text(2)#IteMID存入此中
        else:#顶层章节
            self.mw.chapIdDict[id] = 0#ITEMID为0
                
        item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
        start = 0
        if not TARGET:
            start = 1
            if id in self.mw.posList:#posList用于检测重载时是否勾选Item
                item.setCheckState(start - 1, QtCore.Qt.Checked)
            else:
                item.setCheckState(start - 1, QtCore.Qt.Unchecked)
        item.setText(start, name)
        item.setData(start, 32, [id, type])
        item.setText(start + 1, id)
        #决定是否展开
        folded = (type == 'pres')#如果属性是章节
#        self.tree.setItemExpanded(item, not folded)#折叠
        self.tree.setItemExpanded(item, folded)#打开
        if type == "pres":
            item.setIcon(0, self.mw.folderIcon)
        else:
            item.setIcon(0, self.mw.bookmarkIcon)
        return item
        
    def parseFolderElement(self, element, parentItem=None, TARGET=None):
        '''遍历各层子章节'''
        '''TARGET表示是操作targetTree,在createItem中控制'''
        byName = self.pr.ui.byNameRB.isChecked()
        byID = self.pr.ui.byIDRB.isChecked()
        chapId = element.attribute('id')
        type = element.attribute('type')
        name = element.attribute('name')
        item = parentItem
        if type == "pres" or not TARGET:
            if type != "exercise":
                item = self.setItem(element, parentItem, chapId, type, name, TARGET)
            else:
                if len(self.filter) == 0:
                    item = self.setItem(element, parentItem, chapId, type, name)
                else:
                    if byName:
                        if re.search(self.filter, name):
                            item = self.setItem(element, parentItem, chapId, type, name)
                    elif byID:
                        if re.search(self.filter, chapId):
                            item = self.setItem(element, parentItem, chapId, type, name)            
        ids = []#储存当前章节下的练习id
        child = element.firstChildElement()
        while not child.isNull():
            if child.attribute('type') == 'pres':#如果碰到各级章节,就继续往下挖
                self.parseFolderElement(child, item, TARGET)
            elif child.attribute('type') == 'exercise':#如果碰到练习,将练习ID列表放到allItems,用于写入数据库时参照
                itemId = child.attribute('id')
                name = child.attribute('name')
                type = child.attribute('type')            
                if not TARGET:#表示写左侧
                    if len(self.filter) == 0:
                        itm = self.setItem(child, item, itemId, type, name, TARGET)
                    else:
                        if byName:
                            if re.search(self.filter, name):
                                itm = self.setItem(child, item, itemId, type, name, TARGET)
                        elif byID:
                            if re.search(self.filter, itemId):
                                itm = self.setItem(child, item, itemId, type, name, TARGET)
                ids.append((itemId, name, 0))
            child = child.nextSiblingElement()#循环,深挖这一层
        if not item:
            self.mw.allItems[0] = ids
        else:
            self.mw.allItems[id(item)] = ids#将这一轮得到的练习ID存入allItems        

    def createItem(self, element, parentItem=None, TARGET=None):
        item = QtGui.QTreeWidgetItem()
        if parentItem is not None:#有父章节
            item = QtGui.QTreeWidgetItem(parentItem)
            self.mw.chapDict[id(item)] = id(parentItem)#注意，这里的id不是页面ID
        else:#顶层章节
            if TARGET:
                item = QtGui.QTreeWidgetItem(self.targetTree)
            else:
                item = QtGui.QTreeWidgetItem(self.tree)
            self.mw.chapDict[id(item)] = 0#ITEMID为0
        self.mw.chapElemDict[id(item)] = element#记录下这个element
        return item
    
