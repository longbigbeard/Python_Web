# FileName : CallFirstMainWIn
# Author   : 大长胡子
# Date : 2018/9/11 
# SoftWare : PyCharm
import sys
from hello import *
from PyQt5.QtWidgets import QApplication, QMainWindow


class MyMainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self,parent = None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = MyMainWindow()
    # ui = hello.Ui_MainWindow()
    # ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())