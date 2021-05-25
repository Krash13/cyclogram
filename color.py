# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'color.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.radioButton_3 = QtWidgets.QRadioButton(Dialog)
        self.radioButton_3.setEnabled(True)
        self.radioButton_3.setChecked(True)
        self.radioButton_3.setObjectName("radioButton_3")
        self.gridLayout.addWidget(self.radioButton_3, 0, 0, 1, 1)
        self.radioButton_7 = QtWidgets.QRadioButton(Dialog)
        self.radioButton_7.setObjectName("radioButton_7")
        self.gridLayout.addWidget(self.radioButton_7, 0, 1, 1, 1)
        self.radioButton_4 = QtWidgets.QRadioButton(Dialog)
        self.radioButton_4.setObjectName("radioButton_4")
        self.gridLayout.addWidget(self.radioButton_4, 1, 0, 1, 1)
        self.radioButton_5 = QtWidgets.QRadioButton(Dialog)
        self.radioButton_5.setObjectName("radioButton_5")
        self.gridLayout.addWidget(self.radioButton_5, 1, 1, 1, 1)
        self.radioButton_6 = QtWidgets.QRadioButton(Dialog)
        self.radioButton_6.setObjectName("radioButton_6")
        self.gridLayout.addWidget(self.radioButton_6, 2, 0, 1, 1)
        self.radioButton = QtWidgets.QRadioButton(Dialog)
        self.radioButton.setObjectName("radioButton")
        self.gridLayout.addWidget(self.radioButton, 2, 1, 1, 1)
        self.radioButton_2 = QtWidgets.QRadioButton(Dialog)
        self.radioButton_2.setObjectName("radioButton_2")
        self.gridLayout.addWidget(self.radioButton_2, 3, 0, 1, 1)
        self.radioButton_8 = QtWidgets.QRadioButton(Dialog)
        self.radioButton_8.setObjectName("radioButton_8")
        self.gridLayout.addWidget(self.radioButton_8, 3, 1, 1, 1)
        self.radioButton_10 = QtWidgets.QRadioButton(Dialog)
        self.radioButton_10.setObjectName("radioButton_10")
        self.gridLayout.addWidget(self.radioButton_10, 4, 0, 1, 1)
        self.radioButton_9 = QtWidgets.QRadioButton(Dialog)
        self.radioButton_9.setObjectName("radioButton_9")
        self.gridLayout.addWidget(self.radioButton_9, 4, 1, 1, 1)
        self.radioButton_11 = QtWidgets.QRadioButton(Dialog)
        self.radioButton_11.setObjectName("radioButton_11")
        self.gridLayout.addWidget(self.radioButton_11, 5, 0, 1, 1)
        self.radioButton_12 = QtWidgets.QRadioButton(Dialog)
        self.radioButton_12.setObjectName("radioButton_12")
        self.gridLayout.addWidget(self.radioButton_12, 5, 1, 1, 1)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 6, 0, 1, 2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.radioButton_3.setText(_translate("Dialog", "Красный"))
        self.radioButton_7.setText(_translate("Dialog", "Белый"))
        self.radioButton_4.setText(_translate("Dialog", "Зеленый"))
        self.radioButton_5.setText(_translate("Dialog", "Черный"))
        self.radioButton_6.setText(_translate("Dialog", "Желный"))
        self.radioButton.setText(_translate("Dialog", "Фиолетовый"))
        self.radioButton_2.setText(_translate("Dialog", "Синий"))
        self.radioButton_8.setText(_translate("Dialog", "Коричневый"))
        self.radioButton_10.setText(_translate("Dialog", "Оранжевый"))
        self.radioButton_9.setText(_translate("Dialog", "Розовый"))
        self.radioButton_11.setText(_translate("Dialog", "Голубой"))
        self.radioButton_12.setText(_translate("Dialog", "Золотой"))
        self.pushButton.setText(_translate("Dialog", "PushButton"))
