# FileName : main.py
# Author   : Adil
# DateTime : 2018/2/1 12:00
# SoftWare : PyCharm

import sys
import hello
from PyQt5.QtWidgets import QApplication, QMainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = hello.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())