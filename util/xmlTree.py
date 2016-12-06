#!/usr/bin/env python

from PyQt4 import QtXml, QtCore, QtGui
import re

class XmlTree(object):
    def __init__(self, mw):
        '''利用传入的string,生成章节树'''

        self.domDocument = QtXml.QDomDocument()
        mw.chapElemDict = {}#储存章节列表
        mw.allItems = {}#储存每章节下面的excercise列表
        mw.chapDict = {}#储存每章节对应的父ID
        mw.childDict = {}#以父章节为key,子章节列表为value的字典,主要用于校验chapDict
        self.mw = mw
        self.tree = mw.ui.chapTree
#        self.filter = mw.ui.filterLE.text()

    def read(self, courseXML):
        '''核心程序,此程序解析xml,并将其写入到章节树中'''
        xml_file = QtCore.QFile(courseXML)
        ok, errorStr, errorLine, errorColumn = \
                self.domDocument.setContent(xml_file, False)#这里是True的话,就会多出xmlns命名空间的定义

        root = self.domDocument.documentElement()
        self.tree.clear()
        # It might not be connected.这个是否可以去除
        try:
            self.tree.itemChanged.disconnect(self.updateDomElement)
        except:
            pass
        child = root.firstChildElement('element')#遍历第一层章节
        while not child.isNull():
            self.parseFolderElement(child)#遍历各层子章节,未往里传parentItem表示这是第一层
            child = child.nextSiblingElement('element')
        self.tree.itemChanged.connect(self.updateDomElement)
        return True
    
    def parse(self, result):
        '''result为数据库结果集'''
        '''Number, Name, Type, ParentId'''
        self.tree.clear()
        try:
            self.tree.itemChanged.disconnect(self.updateDomElement)
        except:
            pass
#        parentItem = None
#        ids = []
        for rec in result:
            id, name, type, parentId = rec
#            print(id, name, type, parentId)
            '''转换type'''
            type = str(type)
            id = str(id)
            parentId = str(parentId)
            if type == "5":
                type = "pres"
            elif type == "0":
                type = "exercise"        
            '''#临时#暂不考虑过滤'''
            '''这样的处理是基于每个章节顺序非常规整的情况下,如果章节错乱呢?是否应把数据先发过去按parentId整理?'''
            self.setDbItem(parentId, id, type, name)
#            if type == "pres":
#                if parentId == '0':#表示在根节点下
#                    '''储存上一轮的ids'''
#                    if len(ids) > 0:
#                        self.mw.allItems[0] = ids
#                    item = self.setDbItem(None, id, type, name)
#                else:
#                    if len(ids) > 0:
#                        self.mw.allItems[parentId] = ids
#                    item = self.setDbItem(parentItem, id, type, name)
#                parentItem = item
#                '''重置ids'''
#                ids = []
#            else:
#                if parentId == '0':
#                    item = self.setDbItem(None, id, type, name)
#                else:
#                    item = self.setDbItem(parentItem, id, type, name)
#                    ids.append((id, name, 0))
#        '''储存最后一轮数据'''
#        if len(ids) > 0:
#            if parentId == 0:
#                self.mw.allItems[0] = ids
#            else:
#                self.mw.allItems[parentId] = ids
            
        return True
        
    def write(self, device):
        # 写入,可暂时不用
        indentSize = 4
        out = QtCore.QTextStream(device)
        self.domDocument.save(out, indentSize)
        return True

    def updateDomElement(self, item, column):
        '''此处可修改章节名称,暂不考虑支持章节排序'''
        '''此段代码在本程序中暂不启用'''
        element = self.mw.chapElemDict.get(id(item))
        if not element.isNull():
            if column == 1:#第2栏
                element.setAttribute("name", item.text(1))
                self.mw.chapElemDict[id(item)] = element
            elif column == 0:
                if self.mw.ui.linkageCB.isChecked():
                    self.linkage(item, item.checkState(0))
                    
    def linkage(self, item, checkState):
        '''联动选择'''
        for i in range(item.childCount()):
            child = item.child(i)
            child.setCheckState(0, checkState)
            if child.childCount() > 0:#如果大于0,就再执行本程序
                self.linkage(child)        

    def createDbItem(self, parentId=None):
        '''创建数据库item'''
        item = QtGui.QTreeWidgetItem()
        if parentId != "0":#未在顶层
            parentItem = self.mw.chapInfoDict.get(parentId)
            if parentItem:
                item = QtGui.QTreeWidgetItem(parentItem)
        else:#顶层章节
            item = QtGui.QTreeWidgetItem(self.tree)
#            self.mw.chapDict[id(item)] = 0#ITEMID为0
        return item
        
    def setDbItem(self, parentId, id, type, name):
        '''设置数据库item'''
        item = self.createDbItem(parentId)
        item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
        item.setText(0, name)
        item.setData(0, 32, [id, type])
        #决定是否展开
        folded = (type == 'pres')#如果属性是章节
        self.tree.setItemExpanded(item, not folded)#折叠
        if type == "pres":
            item.setIcon(0, self.mw.folderIcon)
            self.mw.chapInfoDict[id] = item
        else:
            item.setIcon(0, self.mw.bookmarkIcon)
#        return item
        
#    def parseDbElement(self, rec, parentItem=None):
#        '''处理数据库记录'''
#        id, name, type, chapId = rec
#        '''转换type'''
#        if type == 5:
#            type == "pres"
#        elif type == 0:
#            type == "exercise"        
#        '''#临时#暂不考虑过滤'''
#        if type == "pres":
#            item = self.setDbItem(parentItem, id, type, name)
#        else:
#            item = self.setDbItem(parentItem, id, type, name)
        
    def parseFolderElement(self, element, parentItem=None):
        '''遍历各层子章节'''
        chapId = element.attribute('id')
        type = element.attribute('type')
        name = element.attribute('name')
        item = parentItem
        #这里的过滤要彻底一些！
        if type == "pres":
            item = self.setItem(element, parentItem, chapId, type, name)
            #161015新增:初始化时定位到上次储存的curChap
            if chapId == self.mw.curChapId:
                self.mw.curChap = item #将此item作为当前item
        else:
#            if len(self.filter) == 0:
            item = self.setItem(element, parentItem, chapId, type, name)
#            else:
#                if re.search(self.filter, name):
#                    item = self.setItem(element, parentItem, chapId, type, name)
        ids = []#储存当前章节下的练习id
        child = element.firstChildElement()
        while not child.isNull():
            if child.attribute('type') == 'pres':#如果碰到各级章节,就继续往下挖
                self.parseFolderElement(child, item)
            elif child.attribute('type') == 'exercise':#如果碰到练习,将练习ID列表放到allItems,用于写入数据库时参照
                itemId = child.attribute('id')
                name = child.attribute('name')
                type = child.attribute('type')            
#                if len(self.filter) == 0:
                itm = self.setItem(child, item, itemId, type, name)
#                else:
#                    if re.search(self.filter, name):
#                        itm = self.setItem(child, item, itemId, type, name)
                ids.append((itemId, name, 0))
            child = child.nextSiblingElement()#循环,深挖这一层
        if not item:
            self.mw.allItems[0] = ids
        else:
            self.mw.allItems[id(item)] = ids#将这一轮得到的练习ID存入allItems        

    def setItem(self, elem, parent, id, type, name):
        '''设置item,用于parseFolderElement'''
        item = self.createItem(elem, parent)
        item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
#        if id in self.mw.posList:#posList用于检测重载时是否勾选Item
#            item.setCheckState(0, QtCore.Qt.Checked)
#        else:
#            item.setCheckState(0, QtCore.Qt.Unchecked)
        item.setText(0, name)
        item.setData(0, 32, [id, type])
        #决定是否展开
        folded = (type == 'pres')#如果属性是章节
        self.tree.setItemExpanded(item, not folded)#折叠
        if type == "pres":
            item.setIcon(0, self.mw.folderIcon)
        else:
            item.setIcon(0, self.mw.bookmarkIcon)
        return item
        
    def createItem(self, element, parentItem=None):
        item = QtGui.QTreeWidgetItem()
        if parentItem is not None:#有父章节
            item = QtGui.QTreeWidgetItem(parentItem)
            self.mw.chapDict[id(item)] = id(parentItem)
        else:#顶层章节
            item = QtGui.QTreeWidgetItem(self.tree)
            self.mw.chapDict[id(item)] = 0#ITEMID为0
        return item
