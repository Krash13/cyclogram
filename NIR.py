# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'NIR.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 0, 0, 1, 1)
        self.saveButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveButton.setObjectName("saveButton")
        self.gridLayout.addWidget(self.saveButton, 0, 3, 1, 1)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setEnabled(True)
        self.progressBar.setMaximum(8064)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(False)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar, 1, 0, 1, 4)
        self.pushButton_8 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_8.setObjectName("pushButton_8")
        self.gridLayout.addWidget(self.pushButton_8, 0, 1, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 0, 2, 1, 1)
        self.pushButton_14 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_14.setObjectName("pushButton_14")
        self.gridLayout.addWidget(self.pushButton_14, 3, 3, 1, 1)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tableWidget = QtWidgets.QTableWidget(self.tab)
        self.tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout_2.addWidget(self.tableWidget)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tableWidget_2 = QtWidgets.QTableWidget(self.tab_2)
        self.tableWidget_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.tableWidget_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(0)
        self.tableWidget_2.setRowCount(0)
        self.verticalLayout_3.addWidget(self.tableWidget_2)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setAccessibleName("")
        self.tab_3.setObjectName("tab_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.tab_3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.graphicsView = QtWidgets.QGraphicsView(self.tab_3)
        self.graphicsView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.graphicsView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.graphicsView.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.graphicsView.setObjectName("graphicsView")
        self.horizontalLayout.addWidget(self.graphicsView)
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab_4)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.tab_4)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 1, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.tab_4)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_2.addWidget(self.lineEdit, 1, 2, 1, 1)
        self.graphicsView_2 = QtWidgets.QGraphicsView(self.tab_4)
        self.graphicsView_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.graphicsView_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.graphicsView_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.graphicsView_2.setObjectName("graphicsView_2")
        self.gridLayout_2.addWidget(self.graphicsView_2, 0, 0, 1, 4)
        self.label_2 = QtWidgets.QLabel(self.tab_4)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 1, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(self.tab_4)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout_2.addWidget(self.pushButton_3, 2, 0, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(self.tab_4)
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout_2.addWidget(self.pushButton_4, 2, 1, 1, 1)
        self.pushButton_5 = QtWidgets.QPushButton(self.tab_4)
        self.pushButton_5.setObjectName("pushButton_5")
        self.gridLayout_2.addWidget(self.pushButton_5, 3, 0, 1, 1)
        self.pushButton_6 = QtWidgets.QPushButton(self.tab_4)
        self.pushButton_6.setObjectName("pushButton_6")
        self.gridLayout_2.addWidget(self.pushButton_6, 3, 1, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.tab_4)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout_2.addWidget(self.lineEdit_2, 1, 3, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.tab_4)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 2, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.tab_4)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 2, 3, 1, 1)
        self.pushButton_7 = QtWidgets.QPushButton(self.tab_4)
        self.pushButton_7.setObjectName("pushButton_7")
        self.gridLayout_2.addWidget(self.pushButton_7, 3, 3, 1, 1)
        self.tabWidget.addTab(self.tab_4, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.label_6 = QtWidgets.QLabel(self.tab_5)
        self.label_6.setGeometry(QtCore.QRect(10, 80, 362, 25))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.comboBox = QtWidgets.QComboBox(self.tab_5)
        self.comboBox.setGeometry(QtCore.QRect(10, 50, 261, 20))
        self.comboBox.setObjectName("comboBox")
        self.pushButton_9 = QtWidgets.QPushButton(self.tab_5)
        self.pushButton_9.setGeometry(QtCore.QRect(40, 160, 91, 31))
        self.pushButton_9.setObjectName("pushButton_9")
        self.label_7 = QtWidgets.QLabel(self.tab_5)
        self.label_7.setGeometry(QtCore.QRect(10, 420, 401, 25))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.label_5 = QtWidgets.QLabel(self.tab_5)
        self.label_5.setGeometry(QtCore.QRect(9, 9, 111, 33))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.timeEdit = QtWidgets.QTimeEdit(self.tab_5)
        self.timeEdit.setGeometry(QtCore.QRect(180, 120, 80, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.timeEdit.setFont(font)
        self.timeEdit.setObjectName("timeEdit")
        self.label_8 = QtWidgets.QLabel(self.tab_5)
        self.label_8.setGeometry(QtCore.QRect(20, 110, 23, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.spinBox = QtWidgets.QSpinBox(self.tab_5)
        self.spinBox.setGeometry(QtCore.QRect(60, 120, 51, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.spinBox.setFont(font)
        self.spinBox.setObjectName("spinBox")
        self.progressBar_2 = QtWidgets.QProgressBar(self.tab_5)
        self.progressBar_2.setGeometry(QtCore.QRect(10, 460, 741, 23))
        self.progressBar_2.setProperty("value", 0)
        self.progressBar_2.setObjectName("progressBar_2")
        self.pushButton_10 = QtWidgets.QPushButton(self.tab_5)
        self.pushButton_10.setGeometry(QtCore.QRect(170, 160, 91, 31))
        self.pushButton_10.setObjectName("pushButton_10")
        self.radioButton = QtWidgets.QRadioButton(self.tab_5)
        self.radioButton.setGeometry(QtCore.QRect(30, 210, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.radioButton.setFont(font)
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(self.tab_5)
        self.radioButton_2.setGeometry(QtCore.QRect(160, 210, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.radioButton_2.setFont(font)
        self.radioButton_2.setObjectName("radioButton_2")
        self.groupBox = QtWidgets.QGroupBox(self.tab_5)
        self.groupBox.setGeometry(QtCore.QRect(380, 20, 183, 411))
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_9 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.verticalLayout.addWidget(self.label_9)
        self.spinBox_2 = QtWidgets.QSpinBox(self.groupBox)
        self.spinBox_2.setMinimum(1)
        self.spinBox_2.setMaximum(10000)
        self.spinBox_2.setObjectName("spinBox_2")
        self.verticalLayout.addWidget(self.spinBox_2)
        self.label_10 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.verticalLayout.addWidget(self.label_10)
        self.spinBox_3 = QtWidgets.QSpinBox(self.groupBox)
        self.spinBox_3.setMinimum(10)
        self.spinBox_3.setMaximum(10000)
        self.spinBox_3.setObjectName("spinBox_3")
        self.verticalLayout.addWidget(self.spinBox_3)
        self.label_11 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.verticalLayout.addWidget(self.label_11)
        self.spinBox_4 = QtWidgets.QSpinBox(self.groupBox)
        self.spinBox_4.setMinimum(10)
        self.spinBox_4.setMaximum(10000)
        self.spinBox_4.setObjectName("spinBox_4")
        self.verticalLayout.addWidget(self.spinBox_4)
        self.label_12 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.verticalLayout.addWidget(self.label_12)
        self.spinBox_5 = QtWidgets.QSpinBox(self.groupBox)
        self.spinBox_5.setMinimum(1)
        self.spinBox_5.setMaximum(100)
        self.spinBox_5.setObjectName("spinBox_5")
        self.verticalLayout.addWidget(self.spinBox_5)
        self.label_13 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.verticalLayout.addWidget(self.label_13)
        self.spinBox_6 = QtWidgets.QSpinBox(self.groupBox)
        self.spinBox_6.setMinimum(1)
        self.spinBox_6.setMaximum(100)
        self.spinBox_6.setObjectName("spinBox_6")
        self.verticalLayout.addWidget(self.spinBox_6)
        self.label_15 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_15.setFont(font)
        self.label_15.setObjectName("label_15")
        self.verticalLayout.addWidget(self.label_15)
        self.spinBox_7 = QtWidgets.QSpinBox(self.groupBox)
        self.spinBox_7.setMinimum(5)
        self.spinBox_7.setMaximum(10000)
        self.spinBox_7.setObjectName("spinBox_7")
        self.verticalLayout.addWidget(self.spinBox_7)
        self.label_16 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_16.setFont(font)
        self.label_16.setObjectName("label_16")
        self.verticalLayout.addWidget(self.label_16)
        self.spinBox_8 = QtWidgets.QSpinBox(self.groupBox)
        self.spinBox_8.setMinimum(5)
        self.spinBox_8.setMaximum(10000)
        self.spinBox_8.setObjectName("spinBox_8")
        self.verticalLayout.addWidget(self.spinBox_8)
        self.label_14 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.verticalLayout.addWidget(self.label_14)
        self.spinBox_9 = QtWidgets.QSpinBox(self.groupBox)
        self.spinBox_9.setMinimum(1)
        self.spinBox_9.setMaximum(10000)
        self.spinBox_9.setObjectName("spinBox_9")
        self.verticalLayout.addWidget(self.spinBox_9)
        self.tabWidget.addTab(self.tab_5, "")
        self.gridLayout.addWidget(self.tabWidget, 2, 0, 1, 4)
        self.pushButton_13 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_13.setObjectName("pushButton_13")
        self.gridLayout.addWidget(self.pushButton_13, 3, 2, 1, 1)
        self.pushButton_12 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_12.setObjectName("pushButton_12")
        self.gridLayout.addWidget(self.pushButton_12, 3, 1, 1, 1)
        self.pushButton_11 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_11.setObjectName("pushButton_11")
        self.gridLayout.addWidget(self.pushButton_11, 3, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_2.setText(_translate("MainWindow", "?????????????????? ??????????????????????"))
        self.saveButton.setText(_translate("MainWindow", "??????????????????"))
        self.pushButton_8.setText(_translate("MainWindow", "?????????????? ??????????"))
        self.pushButton.setText(_translate("MainWindow", "??????????????"))
        self.pushButton_14.setText(_translate("MainWindow", "?????????????? ????????????????"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "????????????????"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "??????????????????"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "??????????????????????"))
        self.label.setText(_translate("MainWindow", "??????"))
        self.lineEdit.setText(_translate("MainWindow", "400"))
        self.label_2.setText(_translate("MainWindow", "??????????????????????: ??????????????????????????"))
        self.pushButton_3.setText(_translate("MainWindow", "??????"))
        self.pushButton_4.setText(_translate("MainWindow", "??????. ????????"))
        self.pushButton_5.setText(_translate("MainWindow", "??????. ????????"))
        self.pushButton_6.setText(_translate("MainWindow", "??????????????????????????"))
        self.lineEdit_2.setText(_translate("MainWindow", "10"))
        self.label_3.setText(_translate("MainWindow", "???????????????????????? ????????????????"))
        self.label_4.setText(_translate("MainWindow", "???????? ??????????????"))
        self.pushButton_7.setText(_translate("MainWindow", "??????????????????"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "??????????????"))
        self.label_6.setText(_translate("MainWindow", "???????????????????????? ?????????? ???????????? ????????????:"))
        self.pushButton_9.setText(_translate("MainWindow", "????????????"))
        self.label_7.setText(_translate("MainWindow", "???????????????????????? ??????: ..."))
        self.label_5.setText(_translate("MainWindow", "??????????????:"))
        self.label_8.setText(_translate("MainWindow", "??????"))
        self.pushButton_10.setText(_translate("MainWindow", "????????"))
        self.radioButton.setText(_translate("MainWindow", "??????????????"))
        self.radioButton_2.setText(_translate("MainWindow", "IWO"))
        self.groupBox.setTitle(_translate("MainWindow", "?????????????????? IWO"))
        self.label_9.setText(_translate("MainWindow", "???????????????????? ??????????????????"))
        self.label_10.setText(_translate("MainWindow", "?????????????????? ??????????????????"))
        self.label_11.setText(_translate("MainWindow", "???????????????????????? ??????????????????"))
        self.label_12.setText(_translate("MainWindow", "?????????????????????? ?????????? ??????????"))
        self.label_13.setText(_translate("MainWindow", "???????????????????????? ?????????? ??????????"))
        self.label_15.setText(_translate("MainWindow", "???????????????????????? ??????????????"))
        self.label_16.setText(_translate("MainWindow", "?????????????????????? ??????????????"))
        self.label_14.setText(_translate("MainWindow", "m"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("MainWindow", "??????????????????????"))
        self.pushButton_13.setText(_translate("MainWindow", "???????????????????? ????????????????"))
        self.pushButton_12.setText(_translate("MainWindow", "?????????????? ??????????????"))
        self.pushButton_11.setText(_translate("MainWindow", "???????????????????? ??????????????"))
