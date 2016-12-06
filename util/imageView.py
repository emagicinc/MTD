#!/usr/bin/env python
from PyQt4 import QtGui, QtCore
#import PixmapCache
#from .SMApplication import smApp
#from .common import Common

class ImageView(QtGui.QDialog):
    def __init__(self, mw, fileName, parent=None):
        """图片预览"""
        super(ImageView, self).__init__(parent)
           
        self.fileName = fileName
#        self.common = Common()
        type = ""
#        self.index = 0
#        if object:
#            self.object = object
#            type = object.objectName()
#        self.common = smApp().getObject("common")
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        
#        self.imageFolder = "./template"
#        self.imageList = self.common.getFileList("00.*?_0720.png", self.imageFolder)
#        imageName = self.common.strippedName(self.fileName)
#        if type == "tmpImgSpin":
#            self.curNum = int(imageName[2:5])
#            self.index = self.imageList.index(imageName)

        self.imageLbl = QtGui.QLabel(self)
        self.imageLbl.setPixmap(QtGui.QPixmap(self.fileName))
        self.imageLbl.setAlignment(QtCore.Qt.AlignCenter)
        
#        self.imageTextLbl = QtGui.QLabel("图片编号")
#        self.imageTextLbl.setMinimumSize(QtCore.QSize(68, 24))
#        self.imageTextLbl.setMaximumSize(QtCore.QSize(68, 24))
        
#        self.previousBtn = self.common.createBtn("", "full", 24, 24, "previousBtn", sizePolicy, "previous.png", 24, 24, True, "上一张")
#        self.firstBtn = self.common.createBtn("", "full", 24, 24, "firstBtn", sizePolicy, "first.png", 24, 24, True, "第一张")
#        self.lastBtn = self.common.createBtn("", "full", 24, 24, "lastBtn", sizePolicy, "last.png", 24, 24, True, "最后一张")
#        self.nextBtn = self.common.createBtn("", "full", 24, 24, "nextBtn", sizePolicy, "next.png", 24, 24, True, "下一张")
#        self.selectBtn = self.common.createBtn("", "full", 24, 24, "selectBtn", sizePolicy, "select.png", 24, 24, True, "点击此按钮,设置当前图片为背景图.")
#        self.previousBtn = self.common.createBtn("", "full", 24, 24, "previousBtn", sizePolicy, "previous.png", 24, 24, True, "上一张")
#        self.imageNumCombo = self.common.createCombo("full", 24, 68, "imageNumCombo", sizePolicy, True)
#        pattern =QtCore.QRegExp("[\d]+")
#        self.imageNumCombo.setValidator(QtGui.QRegExpValidator(pattern, self.imageNumCombo))#限制输入数字
        
#        for fileName in self.imageList:
#            self.imageNumCombo.addItem(str(int(fileName[2:5])), fileName)
#        try:
#            self.imageNumCombo.setCurrentIndex(self.imageNumCombo.findText(str(int(imageName[2:5]))))
#        except:
#            pass

#        if self.index <= 0:
#            self.previousBtn.setDisabled(True)
#            self.firstBtn.setDisabled(True)            
#        elif self.index == len(self.imageList) - 1:
#            self.nextBtn.setDisabled(True)
#            self.lastBtn.setDisabled(True)
    
        #信号槽
#        self.firstBtn.clicked.connect(self.imageNav)
#        self.previousBtn.clicked.connect(self.imageNav)
#        self.nextBtn.clicked.connect(self.imageNav)
#        self.lastBtn.clicked.connect(self.imageNav)
#        self.selectBtn.clicked.connect(self.setImageNum)
#        self.imageNumCombo.currentIndexChanged.connect(self.imageNav)
#        self.imageNumCombo.editTextChanged.connect(self.verifyNum)
        
        #快捷键
#        self.previousAct = QtGui.QAction(self.trUtf8("Find previous"),
#                self, shortcut="PgUp",
#                statusTip=self.trUtf8("find previous"), triggered=self.imageNav)
#        self.previousAct.setObjectName("previousBtn")
#        self.previousBtn.addAction(self.previousAct)
#        
#        self.nextAct = QtGui.QAction(self.trUtf8("Find next"),
#                self, shortcut="PgDown",
#                statusTip=self.trUtf8("find next"), triggered=self.imageNav)
#        self.nextAct.setObjectName("nextBtn")
#        self.nextBtn.addAction(self.nextAct)
#        
#        self.firstAct = QtGui.QAction(self.trUtf8("Find first"),
#                self, shortcut="Home",
#                statusTip=self.trUtf8("find first"), triggered=self.imageNav)
#        self.firstAct.setObjectName("firstBtn")
#        self.firstBtn.addAction(self.firstAct)
#
#        self.lastAct = QtGui.QAction(self.trUtf8("Find last"),
#                self, shortcut="End",
#                statusTip=self.trUtf8("find last"), triggered=self.imageNav)
#        self.lastAct.setObjectName("lastBtn")
#        self.lastBtn.addAction(self.lastAct)
        
#        buttonLayout = QtGui.QHBoxLayout()
#        buttonLayout.addWidget(self.firstBtn)        
#        buttonLayout.addWidget(self.previousBtn)
#        buttonLayout.addWidget(self.nextBtn)
#        buttonLayout.addWidget(self.lastBtn)
#        buttonLayout.addWidget(self.imageTextLbl)  
#        buttonLayout.addWidget(self.imageNumCombo)        
#        buttonLayout.addWidget(self.selectBtn)
#        buttonLayout.addStretch()
       
#        buttonLayout.addWidget(self.imageNumLbl)
        
        mainLayout = QtGui.QVBoxLayout()
#        if type == "tmpImgSpin":
#            mainLayout.addLayout(buttonLayout)
        mainLayout.addWidget(self.imageLbl)

        mainLayout.addStretch()
        self.setLayout(mainLayout)

        QtCore.QMetaObject.connectSlotsByName(self)
        
        self.setWindowTitle("图片预览")
        self.setWindowIcon(QtGui.QIcon(':/images/icon.png'))
        self.setBackgroundRole(QtGui.QPalette.Base)
        self.setAutoFillBackground(True)
        ###可允许切回主窗口###
#        super().show()
#        self.activateWindow()

#    @QtCore.pyqtSlot(int)
#    def on_imageNumCombo_currentIndexChanged(self):
#        """
#        行号或页面ID输入;
#        """
#        print("on_imageNumCombo_currentIndexChanged")
#        index = self.ui.itemIdCombo.itemData(self.ui.itemIdCombo.currentIndex())
#        if self.type == "txt":
#            if self.ui.itemIdCombo.currentIndex() >= 0:
#                self.viewSourceTxt(index)
#        elif self.type == "xml":
#            self.viewXml(str(index))
            
#    def convertNum(self, imageList):
#        imageNumList = []
#        for fileName in imageList:
#            imageNumList.append(str(int(fileName[2:5])))
#        return imageNumList
#
#    def verifyNum(self):
#        num = self.imageNumCombo.currentText()
#        try:
#            self.imageNumCombo.setCurrentIndex(self.imageNumCombo.findText(num))
#        except:
#            pass
#        
#    def setImageNum(self):
#        self.object.setValue(self.curNum)##这个地方要传spin进来!
#        self.close()
#
#    def imageNav(self):
#        index = 0
#        type = self.sender().objectName()
#        if type == "imageNumCombo":
#            fileName = self.imageNumCombo.itemData(self.imageNumCombo.currentIndex())
#        else:
#            fileName = self.common.strippedName(self.fileName)
#        if fileName in self.imageList:#这个地方要加一个判断,防止文件不在列表内(可能性小)
#            if type == "previousBtn":
#                index = self.imageList.index(fileName) - 1
#            elif type == "nextBtn":
#                index = self.imageList.index(fileName) + 1
#            elif type == "firstBtn":
#                index = 0
#            elif type == "lastBtn":
#                index = len(self.imageList) - 1
#            elif type == "imageNumCombo":
#                index = self.imageList.index(fileName)
#            if index >= 0 and index < len(self.imageList):
#                curImage = self.imageList[index]
#                imageFile = './template/' + curImage
#                self.curNum = int(curImage[2:5])
#                self.imageLbl.setPixmap(QtGui.QPixmap(imageFile))
#                self.imageNumCombo.setCurrentIndex(self.imageNumCombo.findText(str(self.curNum)))
#                self.fileName = imageFile
#                if type in ("nextBtn", "lastBtn", "imageNumCombo"):
#                    if index == len(self.imageList) - 1:
#                        self.nextBtn.setDisabled(True)
#                        self.lastBtn.setDisabled(True)
#                    else:
#                        self.nextBtn.setEnabled(True)
#                        self.lastBtn.setEnabled(True)
#                    self.previousBtn.setEnabled(True)
#                    self.firstBtn.setEnabled(True)
#                elif type in ("previousBtn", "firstBtn", "imageNumCombo"):
#                    if index <= 0:
#                        self.previousBtn.setDisabled(True)
#                        self.firstBtn.setDisabled(True)
#                    else:
#                        self.previousBtn.setEnabled(True)
#                        self.firstBtn.setEnabled(True)
#                    self.nextBtn.setEnabled(True)
#                    self.lastBtn.setEnabled(True)
