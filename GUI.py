from PyQt5 import QtCore, QtGui, QtWidgets


class uIMainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Redskull")
        MainWindow.resize(1000, 550)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")


        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 1000, 550))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("resources/deepLearning.gif"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")


        self.label_right = QtWidgets.QLabel(self.centralwidget)
        self.label_right.setGeometry(QtCore.QRect(500, 0, 1000, 550))
        self.label_right.setStyleSheet('background-color:black')
        self.label_right.setScaledContents(True)
        self.label_right.setObjectName("label_right")


        self.run = QtWidgets.QPushButton(self.centralwidget)
        self.run.setGeometry(QtCore.QRect(650, 430, 80, 80))
        self.run.setStyleSheet("background-color: rgb(0, 255, 0);\n"
                                      "font: 50 12pt \"MS Shell Dlg 2\"; border-radius:40px")
        self.run.setObjectName("run")


        self.stop = QtWidgets.QPushButton(self.centralwidget)
        self.stop.setGeometry(QtCore.QRect(770, 430, 80, 80))
        self.stop.setStyleSheet("background-color:rgb(255, 0, 0);\n"
                                        "font: 50 12pt \"MS Shell Dlg 2\";border-radius:40px")
        self.stop.setObjectName("stop")


        self.time = QtWidgets.QTextBrowser(self.centralwidget)
        self.time.setGeometry(QtCore.QRect(550, 30, 150, 50))
        self.time.setStyleSheet("font: 75 14pt \"MS Shell Dlg 2\";\n"
                                       "background-color:transparent;\ncolor:white;"
                                       "border-radius:none;\n"
                                       "")
        self.time.setObjectName("time")


        self.date = QtWidgets.QTextBrowser(self.centralwidget)
        self.date.setGeometry(QtCore.QRect(850, 30, 150, 50))
        self.date.setStyleSheet("font: 75 14pt \"MS Shell Dlg 2\";\n"
                                         "background-color:transparent;\ncolor:white;"
                                         "border-radius:none;")
        self.date.setObjectName("date")


        self.commands = QtWidgets.QTextBrowser(self.centralwidget)
        self.commands.setGeometry(QtCore.QRect(550, 120, 400, 300))
        self.commands.setStyleSheet("font: 11pt \"MS Shell Dlg 2\";\n"
                                         "background-color:transparent;\ncolor:white;padding:50px")
        self.commands.setObjectName("commands")
        # self.commands.setText('AI: as')
        MainWindow.setCentralWidget(self.centralwidget)

        # self.commands.
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 100, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(self, MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Redskull", "Redskull"))
        self.run.setText(_translate("MainWindow", "Run"))
        self.stop.setText(_translate("MainWindow", "Exit"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = uIMainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
