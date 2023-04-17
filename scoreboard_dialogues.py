from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Scoreboard(object):
    def setupUi(self, Scoreboard):
        Scoreboard.setObjectName("Scoreboard")
        Scoreboard.resize(628, 370)
        self.gridLayout = QtWidgets.QGridLayout(Scoreboard)
        self.gridLayout.setObjectName("gridLayout")
        self.tableWidget = QtWidgets.QTableWidget(Scoreboard)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        self.gridLayout.addWidget(self.tableWidget, 0, 0, 1, 2)
        self.pushButton = QtWidgets.QPushButton(Scoreboard)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 2, 1, 1, 1)

        self.retranslateUi(Scoreboard)
        QtCore.QMetaObject.connectSlotsByName(Scoreboard)

    def retranslateUi(self, Scoreboard):
        _translate = QtCore.QCoreApplication.translate
        Scoreboard.setWindowTitle(_translate("Scoreboard", "Dialog"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Scoreboard", "Name"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Scoreboard", "Date"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Scoreboard", "Score"))
        self.pushButton.setText(_translate("Scoreboard", "OK"))
