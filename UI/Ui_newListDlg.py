# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'newListDlg.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_NewListDlg(object):
    def setupUi(self, NewListDlg):
        NewListDlg.setObjectName(_fromUtf8("NewListDlg"))
        NewListDlg.resize(316, 136)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        NewListDlg.setWindowIcon(icon)
        NewListDlg.setSizeGripEnabled(True)
        self.verticalLayout = QtGui.QVBoxLayout(NewListDlg)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.topWidget = QtGui.QWidget(NewListDlg)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.topWidget.sizePolicy().hasHeightForWidth())
        self.topWidget.setSizePolicy(sizePolicy)
        self.topWidget.setMinimumSize(QtCore.QSize(298, 41))
        self.topWidget.setMaximumSize(QtCore.QSize(16777215, 41))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(17, 98, 160))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(17, 98, 160))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(17, 98, 160))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(17, 98, 160))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(17, 98, 160))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(17, 98, 160))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(17, 98, 160))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(17, 98, 160))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(17, 98, 160))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.topWidget.setPalette(palette)
        self.topWidget.setStyleSheet(_fromUtf8("background:rgb(17, 98, 160);"))
        self.topWidget.setObjectName(_fromUtf8("topWidget"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.topWidget)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(self.topWidget)
        self.label_2.setStyleSheet(_fromUtf8("font: 12pt \"微软雅黑\";color:#fefefe;padding-left:5px;"))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.verticalLayout.addWidget(self.topWidget)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 6, -1, 6)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(9, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label = QtGui.QLabel(NewListDlg)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.nameLE = QtGui.QLineEdit(NewListDlg)
        self.nameLE.setMinimumSize(QtCore.QSize(0, 41))
        self.nameLE.setMaximumSize(QtCore.QSize(16777215, 41))
        self.nameLE.setObjectName(_fromUtf8("nameLE"))
        self.horizontalLayout.addWidget(self.nameLE)
        spacerItem1 = QtGui.QSpacerItem(9, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.okBtn = QtGui.QPushButton(NewListDlg)
        self.okBtn.setMinimumSize(QtCore.QSize(81, 29))
        self.okBtn.setMaximumSize(QtCore.QSize(81, 29))
        self.okBtn.setFocusPolicy(QtCore.Qt.StrongFocus)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/db.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.okBtn.setIcon(icon1)
        self.okBtn.setObjectName(_fromUtf8("okBtn"))
        self.horizontalLayout_3.addWidget(self.okBtn)
        self.closeBtn = QtGui.QPushButton(NewListDlg)
        self.closeBtn.setMinimumSize(QtCore.QSize(81, 29))
        self.closeBtn.setMaximumSize(QtCore.QSize(81, 29))
        self.closeBtn.setFocusPolicy(QtCore.Qt.NoFocus)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/exit.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.closeBtn.setIcon(icon2)
        self.closeBtn.setObjectName(_fromUtf8("closeBtn"))
        self.horizontalLayout_3.addWidget(self.closeBtn)
        spacerItem3 = QtGui.QSpacerItem(9, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        spacerItem4 = QtGui.QSpacerItem(20, 9, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem4)

        self.retranslateUi(NewListDlg)
        QtCore.QMetaObject.connectSlotsByName(NewListDlg)
        NewListDlg.setTabOrder(self.nameLE, self.closeBtn)

    def retranslateUi(self, NewListDlg):
        NewListDlg.setWindowTitle(_translate("NewListDlg", "添加清单", None))
        self.label_2.setText(_translate("NewListDlg", "添加清单", None))
        self.label.setText(_translate("NewListDlg", "清单名称  ", None))
        self.okBtn.setText(_translate("NewListDlg", "确认", None))
        self.closeBtn.setText(_translate("NewListDlg", "取消", None))

import image_rc
