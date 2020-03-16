import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from UI import mainwindow


class MyForm(QMainWindow, mainwindow.Ui_Dialog):
    def __init__(self, parent=None):
        super(MyForm, self).__init__(parent)
        self.setupUi(self)
        self.path = ''
        # 註冊
        self.chooseButtonRP.clicked.connect(self.choosePath)
        self.chooseButtonRN.clicked.connect(self.choosePath)
        self.okButtonRP.clicked.connect(self.RenameRP)
        self.okButtonRN.clicked.connect(self.RenameRN)

    def choosePath(self):

        options = QFileDialog.Options()
        path = QFileDialog.getExistingDirectory(self, "選擇資料夾", options=options)
        if path is '':
            pass
        else:
            if self.tabWidget.currentIndex() is 0:
                self.lineEditPathRP.setText(path)
                self.findDirAllData(path, self.browserRP)
            elif self.tabWidget.currentIndex() is 1:
                self.lineEditPathRN.setText(path)
                self.findDirAllData(path, self.browserRN)

    def findDirAllData(self, path, browserName):
        browserName.clear()
        for i in os.listdir(path):
            browserName.append(i)

    def RenameRP(self):
        if self.lineEditOldRP.text() is '' or self.lineEditNewRP.text() is '':
            QMessageBox.information(self, "Error", "輸入框請勿空白!!")
        else:
            for index, name in enumerate(os.listdir(self.lineEditPathRP.text())):
                subTitle = os.path.splitext(name)[-1]
                currentName = os.path.splitext(name)[0]
                os.rename(os.path.join(self.lineEditPathRP.text(), name),
                          os.path.join(self.lineEditPathRP.text(), currentName.replace(self.lineEditOldRP.text(), self.lineEditNewRP.text()) + subTitle))
        self.findDirAllData(self.lineEditPathRP.text(), self.browserRP)

    def RenameRN(self):
        if self.lineEditNewRN.text() is '':
            QMessageBox.information(self, "Error", "輸入框請勿空白!!")
        else:
            for index, name in enumerate(os.listdir(self.lineEditPathRN.text())):
                subTitle = os.path.splitext(name)[-1]
                os.rename(os.path.join(self.lineEditPathRN.text(), name),
                          os.path.join(self.lineEditPathRN.text(), (self.lineEditNewRN.text() + ('%04d'%index) + subTitle)))
        self.findDirAllData(self.lineEditPathRN.text(), self.browserRN)

if __name__ == "__main__":
    import time
    start_time = time.time()
    app = QApplication(sys.argv)
    app.setDoubleClickInterval(200)
    MainWindow = MyForm()
    MainWindow.show()
    print("開啟時間:{}".format(str((time.time() - start_time))))
    try:
        sys.exit(app.exec_())
    except SystemExit as e:
        if e.code != 0:
            MainWindow.logger.exception('Unexpected System Exit')