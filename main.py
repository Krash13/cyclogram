import NIR  # Это наш конвертированный файл дизайна
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from constans import LABELS, LABELS1, UNITS, COLS
import json
from fpdf import FPDF

class MyScene(QtWidgets.QGraphicsScene):

    def addArrow(self, x1, y1, x2, y2):
        self.addLine(x1, y1, x2, y2)
        self.addLine(x2, y2, x2 - 5, y2 - 5)
        self.addLine(x2, y2, x2 + 5, y2 - 5)

    def addDotted(self, x1, y1, x2, y2):
         for x in range(x1, x2, 10):
             self.addLine(x, y1, x+5, y2)

class MyApp(QtWidgets.QMainWindow, NIR.Ui_MainWindow):

    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
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
        self.pushButton_2.clicked.connect(self.create_ciclogarm1)
        self.utility = "Электричество"
        self.pushButton_3.clicked.connect(lambda: self.set_utility("Пар"))
        self.pushButton_4.clicked.connect(lambda: self.set_utility("Гор. вода"))
        self.pushButton_5.clicked.connect(lambda: self.set_utility("Хол. вода"))
        self.pushButton_6.clicked.connect(lambda: self.set_utility("Электричество"))
        self.pushButton_7.clicked.connect(self.update_utilities)
        self.pushButton_8.clicked.connect(self.create_pdf)
        self.max = 400
        self.cost = 10
        self.progressBar.setVisible(False)

    def set_utility(self, utility):
        self.utility = utility
        self.plot_utilities()

    def plot_arrow(self):
        for i in range(16,21):
            n = 0
            time = 0
            for j in range(self.tableWidget.rowCount()):
                if self.tableWidget.item(j,1) is not None and self.tableWidget.item(j,1).text()!="":
                    n += 1
                    time = (int(self.tableWidget.item(j,13).text()) -1 )*24*60
                    time += int(self.tableWidget.item(j, 12).text())
                    time += int(self.tableWidget.item(j, 11).text()) * 60
                    count = int(self.tableWidget.item(j, 14).text())

                if self.tableWidget.item(j,i) is not None and self.tableWidget.item(j,i).text()!="":
                    time_after = 0
                    time_stad = int(self.tableWidget.item(j, 6).text())
                    l = j
                    while True:
                        time_after += int(self.tableWidget.item(l, 6).text())
                        if self.tableWidget.item(l + 1, 1) is not None:
                            break
                        if self.tableWidget.item(l + 1, 4) is None:
                            break
                        l += 1
                    for k in range(self.tableWidget_2.rowCount()):
                        if self.tableWidget_2.item(k, 2) is not None and self.tableWidget_2.item(k, 2).text() != "" and self.tableWidget_2.item(k, 2).text() == self.tableWidget.item(j,i).text():
                            for cycle in range(count):
                                for l in range(0, 2*time_stad+1, 10):
                                    self.scene.addArrow(200+time*2+l+2*cycle*(time+time_after), 100+60*(n-1), 200+time*2+l+2*cycle*(time+time_after), 50+60*(int(self.tableWidget_2.item(k, 1).text())+self.apparatus_count1 - 1))
                if self.tableWidget.item(j, 6) is not None and self.tableWidget.item(j, 6).text() != "":
                    time+=int(self.tableWidget.item(j,6).text())


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

    def save(self):
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
        dependent.append(apparat)
        apparatus["dependent"] = dependent
        file = QtWidgets.QFileDialog.getSaveFileName(self, "Создание файла")
        with open(file[0]+".json", 'w') as f:
            json.dump(apparatus, f)

    def create_ciclogarm(self):
        self.scene = MyScene()
        x = 200
        for i in range(1,8):
            GraphicPixmap = QtWidgets.QGraphicsPixmapItem()
            GraphicPixmap.setAcceptHoverEvents(True)
            pixmap = QtGui.QPixmap("days/{}.bmp".format(i))
            GraphicPixmap.setPixmap(pixmap)
            GraphicPixmap.setX(x)
            x += pixmap.width()
            self.scene.addItem(GraphicPixmap)
        y = pixmap.height()
        app_cycles = {}
        for i in range(self.tableWidget.rowCount()):
            if self.tableWidget.item(i, 1) is not None:
                self.scene.addRect(0, y, 200, 50, Qt.Qt.black)
                text = QtWidgets.QGraphicsTextItem()
                text.setPlainText(self.tableWidget.item(i, 1).text())
                text.setPos(10, y+10)
                self.scene.addItem(text)
                j = i
                start_day = int(self.tableWidget.item(i, 13).text())
                x = 200 + (start_day - 1) * 24 * 120
                if self.tableWidget.item(i, 11) is not None and self.tableWidget.item(i, 11).text() != "":
                    x += 2 * 60 * int(self.tableWidget.item(i, 11).text())
                if self.tableWidget.item(i, 12) is not None and self.tableWidget.item(i, 12).text() != "":
                    x += 2 * int(self.tableWidget.item(i, 12).text())
                pixels = 24 * 120 * 7
                cicles = int(self.tableWidget.item(i, 14).text())
                app_cycles[self.tableWidget.item(i, 0).text()] = cicles
                while pixels > 0 and cicles > 0:
                    w = min(2*int(self.tableWidget.item(j, 6).text()), pixels)
                    color = self.tableWidget.item(j, 5).background().color()
                    self.scene.addRect(x, y, w, 50, Qt.Qt.black, Qt.QBrush(color))
                    text = QtWidgets.QGraphicsTextItem()
                    text.setPlainText(self.tableWidget.item(j, 3).text())
                    text.setPos(x+10, y + 10)
                    self.scene.addItem(text)
                    pixels -= w
                    x += 2 * int(self.tableWidget.item(j, 6).text())
                    if self.tableWidget.item(j+1, 1) is not None:
                        j = i
                        cicles -= 1
                        continue
                    if self.tableWidget.item(j+1, 4) is None:
                        j = i
                        cicles -= 1
                        continue
                    j += 1
                y += 60

        for i in range(self.tableWidget_2.rowCount()):
            if self.tableWidget_2.item(i, 2) is not None:
                self.scene.addRect(0, y, 200, 50, Qt.Qt.black)
                text = QtWidgets.QGraphicsTextItem()
                text.setPlainText(self.tableWidget_2.item(i, 2).text())
                text.setPos(10, y+10)
                self.scene.addItem(text)
                j = i
                time = 0
                x = 200
                dep_num = int(self.tableWidget_2.item(i, 1).text())
                while True:
                    if self.tableWidget_2.item(j, 0) is not None and self.tableWidget_2.item(j, 0).text()!='':
                        num_op = int(self.tableWidget_2.item(j, 4).text())
                        ind_num = int(self.tableWidget_2.item(j, 0).text())
                        for k in range(self.tableWidget.rowCount()):
                            if self.tableWidget.item(k, 0) is not None and int(self.tableWidget.item(k, 0).text()) == ind_num:
                                x += 2 * 24 * 60 * (int(self.tableWidget.item(i, 13).text()) - 1)
                                if self.tableWidget.item(i, 11) is not None and self.tableWidget.item(i,11).text() != "":
                                    x += 2 * 60 * int(self.tableWidget.item(i, 11).text())
                                if self.tableWidget.item(i, 12) is not None and self.tableWidget.item(i,12).text() != "":
                                    x += 2 * int(self.tableWidget.item(i, 12).text())
                                time_ind = 0
                                while self.tableWidget.item(k+1, 4) is not None:
                                    if self.tableWidget.item(k, 21).text().isdigit() and int(self.tableWidget.item(k, 21).text()) == dep_num:
                                        if self.tableWidget.item(k, 15).text().isdigit() and int(self.tableWidget.item(k, 15).text()) == num_op:
                                            break
                                    time_ind += int(self.tableWidget.item(k, 6).text())
                                    k += 1
                                time_after = 0
                                while True:
                                    k += 1
                                    time_after += int(self.tableWidget.item(k, 6).text())
                                    if self.tableWidget.item(k + 1, 1) is not None:
                                        break
                                    if self.tableWidget.item(k + 1, 4) is None:
                                        break
                                break
                        w_t = 2 * (time_ind - time)
                        self.scene.addRect(x, y, w_t, 50, Qt.Qt.black)
                        x += w_t
                        cycles = app_cycles[str(ind_num)]
                        old_j = j
                        j = i
                        while cycles > 0:
                            w = 2 * int(self.tableWidget_2.item(j, 7).text())
                            color = self.tableWidget_2.item(j, 6).background().color()
                            self.scene.addRect(x, y, w, 50, Qt.Qt.black, Qt.QBrush(color))
                            text = QtWidgets.QGraphicsTextItem()
                            text.setPlainText(self.tableWidget_2.item(j, 4).text())
                            text.setPos(x + 5, y + 10)
                            self.scene.addItem(text)
                            if j == old_j:
                                for xa in range(x, x+w+1, 10):
                                    y1 = pixmap.height() + (ind_num - 1) * 60 + 50
                                    self.scene.addArrow(xa, y1, xa, y)
                            x += w
                            if self.tableWidget_2.item(j + 1, 2) is not None:
                                j = i
                                cycles -= 1
                                self.scene.addRect(x, y, w_t + 2 * time_after, 50, Qt.Qt.black)
                                x += w_t + 2 * time_after
                                continue
                            if self.tableWidget_2.item(j + 1, 5) is None:
                                j = i
                                cycles -= 1
                                self.scene.addRect(x, y, w_t + 2 * time_after, 50, Qt.Qt.black)
                                x += w_t + 2 * time_after
                                continue
                            j += 1
                        j = old_j


                    time += int(self.tableWidget_2.item(j, 7).text())
                    if self.tableWidget_2.item(j+1, 2) is not None:
                        break
                    if self.tableWidget_2.item(j+1, 5) is None:
                        break
                    j += 1
                y += 60
        self.graphicsView.setScene(self.scene)
        #self.plot_utilities()

    def create_ciclogarm1(self):
        self.scene = MyScene()
        x = 200
        for i in range(1,8):
            GraphicPixmap = QtWidgets.QGraphicsPixmapItem()
            GraphicPixmap.setAcceptHoverEvents(True)
            pixmap = QtGui.QPixmap("days/{}.bmp".format(i))
            GraphicPixmap.setPixmap(pixmap)
            GraphicPixmap.setX(x)
            x += pixmap.width()
            self.scene.addItem(GraphicPixmap)
        y = pixmap.height()
        app_cycles = {}
        for i in range(self.tableWidget.rowCount()):
            if self.tableWidget.item(i, 1) is not None:
                self.scene.addRect(0, y, 200, 50, Qt.Qt.black)
                text = QtWidgets.QGraphicsTextItem()
                text.setPlainText(self.tableWidget.item(i, 1).text())
                text.setPos(10, y+10)
                self.scene.addItem(text)
                j = i
                start_day = int(self.tableWidget.item(i, 13).text())
                x = 200 + (start_day - 1) * 24 * 120
                if self.tableWidget.item(i, 11) is not None and self.tableWidget.item(i, 11).text() != "":
                    x += 2 * 60 * int(self.tableWidget.item(i, 11).text())
                if self.tableWidget.item(i, 12) is not None and self.tableWidget.item(i, 12).text() != "":
                    x += 2 * int(self.tableWidget.item(i, 12).text())
                pixels = 24 * 120 * 7
                cicles = int(self.tableWidget.item(i, 14).text())
                app_cycles[self.tableWidget.item(i, 0).text()] = cicles
                while pixels > 0 and cicles > 0:
                    w = min(2*int(self.tableWidget.item(j, 6).text()), pixels)
                    color = self.tableWidget.item(j, 5).background().color()
                    self.scene.addRect(x, y, w, 50, Qt.Qt.black, Qt.QBrush(color))
                    text = QtWidgets.QGraphicsTextItem()
                    text.setPlainText(self.tableWidget.item(j, 3).text())
                    text.setPos(x+10, y + 10)
                    self.scene.addItem(text)
                    pixels -= w
                    x += 2 * int(self.tableWidget.item(j, 6).text())
                    if self.tableWidget.item(j+1, 1) is not None:
                        j = i
                        cicles -= 1
                        continue
                    if self.tableWidget.item(j+1, 4) is None:
                        j = i
                        cicles -= 1
                        continue
                    j += 1
                y += 60
        events = {}
        for i in range(self.tableWidget_2.rowCount()):
            if self.tableWidget_2.item(i, 2) is not None:
                self.scene.addRect(0, y, 200, 50, Qt.Qt.black)
                text = QtWidgets.QGraphicsTextItem()
                text.setPlainText(self.tableWidget_2.item(i, 2).text())
                text.setPos(10, y+10)
                self.scene.addItem(text)
                j = i
                x = 200
                while True:
                    if self.tableWidget_2.item(j, 0) is not None and self.tableWidget_2.item(j, 0).text() != '':
                        events[self.tableWidget_2.item(j, 0).text()] = y
                    if self.tableWidget_2.item(j+1, 2) is not None:
                        break
                    if self.tableWidget_2.item(j+1, 5) is None:
                        break
                    j += 1
                y += 60

        dep_dep = {}
        for i in range(self.tableWidget.rowCount()):
            if self.tableWidget.item(i, 21) is not None and self.tableWidget.item(i, 21).text().isdigit():
                num = self.tableWidget.item(i, 21).text()
                y = events[self.tableWidget.item(i, 21).text()]
                x = 200
                j = i
                time_ind = 0
                while self.tableWidget.item(j, 0) is None:
                    j -= 1
                    time_ind += int(self.tableWidget.item(j, 6).text())
                x += 2 * 24 * 60 * (int(self.tableWidget.item(j, 13).text()) - 1)
                time_minus = 2 * 24 * 60 * (int(self.tableWidget.item(j, 13).text()) - 1)
                cycles = int(self.tableWidget.item(j, 14).text())
                time_minus2 = 0
                if self.tableWidget.item(j, 11) is not None and self.tableWidget.item(j, 11).text() != "":
                    x += 2 * 60 * int(self.tableWidget.item(j, 11).text())
                    time_minus2 += 2 * 60 * int(self.tableWidget.item(j, 11).text())
                if self.tableWidget.item(j, 12) is not None and self.tableWidget.item(j, 12).text() != "":
                    x += 2 * int(self.tableWidget.item(j, 12).text())
                    time_minus2 += 2 * int(self.tableWidget.item(j, 12).text())
                x_start = x - 200
                time_after = 0
                k = i
                while True:
                    k += 1
                    time_after += int(self.tableWidget.item(k, 6).text())
                    if self.tableWidget.item(k + 1, 1) is not None:
                        break
                    if self.tableWidget.item(k + 1, 4) is None:
                        break
                for j in range(self.tableWidget_2.rowCount()):
                    if self.tableWidget_2.item(j,0) is not None and self.tableWidget_2.item(j,0).text() == num:
                        time = 0
                        k = j
                        while self.tableWidget_2.item(k, 1) is None:
                            k -= 1
                            time += int(self.tableWidget_2.item(k, 7).text())
                        w_t = 2 * (time_ind - time)
                        self.scene.addRect(x, y, w_t, 50, Qt.Qt.black)
                        x += w_t
                        old_k = k
                        k = j
                        while True:
                            k += 1
                            if self.tableWidget_2.item(k, 5) is None:
                                break
                            if self.tableWidget_2.item(k, 1) is not None:
                                break
                            time_after -= int(self.tableWidget_2.item(k, 7).text())



                        k = old_k
                        all_cycles = cycles
                        while cycles > 0:
                            if self.tableWidget_2.item(k, 18) is not None and self.tableWidget_2.item(k, 18).text().isdigit():
                                dep_dep["{};{}".format(k,i)] = (all_cycles, w_t, time_after, x_start, time_minus, time_minus2)
                            w = 2 * int(self.tableWidget_2.item(k, 7).text())
                            color = self.tableWidget_2.item(k, 6).background().color()
                            self.scene.addRect(x, y, w, 50, Qt.Qt.black, Qt.QBrush(color))
                            text = QtWidgets.QGraphicsTextItem()
                            text.setPlainText(self.tableWidget_2.item(k, 4).text())
                            text.setPos(x + 5, y + 10)
                            self.scene.addItem(text)
                            x += w
                            if self.tableWidget_2.item(k + 1, 2) is not None:
                                k = old_k
                                cycles -= 1
                                self.scene.addRect(x, y, w_t + 2 * time_after, 50, Qt.Qt.black)
                                x += w_t + 2 * time_after
                                continue
                            if self.tableWidget_2.item(k + 1, 5) is None:
                                k = old_k
                                cycles -= 1
                                self.scene.addRect(x, y, w_t + 2 * time_after, 50, Qt.Qt.black)
                                x += w_t + 2 * time_after
                                continue
                            k += 1

        for i in range(self.tableWidget_2.rowCount()):
            if self.tableWidget_2.item(i, 18) is not None and self.tableWidget_2.item(i, 18).text().isdigit():
                num = self.tableWidget_2.item(i, 18).text()
                y = events[self.tableWidget_2.item(i, 18).text()]
                x = 200
                j = i
                time_ind = 0
                while self.tableWidget_2.item(j, 1) is None:
                    j -= 1
                    time_ind += int(self.tableWidget_2.item(j, 7).text())
                for key in dep_dep.keys():
                    if key.startswith(num):
                        cycles = dep_dep[key][0]
                        wt = dep_dep[key][1] + dep_dep[key][3]
                        time_after = dep_dep[key][2]
                        time_minus = dep_dep[key][4]
                        time_minus2 = dep_dep[key][5]
                        for j in range(self.tableWidget_2.rowCount()):
                            if self.tableWidget_2.item(j,0) is not None and self.tableWidget_2.item(j,0).text() == num:
                                time = 0
                                k = j
                                while self.tableWidget_2.item(k, 1) is None:
                                    k -= 1
                                    time += int(self.tableWidget_2.item(k, 7).text())
                                w_t = 2 * (time_ind - time) + wt
                                self.scene.addRect(x, y, w_t, 50, Qt.Qt.black)
                                x += w_t
                                if w_t - wt < 0:
                                    if w_t < 0:
                                        w_t = 2 * (time - abs(w_t))
                                    else:
                                        temp = (wt - w_t)
                                        w_t += (wt - w_t)
                                        w_t += 2 * (time - abs(temp)) - time_minus2
                                old_k = k
                                k = j
                                while True:
                                    k += 1
                                    if self.tableWidget_2.item(k, 5) is None:
                                        break
                                    if self.tableWidget_2.item(k, 1) is not None:
                                        break
                                    time_after -= int(self.tableWidget_2.item(k, 7).text())
                                k = old_k
                                while cycles > 0:
                                    w = 2 * int(self.tableWidget_2.item(k, 7).text())
                                    color = self.tableWidget_2.item(k, 6).background().color()
                                    self.scene.addRect(x, y, w, 50, Qt.Qt.black, Qt.QBrush(color))
                                    text = QtWidgets.QGraphicsTextItem()
                                    text.setPlainText(self.tableWidget_2.item(k, 4).text())
                                    text.setPos(x + 5, y + 10)
                                    self.scene.addItem(text)
                                    x += w
                                    if self.tableWidget_2.item(k + 1, 2) is not None:
                                        k = old_k
                                        cycles -= 1
                                        self.scene.addRect(x, y, w_t + 2 * time_after - time_minus, 50, Qt.Qt.black)
                                        x += w_t + 2 * time_after - time_minus
                                        continue
                                    if self.tableWidget_2.item(k + 1, 5) is None:
                                        k = old_k
                                        cycles -= 1
                                        self.scene.addRect(x, y, w_t + 2 * time_after - time_minus, 50, Qt.Qt.black)
                                        x += w_t + 2 * time_after - time_minus
                                        continue
                                    k += 1

        self.plot_arrow()
        self.graphicsView.setScene(self.scene)
        return self.plot_utilities1(dep_dep)

    def plot_utilities1(self, dep_dep):
        self.label.setText(UNITS[self.utility])
        self.label_2.setText("Потребление: {}".format(self.utility))
        self.scene2 = MyScene()
        x = 50
        for i in range(1,8):
            GraphicPixmap = QtWidgets.QGraphicsPixmapItem()
            GraphicPixmap.setAcceptHoverEvents(True)
            pixmap = QtGui.QPixmap("days/{}.bmp".format(i))
            GraphicPixmap.setPixmap(pixmap)
            GraphicPixmap.setX(x)
            x += pixmap.width()
            self.scene2.addItem(GraphicPixmap)
        y = pixmap.height()
        ys = []
        ut = []
        for i in range(24 * 7 * 12):
            ys.append(pixmap.height())
            ut.append(0)
        j = i
        apparatus = []
        for i in range(self.tableWidget.rowCount()):
            if self.tableWidget.item(i, 1) is not None:
                apparat = {}
                apparat["color"] = self.tableWidget.item(i, 2).background().color()
                apparat["cycles"] = int(self.tableWidget.item(i, 14).text())
                apparat["start"] = 24 * 60 * (int(self.tableWidget.item(i, 13).text()) - 1)
                if self.tableWidget.item(i, 11) is not None and self.tableWidget.item(i, 11).text() != "":
                    apparat["start"] += 60 * int(self.tableWidget.item(i, 11).text())
                if self.tableWidget.item(i, 12) is not None and self.tableWidget.item(i, 12).text() != "":
                    apparat["start"] += int(self.tableWidget.item(i, 12).text())
                j = i
                apparat["times"] = []
                apparat["utilities"] = []
                while True:
                    apparat["times"].append(
                        int(self.tableWidget.item(j, 6).text())
                    )
                    if self.tableWidget.item(j, COLS[self.utility]) is not None and self.tableWidget.item(j, COLS[self.utility]).text() != "":
                        apparat["utilities"].append(int(self.tableWidget.item(j, COLS[self.utility]).text()))
                    else:
                        apparat["utilities"].append(0)
                    if self.tableWidget.item(j+1, 1) is not None:
                        break
                    if self.tableWidget.item(j+1, 4) is None:
                        break
                    j += 1
                apparat["full_time"] = sum(apparat["times"])
                apparatus.append(apparat)
        x = 50
        for i in range(24 * 7 * 12):
            for apparat in apparatus:
                if i*5 >= apparat["start"] and i*5 < apparat["cycles"] * apparat["full_time"] + apparat["start"]:
                    current_cycle = (i*5 - apparat["start"])//apparat["full_time"]
                    time = current_cycle * apparat["full_time"] + apparat["start"]
                    for j in range(len(apparat["times"])):
                        time += apparat["times"][j]
                        if i * 5 < time:
                            h = 25 * apparat["utilities"][j]//(self.cost)
                            self.scene2.addRect(x + i * pixmap.width()//(24*12), ys[i], pixmap.width()//(24*12), h, Qt.Qt.black,Qt.QBrush(apparat["color"]))
                            ut[i] += apparat["utilities"][j]
                            ys[i] += h
                            break


        apparatus = []
        for i in range(self.tableWidget.rowCount()):
            if self.tableWidget.item(i, 21) is not None and self.tableWidget.item(i, 21).text().isdigit():
                num = self.tableWidget.item(i, 21).text()
                j = i
                time_ind = 0
                while self.tableWidget.item(j, 0) is None:
                    j -= 1
                    time_ind += int(self.tableWidget.item(j, 6).text())
                time_ind += 24 * 60 * (int(self.tableWidget.item(j, 13).text()) - 1)
                time_minus = 24 * 60 * (int(self.tableWidget.item(j, 13).text()) - 1)
                if self.tableWidget.item(j, 11) is not None and self.tableWidget.item(j, 11).text() != "":
                    time_ind += 60 * int(self.tableWidget.item(j, 11).text())
                    time_minus += 60 * int(self.tableWidget.item(j, 11).text())
                if self.tableWidget.item(j, 12) is not None and self.tableWidget.item(j, 12).text() != "":
                    time_ind += int(self.tableWidget.item(j, 12).text())
                    time_minus += int(self.tableWidget.item(j, 12).text())

                apparat = {}
                apparat["cycles"] = int(self.tableWidget.item(j, 14).text())
                time_minus2 = 0
                if self.tableWidget.item(j, 11) is not None and self.tableWidget.item(j, 11).text() != "":
                    x += 2 * 60 * int(self.tableWidget.item(j, 11).text())
                    time_minus2 += 2 * 60 * int(self.tableWidget.item(j, 11).text())
                if self.tableWidget.item(j, 12) is not None and self.tableWidget.item(j, 12).text() != "":
                    x += 2 * int(self.tableWidget.item(j, 12).text())
                    time_minus2 += 2 * int(self.tableWidget.item(j, 12).text())
                time_after = 0
                k = i
                while True:
                    k += 1
                    time_after += int(self.tableWidget.item(k, 6).text())
                    if self.tableWidget.item(k + 1, 1) is not None:
                        break
                    if self.tableWidget.item(k + 1, 4) is None:
                        break

                for j in range(self.tableWidget_2.rowCount()):
                    if self.tableWidget_2.item(j, 0) is not None and self.tableWidget_2.item(j, 0).text() == num:
                        time = 0
                        old_j = j
                        while self.tableWidget.item(j, 1) is None:
                            j -= 1
                            time += int(self.tableWidget_2.item(j, 7).text())
                        apparat["color"] = self.tableWidget_2.item(j, 3).background().color()
                        apparat["times"] = []
                        apparat["utilities"] = []
                        k = old_j
                        old_j = j
                        while True:
                            k += 1
                            if self.tableWidget_2.item(k, 5) is None:
                                break
                            if self.tableWidget_2.item(k, 1) is not None:
                                break
                            time_after -= int(self.tableWidget_2.item(k, 7).text())
                        j = old_j
                        while True:
                            apparat["times"].append(
                                int(self.tableWidget_2.item(j, 7).text())
                            )
                            if self.tableWidget_2.item(j, COLS[self.utility] + 1) is not None and self.tableWidget_2.item(j, COLS[self.utility] + 1).text() != "":
                                apparat["utilities"].append(int(self.tableWidget_2.item(j, COLS[self.utility] + 1).text()))
                            else:
                                apparat["utilities"].append(0)
                            if self.tableWidget_2.item(j+1, 2) is not None:
                                break
                            if self.tableWidget_2.item(j+1, 5) is None:
                                break
                            j += 1
                        apparat["start"] = (time_ind - time)
                        apparat["pause"] = time_after + apparat["start"] - time_minus
                        apparat["full_time"] = sum(apparat["times"])
                        apparatus.append(apparat)

        for apparat in apparatus:
            for cycle in range(apparat["cycles"]):
                start_time = apparat["start"] + cycle * ( apparat["full_time"] + apparat["pause"])
                end_time = start_time + apparat["full_time"]
                for i in range(start_time // 5, end_time // 5):
                    time = start_time
                    for j in range(len(apparat["times"])):
                        time += apparat["times"][j]
                        if i * 5 < time:
                            h = 25 * apparat["utilities"][j] // (self.cost)
                            self.scene2.addRect(x + i * pixmap.width() // (24 * 12), ys[i], pixmap.width() // (24 * 12),
                                                h, Qt.Qt.black, Qt.QBrush(apparat["color"]))
                            ut[i] += apparat["utilities"][j]
                            ys[i] += h
                            break

        apparatus = []
        for i in range(self.tableWidget_2.rowCount()):
            if self.tableWidget_2.item(i, 18) is not None and self.tableWidget_2.item(i, 18).text().isdigit():
                apparat = {}
                num = self.tableWidget_2.item(i, 18).text()
                j = i
                time_ind = 0
                while self.tableWidget_2.item(j, 1) is None:
                    j -= 1
                    time_ind += int(self.tableWidget_2.item(j, 7).text())
                time_ind += 24 * 60 * (int(self.tableWidget.item(j, 13).text()) - 1)
                if self.tableWidget.item(j, 11) is not None and self.tableWidget.item(j, 11).text() != "":
                    time_ind += 60 * int(self.tableWidget.item(j, 11).text())
                if self.tableWidget.item(j, 12) is not None and self.tableWidget.item(j, 12).text() != "":
                    time_ind += int(self.tableWidget.item(j, 12).text())
                for key in dep_dep.keys():
                    if key.startswith(num):
                        apparat["cycles"] = dep_dep[key][0]
                        wt = dep_dep[key][1] + dep_dep[key][3] // 2
                        time_after = dep_dep[key][2]
                        time_minus = dep_dep[key][4]
                        time_minus2 = dep_dep[key][5]
                        for j in range(self.tableWidget_2.rowCount()):
                            if self.tableWidget_2.item(j, 0) is not None and self.tableWidget_2.item(j,
                                                                                                     0).text() == num:
                                time = 0
                                old_j = j
                                while self.tableWidget.item(j, 1) is None:
                                    j -= 1
                                    time += int(self.tableWidget_2.item(j, 7).text())
                                apparat["color"] = self.tableWidget_2.item(j, 3).background().color()
                                apparat["times"] = []
                                apparat["utilities"] = []
                                k = old_j
                                old_j = j
                                while True:
                                    k += 1
                                    if self.tableWidget_2.item(k, 5) is None:
                                        break
                                    if self.tableWidget_2.item(k, 1) is not None:
                                        break
                                    time_after -= int(self.tableWidget_2.item(k, 7).text())
                                j = old_j
                                while True:
                                    apparat["times"].append(
                                        int(self.tableWidget_2.item(j, 7).text())
                                    )
                                    if self.tableWidget_2.item(j, COLS[
                                                                      self.utility] + 1) is not None and self.tableWidget_2.item(
                                            j, COLS[self.utility] + 1).text() != "":
                                        apparat["utilities"].append(
                                            int(self.tableWidget_2.item(j, COLS[self.utility] + 1).text()))
                                    else:
                                        apparat["utilities"].append(0)
                                    if self.tableWidget_2.item(j + 1, 2) is not None:
                                        break
                                    if self.tableWidget_2.item(j + 1, 5) is None:
                                        break
                                    j += 1
                                w_t = 2 * (time_ind - time) + wt
                                self.scene.addRect(x, y, w_t, 50, Qt.Qt.black)
                                x += w_t
                                if w_t - wt < 0:
                                    if w_t < 0:
                                        w_t = (time - abs(w_t))
                                    else:
                                        temp = (wt - w_t)
                                        w_t += (wt - w_t)
                                        w_t += (time - abs(temp)) - time_minus2 // 2
                                apparat["start"] = w_t
                                apparat["pause"] = time_after + apparat["start"] - time_minus
                                apparat["full_time"] = sum(apparat["times"])
                                apparatus.append(apparat)

        for apparat in apparatus:
            for cycle in range(apparat["cycles"]):
                start_time = apparat["start"] + cycle * ( apparat["full_time"] + apparat["pause"])
                end_time = start_time + apparat["full_time"]
                for i in range(start_time // 5, end_time // 5):
                    time = start_time
                    for j in range(len(apparat["times"])):
                        time += apparat["times"][j]
                        if i * 5 < time:
                            h = 25 * apparat["utilities"][j] // (self.cost)
                            try:
                                self.scene2.addRect(x + i * pixmap.width() // (24 * 12), ys[i], pixmap.width() // (24 * 12),
                                                    h, Qt.Qt.black, Qt.QBrush(apparat["color"]))

                                ut[i] += apparat["utilities"][j]
                                ys[i] += h
                            except:
                                pass
                            break

        for i in range(0, self.max + 1, self.cost):
            text = QtWidgets.QGraphicsTextItem()
            text.setPlainText(str(i))
            text.setPos(0, y - 10)
            self.scene2.addItem(text)
            self.scene2.addLine(30, y, 50, y)
            self.scene2.addDotted(50, y, 7*pixmap.width()+50, y)
            y += 25
        self.graphicsView_2.setScene(self.scene2)
        return ut

    def plot_utilities(self):
        self.label.setText(UNITS[self.utility])
        self.label_2.setText("Потребление: {}".format(self.utility))
        self.scene2 = MyScene()
        x = 50
        for i in range(1,8):
            GraphicPixmap = QtWidgets.QGraphicsPixmapItem()
            GraphicPixmap.setAcceptHoverEvents(True)
            pixmap = QtGui.QPixmap("days/{}.bmp".format(i))
            GraphicPixmap.setPixmap(pixmap)
            GraphicPixmap.setX(x)
            x += pixmap.width()
            self.scene2.addItem(GraphicPixmap)
        y = pixmap.height()
        ys = []
        ut = []
        for i in range(24 * 7 * 12):
            ys.append(pixmap.height())
            ut.append(0)
        j = i
        apparatus = []
        for i in range(self.tableWidget.rowCount()):
            if self.tableWidget.item(i, 1) is not None:
                apparat = {}
                apparat["color"] = self.tableWidget.item(i, 2).background().color()
                apparat["cycles"] = int(self.tableWidget.item(i, 14).text())
                apparat["start"] = 24 * 60 * (int(self.tableWidget.item(i, 13).text()) - 1)
                if self.tableWidget.item(i, 11) is not None and self.tableWidget.item(i, 11).text() != "":
                    apparat["start"] += 60 * int(self.tableWidget.item(i, 11).text())
                if self.tableWidget.item(i, 12) is not None and self.tableWidget.item(i, 12).text() != "":
                    apparat["start"] += int(self.tableWidget.item(i, 12).text())
                j = i
                apparat["times"] = []
                apparat["utilities"] = []
                while True:
                    apparat["times"].append(
                        int(self.tableWidget.item(j, 6).text())
                    )
                    if self.tableWidget.item(j, COLS[self.utility]) is not None and self.tableWidget.item(j, COLS[self.utility]).text() != "":
                        apparat["utilities"].append(int(self.tableWidget.item(j, COLS[self.utility]).text()))
                    else:
                        apparat["utilities"].append(0)
                    if self.tableWidget.item(j+1, 1) is not None:
                        break
                    if self.tableWidget.item(j+1, 4) is None:
                        break
                    j += 1
                apparat["full_time"] = sum(apparat["times"])
                apparatus.append(apparat)
        x = 50
        for i in range(24 * 7 * 12):
            for apparat in apparatus:
                if i*5 >= apparat["start"] and i*5 < apparat["cycles"] * apparat["full_time"] + apparat["start"]:
                    current_cycle = (i*5 - apparat["start"])//apparat["full_time"]
                    time = current_cycle * apparat["full_time"] + apparat["start"]
                    for j in range(len(apparat["times"])):
                        time += apparat["times"][j]
                        if i * 5 < time:
                            h = 25 * apparat["utilities"][j]//(self.cost)
                            self.scene2.addRect(x + i * pixmap.width()//(24*12), ys[i], pixmap.width()//(24*12), h, Qt.Qt.black,Qt.QBrush(apparat["color"]))
                            ut[i] += apparat["utilities"][j]
                            ys[i] += h
                            break


        apparatus = []
        for i in range(self.tableWidget_2.rowCount()):
            if self.tableWidget_2.item(i, 2) is not None:
                apparat = {}
                apparat["color"] = self.tableWidget_2.item(i, 3).background().color()
                apparat["times"] = []
                apparat["utilities"] = []
                dep_num = int(self.tableWidget_2.item(i, 1).text())
                j = i
                time = 0
                while True:
                    apparat["times"].append(
                        int(self.tableWidget_2.item(j, 7).text())
                    )
                    if self.tableWidget_2.item(j, COLS[self.utility] + 1) is not None and self.tableWidget_2.item(j, COLS[self.utility] + 1).text() != "":
                        apparat["utilities"].append(int(self.tableWidget_2.item(j, COLS[self.utility] + 1).text()))
                    else:
                        apparat["utilities"].append(0)
                    if self.tableWidget_2.item(j, 0) is not None and self.tableWidget_2.item(j, 0).text()!='':
                        num_op = int(self.tableWidget_2.item(j, 4).text())
                        ind_num = int(self.tableWidget_2.item(j, 0).text())
                        for k in range(self.tableWidget.rowCount()):
                            if self.tableWidget.item(k, 0) is not None and int(self.tableWidget.item(k, 0).text()) == ind_num:
                                apparat["cycles"] = int(self.tableWidget.item(k, 14).text())
                                time_ind = 24 * 60 * (int(self.tableWidget.item(k, 13).text()) - 1)
                                if self.tableWidget.item(k, 11) is not None and self.tableWidget.item(k,11).text() != "":
                                    time_ind += 60 * int(self.tableWidget.item(k, 11).text())
                                if self.tableWidget.item(k, 12) is not None and self.tableWidget.item(k,12).text() != "":
                                    time_ind += int(self.tableWidget.item(k, 12).text())
                                time_minus = time_ind
                                while self.tableWidget.item(k+1, 4) is not None:
                                    if self.tableWidget.item(k, 21).text().isdigit() and int(self.tableWidget.item(k, 21).text()) == dep_num:
                                        if self.tableWidget.item(k, 15).text().isdigit() and int(self.tableWidget.item(k, 15).text()) == num_op:
                                            break
                                    time_ind += int(self.tableWidget.item(k, 6).text())
                                    k += 1
                                time_after = 0
                                while True:
                                    k += 1
                                    time_after += int(self.tableWidget.item(k, 6).text())
                                    if self.tableWidget.item(k + 1, 1) is not None:
                                        break
                                    if self.tableWidget.item(k + 1, 4) is None:
                                        break
                                break
                        apparat["start"] = (time_ind - time)
                        apparat["pause"] = time_after + apparat["start"] - time_minus
                    time += int(self.tableWidget_2.item(j, 7).text())
                    if self.tableWidget_2.item(j+1, 2) is not None:
                        break
                    if self.tableWidget_2.item(j+1, 5) is None:
                        break
                    j += 1
                apparat["full_time"] = sum(apparat["times"])
                apparatus.append(apparat)

        for apparat in apparatus:
            for cycle in range(apparat["cycles"]):
                start_time = apparat["start"] + cycle * ( apparat["full_time"] + apparat["pause"])
                end_time = start_time + apparat["full_time"]
                for i in range(start_time // 5, end_time // 5):
                    time = start_time
                    for j in range(len(apparat["times"])):
                        time += apparat["times"][j]
                        if i * 5 < time:
                            h = 25 * apparat["utilities"][j] // (self.cost)
                            self.scene2.addRect(x + i * pixmap.width() // (24 * 12), ys[i], pixmap.width() // (24 * 12),
                                                h, Qt.Qt.black, Qt.QBrush(apparat["color"]))
                            ut[i] += apparat["utilities"][j]
                            ys[i] += h
                            break


        for i in range(0, self.max + 1, self.cost):
            text = QtWidgets.QGraphicsTextItem()
            text.setPlainText(str(i))
            text.setPos(0, y - 10)
            self.scene2.addItem(text)
            self.scene2.addLine(30, y, 50, y)
            self.scene2.addDotted(50, y, 7*pixmap.width()+50, y)
            y += 25
        self.graphicsView_2.setScene(self.scene2)
        return ut

    def create_pdf(self):
        file = QtWidgets.QFileDialog.getSaveFileName(self, "Создание файла")
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
            ut = self.create_ciclogarm1()
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
        self.create_ciclogarm1()
        pdf.output(file[0]+".pdf")
        self.progressBar.setVisible(False)
        self.setEnabled(True)

    def load(self):
        data = {}
        self.apparatus_count1 = 0
        self.operation_count1 = 0
        file = QtWidgets.QFileDialog.getOpenFileName(self, "Выбор файла")
        with open(file[0], "r") as read_file:
            data = json.load(read_file)
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
                        self.tableWidget.item(j, k).setText(apparat["operations"][j-i][self.tableWidget.horizontalHeaderItem(k).text()])
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
        self.create_ciclogarm1()

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



def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = MyApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
