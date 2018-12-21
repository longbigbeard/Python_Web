# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'hello.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(800, 600)
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_1111 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_1111.setEnabled(True)
        self.pushButton_1111.setGeometry(QtCore.QRect(120, 80, 158, 28))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        self.pushButton_1111.setFont(font)
        self.pushButton_1111.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.pushButton_1111.setObjectName("pushButton_1111")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(140, 150, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(140, 210, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "这里设置窗口标题"))
        MainWindow.setStatusTip(_translate("MainWindow", "状态栏提示信息"))
        self.pushButton_1111.setText(_translate("MainWindow", "确定"))
        self.pushButton.setText(_translate("MainWindow", "取消"))
        self.pushButton_2.setText(_translate("MainWindow", "在取消"))

