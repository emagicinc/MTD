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
        NewListDlg.resize(317, 140)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        NewListDlg.setWindowIcon(icon)
        NewListDlg.setSizeGripEnabled(True)
        self.groupBox = QtGui.QGroupBox(NewListDlg)
        self.groupBox.setGeometry(QtCore.QRect(10, 20, 291, 61))
        self.groupBox.setTitle(_fromUtf8(""))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.nameLE = QtGui.QLineEdit(self.groupBox)
        self.nameLE.setObjectName(_fromUtf8("nameLE"))
        self.horizontalLayout.addWidget(self.nameLE)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.okBtn = QtGui.QPushButton(NewListDlg)
        self.okBtn.setGeometry(QtCore.QRect(130, 90, 81, 24))
        self.okBtn.setMinimumSize(QtCore.QSize(81, 24))
        self.okBtn.setMaximumSize(QtCore.QSize(81, 24))
        self.okBtn.setFocusPolicy(QtCore.Qt.StrongFocus)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/db.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.okBtn.setIcon(icon1)
        self.okBtn.setObjectName(_fromUtf8("okBtn"))
        self.closeBtn = QtGui.QPushButton(NewListDlg)
        self.closeBtn.setGeometry(QtCore.QRect(220, 90, 81, 24))
        self.closeBtn.setMinimumSize(QtCore.QSize(81, 24))
        self.closeBtn.setMaximumSize(QtCore.QSize(81, 24))
        self.closeBtn.setFocusPolicy(QtCore.Qt.NoFocus)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/exit.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.closeBtn.setIcon(icon2)
        self.closeBtn.setObjectName(_fromUtf8("closeBtn"))

        self.retranslateUi(NewListDlg)
        QtCore.QMetaObject.connectSlotsByName(NewListDlg)
        NewListDlg.setTabOrder(self.nameLE, self.closeBtn)

    def retranslateUi(self, NewListDlg):
        NewListDlg.setWindowTitle(_translate("NewListDlg", "添加清单", None))
        self.label.setText(_translate("NewListDlg", "清单名称  ", None))
        self.okBtn.setText(_translate("NewListDlg", "确认", None))
        self.closeBtn.setText(_translate("NewListDlg", "取消", None))

import image_rc
