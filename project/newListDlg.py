#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
from UI.Ui_newListDlg import Ui_NewListDlg


class NewListDlg(QtGui.QDialog):
    def __init__(self, mw):
        super(NewListDlg, self).__init__(mw,
                                         QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowSystemMenuHint)
        """添加清单"""
        self.ui = Ui_NewListDlg()
        self.ui.setupUi(self)
        self.mw = mw
        self.ui.nameLE.setStyleSheet('font: 14pt "微软雅黑,Lucida Sans Unicode,Arial Unicode MS";color:#4C4C4C;')
        
        self.setWindowIcon(QtGui.QIcon(':/images/icon.png'))

    @QtCore.pyqtSlot()
    def on_okBtn_clicked(self):
        self.mw.addList(self.ui.nameLE.text())
        self.accept()
                               
    @QtCore.pyqtSlot()
    def on_closeBtn_clicked(self):
        self.reject()
