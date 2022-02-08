import NIR  # Это наш конвертированный файл дизайна
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtWidgets import QMessageBox
from constans import LABELS, LABELS1, UNITS, COLS
import json
from fpdf import FPDF
from itertools import product
import threading
from Sornyak import sort, myround, my_max, my_min
import random
import numpy as np
from copy import deepcopy


class MyScene(QtWidgets.QGraphicsScene):

    def addArrow(self, x1, y1, x2, y2):
        self.addLine(x1, y1, x2, y2)
        if y1 < y2:
            self.addLine(x2, y2, x2 - 5, y2 - 5)
            self.addLine(x2, y2, x2 + 5, y2 - 5)
        else:
            self.addLine(x2, y2, x2 - 5, y2 + 5)
            self.addLine(x2, y2, x2 + 5, y2 + 5)

    def addDotted(self, x1, y1, x2, y2):
         for x in range(x1, x2, 10):
             self.addLine(x, y1, x+5, y2)

class MyApp(QtWidgets.QMainWindow, NIR.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.apparatus_count1 = 0
        self.operation_count1 = 0
        self.apparatus_count2 = 0
        self.operation_count2 = 0
        self.tableWidget.setColumnCount(len(LABELS))
        self.tableWidget.setHorizontalHeaderLabels(LABELS)
        self.tableWidget.setRowCount(1000)
        self.tableWidget.cellChanged.connect(self.change_table1)
        self.tableWidget.cellClicked.connect(self.click_table1)
        self.tableWidget_2.setColumnCount(len(LABELS1))
        self.tableWidget_2.setHorizontalHeaderLabels(LABELS1)
        self.tableWidget_2.setRowCount(1000)
        self.tableWidget_2.cellChanged.connect(self.change_table2)
        self.tableWidget_2.cellClicked.connect(self.click_table2)
        self.saveButton.clicked.connect(self.save)
        self.pushButton.clicked.connect(self.load)
        self.pushButton_2.clicked.connect(self.create_ciclogarm)
        self.utility = "Электр-во"
        self.pushButton_3.clicked.connect(lambda: self.set_utility("Пар"))
        self.pushButton_4.clicked.connect(lambda: self.set_utility("Гор. вода"))
        self.pushButton_5.clicked.connect(lambda: self.set_utility("Хол. вода"))
        self.pushButton_6.clicked.connect(lambda: self.set_utility("Электр-во"))
        self.pushButton_7.clicked.connect(self.update_utilities)
        self.pushButton_8.clicked.connect(self.create_pdf)
        self.pushButton_9.clicked.connect(self.start_optimization)
        self.pushButton_10.clicked.connect(self.stop_optimization)
        self.pushButton_11.clicked.connect(self.copy_apparat)
        self.pushButton_12.clicked.connect(self.delete_apparat)
        self.pushButton_13.clicked.connect(self.copy_operation)
        self.pushButton_14.clicked.connect(self.delete_operation)
        self.pushButton_10.setEnabled(False)
        self.progressBar_2.setVisible(False)
        self.radioButton.setChecked(True)
        self.method = "Перебор"
        self.radioButton.clicked.connect(lambda: self.set_method("Перебор"))
        self.radioButton_2.clicked.connect(lambda: self.set_method("IWO"))
        self.run = False
        self.spinBox.setMaximum(7)
        self.max = 400
        self.cost = 10
        self.penalty = 0
        self.progressBar.setVisible(False)
        self.groupBox.setVisible(False)
        for key in UNITS.keys():
            self.comboBox.addItem(key)

    def copy_apparat(self):
        if self.tabWidget.currentIndex() == 0:
            if self.tableWidget.currentItem() is not None:
                if self.tableWidget.currentItem().column() < 2:
                    name = self.tableWidget.item(self.tableWidget.currentItem().row(), 1).text()
                    apparatus = self.create_json()
                    copy_app = deepcopy([x for x in apparatus['independent'] if x['name'] == name][0])
                    new_name, done = QtWidgets.QInputDialog.getText(self, 'Имя аппарата', 'Введите имя нового аппарата:')
                    if done:
                        copy_app['name'] = new_name
                        copy_app['id'] = str(self.apparatus_count1 + 1)
                        apparatus['independent'].append(copy_app)
                        self.load(apparatus)
        elif self.tabWidget.currentIndex() == 1:
            if self.tableWidget_2.currentItem() is not None:
                if 0 < self.tableWidget_2.currentItem().column() < 3:
                    name = self.tableWidget_2.item(self.tableWidget_2.currentItem().row(), 2).text()
                    apparatus = self.create_json()
                    copy_app = deepcopy([x for x in apparatus['dependent'] if x['name'] == name][0])
                    new_name, done = QtWidgets.QInputDialog.getText(self, 'Имя аппарата', 'Введите имя нового аппарата:')
                    if done:
                        copy_app['name'] = new_name
                        copy_app['id'] = str(self.apparatus_count2 + 1)
                        apparatus['dependent'].append(copy_app)
                        self.load(apparatus)

    def delete_operation(self):
        if self.tabWidget.currentIndex() == 0:
            if self.tableWidget.currentItem() is not None:
                if 2 < self.tableWidget.currentItem().column() < 5:
                    op_name = self.tableWidget.item(self.tableWidget.currentItem().row(), 4).text()
                    row = self.tableWidget.currentItem().row()
                    while True:
                        if self.tableWidget.item(row, 1) is not None and self.tableWidget.item(row, 1).text() != '':
                            break
                        row -= 1
                    name = self.tableWidget.item(row, 1).text()
                    apparatus = self.create_json()
                    copy_app = [x for x in apparatus['independent'] if x['name'] == name][0]
                    copy_operation = [x for x in copy_app['operations'] if x['Имя опер.'] == op_name][0]
                    copy_app['operations'].remove(copy_operation)
                    for i in range(len(copy_app['operations'])):
                        copy_app['operations'][i]['№ опер.'] = str(i + 1)
                    self.load(apparatus)
        elif self.tabWidget.currentIndex() == 1:
            if self.tableWidget_2.currentItem() is not None:
                if 3 < self.tableWidget_2.currentItem().column() < 6:
                    op_name = self.tableWidget_2.item(self.tableWidget_2.currentItem().row(), 5).text()
                    row = self.tableWidget_2.currentItem().row()
                    while True:
                        if self.tableWidget_2.item(row, 2) is not None and self.tableWidget_2.item(row, 2).text() != '':
                            break
                        row -= 1
                    name = self.tableWidget_2.item(row, 2).text()
                    apparatus = self.create_json()
                    copy_app = [x for x in apparatus['dependent'] if x['name'] == name][0]
                    copy_operation = [x for x in copy_app['operations'] if x['Имя опер.'] == op_name][0]
                    copy_app['operations'].remove(copy_operation)
                    for i in range(len(copy_app['operations'])):
                        copy_app['operations'][i]['№ опер.'] = str(i+1)
                    self.load(apparatus)

    def copy_operation(self):
        if self.tabWidget.currentIndex() == 0:
            if self.tableWidget.currentItem() is not None:
                if 2 < self.tableWidget.currentItem().column() < 5:
                    op_name = self.tableWidget.item(self.tableWidget.currentItem().row(), 4).text()
                    row = self.tableWidget.currentItem().row()
                    while True:
                        if self.tableWidget.item(row, 1) is not None and self.tableWidget.item(row, 1).text() != '':
                            break
                        row -= 1
                    name = self.tableWidget.item(row, 1).text()
                    apparatus = self.create_json()
                    copy_app = [x for x in apparatus['independent'] if x['name'] == name][0]
                    copy_operation = deepcopy([x for x in copy_app['operations'] if x['Имя опер.'] == op_name][0])
                    copy_operation['№ опер.'] = str(len(copy_app['operations']) + 1)
                    copy_app['operations'].append(copy_operation)
                    self.load(apparatus)
        elif self.tabWidget.currentIndex() == 1:
            if self.tableWidget_2.currentItem() is not None:
                if 3 < self.tableWidget_2.currentItem().column() < 6:
                    op_name = self.tableWidget_2.item(self.tableWidget_2.currentItem().row(), 5).text()
                    row = self.tableWidget_2.currentItem().row()
                    while True:
                        if self.tableWidget_2.item(row, 2) is not None and self.tableWidget_2.item(row, 2).text() != '':
                            break
                        row -= 1
                    name = self.tableWidget_2.item(row, 2).text()
                    apparatus = self.create_json()
                    copy_app = [x for x in apparatus['dependent'] if x['name'] == name][0]
                    copy_operation = deepcopy([x for x in copy_app['operations'] if x['Имя опер.'] == op_name][0])
                    copy_operation['№ опер.'] = str(len(copy_app['operations']) + 1)
                    copy_app['operations'].append(copy_operation)
                    self.load(apparatus)

    def delete_apparat(self):
        if self.tabWidget.currentIndex() == 0:
            if self.tableWidget.currentItem() is not None:
                if self.tableWidget.currentItem().column() < 2:
                    name = self.tableWidget.item(self.tableWidget.currentItem().row(), 1).text()
                    apparatus = self.create_json()
                    copy_app = [x for x in apparatus['independent'] if x['name'] == name][0]
                    apparatus['independent'].remove(copy_app)
                    for i in range(len(apparatus['independent'])):
                        apparatus['independent'][i]['id'] = str(i + 1)
                    self.load(apparatus)
        elif self.tabWidget.currentIndex() == 1:
            if self.tableWidget_2.currentItem() is not None:
                if 0 < self.tableWidget_2.currentItem().column() < 3:
                    name = self.tableWidget_2.item(self.tableWidget_2.currentItem().row(), 2).text()
                    apparatus = self.create_json()
                    copy_app = deepcopy([x for x in apparatus['dependent'] if x['name'] == name][0])
                    apparatus['dependent'].remove(copy_app)
                    for i in range(len(apparatus['dependent'])):
                        apparatus['dependent'][i]['id'] = str(i + 1)
                    self.load(apparatus)


    def set_method(self, method):
        self.method = method
        if self.method == "IWO":
            self.groupBox.setVisible(True)
        else:
            self.groupBox.setVisible(False)

    def set_utility(self, utility):
        self.utility = utility
        self.plot_utilities()

    def plot_arrow(self):
        param, work = self.check_admissibility()
        apparatus = self.create_json()
        apparatus = apparatus["independent"] + apparatus["dependent"]
        k = 0
        for apparat in apparatus:
            i = 0
            while i < 14 * 24 * 60:
                if work[apparat['name']][i] is not None:
                    start = i * 2
                    value = work[apparat['name']][i]
                    while i < 14 * 24 * 60 and work[apparat['name']][i] == value:
                        i += 1
                    end = i * 2
                    i -= 1
                    for j in range(1, 6):
                        if apparat['operations'][int(value) - 1]["Стрелка{}".format(j)] != '':
                            arrow_app = [x for x in apparatus if x['name'] == apparat['operations'][int(value) - 1]["Стрелка{}".format(j)]]
                            if arrow_app != []:
                                arrow_app = arrow_app[0]
                                num = apparatus.index(arrow_app)
                                y1 = k * 60 + 50 + 50
                                y2 = num * 60 + 50
                                if num < k:
                                    y1 -= 50
                                    y2 += 50
                                for l in range(start, end + 1, 10):
                                    self.scene.addArrow(
                                        x1=l + 200,
                                        y1=y1,
                                        x2=l + 200,
                                        y2=y2
                                    )
                i += 1
            k += 1

    def update_utilities(self):
        if self.lineEdit.text().isdigit():
            self.max = int(self.lineEdit.text())
        else:
            self.lineEdit.setText(str(self.max))
        if self.lineEdit_2.text().isdigit():
            self.cost = int(self.lineEdit_2.text())
        else:
            self.lineEdit_2.setText(str(self.cost))
        self.plot_utilities()

    def create_json(self):
        apparatus = {}
        independent = []
        i = 0
        while not (self.tableWidget.item(i, 3) is None and self.tableWidget.item(i+1, 3) is None):
            if self.tableWidget.item(i, 0) is not None:
                if i>0:
                    independent.append(apparat)
                apparat = {}
                apparat["id"] = self.tableWidget.item(i, 0).text()
                apparat["name"] = self.tableWidget.item(i, 1).text()
                color = (self.tableWidget.item(i, 2).background().color().red(),
                         self.tableWidget.item(i, 2).background().color().green(),
                         self.tableWidget.item(i, 2).background().color().blue())
                apparat["color"] = color
                apparat["operations"] = []
            operation = {}
            for j in range(3, len(LABELS)):
                if self.tableWidget.horizontalHeaderItem(j).text() == "Цвет опер.":
                    color = (self.tableWidget.item(i, j).background().color().red(),
                             self.tableWidget.item(i, j).background().color().green(),
                             self.tableWidget.item(i, j).background().color().blue())
                    operation[self.tableWidget.horizontalHeaderItem(j).text()] = color
                else:
                    if self.tableWidget.item(i, j) is None:
                        operation[self.tableWidget.horizontalHeaderItem(j).text()] = ""
                    else:
                        operation[self.tableWidget.horizontalHeaderItem(j).text()] = self.tableWidget.item(i, j).text()
            apparat["operations"].append(operation)
            i += 1
        independent.append(apparat)
        apparatus["independent"] = independent

        apparat = None
        dependent = []
        i = 0
        while not (self.tableWidget_2.item(i, 4) is None and self.tableWidget_2.item(i+1, 4) is None):
            if self.tableWidget_2.item(i, 1) is not None:
                if i>0:
                    dependent.append(apparat)
                apparat = {}
                apparat["id"] = self.tableWidget_2.item(i, 1).text()
                apparat["name"] = self.tableWidget_2.item(i, 2).text()
                color = (self.tableWidget_2.item(i, 3).background().color().red(),
                         self.tableWidget_2.item(i, 3).background().color().green(),
                         self.tableWidget_2.item(i, 3).background().color().blue())
                apparat["color"] = color
                apparat["operations"] = []
            operation = {}
            for j in range(4, len(LABELS1)):
                if self.tableWidget_2.horizontalHeaderItem(j).text() == "Цвет опер.":
                    color = (self.tableWidget_2.item(i, j).background().color().red(),
                             self.tableWidget_2.item(i, j).background().color().green(),
                             self.tableWidget_2.item(i, j).background().color().blue())
                    operation[self.tableWidget_2.horizontalHeaderItem(j).text()] = color
                else:
                    if self.tableWidget_2.item(i, j) is None:
                        operation[self.tableWidget_2.horizontalHeaderItem(j).text()] = ""
                    else:
                        operation[self.tableWidget_2.horizontalHeaderItem(j).text()] = self.tableWidget_2.item(i, j).text()
            if self.tableWidget_2.item(i, 0) is None:
                operation[self.tableWidget_2.horizontalHeaderItem(0).text()] = ""
            else:
                operation[self.tableWidget_2.horizontalHeaderItem(0).text()] = self.tableWidget_2.item(i, 0).text()
            apparat["operations"].append(operation)
            i += 1
        if apparat is not None:
            dependent.append(apparat)
        apparatus["dependent"] = dependent
        return apparatus

    def save(self):
        file = QtWidgets.QFileDialog.getSaveFileName(self, "Создание файла", filter="*.json")
        if file[0] == '':
            return
        apparatus = self.create_json()
        with open(file[0], 'w') as f:
            json.dump(apparatus, f)

    def plot_utilities(self):
        self.label.setText(UNITS[self.utility])
        self.label_2.setText("Потребление: {}".format(self.utility))
        self.scene2 = MyScene()
        x = 50
        for j in range(2):
            for i in range(1, 8):
                GraphicPixmap = QtWidgets.QGraphicsPixmapItem()
                GraphicPixmap.setAcceptHoverEvents(True)
                pixmap = QtGui.QPixmap("days/{}.bmp".format(i))
                GraphicPixmap.setPixmap(pixmap)
                GraphicPixmap.setX(x)
                x += pixmap.width()
                self.scene2.addItem(GraphicPixmap)
        y = pixmap.height()
        ys = 24 * 14 * 12 * [pixmap.height()]
        ut = 24 * 14 * 12 * [0]
        param, work = self.check_admissibility()
        if not param:
            return ut
        apparatus = self.create_json()
        apparatus = apparatus['independent'] + apparatus['dependent']
        for apparat in apparatus:
            for i in range(0, 24 * 14 * 60, 5):
                if work[apparat['name']][i] is not None:
                    value = work[apparat['name']][i]
                    if apparat['operations'][int(value) - 1][self.utility] == '':
                        continue
                    color = QtGui.QColor(apparat['color'][0],
                                         apparat['color'][1],
                                         apparat['color'][2])
                    h = int(apparat['operations'][int(value) - 1][self.utility])
                    h = 25 * h // (self.cost)
                    ut[i // 5] += int(apparat['operations'][int(value) - 1][self.utility])
                    self.scene2.addRect(i * 2 + 50, ys[i // 5], pixmap.width() // (24 * 12),
                                        h, Qt.Qt.black, Qt.QBrush(color))
                    ys[i // 5] += h

        for i in range(0, self.max + 1, self.cost):
            text = QtWidgets.QGraphicsTextItem()
            text.setPlainText(str(i))
            text.setPos(0, y - 10)
            self.scene2.addItem(text)
            self.scene2.addLine(30, y, 50, y)
            self.scene2.addDotted(50, y, 14*pixmap.width()+50, y)
            y += 25
        self.graphicsView_2.setScene(self.scene2)
        return ut

    def create_pdf(self):
        file = QtWidgets.QFileDialog.getSaveFileName(self, "Создание файла", filter="*.pdf")
        if file[0] == '':
            return
        self.progressBar.setVisible(True)
        self.setEnabled(False)
        self.progressBar.setValue(0)
        self.progressBar.setMaximum(len(UNITS) * 2016 * 2)
        pdf = FPDF()
        pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
        pdf.add_page()
        old_utility = self.utility
        for utility in UNITS.keys():
            self.utility = utility
            ut = self.plot_utilities()
            max_ut = max(ut)
            pdf.set_font('DejaVu', '', 14)
            pdf.cell(200, 10, txt="Потребление утилиты '{}':".format(utility), ln=1, align="C")
            time = 0
            if max_ut == 0:
                self.progressBar.setValue(
                    self.progressBar.value() + int(self.progressBar.maximum() / len(UNITS))
                )
                continue
            min_uts = list([i for i in ut if i != 0])
            min_ut = min(min_uts)

            pdf.set_font('DejaVu', '', 12)
            i = 0
            pdf.cell(200, 10, txt="МАКСИМУМ", ln=1, align="C")
            while i < len(ut):
                if ut[i] == max_ut:
                    start_time = i * 5
                    while ut[i] == max_ut:
                        time += 5
                        i += 1
                        self.progressBar.setValue(
                            self.progressBar.value() + int(self.progressBar.maximum() / len(UNITS) / len(ut))
                        )
                    pdf.cell(200, 10, txt="День:{}, Время: {:02}:{:02}, max={}, Продолжительность: {} мин".format(
                        start_time//(24*60) + 1,
                        (start_time % (24 * 60))//60,
                        (start_time % (24 * 60)) % 60,
                        max_ut,
                        time
                    ), ln=1, align="C")
                    time = 0
                i += 1
                self.progressBar.setValue(
                    self.progressBar.value() + int(self.progressBar.maximum() / len(UNITS) / len(ut))
                )
            time = 0
            i = 0
            pdf.cell(200, 10, txt="МИНИМУМ", ln=1, align="C")
            while i < len(ut):
                if ut[i] == min_ut:
                    start_time = i * 5
                    while ut[i] == min_ut:
                        time += 5
                        i += 1
                        self.progressBar.setValue(
                            self.progressBar.value() + int(self.progressBar.maximum() / len(UNITS) / len(ut))
                        )
                    pdf.cell(200, 10, txt="День:{}, Время: {:02}:{:02}, min={}, Продолжительность: {} мин".format(
                        start_time // (24 * 60) + 1,
                        (start_time % (24 * 60)) // 60,
                        (start_time % (24 * 60)) % 60,
                        min_ut,
                        time
                    ), ln=1, align="C")
                    time = 0
                i += 1
                self.progressBar.setValue(
                    self.progressBar.value() + int(self.progressBar.maximum() / len(UNITS) / len(ut))
                )
        self.utility = old_utility
        self.plot_utilities()
        pdf.output(file[0])
        self.progressBar.setVisible(False)
        self.setEnabled(True)

    def load(self, json_dict=None):
        if not json_dict:
            file = QtWidgets.QFileDialog.getOpenFileName(self, "Выбор файла", filter="*.json")
            if file[0] == '':
                return
            with open(file[0], "r") as read_file:
                data = json.load(read_file)
        else:
            data = json_dict
        self.apparatus_count1 = 0
        self.operation_count1 = 0
        self.tableWidget.clear()
        self.tableWidget_2.clear()
        self.tableWidget.setColumnCount(len(LABELS))
        self.tableWidget.setHorizontalHeaderLabels(LABELS)
        self.tableWidget.setRowCount(1000)
        self.tableWidget.cellChanged.connect(self.change_table1)
        self.tableWidget.cellClicked.connect(self.click_table1)
        self.tableWidget_2.setColumnCount(len(LABELS1))
        self.tableWidget_2.setHorizontalHeaderLabels(LABELS1)
        self.tableWidget_2.setRowCount(1000)
        self.tableWidget_2.cellChanged.connect(self.change_table2)
        self.tableWidget_2.cellClicked.connect(self.click_table2)
        i = 0
        for apparat in data["independent"]:
            self.apparatus_count1 += 1
            self.operation_count1 = 0
            self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem())
            self.tableWidget.item(i, 0).setText(apparat["id"])
            self.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem())
            self.tableWidget.item(i, 1).setText(apparat["name"])
            self.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem())
            self.tableWidget.item(i, 2).setBackground(QtGui.QColor(apparat["color"][0],
                                                                   apparat["color"][1],
                                                                   apparat["color"][2]))
            for j in range(i, i+len(apparat["operations"])):
                for k in range(3, len(LABELS)):
                    if self.tableWidget.horizontalHeaderItem(k).text() != "Цвет опер.":
                        self.tableWidget.setItem(j, k, QtWidgets.QTableWidgetItem())
                        self.tableWidget.item(j, k).setText(str(apparat["operations"][j-i][self.tableWidget.horizontalHeaderItem(k).text()]))
                    else:
                        color = apparat["operations"][j-i][self.tableWidget.horizontalHeaderItem(k).text()]
                        self.tableWidget.setItem(j, k, QtWidgets.QTableWidgetItem())
                        self.tableWidget.item(j, k).setBackground(QtGui.QColor(color[0],
                                                                               color[1],
                                                                               color[2]))
                self.operation_count1 += 1
            i = j+1
        i = 0
        self.apparatus_count2 = 0
        self.operation_count2 = 0
        for apparat in data["dependent"]:
            self.apparatus_count2 += 1
            self.operation_count2 = 0
            self.tableWidget_2.setItem(i, 1, QtWidgets.QTableWidgetItem())
            self.tableWidget_2.item(i, 1).setText(apparat["id"])
            self.tableWidget_2.setItem(i, 2, QtWidgets.QTableWidgetItem())
            self.tableWidget_2.item(i, 2).setText(apparat["name"])
            self.tableWidget_2.setItem(i, 3, QtWidgets.QTableWidgetItem())
            self.tableWidget_2.item(i, 3).setBackground(QtGui.QColor(apparat["color"][0],
                                                                   apparat["color"][1],
                                                                   apparat["color"][2]))
            for j in range(i, i+len(apparat["operations"])):
                for k in range(4, len(LABELS1)):
                    if self.tableWidget_2.horizontalHeaderItem(k).text() != "Цвет опер.":
                        self.tableWidget_2.setItem(j, k, QtWidgets.QTableWidgetItem())
                        self.tableWidget_2.item(j, k).setText(apparat["operations"][j-i][self.tableWidget_2.horizontalHeaderItem(k).text()])
                    else:
                        color = apparat["operations"][j-i][self.tableWidget_2.horizontalHeaderItem(k).text()]
                        self.tableWidget_2.setItem(j, k, QtWidgets.QTableWidgetItem())
                        self.tableWidget_2.item(j, k).setBackground(QtGui.QColor(color[0],
                                                                               color[1],
                                                                               color[2]))
                self.tableWidget_2.setItem(j, 0, QtWidgets.QTableWidgetItem())
                self.tableWidget_2.item(j, 0).setText(apparat["operations"][j-i][self.tableWidget_2.horizontalHeaderItem(0).text()])
                self.operation_count2 += 1
            i = j+1
        self.create_ciclogarm()

    def change_table1(self, row, column):
        if column == 1 and self.tableWidget.item(row, 0) is None:
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem())
            self.tableWidget.item(row, 0).setText(str(self.apparatus_count1+1))
            self.apparatus_count1 += 1
            self.operation_count1 = 0
            color = QtWidgets.QColorDialog.getColor(QtGui.QColor(0, 0, 0), self)
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem())
            self.tableWidget.item(row, 2).setBackground(QtGui.QColor(color))

        if column == 4 and self.tableWidget.item(row, 3) is None:
            self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem())
            self.tableWidget.item(row, 3).setText(str(self.operation_count1+1))
            self.operation_count1 += 1
            color = QtWidgets.QColorDialog.getColor(QtGui.QColor(0, 0, 0), self)
            self.tableWidget.setItem(row, 5, QtWidgets.QTableWidgetItem())
            self.tableWidget.item(row, 5).setBackground(QtGui.QColor(color))

    def click_table1(self, row, column):
        if column == 5 and self.tableWidget.item(row, 3) is not None:
            color = QtWidgets.QColorDialog.getColor(QtGui.QColor(0, 0, 0), self)
            self.tableWidget.setItem(row, 5, QtWidgets.QTableWidgetItem())
            self.tableWidget.item(row, 5).setBackground(QtGui.QColor(color))

        if column == 2 and self.tableWidget.item(row, 1) is not None:
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem())
            color = QtWidgets.QColorDialog.getColor(QtGui.QColor(0, 0, 0), self)
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem())
            self.tableWidget.item(row, 2).setBackground(QtGui.QColor(color))

    def change_table2(self, row, column):
        if column == 2 and self.tableWidget_2.item(row, 1) is None:
            self.tableWidget_2.setItem(row, 1, QtWidgets.QTableWidgetItem())
            self.tableWidget_2.item(row, 1).setText(str(self.apparatus_count2+1))
            self.apparatus_count2 += 1
            self.operation_count2 = 0
            color = QtWidgets.QColorDialog.getColor(QtGui.QColor(0, 0, 0), self)
            self.tableWidget_2.setItem(row, 3, QtWidgets.QTableWidgetItem())
            self.tableWidget_2.item(row, 3).setBackground(QtGui.QColor(color))

        if column == 5 and self.tableWidget_2.item(row, 4) is None:
            self.tableWidget_2.setItem(row, 4, QtWidgets.QTableWidgetItem())
            self.tableWidget_2.item(row, 4).setText(str(self.operation_count2+1))
            self.operation_count2 += 1
            color = QtWidgets.QColorDialog.getColor(QtGui.QColor(0, 0, 0), self)
            self.tableWidget_2.setItem(row, 6, QtWidgets.QTableWidgetItem())
            self.tableWidget_2.item(row, 6).setBackground(QtGui.QColor(color))

    def click_table2(self, row, column):
        if column == 6 and self.tableWidget_2.item(row, 4) is not None:
            color = QtWidgets.QColorDialog.getColor(QtGui.QColor(0, 0, 0), self)
            self.tableWidget_2.setItem(row, 6, QtWidgets.QTableWidgetItem())
            self.tableWidget_2.item(row, 6).setBackground(QtGui.QColor(color))
        if column == 3 and self.tableWidget_2.item(row, 2) is not None:
            color = QtWidgets.QColorDialog.getColor(QtGui.QColor(0, 0, 0), self)
            self.tableWidget_2.setItem(row, 3, QtWidgets.QTableWidgetItem())
            self.tableWidget_2.item(row, 3).setBackground(QtGui.QColor(color))

    def check_admissibility(self, json_dict=None):
        try:
            apparatus = json_dict
            if json_dict is None:
                apparatus = self.create_json()
        except:
           return False, []
        self.penalty = 0
        work = {}
        for ind in apparatus['independent']:
            work[ind['name']] = 21 * 24 * 60 * [None]
        for dep in apparatus['dependent']:
            work[dep['name']] = 21 * 24 * 60 * [None]
        for ind in apparatus['independent']:
            cycles = int(ind['operations'][0]['кол. циклов'])
            start = 24 * 60 * (int(ind['operations'][0]['День пуск']) - 1) + 60 * int(ind['operations'][0]['Т пуска(ч)']) + int(ind['operations'][0]['Т пуска(м)']) + 7 * 24 * 60
            cycle = 1
            i = start
            while cycle <= cycles:
                for operation in ind['operations']:
                    for j in range(int(operation['Время'])):
                        if i + j > len(work[ind['name']]) - 1:
                            continue
                        work[ind['name']][i+j] = operation['№ опер.']
                    if operation['Следствие'] != '':
                        for apparat in apparatus['dependent']:
                            depended = [x for x in apparat['operations'] if x['Причина'] == operation['Следствие']]
                            if depended != []:
                                num = int(depended[0]['№ опер.']) - 1
                                dep_apparat = apparat
                        minus_time = 0
                        for j in range(num - 1, -1, -1):
                            minus_time -= int(dep_apparat['operations'][j]['Время'])
                        i_dep = i
                        for dep_operation in dep_apparat['operations']:
                            for j in range(int(dep_operation['Время'])):
                                if i_dep + j + minus_time < 0:
                                    continue
                                if i_dep + j + minus_time >= 21 * 24 * 60:
                                    continue
                                if work[dep_apparat['name']][i_dep + j + minus_time] == dep_operation['№ опер.'] or work[dep_apparat['name']][i_dep + j + minus_time] is None:
                                    work[dep_apparat['name']][i_dep + j + minus_time] = dep_operation['№ опер.']
                                else:
                                    self.penalty += 1
                            i_dep += int(dep_operation['Время'])
                    i += int(operation['Время'])
                cycle += 1
        for dep in apparatus['dependent']:
            i = 0
            while i < 21 * 24 * 60:
                if work[dep['name']][i] is not None:
                    if dep['operations'][int(work[dep['name']][i]) - 1]['Следствие'] != '':
                        for apparat in apparatus['dependent']:
                            operation = dep['operations'][int(work[dep['name']][i]) - 1]['Следствие']
                            depended = [x for x in apparat['operations'] if x['Причина'] == operation]
                            if depended != []:
                                num = int(depended[0]['№ опер.']) - 1
                                dep_apparat = apparat
                        minus_time = 0
                        for j in range(num - 1, -1, -1):
                            minus_time -= int(dep_apparat['operations'][j]['Время'])
                        i_dep = i
                        for dep_operation in dep_apparat['operations']:
                            for j in range(int(dep_operation['Время'])):
                                if i_dep + j + minus_time < 0:
                                    continue
                                if work[dep_apparat['name']][i_dep + j + minus_time] == dep_operation['№ опер.'] or work[dep_apparat['name']][i_dep + j + minus_time] is None:
                                    work[dep_apparat['name']][i_dep + j + minus_time] = dep_operation['№ опер.']
                                else:
                                    self.penalty += 1
                            i_dep += int(dep_operation['Время'])
                        k = work[dep['name']][i]
                        while work[dep['name']][i] == k:
                            i += 1
                i += 1
        for key in work.keys():
            work[key] = work[key][7 * 24 * 60:]
        if self.penalty:
            return False, work
        return True, work

    def create_ciclogarm(self):
        param, work = self.check_admissibility()
        if not param:
            QMessageBox.about(self, "Ошибка", "Невозможно построить циклограммы. Некорректные данные или расписание.")
            return
        apparatus = self.create_json()
        self.scene = MyScene()
        x = 200
        for j in range(2):
            for i in range(1, 8):
                GraphicPixmap = QtWidgets.QGraphicsPixmapItem()
                GraphicPixmap.setAcceptHoverEvents(True)
                pixmap = QtGui.QPixmap("days/{}.bmp".format(i))
                GraphicPixmap.setPixmap(pixmap)
                GraphicPixmap.setX(x)
                x += pixmap.width()
                self.scene.addItem(GraphicPixmap)
        x = 200
        y = pixmap.height()
        for value in apparatus:
            for apparat in apparatus[value]:
                self.scene.addRect(0, y, 200, 50, Qt.Qt.black)
                self.scene.addRect(200, y, 24 * 120 * 14, 50, Qt.Qt.black)
                text = QtWidgets.QGraphicsTextItem()
                text.setPlainText(apparat['name'])
                text.setPos(10, y + 10)
                self.scene.addItem(text)
                i = 0
                while i < 14 * 24 * 60:
                    if work[apparat['name']][i] is not None:
                        start = i * 2
                        value = work[apparat['name']][i]
                        text = QtWidgets.QGraphicsTextItem()
                        text.setPlainText(value)
                        text.setPos(x + start + 10, y + 10)
                        while i < 14 * 24 * 60 and work[apparat['name']][i] == value:
                            i += 1
                        end = i * 2
                        color = QtGui.QColor(apparat['operations'][int(value) - 1]['Цвет опер.'][0],
                                             apparat['operations'][int(value) - 1]['Цвет опер.'][1],
                                             apparat['operations'][int(value) - 1]['Цвет опер.'][2])
                        self.scene.addRect(x + start, y, end - start, 50, Qt.Qt.black, Qt.QBrush(color))
                        self.scene.addItem(text)
                        i -= 1
                    i += 1
                y += 60
        self.plot_arrow()
        self.graphicsView.setScene(self.scene)
        self.plot_utilities()

    def optmization_func(self, apparatus, start, times, utility):
        for i in range(1, self.apparatus_count1):
            time = start + times[i-1]
            day = time // (24 * 60)
            time -= day * (24 * 60)
            hour = time // 60
            minute = time - hour * 60
            apparatus['independent'][i]['operations'][0]['День пуск'] = day + 1
            apparatus['independent'][i]['operations'][0]['Т пуска(ч)'] = hour
            apparatus['independent'][i]['operations'][0]['Т пуска(м)'] = minute
        ut = 24 * 14 * 12 * [0]
        param, work = self.check_admissibility(apparatus)
        apparatus = apparatus['independent'] + apparatus['dependent']
        for apparat in apparatus:
            for i in range(0, 24 * 14 * 60, 5):
                if work[apparat['name']][i] is not None:
                    value = work[apparat['name']][i]
                    if apparat['operations'][int(value) - 1][utility] == '':
                        continue
                    ut[i // 5] += int(apparat['operations'][int(value) - 1][utility])
        return max(ut) + self.penalty ** 2


    def optimization(self):
        self.progressBar_2.setVisible(True)
        utility = self.comboBox.currentText()
        days = self.spinBox.value()
        time = self.timeEdit.text()
        hours = int(time.split(':')[0])
        minutes = int(time.split(':')[1])
        max_delta = days * 24 * 60 + hours * 60 + minutes
        apparatus = self.create_json()
        freeze_ap = apparatus['independent'][0]
        start = 24 * 60 * (int(freeze_ap['operations'][0]['День пуск']) - 1) + 60 * int(freeze_ap['operations'][0]['Т пуска(ч)']) + int(freeze_ap['operations'][0]['Т пуска(м)'])
        min_delta = - start
        times = (self.apparatus_count1 - 1) * [min_delta]
        minimum = self.optmization_func(apparatus, start, times, utility)
        min_times = times
        all_times = [i for i in range(min_delta, max_delta+5, 5)]
        N = len(all_times) ** (self.apparatus_count1 - 1)
        k = 0
        for times in product(all_times, repeat=(self.apparatus_count1 - 1)):
            if not self.run:
                break
            value = self.optmization_func(apparatus, start, times, utility)
            procent = 100 * k / N
            k += 1
            self.progressBar_2.setValue(int(procent))
            self.label_7.setText("Максимальный пик: {}".format(minimum))
            if value is None:
                continue
            if minimum is None and value is not None:
                minimum = value
                min_times = times
            if value < minimum:
                minimum = value
                min_times = times
        for i in range(1, self.apparatus_count1):
            time = start + min_times[i-1]
            day = time // (24 * 60)
            time -= day * (24 * 60)
            hour = time // 60
            minute = time - hour * 60
            apparatus['independent'][i]['operations'][0]['День пуск'] = day + 1
            apparatus['independent'][i]['operations'][0]['Т пуска(ч)'] = hour
            apparatus['independent'][i]['operations'][0]['Т пуска(м)'] = minute
        self.label_7.setText("Максимальный пик: {}".format(minimum))
        self.progressBar_2.setVisible(False)
        with open("result.json", "w") as write_file:
            json.dump(apparatus, write_file)
        self.run = False
        self.pushButton_10.setEnabled(False)
        self.pushButton_9.setEnabled(True)

    # def Genetic(self):
    #     self.progressBar_2.setVisible(True)
    #     smax = self.spinBox_4.value()
    #     tmax = self.spinBox_2.value()
    #     par = 20
    #     mutation = 5
    #     utility = self.comboBox.currentText()
    #     days = self.spinBox.value()
    #     time = self.timeEdit.text()
    #     hours = int(time.split(':')[0])
    #     minutes = int(time.split(':')[1])
    #     max_delta = days * 24 * 60 + hours * 60 + minutes
    #     apparatus = self.create_json()
    #     freeze_ap = apparatus['independent'][0]
    #     start = 24 * 60 * (int(freeze_ap['operations'][0]['День пуск']) - 1) + 60 * int(
    #         freeze_ap['operations'][0]['Т пуска(ч)']) + int(freeze_ap['operations'][0]['Т пуска(м)'])
    #     min_delta = - start
    #     times = (self.apparatus_count1 - 1) * [start]
    #     X = []
    #     X.append(times)
    #     Xmin = (self.apparatus_count1 - 1) * [min_delta]
    #     Xmax = (self.apparatus_count1 - 1) * [max_delta]
    #     for i in range(smax - 1):
    #         xi = []
    #         for j in range(len(Xmin)):
    #             xi.append(myround(Xmin[j] + random.random() * (Xmax[j] - Xmin[j])))
    #         X.append(xi)
    #     f = []
    #     for xi in X:
    #         f.append(self.optmization_func(apparatus, start, xi, utility))
    #     t = 0
    #     while t <= tmax:
    #         if not self.run:
    #             break
    #         procent = 100 * t / tmax
    #         self.progressBar_2.setValue(int(procent))
    #         new_X = []
    #         a = random.randint(0, len(X) - 1)
    #         m = random.randint(0, len(X) - 1)
    #         middle =


    def IWO(self):
        self.progressBar_2.setVisible(True)
        s0 = self.spinBox_3.value()
        smax = self.spinBox_4.value()
        nmin = self.spinBox_5.value()
        nmax = self.spinBox_6.value()
        sigma_b = self.spinBox_7.value()
        sigma_e = self.spinBox_8.value()
        m = self.spinBox_9.value()
        tmax = self.spinBox_2.value()
        utility = self.comboBox.currentText()
        days = self.spinBox.value()
        time = self.timeEdit.text()
        hours = int(time.split(':')[0])
        minutes = int(time.split(':')[1])
        max_delta = days * 24 * 60 + hours * 60 + minutes
        apparatus = self.create_json()
        freeze_ap = apparatus['independent'][0]
        start = 24 * 60 * (int(freeze_ap['operations'][0]['День пуск']) - 1) + 60 * int(freeze_ap['operations'][0]['Т пуска(ч)']) + int(freeze_ap['operations'][0]['Т пуска(м)'])
        min_delta = - max_delta
        times = (self.apparatus_count1 - 1) * [start]
        X = []
        X.append(times)
        Xmin = (self.apparatus_count1 - 1) * [min_delta]
        Xmax = (self.apparatus_count1 - 1) * [max_delta]
        for i in range(s0 - 1):
            xi = []
            for j in range(len(Xmin)):
                xi.append(myround(Xmin[j] + random.random() * (Xmax[j] - Xmin[j])))
            X.append(xi)
        f = []
        for xi in X:
            f.append(self.optmization_func(apparatus, start, xi, utility))
        t = 0
        while t < tmax:
            if not self.run:
                break
            procent = 100 * t / tmax
            self.progressBar_2.setValue(int(procent))
            n = []
            fbest = min(f)
            fworst = max(f)
            for fi in f:
                n.append(
                    round(fi * (nmax - nmin) / (fbest - fworst) + (fbest * nmin - fworst * nmax) / (fbest - fworst)))
            Xnew = []
            sigma = (((tmax - t) / tmax) ** m) * (sigma_b - sigma_e) + sigma_e
            for k in range(len(X)):
                for i in range(n[k]):
                    xj = []
                    for j in range(len(X[k])):
                        xj.append(X[k][j] + myround(np.random.normal(0, sigma)))
                        if xj[j] > Xmax[j]:
                            xj[j] = Xmax[j]
                        if xj[j] < Xmin[j]:
                            xj[j] = Xmin[j]
                    Xnew.append(xj)
            X = X + Xnew
            f = []
            for xi in X:
                f.append(self.optmization_func(apparatus, start, xi, utility))
            sort(X, f)
            if len(X) > smax:
                X = X[:smax]
                f = f[:smax]
            t += 1
            self.label_7.setText("Максимальный пик: {}".format(f[0]))
        minimum = f[0]
        min_times = X[0]
        min_times.insert(0, 0)
        min_time = min(min_times)
        if start + min_time < 0:
            delta = abs(start + min_time)
            for i in range(len(min_times)):
                min_times[i] += delta
        for i in range(0, self.apparatus_count1):
            time = start + min_times[i]
            day = time // (24 * 60)
            time -= day * (24 * 60)
            hour = time // 60
            minute = time - hour * 60
            apparatus['independent'][i]['operations'][0]['День пуск'] = day + 1
            apparatus['independent'][i]['operations'][0]['Т пуска(ч)'] = hour
            apparatus['independent'][i]['operations'][0]['Т пуска(м)'] = minute
        self.label_7.setText("Максимальный пик: {}".format(minimum))
        self.progressBar_2.setVisible(False)
        with open("result.json", "w") as write_file:
            json.dump(apparatus, write_file)
        self.run = False
        self.pushButton_10.setEnabled(False)
        self.pushButton_9.setEnabled(True)

    def start_optimization(self):
        self.run = True
        self.pushButton_10.setEnabled(True)
        self.pushButton_9.setEnabled(False)
        self.progressBar_2.setValue(0)
        if self.method == "Перебор":
            threading.Thread(target=self.optimization, name="_optimization").start()
        elif self.method == "IWO":
            threading.Thread(target=self.IWO, name="_optimization").start()

    def stop_optimization(self):
        self.run = False




def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = MyApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
