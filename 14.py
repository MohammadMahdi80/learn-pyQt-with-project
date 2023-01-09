
import sys
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import re
import numpy as np
from natsort import natsorted
import os
from functools import partial
from PySide6 import *
import openpyxl 
import pickle
from PySide6.QtPrintSupport import *
from sympy import E
import random


NUMBER_OF_PARAMETER = 0
NUMBER_OF_SIMULATION = 0
STARTING_SIMULATION_NUMBER = 0
ENDING_SIMULATION_NUMBER = 0
NUMBER_OF_OBSERVED_VARIABLE = 0
NUMBER_OF_DATA_POINTS = 0
NUMBER_OF_OBSERVED_VARIABLE2 = 0
NUMBER_OF_DATA_POINTS2 = 0
NUMBER_OF_OBSERVED_VARIABLE3 = 0
NUMBER_OF_DATA_POINTS3 = 0
BEGINNING_YEAR_OF_SIMULATION = 0
WARMUP_PERIOD = 0
END_YEAR_OF_SIMULATION = 0
NUMBER_OF_VARIABLE_TO_GET = 0
TOTAL_NUMBER_OF_REACHES = 0
BEGINNING_YEAR_OF_SIMULATION2 = 0
WARMUP_PERIOD2 = 0
END_YEAR_OF_SIMULATION2 = 0
NUMBER_OF_VARIABLE_TO_GET2 = 0
TOTAL_NUMBER_OF_REACHES2 = 0
BEGINNING_YEAR_OF_SIMULATION3 = 0
WARMUP_PERIOD3 = 0
END_YEAR_OF_SIMULATION3 = 0
NUMBER_OF_VARIABLE_TO_GET3 = 0
TOTAL_NUMBER_OF_REACHES3 = 0
NUMBER_OF_OBSERVED_VARIABLE_MAIN = 0
OBJECTIVE_FUNCTION_TYPE = 0
NUMBER_OF_DATA_POINTS_MAIN = 0

BEGINNING_YEAR_OF_SIMULATION_NOT_INCLUDING_THE_WARM_UP = 0
BEGINNING_YEAR_OF_SIMULATION_NOT_INCLUDING_THE_WARM_UP2 = 0
BEGINNING_YEAR_OF_SIMULATION_NOT_INCLUDING_THE_WARM_UP3 = 0

width = 0
height = 0

mouse = ''


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


vline = resource_path('vline.png').replace('\\', '/')
branch_closed = resource_path('branch-closed.png').replace('\\', '/')
branch_more = resource_path('branch-more.png').replace('\\', '/')
branch_open = resource_path('branch-open.png').replace('\\', '/')
branch_end = resource_path('branch-end.png').replace('\\', '/')

style = '''QTreeWidget {
            color: #FFFFFF;
            background-color: #33373B;
            font-size: 18px;
            }

            QTreeWidget::item:selected {
            background-color: #2ABf9E;
            }

            QTreeView::branch:open:has-children:has-siblings {
                background: transparent;
            }

            QTreeView::branch:has-siblings:!adjoins-item {
            border-image: url(''' + vline + ''') 0;
            }

            QTreeView::branch:has-siblings:adjoins-item {
            border-image: url(''' + branch_more + ''') 0;
            }

            QTreeView::branch:!has-children:!has-siblings:adjoins-item {
            border-image: url(''' + branch_end + ''') 0;
            }

            QTreeView::branch:has-children:!has-siblings:closed,
            QTreeView::branch:closed:has-children:has-siblings {
                border-image: none;
                image: url(''' + branch_closed + ''');
            }

            QTreeView::branch:open:has-children:!has-siblings,
            QTreeView::branch:open:has-children:has-siblings  {
            border-image: none;
            image: url(''' + branch_open + ''');
            }'''

exc = resource_path('exc.png')
co = resource_path('co.png')
en = resource_path('en.png')


class MySwitch(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setMinimumWidth(66)
        self.setMinimumHeight(22)

    def paintEvent(self, event):
        label = "YES" if self.isChecked() else "NO"
        bg_color = Qt.green if self.isChecked() else Qt.red

        radius = 15
        width = 37
        center = self.rect().center()

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(center)
        painter.setBrush(QColor(0, 0, 0))

        pen = QPen(Qt.black)
        pen.setWidth(2)
        painter.setPen(pen)

        painter.drawRoundedRect(QRect(-width, -radius, 2 * width, 2 * radius), radius, radius)
        painter.setBrush(QBrush(bg_color))
        sw_rect = QRect(-radius, -radius, width + radius, 2 * radius)
        if not self.isChecked():
            sw_rect.moveLeft(-width)
        painter.drawRoundedRect(sw_rect, radius, radius)
        painter.drawText(sw_rect, Qt.AlignCenter, label)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

    def mouseMoveEvent(self, e):
        self.label.setText("mouseMoveEvent")

    def mousePressEvent(self, e):
        self.label.setText("mousePressEvent")

    def mouseReleaseEvent(self, e):
        self.label.setText("mouseReleaseEvent")

    def mouseDoubleClickEvent(self, e):
        self.label.setText("mouseDoubleClickEvent")


class Widget(QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)

        # flag for check if window already opened or not
        self.Par_inf_flg = 0
        self.Sufi2_swEdit_flg = 0
        self.observed_rch_flg = 0
        self.observed_hru_flg = 0
        self.observed_sub_flg = 0
        self.Var_file_rch_flg = 0
        self.Var_file_hru_flg = 0
        self.Var_file_sub_flg = 0
        self.STUFI2_extract_rch_def_flg = 0
        self.STUFI2_extract_hru_def_flg = 0
        self.STUFI2_extract_sub_def_flg = 0
        self.observed_flg = 0
        self.Var_file_name_txt_flg = 0

        # for check QLineEdit
        self.list_label_tik1 = list()

        self.list_label_tik2 = list()

        self.list_label_tik3 = list()

        self.list_label_tik4 = list()

        self.list_label_tik6 = list()

        self.list_label_tik7 = list()

        self.list_label_tik8 = list()

        self.list_label_tik7 = list()

        self.list_label_tik8 = list()

        self.list_of_stations = list()

        self.list_of_stations2 = list()

        self.list_of_stations3 = list()

        self.number_of_observed_variable_ = 0

        self.number_of_observed_variable_2 = 0

        self.number_of_observed_variable_3 = 0

        self.number_of_observed_variable_12 = 0

        self.list_label_tik12 = list()

        self.list_label_tik13 = list()

        # _________________________________ create main widget _______________________________
        self.main_widget1 = QWidget()
        self.main_widget2 = QWidget()
        self.main_widget3 = QWidget()
        self.main_widget4 = QWidget()
        self.main_widget5 = QWidget()
        self.main_widget6 = QWidget()
        self.main_widget7 = QWidget()
        self.main_widget8 = QWidget()
        self.main_widget9 = QWidget()
        self.main_widget10 = QWidget()
        self.main_widget11 = QWidget()
        self.main_widget12 = QWidget()
        self.main_widget13 = QWidget()

        self.stackedWidget = QStackedWidget()
        self.stackedWidget.addWidget(self.main_widget1)
        self.stackedWidget.addWidget(self.main_widget2)
        self.stackedWidget.addWidget(self.main_widget3)
        self.stackedWidget.addWidget(self.main_widget4)
        self.stackedWidget.addWidget(self.main_widget5)
        self.stackedWidget.addWidget(self.main_widget6)
        self.stackedWidget.addWidget(self.main_widget7)
        self.stackedWidget.addWidget(self.main_widget8)
        self.stackedWidget.addWidget(self.main_widget9)
        self.stackedWidget.addWidget(self.main_widget10)
        self.stackedWidget.addWidget(self.main_widget11)
        self.stackedWidget.addWidget(self.main_widget12)
        self.stackedWidget.addWidget(self.main_widget13)

        # __________________________________ create tree view ______________________________
        self.tree = QTreeWidget()
        self.tree.setStyleSheet(style)
        self.tree.setColumnCount(1)
        self.tree.setHeaderLabels(['Calibration Input'])
        self.tree.resize(0.146 * width, 0.833 * height)

        items = list()

        items.append(QTreeWidgetItem(['Par_inf.txt']))

        items.append(QTreeWidgetItem(['Sufi2_swEdit.def']))

        item = QTreeWidgetItem(['Observation'])
        child1 = QTreeWidgetItem(['observed_rch.txt'])
        child2 = QTreeWidgetItem(['observed_hru.txt'])
        child3 = QTreeWidgetItem(['observed_sub.txt'])
        item.addChildren([child1, child2, child3])
        items.append(item)

        item = QTreeWidgetItem(['Extraction'])
        child1 = QTreeWidgetItem(['Var_file_rch.txt'])
        child2 = QTreeWidgetItem(['Var_file_hru.txt'])
        child3 = QTreeWidgetItem(['Var_file_sub.txt'])
        child4 = QTreeWidgetItem(['STUFI2_extract_rch_def'])
        child5 = QTreeWidgetItem(['STUFI2_extract_hru_def'])
        child6 = QTreeWidgetItem(['STUFI2_extract_sub_def'])
        item.addChildren([child1, child2, child3, child4, child5, child6])
        items.append(item)

        item = QTreeWidgetItem(['objective function'])
        child1 = QTreeWidgetItem(['observed'])
        child2 = QTreeWidgetItem(['Var_file_name_txt'])
        item.addChildren([child1, child2])
        items.append(item)

        self.tree.itemClicked.connect(self.handle)
        self.tree.insertTopLevelItems(0, items)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.tree, 1)
        self.layout.addWidget(self.stackedWidget, 4)

        self.setLayout(self.layout)

    @Slot(QTreeWidgetItem, int)
    def handle(self, item, column):
        if item.text(column) == 'Par_inf.txt':
            self.stackedWidget.setCurrentIndex(0)

            if not self.Par_inf_flg:
                label1 = QLabel('Number Of Parameters : ', self.main_widget1)
                label1.setStyleSheet(f'font-size: {int(0.015 * width)}px;')
                label1.resize(int(0.22 * width), int(0.039 * height))
                label1.move(int(0.022 * width), int(0.039 * height))
                label1.show()

                label2 = QLabel('Number Of Simulation : ', self.main_widget1)
                label2.setStyleSheet(f'font-size: {int(0.015 * width)}px;')
                label2.resize(int(0.22 * width), int(0.039 * height))
                label2.move(int(0.022 * width), int(0.104 * height))
                label2.show()

                self.edit_line11 = QLineEdit(self.main_widget1)
                self.edit_line11.move(int(0.195 * width), int(0.039 * height))
                self.edit_line11.resize(int(0.151 * width), int(0.039 * height))
                self.edit_line11.textChanged.connect(self.delete_label_tik11)
                self.edit_line11.show()

                self.edit_line12 = QLineEdit(self.main_widget1)
                self.edit_line12.move(int(0.195 * width), int(0.104 * height))
                self.edit_line12.resize(int(0.151 * width), int(0.039 * height))
                self.edit_line12.textChanged.connect(self.delete_label_tik12)
                self.edit_line12.show()

                button1 = QPushButton('OK', self.main_widget1)
                button1.move(int(0.368 * width), int(0.039 * height))
                button1.resize(int(0.022 * width), int(0.039 * height))
                button1.clicked.connect(self.number_of_parameter)
                button1.show()

                button2 = QPushButton('OK', self.main_widget1)
                button2.move(int(0.368 * width), int(0.104 * height))
                button2.resize(int(0.022 * width), int(0.039 * height))
                button2.clicked.connect(self.number_of_simulation)
                button2.show()

                self.Par_inf_flg = 1

        if item.text(column) == 'Sufi2_swEdit.def':
            self.stackedWidget.setCurrentIndex(1)
            self.edit_line21 = QLineEdit(self.main_widget2)
            self.edit_line21.move(int(0.215 * width), int(0.039 * height))
            self.edit_line21.resize(int(0.051 * width), int(0.039 * height))
            self.edit_line21.setText(str(1))
            self.edit_line21.setReadOnly(True)
            # self.edit_line21.textChanged.connect(self.delete_label_tik21)
            self.edit_line21.show()
            
            STARTING_SIMULATION_NUMBER = 1
            global NUMBER_OF_PARAMETER
            global END_YEAR_OF_SIMULATION
            END_YEAR_OF_SIMULATION = NUMBER_OF_PARAMETER
            self.edit_line22 = QLineEdit(self.main_widget2)
            self.edit_line22.move(int(0.215 * width), int(0.154 * height))
            self.edit_line22.resize(int(0.051 * width), int(0.039 * height))
            self.edit_line22.setText(str(END_YEAR_OF_SIMULATION))
            self.edit_line22.setReadOnly(True)
            # self.edit_line22.textChanged.connect(self.delete_label_tik22)
            self.edit_line22.show()
            if not self.Sufi2_swEdit_flg:
                label1 = QLabel('Starting Simulation Number : ', self.main_widget2)
                label1.setStyleSheet(f'font-size: {int(0.015 * width)}px;')
                label1.resize(int(0.22 * width), int(0.039 * height))
                label1.move(int(0.022 * width), int(0.039 * height))
                label1.show()

                label2 = QLabel('Ending Simulation Number : ', self.main_widget2)
                label2.setStyleSheet(f'font-size: {int(0.015 * width)}px;')
                label2.resize(int(0.22 * width), int(0.039 * height))
                label2.move(int(0.022 * width), int(0.154 * height))
                label2.show()

                
                
                # button1 = QPushButton('OK', self.main_widget2)
                # button1.move(int(0.288 * width), int(0.039 * height))
                # button1.resize(int(0.022 * width), int(0.039 * height))
                # button1.clicked.connect(self.starting_simulation_number)
                # button1.show()

                # button2 = QPushButton('OK', self.main_widget2)
                # button2.move(int(0.288 * width), int(0.154 * height))
                # button2.resize(int(0.022 * width), int(0.039 * height))
                # button2.clicked.connect(self.ending_simulation_number)
                # button2.show()

                self.Sufi2_swEdit_flg = 1

        if item.text(column) == 'observed_rch.txt':
            self.stackedWidget.setCurrentIndex(2)

            if not self.observed_rch_flg:
                img_label = QLabel(self.main_widget3)
                pix = QPixmap(resource_path('question.png'))
                img_label.setPixmap(pix)
                img_label.resize(int(0.026 * width), int(0.04 * height))
                img_label.move(int(0.7 * width), int(0.05 * height))
                img_label.show()

                label = QLabel(self.main_widget3)
                label.setText('آیا دیتا از جنس Rch دارید؟')
                label.setStyleSheet(f'color:darkblue ;font-size: {int(0.018 * width)}px')
                label.move(int(0.5 * width), int(0.05 * height))
                label.show()

                self.switch_btn = MySwitch(self.main_widget3)
                self.switch_btn.move(int(0.4 * width), int(0.055 * height))
                self.switch_btn.resize(int(0.057 * width), int(0.046 * height))
                self.switch_btn.setStyleSheet('border-radius: 10px')
                self.switch_btn.clicked.connect(self.switch_btn_function)
                self.switch_btn.show()

                self.observed_rch_flg = 1

        if item.text(column) == 'observed_hru.txt':
            self.stackedWidget.setCurrentIndex(3)

            if not self.observed_hru_flg:
                img_label = QLabel(self.main_widget4)
                pix = QPixmap(resource_path('question.png'))
                img_label.setPixmap(pix)
                img_label.resize(int(0.026 * width), int(0.04 * height))
                img_label.move(int(0.7 * width), int(0.05 * height))
                img_label.show()

                label = QLabel(self.main_widget4)
                label.setText('آیا دیتا از جنس Hru دارید؟')
                label.setStyleSheet(f'color:darkblue ;font-size: {int(0.018 * width)}px')
                label.move(int(0.5 * width), int(0.05 * height))
                label.show()

                self.switch_btn2 = MySwitch(self.main_widget4)
                self.switch_btn2.move(int(0.4 * width), int(0.055 * height))
                self.switch_btn2.resize(int(0.057 * width), int(0.046 * height))
                self.switch_btn2.setStyleSheet('border-radius: 10px')
                self.switch_btn2.clicked.connect(self.switch_btn_function2)
                self.switch_btn2.show()

                self.observed_hru_flg = 1

        if item.text(column) == 'observed_sub.txt':
            self.stackedWidget.setCurrentIndex(4)

            if not self.observed_sub_flg:
                img_label = QLabel(self.main_widget5)
                pix = QPixmap(resource_path('question.png'))
                img_label.setPixmap(pix)
                img_label.resize(int(0.026 * width), int(0.04 * height))
                img_label.move(int(0.7 * width), int(0.05 * height))
                img_label.show()

                label = QLabel(self.main_widget5)
                label.setText('آیا دیتا از جنس Sub دارید؟')
                label.setStyleSheet(f'color:darkblue ;font-size: {int(0.018 * width)}px')
                label.move(int(0.5 * width), int(0.05 * height))
                label.show()

                self.switch_btn3 = MySwitch(self.main_widget5)
                self.switch_btn3.move(int(0.4 * width), int(0.055 * height))
                self.switch_btn3.resize(int(0.057 * width), int(0.046 * height))
                self.switch_btn3.setStyleSheet('border-radius: 10px')
                self.switch_btn3.clicked.connect(self.switch_btn_function3)
                self.switch_btn3.show()

                self.observed_sub_flg = 1

        if item.text(column) == 'Var_file_rch.txt':
            self.stackedWidget.setCurrentIndex(5)

            if not self.Var_file_rch_flg:
                if self.switch_btn.isChecked():
                    self.window6 = QWidget(self.main_widget6)
                    self.window6.resize(int(0.385 * width), int(NUMBER_OF_OBSERVED_VARIABLE * 0.065 * height + 10))
                    self.window6.show()

                    self.scroll6 = QScrollArea(self.main_widget6)
                    self.scroll6.resize(int(0.4 * width), int(0.79 * height))
                    self.scroll6.move(int(0.001 * width), int(0.1 * height))
                    self.scroll6.setWidget(self.window6)
                    self.scroll6.show()

                    label1 = QLabel('input variable name with  .txt : ', self.main_widget6)
                    label1.setStyleSheet(f'font-size: {int(0.015 * width)}px;')
                    label1.resize(int(0.24 * width), int(0.039 * height))
                    label1.move(int(0.001 * width), int(0.039 * height))
                    label1.show()

                    self.edit_list6 = list()
                    for i in range(NUMBER_OF_OBSERVED_VARIABLE):
                        label = QLabel(f'{i + 1}', self.window6)
                        label.setStyleSheet(f'font-size: {int(0.013 * width)}px; color:red;'
                                            f' background :burlywood;'
                                            f'border-radius: 10px')
                        label.setAlignment(Qt.AlignCenter)
                        label.resize(int(0.02 * width), int(0.04 * height))
                        label.move(int(0.002 * width), int(i * 0.065 * height + 10))
                        label.show()

                        edit1 = QLineEdit(self.window6)
                        edit1.setStyleSheet('background: white')
                        edit1.resize(int(0.234 * width), int(0.039 * height))
                        edit1.move(int(0.025 * width), int(i * 0.065 * height + 10))
                        edit1.show()
                        self.edit_list6.append(edit1)

                    btn = QPushButton('Confirm', self.main_widget6)
                    btn.resize(int(0.051 * width), int(0.039 * height))
                    btn.move(int(0.659 * width), int(0.781 * height))
                    btn.clicked.connect(self.confirm6)
                    btn.show()

                    self.Var_file_rch_flg = 1
                else:
                    self.scroll6.close()
                    self.window6.close()

        if item.text(column) == 'Var_file_hru.txt':
            self.stackedWidget.setCurrentIndex(6)

            if not self.Var_file_hru_flg:
                if self.switch_btn2.isChecked():
                    self.window7 = QWidget(self.main_widget7)
                    self.window7.resize(int(0.385 * width), int(NUMBER_OF_OBSERVED_VARIABLE2 * 0.065 * height + 10))
                    self.window7.show()

                    self.scroll7 = QScrollArea(self.main_widget7)
                    self.scroll7.resize(int(0.4 * width), int(0.79 * height))
                    self.scroll7.move(int(0.001 * width), int(0.1 * height))
                    self.scroll7.setWidget(self.window7)
                    self.scroll7.show()

                    label1 = QLabel('input variable name with  .txt : ', self.main_widget7)
                    label1.setStyleSheet(f'font-size: {int(0.015 * width)}px;')
                    label1.resize(int(0.24 * width), int(0.039 * height))
                    label1.move(int(0.001 * width), int(0.039 * height))
                    label1.show()

                    self.edit_list7 = list()
                    for i in range(NUMBER_OF_OBSERVED_VARIABLE2):
                        label = QLabel(f'{i + 1}', self.window7)
                        label.setStyleSheet(f'font-size: {int(0.013 * width)}px; color:red;'
                                            f' background :burlywood;'
                                            f'border-radius: 10px')
                        label.setAlignment(Qt.AlignCenter)
                        label.resize(int(0.02 * width), int(0.04 * height))
                        label.move(int(0.002 * width), int(i * 0.065 * height + 10))
                        label.show()

                        edit1 = QLineEdit(self.window7)
                        edit1.setStyleSheet('background: white')
                        edit1.resize(int(0.234 * width), int(0.039 * height))
                        edit1.move(int(0.025 * width), int(i * 0.065 * height + 10))
                        edit1.show()
                        self.edit_list7.append(edit1)

                    btn = QPushButton('Confirm', self.main_widget7)
                    btn.resize(int(0.051 * width), int(0.039 * height))
                    btn.move(int(0.659 * width), int(0.781 * height))
                    btn.clicked.connect(self.confirm7)
                    btn.show()

                    self.Var_file_hru_flg = 1
                else:
                    self.scroll7.close()
                    self.window7.close()

        if item.text(column) == 'Var_file_sub.txt':
            self.stackedWidget.setCurrentIndex(7)

            if not self.Var_file_sub_flg:
                if self.switch_btn3.isChecked():
                    self.window8 = QWidget(self.main_widget8)
                    self.window8.resize(int(0.385 * width), int(NUMBER_OF_OBSERVED_VARIABLE3 * 0.065 * height + 10))
                    self.window8.show()

                    self.scroll8 = QScrollArea(self.main_widget8)
                    self.scroll8.resize(int(0.4 * width), int(0.79 * height))
                    self.scroll8.move(int(0.001 * width), int(0.1 * height))
                    self.scroll8.setWidget(self.window8)
                    self.scroll8.show()

                    label1 = QLabel('input variable name with  .txt : ', self.main_widget8)
                    label1.setStyleSheet(f'font-size: {int(0.015 * width)}px;')
                    label1.resize(int(0.24 * width), int(0.039 * height))
                    label1.move(int(0.001 * width), int(0.039 * height))
                    label1.show()

                    self.edit_list8 = list()
                    for i in range(NUMBER_OF_OBSERVED_VARIABLE3):
                        label = QLabel(f'{i + 1}', self.window8)
                        label.setStyleSheet(f'font-size: {int(0.013 * width)}px; color:red;'
                                            f' background :burlywood;'
                                            f'border-radius: 10px')
                        label.setAlignment(Qt.AlignCenter)
                        label.resize(int(0.02 * width), int(0.04 * height))
                        label.move(int(0.002 * width), int(i * 0.065 * height + 10))
                        label.show()

                        edit1 = QLineEdit(self.window8)
                        edit1.setStyleSheet('background: white')
                        edit1.resize(int(0.234 * width), int(0.039 * height))
                        edit1.move(int(0.025 * width), int(i * 0.065 * height + 10))
                        edit1.show()
                        self.edit_list8.append(edit1)

                    btn = QPushButton('Confirm', self.main_widget8)
                    btn.resize(int(0.051 * width), int(0.039 * height))
                    btn.move(int(0.659 * width), int(0.781 * height))
                    btn.clicked.connect(self.confirm8)
                    btn.show()

                    self.Var_file_sub_flg = 1
                else:
                    self.scroll8.close()
                    self.window8.close()

        if item.text(column) == 'STUFI2_extract_rch_def':
            self.stackedWidget.setCurrentIndex(8)

            if not self.STUFI2_extract_rch_def_flg:
                if self.switch_btn.isChecked():
                    self.main_window9 = QWidget(self.main_widget9)
                    self.main_window9.resize(int(0.76 * width), int(0.87 * height))
                    self.main_window9.show()

                    self.main_scroll9 = QScrollArea(self.main_widget9)
                    self.main_scroll9.resize(int(0.78 * width), int(0.89 * height))
                    self.main_scroll9.setWidget(self.main_window9)
                    self.main_scroll9.show()

                    label1 = QLabel('Beginning year of simulation : ', self.main_window9)
                    label1.setStyleSheet(f'font-size: {int(0.015 * width)}px;')
                    label1.resize(int(0.24 * width), int(0.039 * height))
                    label1.move(int(0.022 * width), int(0.039 * height))
                    label1.show()

                    self.edit_line91 = QLineEdit(self.main_window9)
                    self.edit_line91.move(int(0.22 * width), int(0.039 * height))
                    self.edit_line91.resize(int(0.051 * width), int(0.039 * height))
                    self.edit_line91.textChanged.connect(self.delete_label_tik91)
                    self.edit_line91.show()

                    button1 = QPushButton('OK', self.main_window9)
                    button1.move(int(0.282 * width), int(0.039 * height))
                    button1.resize(int(0.022 * width), int(0.039 * height))
                    button1.clicked.connect(self.beginning_year_of_simulation)
                    button1.show()

                    label2 = QLabel('warmup period (number of year) : ', self.main_window9)
                    label2.setStyleSheet(f'font-size: {int(0.015 * width)}px;')
                    label2.resize(int(0.24 * width), int(0.039 * height))
                    label2.move(int(0.022 * width), int(0.104 * height))
                    label2.show()

                    self.edit_line92 = QLineEdit(self.main_window9)
                    self.edit_line92.move(int(0.245 * width), int(0.104 * height))
                    self.edit_line92.resize(int(0.051 * width), int(0.039 * height))
                    self.edit_line92.textChanged.connect(self.delete_label_tik92)
                    self.edit_line92.show()

                    button2 = QPushButton('OK', self.main_window9)
                    button2.move(int(0.302 * width), int(0.104 * height))
                    button2.resize(int(0.022 * width), int(0.039 * height))
                    button2.clicked.connect(self.warmup_period)
                    button2.show()

                    label3 = QLabel('End year of simulation : ', self.main_window9)
                    label3.setStyleSheet(f'font-size: {int(0.015 * width)}px;')
                    label3.resize(int(0.21 * width), int(0.039 * height))
                    label3.move(int(0.022 * width), int(0.169 * height))
                    label3.show()

                    self.edit_line93 = QLineEdit(self.main_window9)
                    self.edit_line93.move(int(0.18 * width), int(0.169 * height))
                    self.edit_line93.resize(int(0.051 * width), int(0.039 * height))
                    self.edit_line93.textChanged.connect(self.delete_label_tik93)
                    self.edit_line93.show()

                    button3 = QPushButton('OK', self.main_window9)
                    button3.move(int(0.242 * width), int(0.169 * height))
                    button3.resize(int(0.022 * width), int(0.039 * height))
                    button3.clicked.connect(self.end_year_of_simulation)
                    button3.show()

                    label4 = QLabel('number of variable to get : ', self.main_window9)
                    label4.setStyleSheet(f'font-size: {int(0.015 * width)}px;')
                    label4.resize(int(0.21 * width), int(0.039 * height))
                    label4.move(int(0.022 * width), int(0.234 * height))
                    label4.show()

                    self.edit_line94 = QLineEdit(self.main_window9)
                    self.edit_line94.move(int(0.2 * width), int(0.234 * height))
                    self.edit_line94.resize(int(0.051 * width), int(0.039 * height))
                    self.edit_line94.textChanged.connect(self.delete_label_tik94)
                    self.edit_line94.show()

                    button4 = QPushButton('OK', self.main_window9)
                    button4.move(int(0.262 * width), int(0.234 * height))
                    button4.resize(int(0.022 * width), int(0.039 * height))
                    button4.clicked.connect(self.number_of_variable_to_get)
                    button4.show()

                    self.STUFI2_extract_rch_def_flg = 1

        if item.text(column) == 'STUFI2_extract_hru_def':
            self.stackedWidget.setCurrentIndex(9)

            if not self.STUFI2_extract_hru_def_flg:
                if self.switch_btn2.isChecked():
                    self.main_window10 = QWidget(self.main_widget10)
                    self.main_window10.resize(int(0.76 * width), int(0.87 * height))
                    self.main_window10.show()

                    self.main_scroll10 = QScrollArea(self.main_widget10)
                    self.main_scroll10.resize(int(0.78 * width), int(0.89 * height))
                    self.main_scroll10.setWidget(self.main_window10)
                    self.main_scroll10.show()

                    label1 = QLabel('Beginning year of simulation : ', self.main_window10)
                    label1.setStyleSheet(f'font-size: {int(0.015 * width)}px;')
                    label1.resize(int(0.24 * width), int(0.039 * height))
                    label1.move(int(0.022 * width), int(0.039 * height))
                    label1.show()

                    self.edit_line101 = QLineEdit(self.main_window10)
                    self.edit_line101.move(int(0.22 * width), int(0.039 * height))
                    self.edit_line101.resize(int(0.051 * width), int(0.039 * height))
                    self.edit_line101.textChanged.connect(self.delete_label_tik101)
                    self.edit_line101.show()

                    button1 = QPushButton('OK', self.main_window10)
                    button1.move(int(0.282 * width), int(0.039 * height))
                    button1.resize(int(0.022 * width), int(0.039 * height))
                    button1.clicked.connect(self.beginning_year_of_simulation2)
                    button1.show()

                    label2 = QLabel('warmup period (number of year) : ', self.main_window10)
                    label2.setStyleSheet(f'font-size: {int(0.015 * width)}px;')
                    label2.resize(int(0.24 * width), int(0.039 * height))
                    label2.move(int(0.022 * width), int(0.104 * height))
                    label2.show()

                    self.edit_line102 = QLineEdit(self.main_window10)
                    self.edit_line102.move(int(0.245 * width), int(0.104 * height))
                    self.edit_line102.resize(int(0.051 * width), int(0.039 * height))
                    self.edit_line102.textChanged.connect(self.delete_label_tik102)
                    self.edit_line102.show()

                    button2 = QPushButton('OK', self.main_window10)
                    button2.move(int(0.302 * width), int(0.104 * height))
                    button2.resize(int(0.022 * width), int(0.039 * height))
                    button2.clicked.connect(self.warmup_period2)
                    button2.show()

                    label3 = QLabel('End year of simulation : ', self.main_window10)
                    label3.setStyleSheet(f'font-size: {int(0.015 * width)}px;')
                    label3.resize(int(0.21 * width), int(0.039 * height))
                    label3.move(int(0.022 * width), int(0.169 * height))
                    label3.show()

                    self.edit_line103 = QLineEdit(self.main_window10)
                    self.edit_line103.move(int(0.18 * width), int(0.169 * height))
                    self.edit_line103.resize(int(0.051 * width), int(0.039 * height))
                    self.edit_line103.textChanged.connect(self.delete_label_tik103)
                    self.edit_line103.show()

                    button3 = QPushButton('OK', self.main_window10)
                    button3.move(int(0.242 * width), int(0.169 * height))
                    button3.resize(int(0.022 * width), int(0.039 * height))
                    button3.clicked.connect(self.end_year_of_simulation2)
                    button3.show()

                    label4 = QLabel('number of variable to get : ', self.main_window10)
                    label4.setStyleSheet(f'font-size: {int(0.015 * width)}px;')
                    label4.resize(int(0.21 * width), int(0.039 * height))
                    label4.move(int(0.022 * width), int(0.234 * height))
                    label4.show()

                    self.edit_line104 = QLineEdit(self.main_window10)
                    self.edit_line104.move(int(0.2 * width), int(0.234 * height))
                    self.edit_line104.resize(int(0.051 * width), int(0.039 * height))
                    self.edit_line104.textChanged.connect(self.delete_label_tik104)
                    self.edit_line104.show()

                    button4 = QPushButton('OK', self.main_window10)
                    button4.move(int(0.262 * width), int(0.234 * height))
                    button4.resize(int(0.022 * width), int(0.039 * height))
                    button4.clicked.connect(self.number_of_variable_to_get2)
                    button4.show()

                    self.STUFI2_extract_hru_def_flg = 1

        if item.text(column) == 'STUFI2_extract_sub_def':
            self.stackedWidget.setCurrentIndex(10)

            if not self.STUFI2_extract_sub_def_flg:
                if self.switch_btn3.isChecked():
                    self.main_window11 = QWidget(self.main_widget11)
                    self.main_window11.resize(int(0.76 * width), int(0.87 * height))
                    self.main_window11.show()

                    self.main_scroll11 = QScrollArea(self.main_widget11)
                    self.main_scroll11.resize(int(0.78 * width), int(0.89 * height))
                    self.main_scroll11.setWidget(self.main_window11)
                    self.main_scroll11.show()

                    label1 = QLabel('Beginning year of simulation : ', self.main_window11)
                    label1.setStyleSheet(f'font-size: {int(0.015 * width)}px;')
                    label1.resize(int(0.24 * width), int(0.039 * height))
                    label1.move(int(0.022 * width), int(0.039 * height))
                    label1.show()

                    self.edit_line111 = QLineEdit(self.main_window11)
                    self.edit_line111.move(int(0.22 * width), int(0.039 * height))
                    self.edit_line111.resize(int(0.051 * width), int(0.039 * height))
                    self.edit_line111.textChanged.connect(self.delete_label_tik111)
                    self.edit_line111.show()

                    button1 = QPushButton('OK', self.main_window11)
                    button1.move(int(0.282 * width), int(0.039 * height))
                    button1.resize(int(0.022 * width), int(0.039 * height))
                    button1.clicked.connect(self.beginning_year_of_simulation3)
                    button1.show()

                    label2 = QLabel('warmup period (number of year) : ', self.main_window11)
                    label2.setStyleSheet(f'font-size: {int(0.015 * width)}px;')
                    label2.resize(int(0.24 * width), int(0.039 * height))
                    label2.move(int(0.022 * width), int(0.104 * height))
                    label2.show()

                    self.edit_line112 = QLineEdit(self.main_window11)
                    self.edit_line112.move(int(0.245 * width), int(0.104 * height))
                    self.edit_line112.resize(int(0.051 * width), int(0.039 * height))
                    self.edit_line112.textChanged.connect(self.delete_label_tik112)
                    self.edit_line112.show()

                    button2 = QPushButton('OK', self.main_window11)
                    button2.move(int(0.302 * width), int(0.104 * height))
                    button2.resize(int(0.022 * width), int(0.039 * height))
                    button2.clicked.connect(self.warmup_period3)
                    button2.show()

                    label3 = QLabel('End year of simulation : ', self.main_window11)
                    label3.setStyleSheet(f'font-size: {int(0.015 * width)}px;')
                    label3.resize(int(0.21 * width), int(0.039 * height))
                    label3.move(int(0.022 * width), int(0.169 * height))
                    label3.show()

                    self.edit_line113 = QLineEdit(self.main_window11)
                    self.edit_line113.move(int(0.18 * width), int(0.169 * height))
                    self.edit_line113.resize(int(0.051 * width), int(0.039 * height))
                    self.edit_line113.textChanged.connect(self.delete_label_tik113)
                    self.edit_line113.show()

                    button3 = QPushButton('OK', self.main_window11)
                    button3.move(int(0.242 * width), int(0.169 * height))
                    button3.resize(int(0.022 * width), int(0.039 * height))
                    button3.clicked.connect(self.end_year_of_simulation3)
                    button3.show()

                    label4 = QLabel('number of variable to get : ', self.main_window11)
                    label4.setStyleSheet(f'font-size: {int(0.015 * width)}px;')
                    label4.resize(int(0.21 * width), int(0.039 * height))
                    label4.move(int(0.022 * width), int(0.234 * height))
                    label4.show()

                    self.edit_line114 = QLineEdit(self.main_window11)
                    self.edit_line114.move(int(0.2 * width), int(0.234 * height))
                    self.edit_line114.resize(int(0.051 * width), int(0.039 * height))
                    self.edit_line114.textChanged.connect(self.delete_label_tik114)
                    self.edit_line114.show()

                    button4 = QPushButton('OK', self.main_window11)
                    button4.move(int(0.262 * width), int(0.234 * height))
                    button4.resize(int(0.022 * width), int(0.039 * height))
                    button4.clicked.connect(self.number_of_variable_to_get3)
                    button4.show()

                    self.STUFI2_extract_sub_def_flg = 1

        if item.text(column) == 'observed':
            self.stackedWidget.setCurrentIndex(11)

            if not self.observed_flg:
                self.main_window12 = QWidget(self.main_widget12)
                self.main_window12.resize(int(0.76 * width), int(1.5 * height))
                self.main_window12.show()

                self.main_scroll12 = QScrollArea(self.main_widget12)
                self.main_scroll12.resize(int(0.78 * width), int(0.89 * height))
                self.main_scroll12.setWidget(self.main_window12)
                self.main_scroll12.show()

                label1 = QLabel('number of observed variable : ', self.main_window12)
                label1.setStyleSheet(f'font-size: {int(0.015 * width)}px;')
                label1.resize(int(0.24 * width), int(0.039 * height))
                label1.move(int(0.022 * width), int(0.039 * height))
                label1.show()

                self.edit_line121 = QLineEdit(self.main_window12)
                self.edit_line121.move(int(0.22 * width), int(0.039 * height))
                self.edit_line121.resize(int(0.051 * width), int(0.039 * height))
                self.edit_line121.textChanged.connect(self.delete_label_tik121)
                self.edit_line121.show()

                button1 = QPushButton('OK', self.main_window12)
                button1.move(int(0.282 * width), int(0.039 * height))
                button1.resize(int(0.022 * width), int(0.039 * height))
                button1.clicked.connect(self.number_of_observed_variable_main)
                button1.show()

                self.observed_flg = 1

        if item.text(column) == 'Var_file_name_txt':
            self.stackedWidget.setCurrentIndex(12)

            if not self.Var_file_name_txt_flg:
                self.window13 = QWidget(self.main_widget13)
                self.window13.resize(int(0.385 * width), int(NUMBER_OF_OBSERVED_VARIABLE_MAIN * 0.065 * height + 10))
                self.window13.show()

                self.scroll13 = QScrollArea(self.main_widget13)
                self.scroll13.resize(int(0.4 * width), int(0.79 * height))
                self.scroll13.move(int(0.001 * width), int(0.053 * height))
                self.scroll13.setWidget(self.window13)
                self.scroll13.show()

                self.edit_list13 = list()
                for i in range(NUMBER_OF_OBSERVED_VARIABLE_MAIN):
                    label = QLabel(f'{i + 1}', self.window13)
                    label.setStyleSheet(f'font-size: {int(0.013 * width)}px; color:red;'
                                        f' background :burlywood;'
                                        f'border-radius: 10px')
                    label.setAlignment(Qt.AlignCenter)
                    label.resize(int(0.02 * width), int(0.04 * height))
                    label.move(int(0.002 * width), int(i * 0.065 * height + 10))
                    label.show()

                    edit1 = QLineEdit(self.window13)
                    edit1.setStyleSheet('background: white')
                    edit1.resize(int(0.234 * width), int(0.039 * height))
                    edit1.move(int(0.025 * width), int(i * 0.065 * height + 10))
                    edit1.show()
                    self.edit_list13.append(edit1)

                btn = QPushButton('Confirm', self.main_widget13)
                btn.resize(int(0.051 * width), int(0.039 * height))
                btn.move(int(0.659 * width), int(0.781 * height))
                btn.clicked.connect(self.confirm13)
                btn.show()
            else:
                self.scroll13.close()
                self.window13.close()

    # Par_inf.txt
    def number_of_parameter(self):
        global NUMBER_OF_PARAMETER
        self.window1 = QWidget(self.main_widget1)
        self.labeltik11 = QLabel(self.main_widget1)
        # self.labeltik11.enterEvent = self.show_error
        try:
            int(self.edit_line11.text())
            NUMBER_OF_PARAMETER = int(self.edit_line11.text())
            pix = QPixmap(resource_path('tik.png'))
            self.labeltik11.setPixmap(pix)
            self.labeltik11.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik11.move(int(0.43 * width), int(0.039 * height))
            self.labeltik11.show()
        except:
            pix = QPixmap(exc)
            self.labeltik11.setPixmap(pix)
            self.labeltik11.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik11.move(int(0.43 * width), int(0.039 * height))
            self.labeltik11.mousePressEvent = partial(self.do_something, self.main_widget1, 0, 0, en)
            self.labeltik11.show()

        self.window1.resize(int(0.512 * width), int(NUMBER_OF_PARAMETER * 0.065 * height))
        self.window1.move(int(0.021 * width), int(0.169 * height))

        scroll = QScrollArea(self.main_widget1)
        scroll.resize(int(0.526 * width), int(0.638 * height))
        scroll.move(int(0.021 * width), int(0.169 * height))

        self.edit_list1 = list()
        if NUMBER_OF_PARAMETER:
            for i in range(NUMBER_OF_PARAMETER):
                label = QLabel(f'{i + 1}', self.window1)
                label.setStyleSheet(f'font-size: {int(0.013 * width)}px; color:red;'
                                    f' background :burlywood;'
                                    f'border-radius: 10px')
                label.setAlignment(Qt.AlignCenter)
                label.resize(int(0.02 * width), int(0.04 * height))
                label.move(int(0.005 * width), int(0.013 * height + i * 0.065 * height))

                edit2 = QLineEdit(self.window1)
                edit2.setStyleSheet('background: white')
                edit2.resize(int(0.434 * width), int(0.039 * height))
                edit2.move(int(0.025 * width), int(0.013 * height + i * 0.065 * height))
                edit2.setReadOnly(False)
                edit2.textChanged.connect(self.separation)
                self.edit_list1.append(edit2)
                edit2.show()

            self.edit_list1[0].setPlaceholderText('Paste all data here')

            scroll.setWidget(self.window1)

            btn = QPushButton('Confirm', self.main_widget1)
            btn.resize(int(0.051 * width), int(0.039 * height))
            btn.move(int(0.659 * width), int(0.781 * height))
            btn.clicked.connect(self.confirm1)
            btn.show()

            scroll.show()

    def separation(self, n):
        if len(n.split('\n')) >= 2:
            edit_list = n.split('\n')
            k = 0
            for i in self.edit_list1:
                i.clear()
            for i in self.edit_list1:
                for j in range(k, len(edit_list)):
                    if len(edit_list[j].replace('\n','').replace(' ', '')) !=0:
                        i.setText(edit_list[j])
                        break
                    k += 1
                k += 1
            
    def confirm1(self):
        try:
            self.final_label.close()
        except:
            self.final_label = QLabel(self.main_widget1)

        if self.list_label_tik1:
            for i in self.list_label_tik1:
                i.close()

        j = 0
        counter = 0

        for i in self.edit_list1:
            if i.text():
                label = QLabel(self.window1)
                pix = QPixmap(resource_path('tik.png'))
                label.setPixmap(pix)
                label.resize(int(0.026 * width), int(0.04 * height))
                label.move(int(0.464 * width), int(0.013 * height + j * 0.065 * height))
                label.show()
                self.list_label_tik1.append(label)
                counter += 1
            else:
                label = QLabel(self.window1)
                pix = QPixmap(exc)
                label.setPixmap(pix)
                label.resize(int(0.026 * width), int(0.04 * height))
                label.move(int(0.464 * width), int(0.013 * height + j * 0.065 * height))
                label.mousePressEvent = partial(self.do_something, self.main_widget1, 0, 0, en)
                label.show()
                self.list_label_tik1.append(label)

            j += 1
        
        if len(self.edit_list1) == counter and NUMBER_OF_SIMULATION:
            print(NUMBER_OF_SIMULATION)
            self.final_label.setText('successfully')
            self.final_label.setStyleSheet(f'font-size: {int(0.02 * width)}px'
                                           f'; color:orangered;'
                                           f'background: lime;border-radius: 10px;'
                                           f'font: italic;')
            self.final_label.move(int(0.61 * width), int(0.701 * height))
            self.final_label.resize(int(0.15 * width), int(0.04 * height))
            self.final_label.setAlignment(Qt.AlignCenter)
            self.final_label.show()
        elif not NUMBER_OF_SIMULATION and len(self.edit_list1) == counter:
            self.final_label.setText('enter the number of simulation')
            self.final_label.setStyleSheet(f'font-size: {int(0.015 * width)}px;'
                                           f';color:red;'
                                           f'background: lime;border-radius: 10px;'
                                           f'font: italic;')
            self.final_label.move(int(0.57 * width), int(0.701 * height))
            self.final_label.resize(int(0.21 * width), int(0.04 * height))
            self.final_label.setAlignment(Qt.AlignCenter)
            self.final_label.show()
        else:
            self.final_label.setText('enter the all parameters')
            self.final_label.setStyleSheet(f'font-size: {int(0.015 * width)}px;'
                                           f';color:red;'
                                           f'background: lime;border-radius: 10px;'
                                           f'font: italic;')
            self.final_label.move(int(0.57 * width), int(0.701 * height))
            self.final_label.resize(int(0.21 * width), int(0.04 * height))
            self.final_label.setAlignment(Qt.AlignCenter)
            self.final_label.show()

    def number_of_simulation(self):
        global NUMBER_OF_SIMULATION
        try:
            self.labeltik12.close()
        except:
            pass
        self.labeltik12 = QLabel(self.main_widget1)
        try:
            int(self.edit_line12.text())
            NUMBER_OF_SIMULATION = int(self.edit_line12.text())
            pix = QPixmap(resource_path('tik.png'))
            self.labeltik12.setPixmap(pix)
            self.labeltik12.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik12.move(int(0.43 * width), int(0.104 * height))
            self.labeltik12.show()
            
        except:
            pix = QPixmap(exc)
            self.labeltik12.setPixmap(pix)
            self.labeltik12.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik12.move(int(0.43 * width), int(0.104 * height))
            self.labeltik12.mousePressEvent = partial(self.do_something, self.main_widget1, 0, 0, en)
            self.labeltik12.show()

    def mouseReleaseEvent(self, e):
        global mouse
        mouse = 'release'
        try:
            self.show_error.close()
        except:
            pass

    def do_something(self, widget, errx, erry, img, event):
        global mouse
        if event.button() == Qt.LeftButton:
            mouse = 'press'
            pos = QCursor.pos()
            self.show_error = QLabel(widget)
            # self.show_error.setText('successfully')
            pix = QPixmap(img)
            self.show_error.setPixmap(pix)
            # self.show_error.setStyleSheet(f'font-size: {int(0.02 * width)}px'
            #                                 f'; color:black;'
            #                                 f'background: red;border-radius: 10px;'
            #                                 f'font: italic;')
            self.show_error.move((pos.x() - 0.28 *width + errx), int(pos.y() - 0.01 * height + erry) )
            self.show_error.resize(int(0.25 * width), int(0.2 * height))
            # self.show_error.setAlignment(Qt.AlignLeft)
            self.show_error.show()

    def delete_label_tik11(self):
        global NUMBER_OF_PARAMETER
        try:
            NUMBER_OF_PARAMETER = 0
            self.labeltik11.close()
        except:
            pass

    def delete_label_tik12(self):
        global NUMBER_OF_SIMULATION
        try:
            NUMBER_OF_SIMULATION = 0
            self.labeltik12.close()
        except:
            pass

    # Sufi2_swEdit.def
    def starting_simulation_number(self):
        try:
            self.remark_label.close()
            self.remark_img.close()
        except:
            self.remark_label = QLabel(self.main_widget2)
            self.remark_img = QLabel(self.main_widget2)

        if self.edit_line21.text() != '1':
            pix = QPixmap(resource_path('remark.png'))
            self.remark_img.setPixmap(pix)
            self.remark_img.resize(int(0.026 * width), int(0.04 * height))
            self.remark_img.move(int(0.7 * width), int(0.100 * height))
            self.remark_img.show()
            self.remark_label.setText(
                'اگر برای اولین بار کالیبراسون انجام میدهید شماره شروع شبیه سازی را برار 1 قرار دهید.')
            self.remark_label.resize(int(0.434 * width), int(0.039 * height))
            self.remark_label.setStyleSheet(f'color:#33373B;font-size: {int(0.012 * width)}px; color:white;'
                                            f' background :blueviolet;'
                                            f'border-radius: 10px')
            font = QFont()
            font.setBold(True)
            self.remark_label.setFont(font)
            self.remark_label.setAlignment(Qt.AlignCenter)
            self.remark_label.move(int(0.260 * width), int(0.100 * height))
            self.remark_label.show()

        self.labeltik21 = QLabel(self.main_widget2)
        try:
            global STARTING_SIMULATION_NUMBER
            STARTING_SIMULATION_NUMBER = int(self.edit_line21.text())
            int(self.edit_line21.text())
            pix = QPixmap(resource_path('tik.png'))
            self.labeltik21.setPixmap(pix)
            self.labeltik21.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik21.move(int(0.35 * width), int(0.039 * height))
            self.labeltik21.show()
        except:
            pix = QPixmap(exc)
            self.labeltik21.setPixmap(pix)
            self.labeltik21.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik21.move(int(0.35 * width), int(0.039 * height))
            self.labeltik21.mousePressEvent = partial(self.do_something, self.main_widget2, 0, 0, en)
            self.labeltik21.show()

    def ending_simulation_number(self):
        global ENDING_SIMULATION_NUMBER
        self.labeltik22 = QLabel(self.main_widget2)
        try:
            ENDING_SIMULATION_NUMBER = int(self.edit_line22.text())
            int(self.edit_line22.text())
            pix = QPixmap(resource_path('tik.png'))
            self.labeltik22.setPixmap(pix)
            self.labeltik22.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik22.move(int(0.35 * width), int(0.154 * height))
            self.labeltik22.show()
        except:
            pix = QPixmap(exc)
            self.labeltik22.setPixmap(pix)
            self.labeltik22.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik22.move(int(0.35 * width), int(0.154 * height))
            self.labeltik22.mousePressEvent = partial(self.do_something, self.main_widget2, 0, 0, en)
            self.labeltik22.show()

    def delete_label_tik21(self):
        global STARTING_SIMULATION_NUMBER
        try:
            STARTING_SIMULATION_NUMBER = 0
            self.labeltik21.close()
        except:
            pass

    def delete_label_tik22(self):
        global ENDING_SIMULATION_NUMBER
        try:
            ENDING_SIMULATION_NUMBER = 0
            self.labeltik22.close()
        except:
            pass

    # observed_rch.txt
    def switch_btn_function(self):
        self.number_of_observed_variable_ = 0
        self.list_of_stations = list()
        if MySwitch.isChecked(self.switch_btn):
            self.window2 = QWidget(self.main_widget3)
            self.window2.resize(int(0.75 * width), int(0.8 * height))
            self.window2.move(int(0.021 * width), int(0.1 * height))
            self.window2.show()

            self.label31 = QLabel('Number Of Observed variable : ', self.window2)
            self.label31.setStyleSheet(f'font-size: {int(0.015 * width)}px;')
            self.label31.resize(int(0.22 * width), int(0.039 * height))
            self.label31.move(int(0.002 * width), int(0.035 * height))
            self.label31.show()

            self.edit_line31 = QLineEdit(self.window2)
            self.edit_line31.move(int(0.21 * width), int(0.035 * height))
            self.edit_line31.resize(int(0.151 * width), int(0.039 * height))
            self.edit_line31.textChanged.connect(self.delete_label_tik31)
            self.edit_line31.show()

            self.button31 = QPushButton('OK', self.window2)
            self.button31.move(int(0.38 * width), int(0.035 * height))
            self.button31.resize(int(0.022 * width), int(0.039 * height))
            self.button31.clicked.connect(self.number_of_observed_variable)
            self.button31.show()
        else:
            try:
                self.window2.close()
            except:
                pass

    def number_of_observed_variable(self, n):
        global NUMBER_OF_OBSERVED_VARIABLE
        try:
            try:
                self.labeltik31.close()
            except:
                pass
            self.labeltik31 = QLabel(self.window2)
            int(self.edit_line31.text())
            NUMBER_OF_OBSERVED_VARIABLE = int(self.edit_line31.text())
            if n :
                self.number_of_observed_variable_ += 1
            else:
                self.number_of_observed_variable_ = 1
            pix = QPixmap(resource_path('tik.png'))
            self.labeltik31.setPixmap(pix)
            self.labeltik31.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik31.move(int(0.43 * width), int(0.035 * height))
            self.labeltik31.show()

            try:
                self.window22.close()
                self.scroll.close()
            except:
                pass
            try:
                self.next_btn.close()
            except:
                pass

            try:
                try:
                    self.label32.close()
                    self.labeltik32.close()
                    self.label33.close()
                    self.edit_line33.close()
                    self.button33.close()
                    self.labeltik33.close()
                except:
                    pass
                try:
                    self.edit_line32.close()
                except:
                    pass
                try:
                    self.button32.close()
                except:
                    pass
                try:
                    self.remark_img2.close()
                    self.remark_img_new1.close()
                    self.remark_label_new1.close()
                except:
                    pass
                try:
                    self.remark_label2.close()
                except:
                    pass
            except:
                pass
            self.label32 = QLabel('Variable Name : ', self.window2)
            self.label32.setStyleSheet(f'font-size: {int(0.015 * width)}px;')
            self.label32.resize(int(0.22 * width), int(0.039 * height))
            self.label32.move(int(0.002 * width), int(0.085 * height))
            self.label32.show()

            self.edit_line32 = QLineEdit(self.window2)
            self.edit_line32.move(int(0.12 * width), int(0.085 * height))
            self.edit_line32.resize(int(0.17 * width), int(0.039 * height))
            self.edit_line32.textChanged.connect(self.delete_label_tik32)
            self.edit_line32.show()

            self.button32 = QPushButton('OK', self.window2)
            self.button32.move(int(0.31 * width), int(0.085 * height))
            self.button32.resize(int(0.022 * width), int(0.039 * height))
            self.button32.clicked.connect(self.station_name)
            self.button32.show()

            self.remark_label2 = QLabel(self.window2)
            self.remark_img2 = QLabel(self.window2)
            pix = QPixmap(resource_path('remark.png'))
            self.remark_img2.setPixmap(pix)
            self.remark_img2.resize(int(0.026 * width), int(0.04 * height))
            self.remark_img2.move(int(0.72 * width), int(0.085 * height))
            self.remark_img2.show()
            self.remark_label2.setText(
                'ایستگاه های خود را بصورت صعودی وارد کنید.')
            self.remark_label2.resize(int(0.234 * width), int(0.039 * height))
            self.remark_label2.setStyleSheet(f'color:#33373B;font-size: {int(0.012 * width)}px; color:white;'
                                             f' background :blueviolet;'
                                             f'border-radius: 10px')
            font = QFont()
            font.setBold(True)
            self.remark_label2.setFont(font)
            self.remark_label2.setAlignment(Qt.AlignCenter)
            self.remark_label2.move(int(0.485 * width), int(0.085 * height))
            self.remark_label2.show()

            self.remark_label_new1 = QLabel(f'variable{self.number_of_observed_variable_}', self.window2)
            self.remark_label_new1.setStyleSheet(f'color:rgb(56, 56, 122);font-size: {int(0.013 * width)}px;background :rgb(219, 174, 209);border-radius: 10px')
            self.remark_label_new1.move(int(0.42 * width), int(0.085 * height))
            self.remark_label_new1.resize(int(0.06 * width), int(0.039 * height))
            self.remark_label_new1.setAlignment(Qt.AlignCenter)
            font = QFont()
            font.setBold(True)
            self.remark_label_new1.setFont(font)
            self.remark_label_new1.show()

            self.remark_img_new1 = QLabel(self.window2)
            pix = QPixmap(resource_path('f.png'))
            self.remark_img_new1.setPixmap(pix)
            self.remark_img_new1.resize(int(0.033 * width), int(0.045 * height))
            self.remark_img_new1.move(int(0.385 * width), int(0.085 * height))
            self.remark_img_new1.show()

        except:
            try:
                self.labeltik31.close()
            except:
                pass
            self.labeltik31 = QLabel(self.window2)
            pix = QPixmap(exc)
            self.labeltik31.setPixmap(pix)
            self.labeltik31.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik31.move(int(0.43 * width), int(0.035 * height))
            self.labeltik31.mousePressEvent = partial(self.do_something, self.window2, 0, int(-0.1 * height), en)
            self.labeltik31.show()

    def station_name(self):
        if self.edit_line32.text():
            if re.search(r'(\D*)\d*', self.edit_line32.text()):
                if len(self.list_of_stations) + 1 == self.number_of_observed_variable_:
                    self.list_of_stations.append(self.edit_line32.text())
                if len(self.list_of_stations) == self.number_of_observed_variable_:
                    self.list_of_stations[self.number_of_observed_variable_ - 1] = self.edit_line32.text()
                print(len(self.list_of_stations))
                correct = False
                if len(self.list_of_stations) == 1:
                    correct = True
                elif ((re.findall(r'(\D*)\d*', self.list_of_stations[-1])[0] ==
                       re.findall(r'(\D*)\d*', self.list_of_stations[-2])[0] and len(self.list_of_stations) > 1) and (
                              re.findall(r'\D*(\d*)', self.list_of_stations[-1])[0] >
                              re.findall(r'\D*(\d*)', self.list_of_stations[-2])[0])) or (
                        re.findall(r'(\D*)\d*', self.list_of_stations[-1])[0] !=
                        re.findall(r'(\D*)\d*', self.list_of_stations[-2])[0]):
                    correct = True

                if correct:
                    self.labeltik32 = QLabel(self.window2)
                    pix = QPixmap(resource_path('tik.png'))
                    self.labeltik32.setPixmap(pix)
                    self.labeltik32.resize(int(0.026 * width), int(0.04 * height))
                    self.labeltik32.move(int(0.37 * width), int(0.085 * height))
                    self.labeltik32.show()

                    self.label33 = QLabel('Number Of Data Points For This Variable : ', self.window2)
                    self.label33.setStyleSheet(f'font-size: {int(0.015 * width)}px;')
                    self.label33.resize(int(0.32 * width), int(0.039 * height))
                    self.label33.move(int(0.002 * width), int(0.14 * height))
                    self.label33.show()

                    self.edit_line33 = QLineEdit(self.window2)
                    self.edit_line33.move(int(0.28 * width), int(0.14 * height))
                    self.edit_line33.resize(int(0.151 * width), int(0.039 * height))
                    self.edit_line33.textChanged.connect(self.delete_label_tik33)
                    self.edit_line33.show()

                    self.button33 = QPushButton('OK', self.window2)
                    self.button33.move(int(0.45 * width), int(0.14 * height))
                    self.button33.resize(int(0.022 * width), int(0.039 * height))
                    self.button33.clicked.connect(self.browse_xlsx_0)
                    self.button33.show()

                else:
                    self.remark_label2.close()
                    self.remark_img2.close()
                    self.remark_label3 = QLabel(self.window2)
                    self.remark_img3 = QLabel(self.window2)
                    pix = QPixmap(exc)
                    self.remark_img3.setPixmap(pix)
                    self.remark_img3.resize(int(0.026 * width), int(0.04 * height))
                    self.remark_img3.move(int(0.655 * width), int(0.085 * height))
                    self.remark_img3.show()
                    self.remark_label3.setText(
                        'ایستگاه ها باید بصورت صعودی وارد شوند!')
                    self.remark_label3.resize(int(0.234 * width), int(0.039 * height))
                    self.remark_label3.setStyleSheet(f'color:#33373B;font-size: {int(0.012 * width)}px; color:white;'
                                                     f' background :red;'
                                                     f'border-radius: 10px')
                    font = QFont()
                    font.setBold(True)
                    self.remark_label3.setFont(font)
                    self.remark_label3.setAlignment(Qt.AlignCenter)
                    self.remark_label3.move(int(0.42 * width), int(0.085 * height))
                    self.remark_label3.show()
            else:
                self.labeltik32 = QLabel(self.window2)
                pix = QPixmap(exc)
                self.labeltik32.setPixmap(pix)
                self.labeltik32.resize(int(0.026 * width), int(0.04 * height))
                self.labeltik32.move(int(0.37 * width), int(0.085 * height))
                self.labeltik32.mousePressEvent = partial(self.do_something, self.window2, 0, int(-0.1 * height), en)
                self.labeltik32.show()
        else:
            self.labeltik32 = QLabel(self.window2)
            pix = QPixmap(exc)
            self.labeltik32.setPixmap(pix)
            self.labeltik32.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik32.move(int(0.37 * width), int(0.085 * height))
            self.labeltik32.mousePressEvent = partial(self.do_something, self.window2, 0, int(-0.1 * height), en)
            self.labeltik32.show()

    def browse_xlsx_0(self):
        global NUMBER_OF_DATA_POINTS
        try:
            self.brw_btn1.close()
        except:
            pass
        try:
            self.next_btn.close()
        except:
            pass
        try:
            self.window22.close()
        except:
            pass
        try:
            self.scroll.close()
        except:
            pass
        try:
            
            NUMBER_OF_DATA_POINTS = int(self.edit_line33.text())
            self.labeltik33 = QLabel(self.window2)
            pix = QPixmap(resource_path('tik.png'))
            self.labeltik33.setPixmap(pix)
            self.labeltik33.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik33.move(int(0.5 * width), int(0.14 * height))
            self.labeltik33.show()
            self.brw_btn1 = QPushButton('Browse .xlsx file ...', self.window2)
            self.brw_btn1.resize(int(0.15 * width), int(0.039 * height))
            self.brw_btn1.move(int(0.55 * width), int(0.14 * height))
            self.brw_btn1.clicked.connect(self.browse_xlsx_1)
            self.brw_btn1.show()
        except:
            self.labeltik33 = QLabel(self.window2)
            pix = QPixmap(exc)
            self.labeltik33.setPixmap(pix)
            self.labeltik33.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik33.move(int(0.5 * width), int(0.14 * height))
            self.labeltik33.mousePressEvent = partial(self.do_something, self.window2, 0, int(-0.1 * height), en)
            self.labeltik33.show()

    def browse_xlsx_1(self):
        try:
            self.brw_btn1.close()
        except:
            pass
        try:
            self.next_btn.close()
        except:
            pass
        try:
            self.window22.close()
        except:
            pass
        try:
            self.scroll.close()
        except:
            pass   
        try:
            self.brw_btn1.close()
        except:
            pass
        try:
            self.brw_btn1 = QPushButton('Confirm', self.window2)
            self.brw_btn1.resize(int(0.051 * width), int(0.039 * height))
            self.brw_btn1.move(int(0.55 * width), int(0.14 * height))
            self.brw_btn1.clicked.connect(self.number_of_data_points_for_this_variable)
            self.brw_btn1.show()
            MainWindow = QMainWindow()
            self.loc1 = showDialog(MainWindow)
        except:
            pass

    def number_of_data_points_for_this_variable(self):
        global NUMBER_OF_DATA_POINTS
        try:
            self.next_btn.close()
        except:
            pass
        try:
            self.window22.close()
        except:
            pass
        try:
            self.scroll.close()
        except:
            pass
        if 'xlsx' in self.loc1:
            try:
                self.brw_btn1.close()
                self.label_brw1 = QLabel('successfully', self.window2)
                self.label_brw1.setStyleSheet(f'font-size: {int(0.015 * width)}px;')
                self.label_brw1.resize(int(0.15 * width), int(0.039 * height))
                self.label_brw1.move(int(0.55 * width), int(0.14 * height))
                self.label_brw1.show()
            except:
                pass
        else:
            try:
                self.brw_btn1.close()
                self.brw_btn1 = QPushButton('Browse .xlsx file ...', self.window2)
                self.brw_btn1.resize(int(0.15 * width), int(0.039 * height))
                self.brw_btn1.move(int(0.55 * width), int(0.14 * height))
                self.brw_btn1.clicked.connect(self.browse_xlsx_1)
                self.brw_btn1.show()
            except:
                pass
        try:
            NUMBER_OF_DATA_POINTS = int(self.edit_line33.text())

            self.window22 = QWidget(self.window2)
            # self.window22.resize(int(0.385 * width), int(8 * 0.065 * height + 10))
            self.window22.resize(int(0.4 * width), int(0.59 * height))
            self.window22.move(int(0.001 * width), int(0.193 * height))
            self.window22.show()
            # self.window22.move(int(0.001 * width), int(0.193 * height))

            self.editor = QPlainTextEdit(self.window22) 
            # self.editor.setStyleSheet('background: white')
            self.editor.resize(int(0.547 * width), int(8.84 * 0.065 * height + 10))
            # self.xlsxedit1.textChanged.connect(self.separation_new1)
            self.editor.show()

            self.scroll = QScrollArea(self.window2)
            self.scroll.resize(int(0.55 * width), int(0.59 * height))
            self.scroll.move(int(0.001 * width), int(0.193 * height))
            self.scroll.setWidget(self.editor)

            wb_obj = openpyxl.load_workbook(self.loc1)
            sheet = wb_obj.active
            rows = sheet.rows
            columns = sheet.columns
            first_clm = list()
            second_clm = list()
            third_clm = list()
            i = 1
            for column in columns:
                if i == 1:
                    for cell in column:
                        first_clm.append(cell.value)
                if i == 2:
                    for cell in column:
                        second_clm.append(cell.value)
                if i == 3:
                    for cell in column:
                        third_clm.append(cell.value)
                i += 1
            data = ''
            
            

            redColor = QColor('#FF0000')
            blackColor = QColor('#000000')
            greenColor = QColor('#00FF00')
            blueColor = QColor('#0000FF')
            all_clm = list(zip(first_clm, second_clm, third_clm))
            all_clm.sort(key=lambda e:e[0])
            for j in range(min(sheet.max_row, NUMBER_OF_DATA_POINTS)):
                    if all_clm[j][0] and all_clm[j][1] and all_clm[j][2]:
                        colr = [blueColor, blackColor, blackColor, blackColor, greenColor]
                        try:
                            if all_clm[j][0] == all_clm[j-1][0]:
                                colr[0] = redColor
                                colr[4] = redColor
                                st = '\tIncorrect\n' + 42*'\u2796'+'\n'
                            else:
                                st = '\tCorrect\n' + 42*'\u2796'+'\n'
                        except:
                            st = '\tCorrect\n' + 42*'\u2796'+'\n'
                        for q in range(len(colr)):
                            color = QColor(colr[q])
                            
                            data = [str(j+1)+')\t', str(all_clm[j][0])+'\t', str(all_clm[j][1])+'\t', str(all_clm[j][2])+'\t', st]
                            color_format = self.editor.currentCharFormat()
                            color_format.setForeground(color)
                            self.editor.setCurrentCharFormat(color_format)
                            self.editor.setCurrentCharFormat(color_format)
                            self.editor.insertPlainText(data[q])
                            
                        # data = data + f'{str(j+1)}\t {str(first_clm[j])} \t {second_clm[j]} \t {third_clm[j]}'
                    else:
                        colr = [blueColor, blackColor, blackColor, blackColor, redColor]
                        if not all_clm[j][0]:
                            colr[1] = redColor
                        if not all_clm[j][1]:
                            colr[2] = redColor
                        if not all_clm[j][2]:
                            colr[3] = redColor
                        for q in range(len(colr)):
                            color = QColor(colr[q])
                            st = '\tIncorrect\n' +  + 42*'\u2796'+'\n'
                            data = [str(j+1)+')\t', str(all_clm[j][0])+'\t', str(all_clm[j][1])+'\t', str(all_clm[j][2])+'\t', st]
                            color_format = self.editor.currentCharFormat()
                            color_format.setForeground(color)
                            self.editor.setCurrentCharFormat(color_format)
                            self.editor.setCurrentCharFormat(color_format)
                            self.editor.insertPlainText(data[q])
            
            # self.edit_list2 = list()
            # for i in range(NUMBER_OF_DATA_POINTS):
                # label = QLabel(f'{i + 1}', self.window22)
                # label.setStyleSheet(f'font-size: {int(0.013 * width)}px; color:red;'
                #                     f' background :burlywood;'
                #                     f'border-radius: 10px')
                # label.setAlignment(Qt.AlignCenter)
                # label.resize(int(0.02 * width), int(0.04 * height))
                # label.move(int(0.002 * width), int(i * 0.065 * height + 10))
                # label.show()

                # edit1 = QLineEdit(self.window22)
                # edit1.setStyleSheet('background: white; color:red')
                # edit1.resize(int(0.074 * width), int(0.039 * height))
                # edit1.move(int(0.025 * width), int(i * 0.065 * height + 10))
                # edit1.textChanged.connect(self.separation_new1)
                # edit1.setReadOnly(False)
                # edit1.show()

                # edit2 = QLineEdit(self.window22)
                # edit2.setStyleSheet('background: white')
                # edit2.resize(int(0.17 * width), int(0.039 * height))
                # edit2.move(int(0.105 * width), int(i * 0.065 * height + 10))
                # edit2.textChanged.connect(self.separation_new1)
                # edit2.setReadOnly(False)
                # edit2.show()

                # edit3 = QLineEdit(self.window22)
                # edit3.setStyleSheet('background: white; color:red')
                # edit3.resize(int(0.06 * width), int(0.039 * height))
                # edit3.move(int(0.28 * width), int(i * 0.065 * height + 10))
                # edit3.setReadOnly(False)
                # edit3.textChanged.connect(self.separation_new1)
                # edit3.show()

                # self.edit_list2.append([edit1, edit2, edit3])


            # self.edit_list2[0][1].setPlaceholderText('Paste all data here')
            self.check_plain1 = QPushButton('Check', self.window2)
            self.check_plain1.resize(int(0.051 * width), int(0.039 * height))
            self.check_plain1.move(int(0.6 * width), int(0.6 * height))
            self.check_plain1.clicked.connect(self.get_plain_text)
            self.check_plain1.show()


            self.confirm_btn = QPushButton('Confirm', self.window2)
            self.confirm_btn.resize(int(0.051 * width), int(0.039 * height))
            self.confirm_btn.move(int(0.6 * width), int(0.7 * height))
            self.confirm_btn.clicked.connect(self.confirm2)
            self.confirm_btn.show()

            self.scroll.show()
        except:
            pass
        

    def get_plain_text(self):
        redColor = QColor('#FF0000')
        blackColor = QColor('#000000')
        greenColor = QColor('#00FF00')
        blueColor = QColor('#0000FF')
        text = self.editor.toPlainText()
        text = text.replace('\u2796\n','').replace('\u2796','').replace('Correct','').replace('Incorrect','').split('\n')
        self.editor.clear()
        for j in text:
                if len(j) < 1 :
                    continue
                row_text = j.split('\t')
                n = row_text[0]
                first_clm = row_text[1]
                second_clm = row_text[2]
                third_clm = row_text[3]
                if first_clm !='None' and second_clm != 'None' and third_clm != 'None':
                    colr = [blueColor, blackColor, blackColor, blackColor, greenColor]
                    for q in range(len(colr)):
                        color = QColor(colr[q])
                        st = '\tCorrect\n' + 42*'\u2796'+'\n'
                        data = [str(n)+'\t', str(first_clm)+'\t', str(second_clm)+'\t', str(third_clm)+'\t', st]
                        color_format = self.editor.currentCharFormat()
                        color_format.setForeground(color)
                        self.editor.setCurrentCharFormat(color_format)
                        self.editor.setCurrentCharFormat(color_format)
                        self.editor.insertPlainText(data[q])
                    # data = data + f'{str(j+1)}\t {str(first_clm[j])} \t {second_clm[j]} \t {third_clm[j]}'
                else:
                    colr = [blueColor, blackColor, blackColor, blackColor, redColor]
                    if first_clm == 'None':
                        colr[1] = redColor
                    if second_clm == 'None':
                        colr[2] = redColor
                    if third_clm == 'None':
                        colr[3] = redColor
                    for q in range(len(colr)):
                        color = QColor(colr[q])
                        st = '\tIncorrect\n' +  + 42*'\u2796'+'\n'
                        data = [str(n)+'\t', str(first_clm)+'\t', str(second_clm)+'\t', str(third_clm)+'\t', st]
                        color_format = self.editor.currentCharFormat()
                        color_format.setForeground(color)
                        self.editor.setCurrentCharFormat(color_format)
                        self.editor.setCurrentCharFormat(color_format)
                        self.editor.insertPlainText(data[q])

    def separation_new1(self, n):
        if len(n.split('\n')) >= 2:
            edit_list = n.split('\n')
            j = 0
            for i in self.edit_list2:
                for f in i:
                    f.clear()
            for i in self.edit_list2:
                z = 0
                for k in i:
                    k.setText(edit_list[j].split('\t')[z])
                    z += 1
                j += 1

    def confirm2(self):
        list_of_first_number = list()
        list_of_first_column_error = list()
        for i in self.edit_list2:
            if i[0].text():
                try:
                    list_of_first_number.append(int(i[0].text()))
                    if list_of_first_number != natsorted(list_of_first_number) or len(
                            np.unique(list_of_first_number)) != len(list_of_first_number):
                        list_of_first_column_error.append(self.edit_list2.index(i))
                except:
                    list_of_first_column_error.append(self.edit_list2.index(i))
            else:
                list_of_first_column_error.append(self.edit_list2.index(i))

        list_of_text = list()
        list_of_second_column_error = list()
        for i in self.edit_list2:
            if i[1].text():
                list_of_text.append(i[1].text())
            else:
                list_of_second_column_error.append(self.edit_list2.index(i))

        list_of_second_number = list()
        list_of_third_column_error = list()
        for i in self.edit_list2:
            if i[2].text():
                try:
                    list_of_second_number.append(float(i[2].text()))
                except:
                    list_of_third_column_error.append(self.edit_list2.index(i))
            else:
                list_of_third_column_error.append(self.edit_list2.index(i))

        if self.list_label_tik2:
            for i in self.list_label_tik2:
                i.close()
        try:
            self.next_btn.close()
        except:
            pass

        counter = 0
        for i in range(NUMBER_OF_DATA_POINTS):
            if i in list_of_first_column_error or i in list_of_second_column_error or i in list_of_third_column_error:
                label = QLabel(self.window22)
                pix = QPixmap(exc)
                label.setPixmap(pix)
                label.resize(int(0.026 * width), int(0.04 * height))
                label.move(int(0.34 * width), int(i * 0.065 * height + 10))
                label.mousePressEvent = partial(self.do_something, self.window2, 0, int(-0.1 * height), en)
                label.show()
                self.list_label_tik2.append(label)
            else:
                label = QLabel(self.window22)
                pix = QPixmap(resource_path('tik.png'))
                label.setPixmap(pix)
                label.resize(int(0.026 * width), int(0.04 * height))
                label.move(int(0.34 * width), int(i * 0.065 * height + 10))
                label.show()
                self.list_label_tik2.append(label)
                counter += 1

        if counter == NUMBER_OF_DATA_POINTS and self.number_of_observed_variable_ != NUMBER_OF_OBSERVED_VARIABLE:
            self.next_btn = QPushButton('Next', self.window2)
            self.next_btn.resize(int(0.051 * width), int(0.039 * height))
            self.next_btn.move(int(0.65 * width), int(0.7 * height))
            t = True
            self.next_btn.clicked.connect(partial(self.number_of_observed_variable, t))
            self.next_btn.show()

    def delete_label_tik31(self):
        global NUMBER_OF_OBSERVED_VARIABLE
        try:
            NUMBER_OF_OBSERVED_VARIABLE = 0
            self.labeltik31.close()
        except:
            pass

    def delete_label_tik32(self):
        
        try:
            try:
                self.labeltik32.close()
            except:
                pass
            try:
                self.remark_label3.close()
            except:
                pass
            try:
                self.remark_label2.close()
            except:
                pass
            try:
                self.remark_img3.close()
            except:
                pass
            try:
                self.remark_img2.close()
            except:
                pass

            self.remark_label2 = QLabel(self.window2)
            self.remark_img2 = QLabel(self.window2)
            pix = QPixmap(resource_path('remark.png'))
            self.remark_img2.setPixmap(pix)
            self.remark_img2.resize(int(0.026 * width), int(0.04 * height))
            self.remark_img2.move(int(0.72 * width), int(0.085 * height))
            self.remark_img2.show()
            self.remark_label2.setText(
                'ایستگاه های خود را بصورت صعودی وارد کنید.')
            self.remark_label2.resize(int(0.234 * width), int(0.039 * height))
            self.remark_label2.setStyleSheet(f'color:#33373B;font-size: {int(0.012 * width)}px; color:white;'
                                             f' background :blueviolet;'
                                             f'border-radius: 10px')
            font = QFont()
            font.setBold(True)
            self.remark_label2.setFont(font)
            self.remark_label2.setAlignment(Qt.AlignCenter)
            self.remark_label2.move(int(0.485 * width), int(0.085 * height))
            self.remark_label2.show()
        except:
            pass

    def delete_label_tik33(self):
        global NUMBER_OF_DATA_POINTS
        NUMBER_OF_DATA_POINTS = 0
        try:
            self.labeltik33.close()
        except:
            pass

    # observed_hru.txt
    def switch_btn_function2(self):
        self.number_of_observed_variable_2 = 0
        self.list_of_stations2 = list()
        if MySwitch.isChecked(self.switch_btn2):
            self.window3 = QWidget(self.main_widget4)
            self.window3.resize(int(0.75 * width), int(0.8 * height))
            self.window3.move(int(0.021 * width), int(0.1 * height))
            self.window3.show()

            self.label41 = QLabel('Number Of Observed variable : ', self.window3)
            self.label41.setStyleSheet(f'font-size: {int(0.015 * width)}px;')
            self.label41.resize(int(0.22 * width), int(0.039 * height))
            self.label41.move(int(0.002 * width), int(0.035 * height))
            self.label41.show()

            self.edit_line41 = QLineEdit(self.window3)
            self.edit_line41.move(int(0.21 * width), int(0.035 * height))
            self.edit_line41.resize(int(0.151 * width), int(0.039 * height))
            self.edit_line41.textChanged.connect(self.delete_label_tik41)
            self.edit_line41.show()

            self.button41 = QPushButton('OK', self.window3)
            self.button41.move(int(0.38 * width), int(0.035 * height))
            self.button41.resize(int(0.022 * width), int(0.039 * height))
            self.button41.clicked.connect(self.number_of_observed_variable2)
            self.button41.show()
        else:
            try:
                self.window3.close()
            except:
                pass

    def number_of_observed_variable2(self, n):
        global NUMBER_OF_OBSERVED_VARIABLE2
        
        try:
            try:
                self.labeltik41.close()
            except:
                pass
            self.labeltik41 = QLabel(self.window3)
            int(self.edit_line41.text())
            NUMBER_OF_OBSERVED_VARIABLE2 = int(self.edit_line41.text())
            if n :
                self.number_of_observed_variable_2 += 1
            else:
                self.number_of_observed_variable_2 = 1
            pix = QPixmap(resource_path('tik.png'))
            self.labeltik41.setPixmap(pix)
            self.labeltik41.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik41.move(int(0.43 * width), int(0.035 * height))
            self.labeltik41.show()

            try:
                self.window32.close()
                self.scroll2.close()
            except:
                pass
            try:
                self.next_btn2.close()
            except:
                pass

            try:
                try:
                    self.label42.close()
                    self.labeltik42.close()
                    self.label43.close()
                    self.edit_line43.close()
                    self.button43.close()
                    self.labeltik43.close()
                except:
                    pass
                try:
                    self.edit_line42.close()
                except:
                    pass
                try:
                    self.button42.close()
                except:
                    pass
                try:
                    self.remark_img4.close()
                    self.remark_img_new2.close()
                    self.remark_label_new2.close()
                except:
                    pass
                try:
                    self.remark_label4.close()
                except:
                    pass
            except:
                pass
            self.label42 = QLabel('Variable Name : ', self.window3)
            self.label42.setStyleSheet(f'font-size: {int(0.015 * width)}px;')
            self.label42.resize(int(0.22 * width), int(0.039 * height))
            self.label42.move(int(0.002 * width), int(0.085 * height))
            self.label42.show()

            self.edit_line42 = QLineEdit(self.window3)
            self.edit_line42.move(int(0.12 * width), int(0.085 * height))
            self.edit_line42.resize(int(0.17 * width), int(0.039 * height))
            self.edit_line42.textChanged.connect(self.delete_label_tik42)
            self.edit_line42.show()

            self.button42 = QPushButton('OK', self.window3)
            self.button42.move(int(0.31 * width), int(0.085 * height))
            self.button42.resize(int(0.022 * width), int(0.039 * height))
            self.button42.clicked.connect(self.station_name2)
            self.button42.show()

            self.remark_label4 = QLabel(self.window3)
            self.remark_img4 = QLabel(self.window3)
            pix = QPixmap(resource_path('remark.png'))
            self.remark_img4.setPixmap(pix)
            self.remark_img4.resize(int(0.026 * width), int(0.04 * height))
            self.remark_img4.move(int(0.72 * width), int(0.085 * height))
            self.remark_img4.show()
            self.remark_label4.setText(
                'ایستگاه های خود را بصورت صعودی وارد کنید.')
            self.remark_label4.resize(int(0.234 * width), int(0.039 * height))
            self.remark_label4.setStyleSheet(f'color:#33373B;font-size: {int(0.012 * width)}px; color:white;'
                                             f' background :blueviolet;'
                                             f'border-radius: 10px')
            font = QFont()
            font.setBold(True)
            self.remark_label4.setFont(font)
            self.remark_label4.setAlignment(Qt.AlignCenter)
            self.remark_label4.move(int(0.485 * width), int(0.085 * height))
            self.remark_label4.show()

            self.remark_label_new2 = QLabel(f'variable{self.number_of_observed_variable_2}', self.window3)
            self.remark_label_new2.setStyleSheet(f'color:rgb(56, 56, 122);font-size: {int(0.013 * width)}px;background :rgb(219, 174, 209);border-radius: 10px')
            self.remark_label_new2.move(int(0.42 * width), int(0.085 * height))
            self.remark_label_new2.resize(int(0.06 * width), int(0.039 * height))
            self.remark_label_new2.setAlignment(Qt.AlignCenter)
            font = QFont()
            font.setBold(True)
            self.remark_label_new2.setFont(font)
            self.remark_label_new2.show()

            self.remark_img_new2 = QLabel(self.window3)
            pix = QPixmap(resource_path('f.png'))
            self.remark_img_new2.setPixmap(pix)
            self.remark_img_new2.resize(int(0.033 * width), int(0.045 * height))
            self.remark_img_new2.move(int(0.385 * width), int(0.085 * height))
            self.remark_img_new2.show()

        except:
            try:
                self.labeltik41.close()
            except:
                pass
            self.labeltik41 = QLabel(self.window3)
            pix = QPixmap(exc)
            self.labeltik41.setPixmap(pix)
            self.labeltik41.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik41.move(int(0.43 * width), int(0.035 * height))
            self.labeltik41.mousePressEvent = partial(self.do_something, self.window3, 0, int(-0.1 * height), en)
            self.labeltik41.show()

    def station_name2(self):
        if self.edit_line42.text():
            if re.search(r'(\D*)\d*', self.edit_line42.text()):
                if len(self.list_of_stations2) + 1 == self.number_of_observed_variable_2:
                    self.list_of_stations2.append(self.edit_line42.text())
                if len(self.list_of_stations2) == self.number_of_observed_variable_2:
                    self.list_of_stations2[self.number_of_observed_variable_2 - 1] = self.edit_line42.text()
                correct = False
                if len(self.list_of_stations2) == 1:
                    correct = True
                elif ((re.findall(r'(\D*)\d*', self.list_of_stations2[-1])[0] ==
                       re.findall(r'(\D*)\d*', self.list_of_stations2[-2])[0] and len(self.list_of_stations2) > 1) and (
                              re.findall(r'\D*(\d*)', self.list_of_stations2[-1])[0] >
                              re.findall(r'\D*(\d*)', self.list_of_stations2[-2])[0])) or (
                        re.findall(r'(\D*)\d*', self.list_of_stations2[-1])[0] !=
                        re.findall(r'(\D*)\d*', self.list_of_stations2[-2])[0]):
                    correct = True

                if correct:
                    self.labeltik42 = QLabel(self.window3)
                    pix = QPixmap(resource_path('tik.png'))
                    self.labeltik42.setPixmap(pix)
                    self.labeltik42.resize(int(0.026 * width), int(0.04 * height))
                    self.labeltik42.move(int(0.37 * width), int(0.085 * height))
                    self.labeltik42.show()

                    self.label43 = QLabel('Number Of Data Points For This Variable : ', self.window3)
                    self.label43.setStyleSheet(f'font-size: {int(0.015 * width)}px;')
                    self.label43.resize(int(0.32 * width), int(0.039 * height))
                    self.label43.move(int(0.002 * width), int(0.14 * height))
                    self.label43.show()

                    self.edit_line43 = QLineEdit(self.window3)
                    self.edit_line43.move(int(0.28 * width), int(0.14 * height))
                    self.edit_line43.resize(int(0.151 * width), int(0.039 * height))
                    self.edit_line43.textChanged.connect(self.delete_label_tik43)
                    self.edit_line43.show()

                    self.button43 = QPushButton('OK', self.window3)
                    self.button43.move(int(0.45 * width), int(0.14 * height))
                    self.button43.resize(int(0.022 * width), int(0.039 * height))
                    self.button43.clicked.connect(self.number_of_data_points_for_this_variable2)
                    self.button43.show()

                else:
                    self.remark_label4.close()
                    self.remark_img4.close()
                    self.remark_label5 = QLabel(self.window3)
                    self.remark_img5 = QLabel(self.window3)
                    pix = QPixmap(exc)
                    self.remark_img5.setPixmap(pix)
                    self.remark_img5.resize(int(0.026 * width), int(0.04 * height))
                    self.remark_img5.move(int(0.655 * width), int(0.085 * height))
                    self.remark_img5.show()
                    self.remark_label5.setText(
                        'ایستگاه ها باید بصورت صعودی وارد شوند!')
                    self.remark_label5.resize(int(0.234 * width), int(0.039 * height))
                    self.remark_label5.setStyleSheet(f'color:#33373B;font-size: {int(0.012 * width)}px; color:white;'
                                                     f' background :red;'
                                                     f'border-radius: 10px')
                    font = QFont()
                    font.setBold(True)
                    self.remark_label5.setFont(font)
                    self.remark_label5.setAlignment(Qt.AlignCenter)
                    self.remark_label5.move(int(0.42 * width), int(0.085 * height))
                    self.remark_label5.show()
            else:
                self.labeltik42 = QLabel(self.window3)
                pix = QPixmap(exc)
                self.labeltik42.setPixmap(pix)
                self.labeltik42.resize(int(0.026 * width), int(0.04 * height))
                self.labeltik42.move(int(0.37 * width), int(0.085 * height))
                self.labeltik42.mousePressEvent = partial(self.do_something, self.window3, 0, int(-0.1 * height), en)
                self.labeltik42.show()
        else:
            self.labeltik42 = QLabel(self.window3)
            pix = QPixmap(exc)
            self.labeltik42.setPixmap(pix)
            self.labeltik42.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik42.move(int(0.37 * width), int(0.085 * height))
            self.labeltik42.mousePressEvent = partial(self.do_something, self.window3, 0, int(-0.1 * height), en)
            self.labeltik42.show()

    def number_of_data_points_for_this_variable2(self):
        global NUMBER_OF_DATA_POINTS2
        try:
            self.next_btn2.close()
        except:
            pass
        try:
            self.window32.close()
        except:
            pass
        try:
            self.scroll2.close()
        except:
            pass
        try:
            NUMBER_OF_DATA_POINTS2 = int(self.edit_line43.text())
            self.labeltik43 = QLabel(self.window3)
            pix = QPixmap(resource_path('tik.png'))
            self.labeltik43.setPixmap(pix)
            self.labeltik43.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik43.move(int(0.51 * width), int(0.14 * height))
            self.labeltik43.show()

            self.window32 = QWidget(self.window3)
            self.window32.resize(int(0.385 * width), int(NUMBER_OF_DATA_POINTS2 * 0.065 * height + 10))
            self.window32.show()
            # self.window22.move(int(0.001 * width), int(0.193 * height))
            self.scroll2 = QScrollArea(self.window3)
            self.scroll2.resize(int(0.4 * width), int(0.59 * height))
            self.scroll2.move(int(0.001 * width), int(0.193 * height))
            self.scroll2.setWidget(self.window32)

            self.edit_list3 = list()
            for i in range(NUMBER_OF_DATA_POINTS2):
                label = QLabel(f'{i + 1}', self.window32)
                label.setStyleSheet(f'font-size: {int(0.013 * width)}px; color:red;'
                                    f' background :burlywood;'
                                    f'border-radius: 10px')
                label.setAlignment(Qt.AlignCenter)
                label.resize(int(0.02 * width), int(0.04 * height))
                label.move(int(0.002 * width), int(i * 0.065 * height + 10))
                label.show()

                edit1 = QLineEdit(self.window32)
                edit1.setStyleSheet('background: white; color:red')
                edit1.resize(int(0.074 * width), int(0.039 * height))
                edit1.move(int(0.025 * width), int(i * 0.065 * height + 10))
                edit1.textChanged.connect(self.separation_new2)
                edit1.setReadOnly(False)
                edit1.show()

                edit2 = QLineEdit(self.window32)
                edit2.setStyleSheet('background: white')
                edit2.resize(int(0.17 * width), int(0.039 * height))
                edit2.move(int(0.105 * width), int(i * 0.065 * height + 10))
                edit2.textChanged.connect(self.separation_new2)
                edit2.setReadOnly(False)
                edit2.show()

                edit3 = QLineEdit(self.window32)
                edit3.setStyleSheet('background: white; color:red')
                edit3.resize(int(0.06 * width), int(0.039 * height))
                edit3.move(int(0.28 * width), int(i * 0.065 * height + 10))
                edit3.textChanged.connect(self.separation_new2)
                edit3.setReadOnly(False)
                edit3.show()

                self.edit_list3.append([edit1, edit2, edit3])

            self.edit_list3[0][1].setPlaceholderText('Paste all data here')

            self.confirm_btn2 = QPushButton('Confirm', self.window3)
            self.confirm_btn2.resize(int(0.051 * width), int(0.039 * height))
            self.confirm_btn2.move(int(0.6 * width), int(0.7 * height))
            self.confirm_btn2.clicked.connect(self.confirm3)
            self.confirm_btn2.show()

            self.scroll2.show()
        except:
            self.labeltik43 = QLabel(self.window3)
            pix = QPixmap(exc)
            self.labeltik43.setPixmap(pix)
            self.labeltik43.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik43.move(int(0.51 * width), int(0.14 * height))
            self.labeltik43.mousePressEvent = partial(self.do_something, self.window3, 0, int(-0.1 * height), en)
            self.labeltik43.show()

    def separation_new2(self, n):
        if len(n.split('\n')) >= 2:
            edit_list = n.split('\n')
            j = 0
            for i in self.edit_list3:
                for f in i:
                    f.clear()
            for i in self.edit_list3:
                z = 0
                for k in i:
                    k.setText(edit_list[j].split('\t')[z])
                    z += 1
                j += 1

    def confirm3(self):
        list_of_first_number = list()
        list_of_first_column_error = list()
        for i in self.edit_list3:
            if i[0].text():
                try:
                    list_of_first_number.append(int(i[0].text()))
                    if list_of_first_number != natsorted(list_of_first_number) or len(
                            np.unique(list_of_first_number)) != len(list_of_first_number):
                        list_of_first_column_error.append(self.edit_list3.index(i))
                except:
                    list_of_first_column_error.append(self.edit_list3.index(i))
            else:
                list_of_first_column_error.append(self.edit_list3.index(i))

        list_of_text = list()
        list_of_second_column_error = list()
        for i in self.edit_list3:
            if i[1].text():
                list_of_text.append(i[1].text())
            else:
                list_of_second_column_error.append(self.edit_list3.index(i))

        list_of_second_number = list()
        list_of_third_column_error = list()
        for i in self.edit_list3:
            if i[2].text():
                try:
                    list_of_second_number.append(float(i[2].text()))
                except:
                    list_of_third_column_error.append(self.edit_list3.index(i))
            else:
                list_of_third_column_error.append(self.edit_list3.index(i))

        if self.list_label_tik3:
            for i in self.list_label_tik3:
                i.close()
        try:
            self.next_btn2.close()
        except:
            pass

        counter = 0
        for i in range(NUMBER_OF_DATA_POINTS2):
            if i in list_of_first_column_error or i in list_of_second_column_error or i in list_of_third_column_error:
                label = QLabel(self.window32)
                pix = QPixmap(exc)
                label.setPixmap(pix)
                label.resize(int(0.026 * width), int(0.04 * height))
                label.move(int(0.34 * width), int(i * 0.065 * height + 10))
                label.mousePressEvent = partial(self.do_something, self.window3, 0, int(-0.1 * height), en)
                label.show()
                self.list_label_tik3.append(label)
            else:
                label = QLabel(self.window32)
                pix = QPixmap(resource_path('tik.png'))
                label.setPixmap(pix)
                label.resize(int(0.026 * width), int(0.04 * height))
                label.move(int(0.34 * width), int(i * 0.065 * height + 10))
                label.show()
                self.list_label_tik3.append(label)
                counter += 1

        if counter == NUMBER_OF_DATA_POINTS2 and self.number_of_observed_variable_2 != NUMBER_OF_OBSERVED_VARIABLE2:
            self.next_btn2 = QPushButton('Next', self.window3)
            self.next_btn2.resize(int(0.051 * width), int(0.039 * height))
            self.next_btn2.move(int(0.65 * width), int(0.7 * height))
            t = True
            self.next_btn2.clicked.connect((partial(self.number_of_observed_variable2, t)))
            self.next_btn2.show()

    def delete_label_tik41(self):
        try:
            self.labeltik41.close()
        except:
            pass

    def delete_label_tik42(self):
        try:
            try:
                self.labeltik42.close()
            except:
                pass
            try:
                self.remark_label5.close()
            except:
                pass
            try:
                self.remark_label4.close()
            except:
                pass
            try:
                self.remark_img5.close()
            except:
                pass
            try:
                self.remark_img4.close()
            except:
                pass

            self.remark_label4 = QLabel(self.window3)
            self.remark_img4 = QLabel(self.window3)
            pix = QPixmap(resource_path('remark.png'))
            self.remark_img4.setPixmap(pix)
            self.remark_img4.resize(int(0.026 * width), int(0.04 * height))
            self.remark_img4.move(int(0.72 * width), int(0.085 * height))
            self.remark_img4.show()
            self.remark_label4.setText(
                'ایستگاه های خود را بصورت صعودی وارد کنید.')
            self.remark_label4.resize(int(0.234 * width), int(0.039 * height))
            self.remark_label4.setStyleSheet(f'color:#33373B;font-size: {int(0.012 * width)}px; color:white;'
                                             f' background :blueviolet;'
                                             f'border-radius: 10px')
            font = QFont()
            font.setBold(True)
            self.remark_label4.setFont(font)
            self.remark_label4.setAlignment(Qt.AlignCenter)
            self.remark_label4.move(int(0.485 * width), int(0.085 * height))
            self.remark_label4.show()
        except:
            pass

    def delete_label_tik43(self):
        try:
            self.labeltik43.close()
        except:
            pass

    # observed_sub.txt
    def switch_btn_function3(self):
        self.number_of_observed_variable_3 = 0
        self.list_of_stations3 = list()
        if MySwitch.isChecked(self.switch_btn3):
            self.window4 = QWidget(self.main_widget5)
            self.window4.resize(int(0.75 * width), int(0.8 * height))
            self.window4.move(int(0.021 * width), int(0.1 * height))
            self.window4.show()

            self.label51 = QLabel('Number Of Observed variable : ', self.window4)
            self.label51.setStyleSheet(f'font-size: {int(0.015 * width)}px;')
            self.label51.resize(int(0.22 * width), int(0.039 * height))
            self.label51.move(int(0.002 * width), int(0.035 * height))
            self.label51.show()

            self.edit_line51 = QLineEdit(self.window4)
            self.edit_line51.move(int(0.21 * width), int(0.035 * height))
            self.edit_line51.resize(int(0.151 * width), int(0.039 * height))
            self.edit_line51.textChanged.connect(self.delete_label_tik51)
            self.edit_line51.show()

            self.button51 = QPushButton('OK', self.window4)
            self.button51.move(int(0.38 * width), int(0.035 * height))
            self.button51.resize(int(0.022 * width), int(0.039 * height))
            self.button51.clicked.connect(self.number_of_observed_variable3)
            self.button51.show()
        else:
            try:
                self.window4.close()
            except:
                pass

    def number_of_observed_variable3(self, n):
        global NUMBER_OF_OBSERVED_VARIABLE3
        try:
            try:
                self.labeltik41.close()
            except:
                pass
            self.labeltik51 = QLabel(self.window4)
            int(self.edit_line51.text())
            NUMBER_OF_OBSERVED_VARIABLE3 = int(self.edit_line51.text())
            if n :
                self.number_of_observed_variable_3 += 1
            else:
                self.number_of_observed_variable_3 = 1
            pix = QPixmap(resource_path('tik.png'))
            self.labeltik51.setPixmap(pix)
            self.labeltik51.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik51.move(int(0.43 * width), int(0.035 * height))
            self.labeltik51.show()

            try:
                self.window42.close()
                self.scroll3.close()
            except:
                pass
            try:
                self.next_btn3.close()
            except:
                pass

            try:
                try:
                    self.label52.close()
                    self.labeltik52.close()
                    self.label53.close()
                    self.edit_line53.close()
                    self.button53.close()
                    self.labeltik53.close()
                except:
                    pass
                try:
                    self.edit_line52.close()
                except:
                    pass
                try:
                    self.button52.close()
                except:
                    pass
                try:
                    self.remark_img6.close()
                    self.remark_label_new3.close()
                    self.remark_img_new3.close()
                except:
                    pass
                try:
                    self.remark_label6.close()
                except:
                    pass
            except:
                pass
            self.label52 = QLabel('Variavle Name : ', self.window4)
            self.label52.setStyleSheet(f'font-size: {int(0.015 * width)}px;')
            self.label52.resize(int(0.22 * width), int(0.039 * height))
            self.label52.move(int(0.002 * width), int(0.085 * height))
            self.label52.show()

            self.edit_line52 = QLineEdit(self.window4)
            self.edit_line52.move(int(0.12 * width), int(0.085 * height))
            self.edit_line52.resize(int(0.17 * width), int(0.039 * height))
            self.edit_line52.textChanged.connect(self.delete_label_tik52)
            self.edit_line52.show()

            self.button52 = QPushButton('OK', self.window4)
            self.button52.move(int(0.31 * width), int(0.085 * height))
            self.button52.resize(int(0.022 * width), int(0.039 * height))
            self.button52.clicked.connect(self.station_name3)
            self.button52.show()

            self.remark_label6 = QLabel(self.window4)
            self.remark_img6 = QLabel(self.window4)
            pix = QPixmap(resource_path('remark.png'))
            self.remark_img6.setPixmap(pix)
            self.remark_img6.resize(int(0.026 * width), int(0.04 * height))
            self.remark_img6.move(int(0.72 * width), int(0.085 * height))
            self.remark_img6.show()
            self.remark_label6.setText(
                'ایستگاه های خود را بصورت صعودی وارد کنید.')
            self.remark_label6.resize(int(0.234 * width), int(0.039 * height))
            self.remark_label6.setStyleSheet(f'color:#33373B;font-size: {int(0.012 * width)}px; color:white;'
                                             f' background :blueviolet;'
                                             f'border-radius: 10px')
            font = QFont()
            font.setBold(True)
            self.remark_label6.setFont(font)
            self.remark_label6.setAlignment(Qt.AlignCenter)
            self.remark_label6.move(int(0.485 * width), int(0.085 * height))
            self.remark_label6.show()

            self.remark_label_new3 = QLabel(f'variable{self.number_of_observed_variable_3}', self.window4)
            self.remark_label_new3.setStyleSheet(f'color:rgb(56, 56, 122);font-size: {int(0.013 * width)}px;background :rgb(219, 174, 209);border-radius: 10px')
            self.remark_label_new3.move(int(0.42 * width), int(0.085 * height))
            self.remark_label_new3.resize(int(0.06 * width), int(0.039 * height))
            self.remark_label_new3.setAlignment(Qt.AlignCenter)
            font = QFont()
            font.setBold(True)
            self.remark_label_new3.setFont(font)
            self.remark_label_new3.show()

            self.remark_img_new3 = QLabel(self.window4)
            pix = QPixmap(resource_path('f.png'))
            self.remark_img_new3.setPixmap(pix)
            self.remark_img_new3.resize(int(0.033 * width), int(0.045 * height))
            self.remark_img_new3.move(int(0.385 * width), int(0.085 * height))
            self.remark_img_new3.show()

        except:
            try:
                self.labeltik51.close()
            except:
                pass
            self.labeltik51 = QLabel(self.window4)
            pix = QPixmap(exc)
            self.labeltik51.setPixmap(pix)
            self.labeltik51.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik51.move(int(0.47 * width), int(0.035 * height))
            self.labeltik51.mousePressEvent = partial(self.do_something, self.window4, 0, int(-0.1 * height), en)
            self.labeltik51.show()

    def station_name3(self):
        if self.edit_line52.text():
            if re.search(r'(\D*)\d*', self.edit_line52.text()):
                if len(self.list_of_stations3) + 1 == self.number_of_observed_variable_3:
                    self.list_of_stations3.append(self.edit_line52.text())
                if len(self.list_of_stations3) == self.number_of_observed_variable_3:
                    self.list_of_stations3[self.number_of_observed_variable_3 - 1] = self.edit_line52.text()
                correct = False
                if len(self.list_of_stations3) == 1:
                    correct = True
                elif ((re.findall(r'(\D*)\d*', self.list_of_stations3[-1])[0] ==
                       re.findall(r'(\D*)\d*', self.list_of_stations3[-2])[0] and len(self.list_of_stations3) > 1) and (
                              re.findall(r'\D*(\d*)', self.list_of_stations3[-1])[0] >
                              re.findall(r'\D*(\d*)', self.list_of_stations3[-2])[0])) or (
                        re.findall(r'(\D*)\d*', self.list_of_stations3[-1])[0] !=
                        re.findall(r'(\D*)\d*', self.list_of_stations3[-2])[0]):
                    correct = True

                if correct:
                    self.labeltik52 = QLabel(self.window4)
                    pix = QPixmap(resource_path('tik.png'))
                    self.labeltik52.setPixmap(pix)
                    self.labeltik52.resize(int(0.026 * width), int(0.04 * height))
                    self.labeltik52.move(int(0.37 * width), int(0.085 * height))
                    self.labeltik52.show()

                    self.label53 = QLabel('Number Of Data Points For This Variable : ', self.window4)
                    self.label53.setStyleSheet(f'font-size: {int(0.015 * width)}px;')
                    self.label53.resize(int(0.32 * width), int(0.039 * height))
                    self.label53.move(int(0.002 * width), int(0.14 * height))
                    self.label53.show()

                    self.edit_line53 = QLineEdit(self.window4)
                    self.edit_line53.move(int(0.28 * width), int(0.14 * height))
                    self.edit_line53.resize(int(0.151 * width), int(0.039 * height))
                    self.edit_line53.textChanged.connect(self.delete_label_tik53)
                    self.edit_line53.show()

                    self.button53 = QPushButton('OK', self.window4)
                    self.button53.move(int(0.45 * width), int(0.14 * height))
                    self.button53.resize(int(0.022 * width), int(0.039 * height))
                    self.button53.clicked.connect(self.number_of_data_points_for_this_variable3)
                    self.button53.show()

                else:
                    self.remark_label6.close()
                    self.remark_img6.close()
                    self.remark_label7 = QLabel(self.window4)
                    self.remark_img7 = QLabel(self.window4)
                    pix = QPixmap(exc)
                    self.remark_img7.setPixmap(pix)
                    self.remark_img7.resize(int(0.026 * width), int(0.04 * height))
                    self.remark_img7.move(int(0.655 * width), int(0.085 * height))
                    self.remark_img7.show()
                    self.remark_label7.setText(
                        'ایستگاه ها باید بصورت صعودی وارد شوند!')
                    self.remark_label7.resize(int(0.234 * width), int(0.039 * height))
                    self.remark_label7.setStyleSheet(f'color:#33373B;font-size: {int(0.012 * width)}px; color:white;'
                                                     f' background :red;'
                                                     f'border-radius: 10px')
                    font = QFont()
                    font.setBold(True)
                    self.remark_label7.setFont(font)
                    self.remark_label7.setAlignment(Qt.AlignCenter)
                    self.remark_label7.move(int(0.42 * width), int(0.085 * height))
                    self.remark_label7.show()
            else:
                self.labeltik52 = QLabel(self.window4)
                pix = QPixmap(exc)
                self.labeltik52.setPixmap(pix)
                self.labeltik52.resize(int(0.026 * width), int(0.04 * height))
                self.labeltik52.move(int(0.37 * width), int(0.085 * height))
                self.labeltik52.show()
        else:
            self.labeltik52 = QLabel(self.window4)
            pix = QPixmap(exc)
            self.labeltik52.setPixmap(pix)
            self.labeltik52.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik52.move(int(0.37 * width), int(0.085 * height))
            self.labeltik52.show()

    def number_of_data_points_for_this_variable3(self):
        global NUMBER_OF_DATA_POINTS3
        try:
            self.next_btn3.close()
        except:
            pass
        try:
            self.window42.close()
        except:
            pass
        try:
            self.scroll3.close()
        except:
            pass
        try:
            NUMBER_OF_DATA_POINTS3 = int(self.edit_line53.text())
            self.labeltik53 = QLabel(self.window4)
            pix = QPixmap(resource_path('tik.png'))
            self.labeltik53.setPixmap(pix)
            self.labeltik53.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik53.move(int(0.51 * width), int(0.14 * height))
            self.labeltik53.show()

            self.window42 = QWidget(self.window4)
            self.window42.resize(int(0.385 * width), int(NUMBER_OF_DATA_POINTS3 * 0.065 * height + 10))
            self.window42.show()
            # self.window22.move(int(0.001 * width), int(0.193 * height))
            self.scroll3 = QScrollArea(self.window4)
            self.scroll3.resize(int(0.4 * width), int(0.59 * height))
            self.scroll3.move(int(0.001 * width), int(0.193 * height))
            self.scroll3.setWidget(self.window42)

            self.edit_list4 = list()
            for i in range(NUMBER_OF_DATA_POINTS3):
                label = QLabel(f'{i + 1}', self.window42)
                label.setStyleSheet(f'font-size: {int(0.013 * width)}px; color:red;'
                                    f' background :burlywood;'
                                    f'border-radius: 10px')
                label.setAlignment(Qt.AlignCenter)
                label.resize(int(0.02 * width), int(0.04 * height))
                label.move(int(0.002 * width), int(i * 0.065 * height + 10))
                label.show()

                edit1 = QLineEdit(self.window42)
                edit1.setStyleSheet('background: white; color:red')
                edit1.resize(int(0.074 * width), int(0.039 * height))
                edit1.move(int(0.025 * width), int(i * 0.065 * height + 10))
                edit1.textChanged.connect(self.separation_new3)
                edit1.setReadOnly(False)
                edit1.show()

                edit2 = QLineEdit(self.window42)
                edit2.setStyleSheet('background: white')
                edit2.resize(int(0.17 * width), int(0.039 * height))
                edit2.move(int(0.105 * width), int(i * 0.065 * height + 10))
                edit2.textChanged.connect(self.separation_new3)
                edit2.setReadOnly(False)
                edit2.show()

                edit3 = QLineEdit(self.window42)
                edit3.setStyleSheet('background: white; color:red')
                edit3.resize(int(0.06 * width), int(0.039 * height))
                edit3.move(int(0.28 * width), int(i * 0.065 * height + 10))
                edit3.textChanged.connect(self.separation_new3)
                edit3.setReadOnly(False)
                edit3.show()

                self.edit_list4.append([edit1, edit2, edit3])

            self.edit_list4[0][1].setPlaceholderText('Paste all data here')

            self.confirm_btn3 = QPushButton('Confirm', self.window4)
            self.confirm_btn3.resize(int(0.051 * width), int(0.039 * height))
            self.confirm_btn3.move(int(0.6 * width), int(0.7 * height))
            self.confirm_btn3.clicked.connect(self.confirm4)
            self.confirm_btn3.show()

            self.scroll3.show()
        except:
            self.labeltik53 = QLabel(self.window4)
            pix = QPixmap(exc)
            self.labeltik53.setPixmap(pix)
            self.labeltik53.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik53.move(int(0.51 * width), int(0.14 * height))
            self.labeltik53.show()

    def separation_new3(self, n):
        if len(n.split('\n')) >= 2:
            edit_list = n.split('\n')
            j = 0
            for i in self.edit_list4:
                for f in i:
                    f.clear()
            for i in self.edit_list4:
                z = 0
                for k in i:
                    k.setText(edit_list[j].split('\t')[z])
                    z += 1
                j += 1

    def confirm4(self):
        list_of_first_number = list()
        list_of_first_column_error = list()
        for i in self.edit_list4:
            if i[0].text():
                try:
                    list_of_first_number.append(int(i[0].text()))
                    if list_of_first_number != natsorted(list_of_first_number) or len(
                            np.unique(list_of_first_number)) != len(list_of_first_number):
                        list_of_first_column_error.append(self.edit_list4.index(i))
                except:
                    list_of_first_column_error.append(self.edit_list4.index(i))
            else:
                list_of_first_column_error.append(self.edit_list4.index(i))

        list_of_text = list()
        list_of_second_column_error = list()
        for i in self.edit_list4:
            if i[1].text():
                list_of_text.append(i[1].text())
            else:
                list_of_second_column_error.append(self.edit_list4.index(i))

        list_of_second_number = list()
        list_of_third_column_error = list()
        for i in self.edit_list4:
            if i[2].text():
                try:
                    list_of_second_number.append(float(i[2].text()))
                except:
                    list_of_third_column_error.append(self.edit_list4.index(i))
            else:
                list_of_third_column_error.append(self.edit_list4.index(i))

        if self.list_label_tik4:
            for i in self.list_label_tik4:
                i.close()
        try:
            self.next_btn3.close()
        except:
            pass

        counter = 0
        for i in range(NUMBER_OF_DATA_POINTS3):
            if i in list_of_first_column_error or i in list_of_second_column_error or i in list_of_third_column_error:
                label = QLabel(self.window42)
                pix = QPixmap(exc)
                label.setPixmap(pix)
                label.resize(int(0.026 * width), int(0.04 * height))
                label.move(int(0.34 * width), int(i * 0.065 * height + 10))
                label.mousePressEvent = partial(self.do_something, self.window4, 0, int(-0.1 * height), en)
                label.show()
                self.list_label_tik4.append(label)
            else:
                label = QLabel(self.window42)
                pix = QPixmap(resource_path('tik.png'))
                label.setPixmap(pix)
                label.resize(int(0.026 * width), int(0.04 * height))
                label.move(int(0.34 * width), int(i * 0.065 * height + 10))
                label.show()
                self.list_label_tik4.append(label)
                counter += 1

        if counter == NUMBER_OF_DATA_POINTS3 and self.number_of_observed_variable_3 != NUMBER_OF_OBSERVED_VARIABLE3:
            self.next_btn3 = QPushButton('Next', self.window4)
            self.next_btn3.resize(int(0.051 * width), int(0.039 * height))
            self.next_btn3.move(int(0.65 * width), int(0.7 * height))
            t = True
            self.next_btn3.clicked.connect(partial(self.number_of_observed_variable3, t))
            self.next_btn3.show()

    def delete_label_tik51(self):
        try:
            self.labeltik51.close()
        except:
            pass

    def delete_label_tik52(self):
        try:
            try:
                self.labeltik52.close()
            except:
                pass
            try:
                self.remark_label7.close()
            except:
                pass
            try:
                self.remark_label6.close()
            except:
                pass
            try:
                self.remark_img7.close()
            except:
                pass
            try:
                self.remark_img6.close()
            except:
                pass

            self.remark_label6 = QLabel(self.window4)
            self.remark_img6 = QLabel(self.window4)
            pix = QPixmap(resource_path('remark.png'))
            self.remark_img6.setPixmap(pix)
            self.remark_img6.resize(int(0.026 * width), int(0.04 * height))
            self.remark_img6.move(int(0.72 * width), int(0.085 * height))
            self.remark_img6.show()
            self.remark_label6.setText(
                'ایستگاه های خود را بصورت صعودی وارد کنید.')
            self.remark_label6.resize(int(0.234 * width), int(0.039 * height))
            self.remark_label6.setStyleSheet(f'color:#33373B;font-size: {int(0.012 * width)}px; color:white;'
                                             f' background :blueviolet;'
                                             f'border-radius: 10px')
            font = QFont()
            font.setBold(True)
            self.remark_label6.setFont(font)
            self.remark_label6.setAlignment(Qt.AlignCenter)
            self.remark_label6.move(int(0.485 * width), int(0.085 * height))
            self.remark_label6.show()
        except:
            pass

    def delete_label_tik53(self):
        try:
            self.labeltik53.close()
        except:
            pass

    def confirm6(self):
        if self.list_label_tik6:
            for i in self.list_label_tik6:
                i.close()

        for i in range(NUMBER_OF_OBSERVED_VARIABLE):
            try:
                re.findall(r'(.+)\.txt', self.edit_list6[i].text())[0]

                if self.edit_list6[i].text() and re.findall(r'(.+)\.txt', self.edit_list6[i].text())[0] == \
                        self.list_of_stations[i] and re.search(r'(.+)\.txt', self.edit_list6[i].text()):
                    label = QLabel(self.window6)
                    pix = QPixmap(resource_path('tik.png'))
                    label.setPixmap(pix)
                    label.resize(int(0.026 * width), int(0.04 * height))
                    label.move(int(0.28 * width), int(i * 0.065 * height + 10))
                    label.show()
                    self.list_label_tik6.append(label)
                else:
                    label = QLabel(self.window6)
                    pix = QPixmap(exc)
                    label.setPixmap(pix)
                    label.resize(int(0.026 * width), int(0.04 * height))
                    label.move(int(0.28 * width), int(i * 0.065 * height + 10))
                    label.show()
                    self.list_label_tik6.append(label)
            except:
                label = QLabel(self.window6)
                pix = QPixmap(exc)
                label.setPixmap(pix)
                label.resize(int(0.026 * width), int(0.04 * height))
                label.move(int(0.28 * width), int(i * 0.065 * height + 10))
                label.show()
                self.list_label_tik6.append(label)

    def confirm7(self):
        if self.list_label_tik7:
            for i in self.list_label_tik7:
                i.close()

        for i in range(NUMBER_OF_OBSERVED_VARIABLE2):
            try:
                re.findall(r'(.+)\.txt', self.edit_list7[i].text())[0]

                if self.edit_list7[i].text() and re.findall(r'(.+)\.txt', self.edit_list7[i].text())[0] == \
                        self.list_of_stations2[i] and re.search(r'(.+)\.txt', self.edit_list7[i].text()):
                    label = QLabel(self.window7)
                    pix = QPixmap(resource_path('tik.png'))
                    label.setPixmap(pix)
                    label.resize(int(0.026 * width), int(0.04 * height))
                    label.move(int(0.28 * width), int(i * 0.065 * height + 10))
                    label.show()
                    self.list_label_tik7.append(label)
                else:
                    label = QLabel(self.window7)
                    pix = QPixmap(exc)
                    label.setPixmap(pix)
                    label.resize(int(0.026 * width), int(0.04 * height))
                    label.move(int(0.28 * width), int(i * 0.065 * height + 10))
                    label.show()
                    self.list_label_tik7.append(label)
            except:
                label = QLabel(self.window7)
                pix = QPixmap(exc)
                label.setPixmap(pix)
                label.resize(int(0.026 * width), int(0.04 * height))
                label.move(int(0.28 * width), int(i * 0.065 * height + 10))
                label.show()
                self.list_label_tik7.append(label)

    def confirm8(self):
        if self.list_label_tik8:
            for i in self.list_label_tik8:
                i.close()

        for i in range(NUMBER_OF_OBSERVED_VARIABLE3):
            try:
                re.findall(r'(.+)\.txt', self.edit_list8[i].text())[0]

                if self.edit_list8[i].text() and re.findall(r'(.+)\.txt', self.edit_list8[i].text())[0] == \
                        self.list_of_stations3[i] and re.search(r'(.+)\.txt', self.edit_list8[i].text()):
                    label = QLabel(self.window8)
                    pix = QPixmap(resource_path('tik.png'))
                    label.setPixmap(pix)
                    label.resize(int(0.026 * width), int(0.04 * height))
                    label.move(int(0.28 * width), int(i * 0.065 * height + 10))
                    label.show()
                    self.list_label_tik8.append(label)
                else:
                    label = QLabel(self.window8)
                    pix = QPixmap(exc)
                    label.setPixmap(pix)
                    label.resize(int(0.026 * width), int(0.04 * height))
                    label.move(int(0.28 * width), int(i * 0.065 * height + 10))
                    label.show()
                    self.list_label_tik8.append(label)
            except:
                label = QLabel(self.window8)
                pix = QPixmap(exc)
                label.setPixmap(pix)
                label.resize(int(0.026 * width), int(0.04 * height))
                label.move(int(0.28 * width), int(i * 0.065 * height + 10))
                label.show()
                self.list_label_tik8.append(label)

    # STUFI2_extract_rch_def
    def beginning_year_of_simulation(self):
        global BEGINNING_YEAR_OF_SIMULATION
        self.labeltik91 = QLabel(self.main_window9)
        try:
            BEGINNING_YEAR_OF_SIMULATION = int(self.edit_line91.text())
            pix = QPixmap(resource_path('tik.png'))
            self.labeltik91.setPixmap(pix)
            self.labeltik91.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik91.move(int(0.33 * width), int(0.039 * height))
            self.labeltik91.show()
        except:
            pix = QPixmap(exc)
            self.labeltik91.setPixmap(pix)
            self.labeltik91.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik91.move(int(0.33 * width), int(0.039 * height))
            self.labeltik91.show()

    def warmup_period(self):
        global WARMUP_PERIOD
        self.labeltik92 = QLabel(self.main_window9)
        try:
            WARMUP_PERIOD = int(self.edit_line92.text())
            pix = QPixmap(resource_path('tik.png'))
            self.labeltik92.setPixmap(pix)
            self.labeltik92.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik92.move(int(0.352 * width), int(0.104 * height))
            self.labeltik92.show()
        except:
            pix = QPixmap(exc)
            self.labeltik92.setPixmap(pix)
            self.labeltik92.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik92.move(int(0.352 * width), int(0.104 * height))
            self.labeltik92.show()

    def end_year_of_simulation(self):
        global END_YEAR_OF_SIMULATION
        self.labeltik93 = QLabel(self.main_window9)
        try:
            END_YEAR_OF_SIMULATION = int(self.edit_line93.text())
            pix = QPixmap(resource_path('tik.png'))
            self.labeltik93.setPixmap(pix)
            self.labeltik93.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik93.move(int(0.292 * width), int(0.169 * height))
            self.labeltik93.show()
        except:
            pix = QPixmap(exc)
            self.labeltik93.setPixmap(pix)
            self.labeltik93.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik93.move(int(0.292 * width), int(0.169 * height))
            self.labeltik93.show()

    def total_number_of_reaches(self):
        global TOTAL_NUMBER_OF_REACHES
        self.labeltik95 = QLabel(self.main_window9)
        if NUMBER_OF_VARIABLE_TO_GET >= 7:
            h = int(0.468 * height)
        else:
            h = int(NUMBER_OF_VARIABLE_TO_GET * 0.065 * height + 10)
        try:
            TOTAL_NUMBER_OF_REACHES = int(self.edit_line95.text())
            pix = QPixmap(resource_path('tik.png'))
            self.labeltik95.setPixmap(pix)
            self.labeltik95.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik95.move(int(0.51 * width), h + int(0.38 * height))
            self.labeltik95.show()
        except:
            pix = QPixmap(exc)
            self.labeltik95.setPixmap(pix)
            self.labeltik95.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik95.move(int(0.51 * width), h + int(0.38 * height))
            self.labeltik95.show()

    def number_of_variable_to_get(self):
        global NUMBER_OF_VARIABLE_TO_GET
        self.labeltik94 = QLabel(self.main_window9)
        try:
            try:
                self.scroll9.close()
                self.window9.close()
                self.scroll92.close()
                self.window92.close()
                self.label95.close()
                self.edit_line95.close()
                self.button95.close()
                self.labeltik95.close()
                self.labeltik96.close()
                self.confirm_btn9.close()
            except:
                pass

            NUMBER_OF_VARIABLE_TO_GET = int(self.edit_line94.text())
            pix = QPixmap(resource_path('tik.png'))
            self.labeltik94.setPixmap(pix)
            self.labeltik94.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik94.move(int(0.312 * width), int(0.234 * height))
            self.labeltik94.show()

            self.window9 = QWidget(self.main_window9)
            self.window9.resize(int(0.235 * width), int(NUMBER_OF_VARIABLE_TO_GET * 0.065 * height + 9))
            self.window9.show()

            self.scroll9 = QScrollArea(self.main_window9)
            if NUMBER_OF_VARIABLE_TO_GET >= 7:
                h = int(0.468 * height)
            else:
                h = int(NUMBER_OF_VARIABLE_TO_GET * 0.065 * height + 10)
            self.scroll9.resize(int(0.25 * width), h)
            self.scroll9.move(int(0.022 * width), int(0.3 * height))
            self.scroll9.setWidget(self.window9)
            self.scroll9.show()

            self.window92 = QWidget(self.main_window9)
            self.window92.resize(int(0.435 * width), int(NUMBER_OF_VARIABLE_TO_GET * 0.15 * height + 9))
            self.window92.show()

            self.scroll92 = QScrollArea(self.main_window9)
            if NUMBER_OF_VARIABLE_TO_GET >= 7:
                h2 = int(0.6 * height)
            else:
                h2 = int(NUMBER_OF_VARIABLE_TO_GET * 0.13 * height + 10)
            self.scroll92.resize(int(0.45 * width), h2)
            self.scroll92.move(int(0.022 * width), h + int(0.45 * height))
            self.scroll92.setWidget(self.window92)
            self.scroll92.show()

            self.main_window9.resize(int(0.76 * width), int(0.87 * height + 2 * h2))

            label = QLabel(self.window9)
            label.setText('variable column number(s) in the swat output file')
            label.setStyleSheet(f'color:#33373B;font-size: {int(0.01 * width)}px; color:white;'
                                f' background :blueviolet;')
            label.resize(int(0.25 * width), int(0.03 * height))
            label.setAlignment(Qt.AlignCenter)
            label.show()

            self.edit_list9 = list()
            self.edit_list92 = list()
            self.label_list9 = list()
            self.btn_list91 = list()
            self.btn_list92 = list()
            self.multiply_label1 = dict()
            self.multiply_edit1 = dict()

            if self.edit_list9:
                for i in self.edit_list9:
                    i.close()
                for i in self.edit_list92:
                    i.close()
                for i in self.label_list9:
                    i.close()
                for i in self.btn_list92:
                    i.close()
                for i in self.btn_list91:
                    i.close()

            number_list = ['first', 'second', 'third', 'forth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth', 'tenth',
                           'eleventh', 'twelfth']

            for i in range(NUMBER_OF_VARIABLE_TO_GET):
                self.multiply_label1[i] = None

            for i in range(NUMBER_OF_VARIABLE_TO_GET):
                self.multiply_edit1[i] = None

            for i in range(NUMBER_OF_VARIABLE_TO_GET):
                label = QLabel(f'{i + 1}', self.window9)
                label.setStyleSheet(f'font-size: {int(0.013 * width)}px; color:red;'
                                    f' background :burlywood;'
                                    f'border-radius: 10px')
                label.setAlignment(Qt.AlignCenter)
                label.resize(int(0.02 * width), int(0.04 * height))
                label.move(int(0.002 * width), int(i * 0.065 * height + 0.039 * height))
                label.show()

                edit = QLineEdit(self.window9)
                edit.resize(int(0.051 * width), int(0.039 * height))
                edit.move(int(0.03 * width), int(i * 0.065 * height + 0.039 * height))
                edit.setStyleSheet('background:white')
                edit.show()
                self.edit_list9.append(edit)
                self.label_list9.append(label)

                btn1 = QPushButton('OK', self.window9)
                btn1.move(int(0.09 * width), int(i * 0.065 * height + 0.039 * height))
                btn1.resize(int(0.022 * width), int(0.039 * height))
                btn1.clicked.connect(self.multiply_btn1)
                btn1.setCheckable(True)
                btn1.setChecked(False)
                btn1.show()
                self.btn_list91.append(btn1)

                label2 = QLabel(self.window92)
                label2.setStyleSheet(f'font-size: {int(0.012 * width)}px;')
                label2.move(int(0.002 * width), int(i * 0.15 * height + 0.019 * height))
                label2.setText(f'number of reaches to get {number_list[i]} variable :')
                label2.show()
                self.label_list9.append(label2)

                edit2 = QLineEdit(self.window92)
                edit2.resize(int(0.051 * width), int(0.039 * height))
                edit2.move(int(0.24 * width), int(i * 0.15 * height + 0.019 * height))
                edit2.setStyleSheet('background:white')
                edit2.show()
                self.edit_list92.append(edit2)

                btn2 = QPushButton('OK', self.window92)
                btn2.move(int(0.3 * width), int(i * 0.15 * height + 0.019 * height))
                btn2.resize(int(0.022 * width), int(0.039 * height))
                btn2.clicked.connect(self.multiply_btn2)
                btn2.setCheckable(True)
                btn2.setChecked(False)
                btn2.show()
                self.btn_list92.append(btn2)

            self.label95 = QLabel('total number of reaches (subbasins) in the project : ', self.main_window9)
            self.label95.setStyleSheet(f'font-size: {int(0.015 * width)}px;')
            self.label95.resize(int(0.35 * width), int(0.039 * height))
            self.label95.move(int(0.022 * width), h + int(0.38 * height))
            self.label95.show()

            self.edit_line95 = QLineEdit(self.main_window9)
            self.edit_line95.move(int(0.4 * width), h + int(0.38 * height))
            self.edit_line95.resize(int(0.051 * width), int(0.039 * height))
            self.edit_line95.textChanged.connect(self.delete_label_tik95)
            self.edit_line95.show()

            self.button95 = QPushButton('OK', self.main_window9)
            self.button95.move(int(0.46 * width), h + int(0.38 * height))
            self.button95.resize(int(0.022 * width), int(0.039 * height))
            self.button95.clicked.connect(self.total_number_of_reaches)
            self.button95.show()

            self.confirm_btn9 = QPushButton('Confirm', self.main_window9)
            self.confirm_btn9.resize(int(0.051 * width), int(0.039 * height))
            self.confirm_btn9.move(int(0.5 * width), int(h + h2 + 0.4 * height))
            self.confirm_btn9.clicked.connect(self.confirm9)
            self.confirm_btn9.show()

            self.label96 = QLabel('beginning year of simulation not including the warm up : ', self.main_window9)
            self.label96.setStyleSheet(f'font-size: {int(0.015 * width)}px;')
            self.label96.resize(int(0.4 * width), int(0.039 * height))
            self.label96.move(int(0.022 * width), int(h + h2 + 0.55 * height))
            self.label96.show()

            self.edit_line96 = QLineEdit(self.main_window9)
            self.edit_line96.move(int(0.4 * width),int(h + h2 + 0.55 * height))
            self.edit_line96.resize(int(0.051 * width), int(0.039 * height))
            self.edit_line96.textChanged.connect(self.delete_label_tik97)
            self.edit_line96.show()

            self.button96 = QPushButton('OK', self.main_window9)
            self.button96.move(int(0.46 * width), int(h + h2 + 0.55 * height))
            self.button96.resize(int(0.022 * width), int(0.039 * height))
            self.button96.clicked.connect(self.beginning_year_of_simulation_not_including_the_warm_up)
            self.button96.show()

        except:
            pix = QPixmap(exc)
            self.labeltik94.setPixmap(pix)
            self.labeltik94.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik94.move(int(0.312 * width), int(0.234 * height))
            self.labeltik94.show()

    def multiply_btn1(self):
        j = 0
        for i in self.btn_list91:
            if i.isChecked():
                try:
                    try:
                        self.multiply_label1[j].close()
                    except:
                        pass
                    label = QLabel(self.edit_list9[j].text(), self.window9)
                    label.resize(int(0.051 * width), int(0.039 * height))
                    label.move(int(0.15 * width), int(j * 0.065 * height + 0.039 * height))
                    label.show()
                    self.multiply_label1[j] = label
                except:
                    pass
                i.setChecked(False)
            j += 1

    def multiply_btn2(self):
        list_ = list()
        j = 0
        for i in self.btn_list92:
            if i.isChecked():
                try:
                    for k in self.multiply_edit1[j]:
                        k.close()
                except:
                    pass
                window = QWidget(self.window92)
                window.resize(int(0.002 * width + int(self.edit_list92[j].text()) * 0.055 * width), int(0.05 * height))
                scroll = QScrollArea(self.window92)
                scroll.move(int(0.002 * width), int(j * 0.15 * height + 0.06 * height))
                scroll.resize(int(0.337 * width), int(0.075 * height))
                scroll.setWidget(window)
                scroll.show()
                window.show()
                try:
                    for k in range(int(self.edit_list92[j].text())):
                        edit2 = QLineEdit(window)
                        edit2.resize(int(0.051 * width), int(0.039 * height))
                        edit2.move(int(0.002 * width + k * 0.055 * width), int(0.005 * height))
                        edit2.setStyleSheet('background:darkseagreen')
                        edit2.show()
                        list_.append(edit2)

                except:
                    pass
                self.multiply_edit1[j] = list_
                i.setChecked(False)
            j += 1

    def confirm9(self):
        if NUMBER_OF_VARIABLE_TO_GET >= 7:
            h = int(0.468 * height)
        else:
            h = int(NUMBER_OF_VARIABLE_TO_GET * 0.065 * height + 10)
        if NUMBER_OF_VARIABLE_TO_GET >= 7:
            h2 = int(0.6 * height)

        try:
            self.labeltik96.close()
        except:
            pass
        try:
            total = 0
            for i in self.edit_list92:
                total += int(i.text())

            else:
                h2 = int(NUMBER_OF_VARIABLE_TO_GET * 0.13 * height + 10)

            bol = False
            for i in self.multiply_edit1.values():
                for j in i:
                    if int(j.text()):
                        bol = True
                    else:
                        bol = False

            if NUMBER_OF_OBSERVED_VARIABLE == total and bol:
                self.labeltik96 = QLabel(self.main_window9)
                pix = QPixmap(resource_path('tik.png'))
                self.labeltik96.setPixmap(pix)
                self.labeltik96.resize(int(0.026 * width), int(0.04 * height))
                self.labeltik96.move(int(0.56 * width), int(h + h2 + 0.4 * height))
                self.labeltik96.show()
            else:
                self.labeltik96 = QLabel(self.main_window9)
                pix = QPixmap(exc)
                self.labeltik96.setPixmap(pix)
                self.labeltik96.resize(int(0.026 * width), int(0.04 * height))
                self.labeltik96.move(int(0.56 * width), int(h + h2 + 0.4 * height))
                self.labeltik96.show()
        except:
            self.labeltik96 = QLabel(self.main_window9)
            pix = QPixmap(exc)
            self.labeltik96.setPixmap(pix)
            self.labeltik96.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik96.move(int(0.56 * width), int(h + h2 + 0.4 * height))
            self.labeltik96.show()

    def beginning_year_of_simulation_not_including_the_warm_up(self):
        global BEGINNING_YEAR_OF_SIMULATION_NOT_INCLUDING_THE_WARM_UP

        if NUMBER_OF_VARIABLE_TO_GET >= 7:
            h2 = int(0.6 * height)
        else:
            h2 = int(NUMBER_OF_VARIABLE_TO_GET * 0.13 * height + 10)
        
        if NUMBER_OF_VARIABLE_TO_GET >= 7:
            h = int(0.468 * height)
        else:
            h = int(NUMBER_OF_VARIABLE_TO_GET * 0.065 * height + 10)

        self.labeltik97 = QLabel(self.main_window9)
        try:
            BEGINNING_YEAR_OF_SIMULATION_NOT_INCLUDING_THE_WARM_UP = int(self.edit_line96.text())
            pix = QPixmap(resource_path('tik.png'))
            self.labeltik97.setPixmap(pix)
            self.labeltik97.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik97.move(int(0.51 * width), int(h + h2 + 0.55 * height))
            self.labeltik97.show()

            self.label97 = QLabel(self.main_window9)
            self.label97.setText('دوره قابل استفاده شما برای شبیه سازی این بازه خواهد بود :\n شروع بازه : {}'.format(BEGINNING_YEAR_OF_SIMULATION + WARMUP_PERIOD))
            self.label97.resize(int(0.45 * width), int(0.1 * height))
            self.label97.move(int(0.2 * width), int(h + h2 + 0.6 * height))
            self.label97.setStyleSheet(f'font-size: {int(0.013 * width)}px;color:darkmagenta')
            self.label97.show()
        except:
            pix = QPixmap(exc)
            self.labeltik97.setPixmap(pix)
            self.labeltik97.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik97.move(int(0.51 * width),  int(h + h2 + 0.55 * height))
            self.labeltik97.show()

    def delete_label_tik91(self):
        try:
            self.labeltik91.close()
        except:
            pass

    def delete_label_tik92(self):
        try:
            self.labeltik92.close()
        except:
            pass

    def delete_label_tik93(self):
        try:
            self.labeltik93.close()
        except:
            pass

    def delete_label_tik94(self):
        try:
            self.labeltik94.close()
        except:
            pass

    def delete_label_tik95(self):
        try:
            self.labeltik95.close()
        except:
            pass
    
    def delete_label_tik97(self):
        try:
            self.labeltik97.close()
        except:
            pass

    # STUFI2_extract_hru_def
    def beginning_year_of_simulation2(self):
        global BEGINNING_YEAR_OF_SIMULATION2
        self.labeltik101 = QLabel(self.main_window10)
        try:
            BEGINNING_YEAR_OF_SIMULATION2 = int(self.edit_line101.text())
            pix = QPixmap(resource_path('tik.png'))
            self.labeltik101.setPixmap(pix)
            self.labeltik101.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik101.move(int(0.33 * width), int(0.039 * height))
            self.labeltik101.show()
        except:
            pix = QPixmap(exc)
            self.labeltik101.setPixmap(pix)
            self.labeltik101.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik101.move(int(0.33 * width), int(0.039 * height))
            self.labeltik101.show()

    def warmup_period2(self):
        global WARMUP_PERIOD2
        self.labeltik102 = QLabel(self.main_window10)
        try:
            WARMUP_PERIOD2 = int(self.edit_line92.text())
            pix = QPixmap(resource_path('tik.png'))
            self.labeltik102.setPixmap(pix)
            self.labeltik102.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik102.move(int(0.352 * width), int(0.104 * height))
            self.labeltik102.show()
        except:
            pix = QPixmap(exc)
            self.labeltik102.setPixmap(pix)
            self.labeltik102.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik102.move(int(0.352 * width), int(0.104 * height))
            self.labeltik102.show()

    def end_year_of_simulation2(self):
        global END_YEAR_OF_SIMULATION2
        self.labeltik103 = QLabel(self.main_window10)
        try:
            END_YEAR_OF_SIMULATION2 = int(self.edit_line103.text())
            pix = QPixmap(resource_path('tik.png'))
            self.labeltik103.setPixmap(pix)
            self.labeltik103.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik103.move(int(0.292 * width), int(0.169 * height))
            self.labeltik103.show()
        except:
            pix = QPixmap(exc)
            self.labeltik103.setPixmap(pix)
            self.labeltik103.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik103.move(int(0.292 * width), int(0.169 * height))
            self.labeltik103.show()

    def total_number_of_reaches2(self):
        global TOTAL_NUMBER_OF_REACHES2
        self.labeltik105 = QLabel(self.main_window10)
        if NUMBER_OF_VARIABLE_TO_GET2 >= 7:
            h = int(0.468 * height)
        else:
            h = int(NUMBER_OF_VARIABLE_TO_GET2 * 0.065 * height + 10)
        try:
            TOTAL_NUMBER_OF_REACHES2 = int(self.edit_line105.text())
            pix = QPixmap(resource_path('tik.png'))
            self.labeltik105.setPixmap(pix)
            self.labeltik105.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik105.move(int(0.51 * width), h + int(0.38 * height))
            self.labeltik105.show()
        except:
            pix = QPixmap(exc)
            self.labeltik105.setPixmap(pix)
            self.labeltik105.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik105.move(int(0.51 * width), h + int(0.38 * height))
            self.labeltik105.show()

    def number_of_variable_to_get2(self):
        global NUMBER_OF_VARIABLE_TO_GET2
        self.labeltik104 = QLabel(self.main_window10)
        try:
            try:
                self.scroll10.close()
                self.window10.close()
                self.scroll102.close()
                self.window102.close()
                self.label105.close()
                self.edit_line105.close()
                self.button105.close()
                self.labeltik105.close()
                self.labeltik106.close()
                self.confirm_btn10.close()
            except:
                pass

            NUMBER_OF_VARIABLE_TO_GET2 = int(self.edit_line104.text())
            pix = QPixmap(resource_path('tik.png'))
            self.labeltik104.setPixmap(pix)
            self.labeltik104.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik104.move(int(0.312 * width), int(0.234 * height))
            self.labeltik104.show()

            self.window10 = QWidget(self.main_window10)
            self.window10.resize(int(0.235 * width), int(NUMBER_OF_VARIABLE_TO_GET2 * 0.065 * height + 9))
            self.window10.show()

            self.scroll10 = QScrollArea(self.main_window10)
            if NUMBER_OF_VARIABLE_TO_GET2 >= 7:
                h = int(0.468 * height)
            else:
                h = int(NUMBER_OF_VARIABLE_TO_GET2 * 0.065 * height + 10)
            self.scroll10.resize(int(0.25 * width), h)
            self.scroll10.move(int(0.022 * width), int(0.3 * height))
            self.scroll10.setWidget(self.window10)
            self.scroll10.show()

            self.window102 = QWidget(self.main_window10)
            self.window102.resize(int(0.435 * width), int(NUMBER_OF_VARIABLE_TO_GET2 * 0.15 * height + 9))
            self.window102.show()

            self.scroll102 = QScrollArea(self.main_window10)
            if NUMBER_OF_VARIABLE_TO_GET2 >= 7:
                h2 = int(0.6 * height)
            else:
                h2 = int(NUMBER_OF_VARIABLE_TO_GET2 * 0.13 * height + 10)
            self.scroll102.resize(int(0.45 * width), h2)
            self.scroll102.move(int(0.022 * width), h + int(0.45 * height))
            self.scroll102.setWidget(self.window102)
            self.scroll102.show()

            self.main_window10.resize(int(0.76 * width), int(0.87 * height + 2 * h2))

            label = QLabel(self.window10)
            label.setText('variable column number(s) in the swat output file')
            label.setStyleSheet(f'color:#33373B;font-size: {int(0.01 * width)}px; color:white;'
                                f' background :blueviolet;')
            label.resize(int(0.25 * width), int(0.03 * height))
            label.setAlignment(Qt.AlignCenter)
            label.show()

            self.edit_list10 = list()
            self.edit_list102 = list()
            self.label_list10 = list()
            self.btn_list101 = list()
            self.btn_list102 = list()
            self.multiply_label12 = dict()
            self.multiply_edit12 = dict()

            if self.edit_list10:
                for i in self.edit_list10:
                    i.close()
                for i in self.edit_list102:
                    i.close()
                for i in self.label_list10:
                    i.close()
                for i in self.btn_list102:
                    i.close()
                for i in self.btn_list101:
                    i.close()

            number_list = ['first', 'second', 'third', 'forth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth', 'tenth',
                           'eleventh', 'twelfth']

            for i in range(NUMBER_OF_VARIABLE_TO_GET2):
                self.multiply_label12[i] = None

            for i in range(NUMBER_OF_VARIABLE_TO_GET2):
                self.multiply_edit12[i] = None

            for i in range(NUMBER_OF_VARIABLE_TO_GET2):
                label = QLabel(f'{i + 1}', self.window10)
                label.setStyleSheet(f'font-size: {int(0.013 * width)}px; color:red;'
                                    f' background :burlywood;'
                                    f'border-radius: 10px')
                label.setAlignment(Qt.AlignCenter)
                label.resize(int(0.02 * width), int(0.04 * height))
                label.move(int(0.002 * width), int(i * 0.065 * height + 0.039 * height))
                label.show()

                edit = QLineEdit(self.window10)
                edit.resize(int(0.051 * width), int(0.039 * height))
                edit.move(int(0.03 * width), int(i * 0.065 * height + 0.039 * height))
                edit.setStyleSheet('background:white')
                edit.show()
                self.edit_list10.append(edit)
                self.label_list10.append(label)

                btn1 = QPushButton('OK', self.window10)
                btn1.move(int(0.09 * width), int(i * 0.065 * height + 0.039 * height))
                btn1.resize(int(0.022 * width), int(0.039 * height))
                btn1.clicked.connect(self.multiply_btn12)
                btn1.setCheckable(True)
                btn1.setChecked(False)
                btn1.show()
                self.btn_list101.append(btn1)

                label2 = QLabel(self.window102)
                label2.setStyleSheet(f'font-size: {int(0.012 * width)}px;')
                label2.move(int(0.002 * width), int(i * 0.15 * height + 0.019 * height))
                label2.setText(f'number of reaches to get {number_list[i]} variable :')
                label2.show()
                self.label_list10.append(label2)

                edit2 = QLineEdit(self.window102)
                edit2.resize(int(0.051 * width), int(0.039 * height))
                edit2.move(int(0.24 * width), int(i * 0.15 * height + 0.019 * height))
                edit2.setStyleSheet('background:white')
                edit2.show()
                self.edit_list102.append(edit2)

                btn2 = QPushButton('OK', self.window102)
                btn2.move(int(0.3 * width), int(i * 0.15 * height + 0.019 * height))
                btn2.resize(int(0.022 * width), int(0.039 * height))
                btn2.clicked.connect(self.multiply_btn22)
                btn2.setCheckable(True)
                btn2.setChecked(False)
                btn2.show()
                self.btn_list102.append(btn2)

            self.label105 = QLabel('total number of reaches (subbasins) in the project : ', self.main_window10)
            self.label105.setStyleSheet(f'font-size: {int(0.015 * width)}px;')
            self.label105.resize(int(0.35 * width), int(0.039 * height))
            self.label105.move(int(0.022 * width), h + int(0.38 * height))
            self.label105.show()

            self.edit_line105 = QLineEdit(self.main_window10)
            self.edit_line105.move(int(0.4 * width), h + int(0.38 * height))
            self.edit_line105.resize(int(0.051 * width), int(0.039 * height))
            self.edit_line105.textChanged.connect(self.delete_label_tik105)
            self.edit_line105.show()

            self.button105 = QPushButton('OK', self.main_window10)
            self.button105.move(int(0.46 * width), h + int(0.38 * height))
            self.button105.resize(int(0.022 * width), int(0.039 * height))
            self.button105.clicked.connect(self.total_number_of_reaches2)
            self.button105.show()

            self.confirm_btn10 = QPushButton('Confirm', self.main_window10)
            self.confirm_btn10.resize(int(0.051 * width), int(0.039 * height))
            self.confirm_btn10.move(int(0.5 * width), int(h + h2 + 0.4 * height))
            self.confirm_btn10.clicked.connect(self.confirm10)
            self.confirm_btn10.show()

            self.label106 = QLabel('beginning year of simulation not including the warm up : ', self.main_window10)
            self.label106.setStyleSheet(f'font-size: {int(0.015 * width)}px;')
            self.label106.resize(int(0.4 * width), int(0.039 * height))
            self.label106.move(int(0.022 * width), int(h + h2 + 0.55 * height))
            self.label106.show()

            self.edit_line106 = QLineEdit(self.main_window10)
            self.edit_line106.move(int(0.4 * width),int(h + h2 + 0.55 * height))
            self.edit_line106.resize(int(0.051 * width), int(0.039 * height))
            self.edit_line106.textChanged.connect(self.delete_label_tik107)
            self.edit_line106.show()

            self.button106 = QPushButton('OK', self.main_window10)
            self.button106.move(int(0.46 * width), int(h + h2 + 0.55 * height))
            self.button106.resize(int(0.022 * width), int(0.039 * height))
            self.button106.clicked.connect(self.beginning_year_of_simulation_not_including_the_warm_up2)
            self.button106.show()

        except:
            pix = QPixmap(exc)
            self.labeltik104.setPixmap(pix)
            self.labeltik104.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik104.move(int(0.312 * width), int(0.234 * height))
            self.labeltik104.show()

    def multiply_btn12(self):
        j = 0
        for i in self.btn_list101:
            if i.isChecked():
                try:
                    try:
                        self.multiply_label12[j].close()
                    except:
                        pass
                    label = QLabel(self.edit_list10[j].text(), self.window10)
                    label.resize(int(0.051 * width), int(0.039 * height))
                    label.move(int(0.15 * width), int(j * 0.065 * height + 0.039 * height))
                    label.show()
                    self.multiply_label12[j] = label
                except:
                    pass
                i.setChecked(False)
            j += 1

    def multiply_btn22(self):
        list_ = list()
        j = 0
        for i in self.btn_list102:
            if i.isChecked():
                try:
                    for k in self.multiply_edit12[j]:
                        k.close()
                except:
                    pass
                window = QWidget(self.window102)
                window.resize(int(0.002 * width + int(self.edit_list102[j].text()) * 0.055 * width), int(0.05 * height))
                scroll = QScrollArea(self.window102)
                scroll.move(int(0.002 * width), int(j * 0.15 * height + 0.06 * height))
                scroll.resize(int(0.337 * width), int(0.075 * height))
                scroll.setWidget(window)
                scroll.show()
                window.show()
                try:
                    for k in range(int(self.edit_list102[j].text())):
                        edit2 = QLineEdit(window)
                        edit2.resize(int(0.051 * width), int(0.039 * height))
                        edit2.move(int(0.002 * width + k * 0.055 * width), int(0.005 * height))
                        edit2.setStyleSheet('background:darkseagreen')
                        edit2.show()
                        list_.append(edit2)

                except:
                    pass
                self.multiply_edit12[j] = list_
                i.setChecked(False)
            j += 1

    def confirm10(self):
        if NUMBER_OF_VARIABLE_TO_GET2 >= 7:
            h = int(0.468 * height)
        else:
            h = int(NUMBER_OF_VARIABLE_TO_GET2 * 0.065 * height + 10)
        if NUMBER_OF_VARIABLE_TO_GET2 >= 7:
            h2 = int(0.6 * height)

        try:
            self.labeltik106.close()
        except:
            pass
        try:
            total = 0
            for i in self.edit_list102:
                total += int(i.text())

            else:
                h2 = int(NUMBER_OF_VARIABLE_TO_GET2 * 0.13 * height + 10)

            bol = False
            for i in self.multiply_edit12.values():
                for j in i:
                    if int(j.text()):
                        bol = True
                    else:
                        bol = False

            if NUMBER_OF_OBSERVED_VARIABLE2 == total and bol:
                self.labeltik106 = QLabel(self.main_window10)
                pix = QPixmap(resource_path('tik.png'))
                self.labeltik106.setPixmap(pix)
                self.labeltik106.resize(int(0.026 * width), int(0.04 * height))
                self.labeltik106.move(int(0.56 * width), int(h + h2 + 0.4 * height))
                self.labeltik106.show()
            else:
                self.labeltik96 = QLabel(self.main_window10)
                pix = QPixmap(exc)
                self.labeltik106.setPixmap(pix)
                self.labeltik106.resize(int(0.026 * width), int(0.04 * height))
                self.labeltik106.move(int(0.56 * width), int(h + h2 + 0.4 * height))
                self.labeltik106.show()
        except:
            self.labeltik106 = QLabel(self.main_window10)
            pix = QPixmap(exc)
            self.labeltik106.setPixmap(pix)
            self.labeltik106.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik106.move(int(0.56 * width), int(h + h2 + 0.4 * height))
            self.labeltik106.show()

    def beginning_year_of_simulation_not_including_the_warm_up2(self):
        global BEGINNING_YEAR_OF_SIMULATION_NOT_INCLUDING_THE_WARM_UP2

        if NUMBER_OF_VARIABLE_TO_GET2 >= 7:
            h2 = int(0.6 * height)
        else:
            h2 = int(NUMBER_OF_VARIABLE_TO_GET2 * 0.13 * height + 10)
        
        if NUMBER_OF_VARIABLE_TO_GET2 >= 7:
            h = int(0.468 * height)
        else:
            h = int(NUMBER_OF_VARIABLE_TO_GET2 * 0.065 * height + 10)

        self.labeltik107 = QLabel(self.main_window10)
        try:
            BEGINNING_YEAR_OF_SIMULATION_NOT_INCLUDING_THE_WARM_UP2 = int(self.edit_line106.text())
            pix = QPixmap(resource_path('tik.png'))
            self.labeltik107.setPixmap(pix)
            self.labeltik107.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik107.move(int(0.51 * width), int(h + h2 + 0.55 * height))
            self.labeltik107.show()

            self.label107 = QLabel(self.main_window10)
            self.label107.setText('دوره قابل استفاده شما برای شبیه سازی این بازه خواهد بود :\n شروع بازه : {}'.format(BEGINNING_YEAR_OF_SIMULATION2 + WARMUP_PERIOD2))
            self.label107.resize(int(0.45 * width), int(0.1 * height))
            self.label107.move(int(0.2 * width), int(h + h2 + 0.6 * height))
            self.label107.setStyleSheet(f'font-size: {int(0.013 * width)}px;color:darkmagenta')
            self.label107.show()
        except:
            pix = QPixmap(exc)
            self.labeltik107.setPixmap(pix)
            self.labeltik107.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik107.move(int(0.51 * width),  int(h + h2 + 0.55 * height))
            self.labeltik107.show()

    def delete_label_tik101(self):
        try:
            self.labeltik101.close()
        except:
            pass

    def delete_label_tik102(self):
        try:
            self.labeltik102.close()
        except:
            pass

    def delete_label_tik103(self):
        try:
            self.labeltik103.close()
        except:
            pass

    def delete_label_tik104(self):
        try:
            self.labeltik104.close()
        except:
            pass

    def delete_label_tik105(self):
        try:
            self.labeltik105.close()
        except:
            pass

    def delete_label_tik107(self):
        try:
            self.labeltik107.close()
        except:
            pass

    # STUFI2_extract_sub_def
    def beginning_year_of_simulation3(self):
        global BEGINNING_YEAR_OF_SIMULATION3
        self.labeltik111 = QLabel(self.main_window11)
        try:
            BEGINNING_YEAR_OF_SIMULATION3 = int(self.edit_line111.text())
            pix = QPixmap(resource_path('tik.png'))
            self.labeltik111.setPixmap(pix)
            self.labeltik111.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik111.move(int(0.33 * width), int(0.039 * height))
            self.labeltik111.show()
        except:
            pix = QPixmap(exc)
            self.labeltik111.setPixmap(pix)
            self.labeltik111.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik111.move(int(0.33 * width), int(0.039 * height))
            self.labeltik111.show()

    def warmup_period3(self):
        global WARMUP_PERIOD3
        self.labeltik112 = QLabel(self.main_window11)
        try:
            WARMUP_PERIOD3 = int(self.edit_line112.text())
            pix = QPixmap(resource_path('tik.png'))
            self.labeltik112.setPixmap(pix)
            self.labeltik112.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik112.move(int(0.352 * width), int(0.104 * height))
            self.labeltik112.show()
        except:
            pix = QPixmap(exc)
            self.labeltik112.setPixmap(pix)
            self.labeltik112.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik112.move(int(0.352 * width), int(0.104 * height))
            self.labeltik112.show()

    def end_year_of_simulation3(self):
        global END_YEAR_OF_SIMULATION3
        self.labeltik113 = QLabel(self.main_window11)
        try:
            END_YEAR_OF_SIMULATION3 = int(self.edit_line113.text())
            pix = QPixmap(resource_path('tik.png'))
            self.labeltik113.setPixmap(pix)
            self.labeltik113.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik113.move(int(0.292 * width), int(0.169 * height))
            self.labeltik113.show()
        except:
            pix = QPixmap(exc)
            self.labeltik113.setPixmap(pix)
            self.labeltik113.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik113.move(int(0.292 * width), int(0.169 * height))
            self.labeltik113.show()

    def total_number_of_reaches3(self):
        global TOTAL_NUMBER_OF_REACHES3
        self.labeltik115 = QLabel(self.main_window11)
        if NUMBER_OF_VARIABLE_TO_GET3 >= 7:
            h = int(0.468 * height)
        else:
            h = int(NUMBER_OF_VARIABLE_TO_GET3 * 0.065 * height + 10)
        try:
            TOTAL_NUMBER_OF_REACHES3 = int(self.edit_line115.text())
            pix = QPixmap(resource_path('tik.png'))
            self.labeltik115.setPixmap(pix)
            self.labeltik115.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik115.move(int(0.51 * width), h + int(0.38 * height))
            self.labeltik115.show()
        except:
            pix = QPixmap(exc)
            self.labeltik115.setPixmap(pix)
            self.labeltik115.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik115.move(int(0.51 * width), h + int(0.38 * height))
            self.labeltik115.show()

    def number_of_variable_to_get3(self):
        global NUMBER_OF_VARIABLE_TO_GET3
        self.labeltik114 = QLabel(self.main_window11)
        try:
            try:
                self.scroll11.close()
                self.window11.close()
                self.scroll112.close()
                self.window112.close()
                self.label115.close()
                self.edit_line115.close()
                self.button115.close()
                self.labeltik115.close()
                self.labeltik116.close()
                self.confirm_btn11.close()
            except:
                pass

            NUMBER_OF_VARIABLE_TO_GET3 = int(self.edit_line114.text())
            pix = QPixmap(resource_path('tik.png'))
            self.labeltik114.setPixmap(pix)
            self.labeltik114.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik114.move(int(0.312 * width), int(0.234 * height))
            self.labeltik114.show()

            self.window11 = QWidget(self.main_window11)
            self.window11.resize(int(0.235 * width), int(NUMBER_OF_VARIABLE_TO_GET3 * 0.065 * height + 9))
            self.window11.show()

            self.scroll11 = QScrollArea(self.main_window11)
            if NUMBER_OF_VARIABLE_TO_GET3 >= 7:
                h = int(0.468 * height)
            else:
                h = int(NUMBER_OF_VARIABLE_TO_GET3 * 0.065 * height + 10)
            self.scroll11.resize(int(0.25 * width), h)
            self.scroll11.move(int(0.022 * width), int(0.3 * height))
            self.scroll11.setWidget(self.window11)
            self.scroll11.show()

            self.window112 = QWidget(self.main_window11)
            self.window112.resize(int(0.435 * width), int(NUMBER_OF_VARIABLE_TO_GET3 * 0.15 * height + 9))
            self.window112.show()

            self.scroll112 = QScrollArea(self.main_window11)
            if NUMBER_OF_VARIABLE_TO_GET3 >= 7:
                h2 = int(0.6 * height)
            else:
                h2 = int(NUMBER_OF_VARIABLE_TO_GET3 * 0.13 * height + 10)
            self.scroll112.resize(int(0.45 * width), h2)
            self.scroll112.move(int(0.022 * width), h + int(0.45 * height))
            self.scroll112.setWidget(self.window112)
            self.scroll112.show()

            self.main_window11.resize(int(0.76 * width), int(0.87 * height + 2 * h2))

            label = QLabel(self.window11)
            label.setText('variable column number(s) in the swat output file')
            label.setStyleSheet(f'color:#33373B;font-size: {int(0.01 * width)}px; color:white;'
                                f' background :blueviolet;')
            label.resize(int(0.25 * width), int(0.03 * height))
            label.setAlignment(Qt.AlignCenter)
            label.show()

            self.edit_list11 = list()
            self.edit_list112 = list()
            self.label_list11 = list()
            self.btn_list111 = list()
            self.btn_list112 = list()
            self.multiply_label13 = dict()
            self.multiply_edit13 = dict()

            if self.edit_list11:
                for i in self.edit_list11:
                    i.close()
                for i in self.edit_list112:
                    i.close()
                for i in self.label_list11:
                    i.close()
                for i in self.btn_list112:
                    i.close()
                for i in self.btn_list111:
                    i.close()

            number_list = ['first', 'second', 'third', 'forth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth', 'tenth',
                           'eleventh', 'twelfth']

            for i in range(NUMBER_OF_VARIABLE_TO_GET3):
                self.multiply_label13[i] = None

            for i in range(NUMBER_OF_VARIABLE_TO_GET3):
                self.multiply_edit13[i] = None

            for i in range(NUMBER_OF_VARIABLE_TO_GET3):
                label = QLabel(f'{i + 1}', self.window11)
                label.setStyleSheet(f'font-size: {int(0.013 * width)}px; color:red;'
                                    f' background :burlywood;'
                                    f'border-radius: 10px')
                label.setAlignment(Qt.AlignCenter)
                label.resize(int(0.02 * width), int(0.04 * height))
                label.move(int(0.002 * width), int(i * 0.065 * height + 0.039 * height))
                label.show()

                edit = QLineEdit(self.window11)
                edit.resize(int(0.051 * width), int(0.039 * height))
                edit.move(int(0.03 * width), int(i * 0.065 * height + 0.039 * height))
                edit.setStyleSheet('background:white')
                edit.show()
                self.edit_list11.append(edit)
                self.label_list11.append(label)

                btn1 = QPushButton('OK', self.window11)
                btn1.move(int(0.09 * width), int(i * 0.065 * height + 0.039 * height))
                btn1.resize(int(0.022 * width), int(0.039 * height))
                btn1.clicked.connect(self.multiply_btn13)
                btn1.setCheckable(True)
                btn1.setChecked(False)
                btn1.show()
                self.btn_list111.append(btn1)

                label2 = QLabel(self.window112)
                label2.setStyleSheet(f'font-size: {int(0.012 * width)}px;')
                label2.move(int(0.002 * width), int(i * 0.15 * height + 0.019 * height))
                label2.setText(f'number of reaches to get {number_list[i]} variable :')
                label2.show()
                self.label_list11.append(label2)

                edit2 = QLineEdit(self.window112)
                edit2.resize(int(0.051 * width), int(0.039 * height))
                edit2.move(int(0.24 * width), int(i * 0.15 * height + 0.019 * height))
                edit2.setStyleSheet('background:white')
                edit2.show()
                self.edit_list112.append(edit2)

                btn2 = QPushButton('OK', self.window112)
                btn2.move(int(0.3 * width), int(i * 0.15 * height + 0.019 * height))
                btn2.resize(int(0.022 * width), int(0.039 * height))
                btn2.clicked.connect(self.multiply_btn23)
                btn2.setCheckable(True)
                btn2.setChecked(False)
                btn2.show()
                self.btn_list112.append(btn2)

            self.label115 = QLabel('total number of reaches (subbasins) in the project : ', self.main_window11)
            self.label115.setStyleSheet(f'font-size: {int(0.015 * width)}px;')
            self.label115.resize(int(0.35 * width), int(0.039 * height))
            self.label115.move(int(0.022 * width), h + int(0.38 * height))
            self.label115.show()

            self.edit_line115 = QLineEdit(self.main_window11)
            self.edit_line115.move(int(0.4 * width), h + int(0.38 * height))
            self.edit_line115.resize(int(0.051 * width), int(0.039 * height))
            self.edit_line115.textChanged.connect(self.delete_label_tik115)
            self.edit_line115.show()

            self.button115 = QPushButton('OK', self.main_window11)
            self.button115.move(int(0.46 * width), h + int(0.38 * height))
            self.button115.resize(int(0.022 * width), int(0.039 * height))
            self.button115.clicked.connect(self.total_number_of_reaches3)
            self.button115.show()

            self.confirm_btn11 = QPushButton('Confirm', self.main_window11)
            self.confirm_btn11.resize(int(0.051 * width), int(0.039 * height))
            self.confirm_btn11.move(int(0.5 * width), int(h + h2 + 0.4 * height))
            self.confirm_btn11.clicked.connect(self.confirm11)
            self.confirm_btn11.show()

            self.label116 = QLabel('beginning year of simulation not including the warm up : ', self.main_window11)
            self.label116.setStyleSheet(f'font-size: {int(0.015 * width)}px;')
            self.label116.resize(int(0.4 * width), int(0.039 * height))
            self.label116.move(int(0.022 * width), int(h + h2 + 0.55 * height))
            self.label116.show()

            self.edit_line116 = QLineEdit(self.main_window11)
            self.edit_line116.move(int(0.4 * width),int(h + h2 + 0.55 * height))
            self.edit_line116.resize(int(0.051 * width), int(0.039 * height))
            self.edit_line116.textChanged.connect(self.delete_label_tik117)
            self.edit_line116.show()

            self.button116 = QPushButton('OK', self.main_window11)
            self.button116.move(int(0.46 * width), int(h + h2 + 0.55 * height))
            self.button116.resize(int(0.022 * width), int(0.039 * height))
            self.button116.clicked.connect(self.beginning_year_of_simulation_not_including_the_warm_up3)
            self.button116.show()

        except:
            pix = QPixmap(exc)
            self.labeltik114.setPixmap(pix)
            self.labeltik114.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik114.move(int(0.312 * width), int(0.234 * height))
            self.labeltik114.show()

    def multiply_btn13(self):
        j = 0
        for i in self.btn_list111:
            if i.isChecked():
                try:
                    try:
                        self.multiply_label13[j].close()
                    except:
                        pass
                    label = QLabel(self.edit_list11[j].text(), self.window11)
                    label.resize(int(0.051 * width), int(0.039 * height))
                    label.move(int(0.15 * width), int(j * 0.065 * height + 0.039 * height))
                    label.show()
                    self.multiply_label13[j] = label
                except:
                    pass
                i.setChecked(False)
            j += 1

    def multiply_btn23(self):
        list_ = list()
        j = 0
        for i in self.btn_list112:
            if i.isChecked():
                try:
                    for k in self.multiply_edit13[j]:
                        k.close()
                except:
                    pass
                window = QWidget(self.window112)
                window.resize(int(0.002 * width + int(self.edit_list112[j].text()) * 0.055 * width), int(0.05 * height))
                scroll = QScrollArea(self.window112)
                scroll.move(int(0.002 * width), int(j * 0.15 * height + 0.06 * height))
                scroll.resize(int(0.337 * width), int(0.075 * height))
                scroll.setWidget(window)
                scroll.show()
                window.show()
                try:
                    for k in range(int(self.edit_list112[j].text())):
                        edit2 = QLineEdit(window)
                        edit2.resize(int(0.051 * width), int(0.039 * height))
                        edit2.move(int(0.002 * width + k * 0.055 * width), int(0.005 * height))
                        edit2.setStyleSheet('background:darkseagreen')
                        edit2.show()
                        list_.append(edit2)

                except:
                    pass
                self.multiply_edit13[j] = list_
                i.setChecked(False)
            j += 1

    def confirm11(self):
        if NUMBER_OF_VARIABLE_TO_GET3 >= 7:
            h = int(0.468 * height)
        else:
            h = int(NUMBER_OF_VARIABLE_TO_GET3 * 0.065 * height + 10)
        if NUMBER_OF_VARIABLE_TO_GET3 >= 7:
            h2 = int(0.6 * height)

        try:
            self.labeltik116.close()
        except:
            pass
        try:
            total = 0
            for i in self.edit_list112:
                total += int(i.text())

            else:
                h2 = int(NUMBER_OF_VARIABLE_TO_GET3 * 0.13 * height + 10)

            bol = False
            for i in self.multiply_edit13.values():
                for j in i:
                    if int(j.text()):
                        bol = True
                    else:
                        bol = False

            if NUMBER_OF_OBSERVED_VARIABLE3 == total and bol:
                self.labeltik116 = QLabel(self.main_window11)
                pix = QPixmap(resource_path('tik.png'))
                self.labeltik116.setPixmap(pix)
                self.labeltik116.resize(int(0.026 * width), int(0.04 * height))
                self.labeltik116.move(int(0.56 * width), int(h + h2 + 0.4 * height))
                self.labeltik116.show()
            else:
                self.labeltik116 = QLabel(self.main_window11)
                pix = QPixmap(exc)
                self.labeltik116.setPixmap(pix)
                self.labeltik116.resize(int(0.026 * width), int(0.04 * height))
                self.labeltik116.move(int(0.56 * width), int(h + h2 + 0.4 * height))
                self.labeltik116.show()
        except:
            self.labeltik116 = QLabel(self.main_window11)
            pix = QPixmap(exc)
            self.labeltik116.setPixmap(pix)
            self.labeltik116.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik116.move(int(0.56 * width), int(h + h2 + 0.4 * height))
            self.labeltik116.show()

    def beginning_year_of_simulation_not_including_the_warm_up3(self):
        global BEGINNING_YEAR_OF_SIMULATION_NOT_INCLUDING_THE_WARM_UP3

        if NUMBER_OF_VARIABLE_TO_GET3 >= 7:
            h2 = int(0.6 * height)
        else:
            h2 = int(NUMBER_OF_VARIABLE_TO_GET3 * 0.13 * height + 10)
        
        if NUMBER_OF_VARIABLE_TO_GET3 >= 7:
            h = int(0.468 * height)
        else:
            h = int(NUMBER_OF_VARIABLE_TO_GET3 * 0.065 * height + 10)

        self.labeltik117 = QLabel(self.main_window11)
        try:
            BEGINNING_YEAR_OF_SIMULATION_NOT_INCLUDING_THE_WARM_UP3 = int(self.edit_line116.text())
            pix = QPixmap(resource_path('tik.png'))
            self.labeltik117.setPixmap(pix)
            self.labeltik117.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik117.move(int(0.51 * width), int(h + h2 + 0.55 * height))
            self.labeltik117.show()

            self.label117 = QLabel(self.main_window11)
            self.label117.setText('دوره قابل استفاده شما برای شبیه سازی این بازه خواهد بود :\n شروع بازه : {}'.format(BEGINNING_YEAR_OF_SIMULATION3 + WARMUP_PERIOD3))
            self.label117.resize(int(0.45 * width), int(0.1 * height))
            self.label117.move(int(0.2 * width), int(h + h2 + 0.6 * height))
            self.label117.setStyleSheet(f'font-size: {int(0.013 * width)}px;color:darkmagenta')
            self.label117.show()
        except:
            pix = QPixmap(exc)
            self.labeltik117.setPixmap(pix)
            self.labeltik117.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik117.move(int(0.51 * width),  int(h + h2 + 0.55 * height))
            self.labeltik117.show()

    def delete_label_tik111(self):
        try:
            self.labeltik111.close()
        except:
            pass

    def delete_label_tik112(self):
        try:
            self.labeltik112.close()
        except:
            pass

    def delete_label_tik113(self):
        try:
            self.labeltik113.close()
        except:
            pass

    def delete_label_tik114(self):
        try:
            self.labeltik114.close()
        except:
            pass

    def delete_label_tik115(self):
        try:
            self.labeltik115.close()
        except:
            pass
    
    def delete_label_tik117(self):
        try:
            self.labeltik117.close()
        except:
            pass

    # observed
    def number_of_observed_variable_main(self):
        global NUMBER_OF_OBSERVED_VARIABLE_MAIN
        self.window12 = QWidget(self.main_window12)
        self.labeltik121 = QLabel(self.main_window12)

        try:
            self.confirm_btn12.close()
            self.label122.close()
            self.button122.close()
            self.edit_line122.close()
            self.labeltik121.close()
        except:
            pass
        try:
            self.labeltik123.close()
        except:
            pass
        try:
            self.label124.close()
            self.edit_line124.close()
            self.button124.close()
            self.label123.close()
            self.edit_line123.close()
            self.button123.close()
        except:
            pass
        try:
            self.labeltik125.close()
        except:
            pass
        try:
            self.window12_.close()
            self.scroll12_.close()
            self.confirm_btn12_.close()
        except:
            pass
        try:
            self.next_btn12.close()
        except:
            pass
        try:
            int(self.edit_line121.text())
            NUMBER_OF_OBSERVED_VARIABLE_MAIN = int(self.edit_line121.text())
            if NUMBER_OF_OBSERVED_VARIABLE_MAIN <= NUMBER_OF_OBSERVED_VARIABLE + NUMBER_OF_OBSERVED_VARIABLE2 + NUMBER_OF_OBSERVED_VARIABLE3:
                pix = QPixmap(resource_path('tik.png'))
                self.labeltik121.setPixmap(pix)
                self.labeltik121.resize(int(0.026 * width), int(0.04 * height))
                self.labeltik121.move(int(0.33 * width), int(0.039 * height))
                self.labeltik121.show()

                self.window12.resize(int(0.285 * width), int(NUMBER_OF_OBSERVED_VARIABLE_MAIN * 0.065 * height))
                # self.window12.move(int(0.021 * width), int(0.1 * height))

                scroll = QScrollArea(self.main_window12)
                scroll.resize(int(0.32 * width), int(0.6 * height))
                scroll.move(int(0.021 * width), int(0.1 * height))

                self.edit_list12 = list()
                if NUMBER_OF_OBSERVED_VARIABLE_MAIN:
                    for i in range(NUMBER_OF_OBSERVED_VARIABLE_MAIN):
                        label = QLabel(f'{i + 1}', self.window12)
                        label.setStyleSheet(f'font-size: {int(0.013 * width)}px; color:red;'
                                            f' background :burlywood;'
                                            f'border-radius: 10px')
                        label.setAlignment(Qt.AlignCenter)
                        label.resize(int(0.02 * width), int(0.04 * height))
                        label.move(int(0.005 * width), int(0.013 * height + i * 0.065 * height))

                        edit2 = QLineEdit(self.window12)
                        edit2.setStyleSheet('background: white')
                        edit2.resize(int(0.234 * width), int(0.039 * height))
                        edit2.move(int(0.025 * width), int(0.013 * height + i * 0.065 * height))
                        self.edit_list12.append(edit2)
                        edit2.show()

                    self.edit_list12[0].textChanged.connect(self.separation12)

                    scroll.setWidget(self.window12)

                    self.confirm_btn12 = QPushButton('Confirm', self.main_window12)
                    self.confirm_btn12.resize(int(0.051 * width), int(0.039 * height))
                    self.confirm_btn12.move(int(0.35 * width), int(0.66 * height))
                    self.confirm_btn12.clicked.connect(self.confirm12)
                    self.confirm_btn12.show()

                    scroll.show()
            else:
                raise
        except:
            pix = QPixmap(exc)
            self.labeltik121.setPixmap(pix)
            self.labeltik121.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik121.move(int(0.33 * width), int(0.039 * height))
            self.labeltik121.show()

    def separation12(self):
        if len(self.edit_list12[0].text().split('\n')) >= 2:
            edit_list = self.edit_list12[0].text().split('\n')
            j = 0
            for i in self.edit_list12:
                i.setText(edit_list[j])
                j += 1

    def confirm12(self):
        self.list_of_stations12 = list()
        try:
            self.labeltik122.close()
        except:
            pass
        self.labeltik122 = QLabel(self.main_window12)
        counter = 0
        for i in self.edit_list12:
            if i.text():
                counter += 1
        if counter == len(self.edit_list12):
            pix = QPixmap(resource_path('tik.png'))
            self.labeltik122.setPixmap(pix)
            self.labeltik122.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik122.move(int(0.41 * width), int(0.66 * height))
            self.labeltik122.show()

            self.label122 = QLabel('objective function Type : ', self.main_window12)
            self.label122.setStyleSheet(f'font-size: {int(0.015 * width)}px;')
            self.label122.resize(int(0.24 * width), int(0.039 * height))
            self.label122.move(int(0.022 * width), int(0.72 * height))
            self.label122.show()

            self.edit_line122 = QLineEdit(self.main_window12)
            self.edit_line122.move(int(0.22 * width), int(0.72 * height))
            self.edit_line122.resize(int(0.051 * width), int(0.039 * height))
            self.edit_line122.textChanged.connect(self.delete_label_tik122)
            self.edit_line122.show()

            self.button122 = QPushButton('OK', self.main_window12)
            self.button122.move(int(0.282 * width), int(0.72 * height))
            self.button122.resize(int(0.022 * width), int(0.039 * height))
            self.button122.clicked.connect(self.objective_function_type)
            self.button122.show()
        else:
            pix = QPixmap(exc)
            self.labeltik122.setPixmap(pix)
            self.labeltik122.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik122.move(int(0.41 * width), int(0.66 * height))
            self.labeltik122.show()

    def objective_function_type(self):
        global OBJECTIVE_FUNCTION_TYPE
        self.labeltik123 = QLabel(self.main_window12)
        self.number_of_observed_variable_12 += 1
        try:
            self.labeltik123.close()
        except:
            pass
        try:
            self.label124.close()
            self.edit_line124.close()
            self.button124.close()
            self.label123.close()
            self.edit_line123.close()
            self.button123.close()
        except:
            pass
        try:
            self.labeltik125.close()
        except:
            pass
        try:
            self.window12_.close()
            self.scroll12_.close()
            self.confirm_btn12_.close()
        except:
            pass
        try:
            self.next_btn12.close()
        except:
            pass
        try:
            OBJECTIVE_FUNCTION_TYPE = int(self.edit_line122.text())
            if 1 <= OBJECTIVE_FUNCTION_TYPE <= 11:
                pix = QPixmap(resource_path('tik.png'))
                self.labeltik123.setPixmap(pix)
                self.labeltik123.resize(int(0.026 * width), int(0.04 * height))
                self.labeltik123.move(int(0.34 * width), int(0.72 * height))
                self.labeltik123.show()

                self.label124 = QLabel('Station Name : ', self.main_window12)
                self.label124.setStyleSheet(f'font-size: {int(0.015 * width)}px;')
                self.label124.resize(int(0.22 * width), int(0.039 * height))
                self.label124.move(int(0.022 * width), int(0.78 * height))
                self.label124.show()

                self.edit_line124 = QLineEdit(self.main_window12)
                self.edit_line124.move(int(0.14 * width), int(0.78 * height))
                self.edit_line124.resize(int(0.17 * width), int(0.039 * height))
                self.edit_line124.textChanged.connect(self.delete_label_tik124)
                self.edit_line124.show()

                self.button124 = QPushButton('OK', self.main_window12)
                self.button124.move(int(0.33 * width), int(0.78 * height))
                self.button124.resize(int(0.022 * width), int(0.039 * height))
                self.button124.clicked.connect(self.station_name12)
                self.button124.show()

                self.label123 = QLabel('Number Of Data Points For This Variable : ', self.main_window12)
                self.label123.setStyleSheet(f'font-size: {int(0.015 * width)}px;')
                self.label123.resize(int(0.32 * width), int(0.039 * height))
                self.label123.move(int(0.022 * width), int(0.83 * height))
                self.label123.show()

                self.edit_line123 = QLineEdit(self.main_window12)
                self.edit_line123.move(int(0.3 * width), int(0.83 * height))
                self.edit_line123.resize(int(0.051 * width), int(0.039 * height))
                self.edit_line123.textChanged.connect(self.delete_label_tik123)
                self.edit_line123.show()

                self.button123 = QPushButton('OK', self.main_window12)
                self.button123.move(int(0.37 * width), int(0.83 * height))
                self.button123.resize(int(0.022 * width), int(0.039 * height))
                self.button123.clicked.connect(self.number_of_data_points_for_this_variable_main)
                self.button123.show()

            else:
                raise
        except:
            pix = QPixmap(exc)
            self.labeltik122.setPixmap(pix)
            self.labeltik122.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik122.move(int(0.34 * width), int(0.72 * height))
            self.labeltik122.show()

    def station_name12(self):
        try:
            self.list_of_stations12.append(self.edit_line124.text())
            self.labeltik125 = QLabel(self.main_window12)
            pix = QPixmap(resource_path('tik.png'))
            self.labeltik125.setPixmap(pix)
            self.labeltik125.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik125.move(int(0.38 * width), int(0.78 * height))
            self.labeltik125.show()
        except:
            self.labeltik125 = QLabel(self.main_window12)
            pix = QPixmap(exc)
            self.labeltik125.setPixmap(pix)
            self.labeltik125.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik125.move(int(0.38 * width), int(0.78 * height))
            self.labeltik125.show()

    def number_of_data_points_for_this_variable_main(self):
        global NUMBER_OF_DATA_POINTS_MAIN
        try:
            self.window12_.close()
        except:
            pass
        try:
            self.scroll12_.close()
        except:
            pass
        try:
            NUMBER_OF_DATA_POINTS_MAIN = int(self.edit_line123.text())
            self.labeltik124 = QLabel(self.main_window12)
            pix = QPixmap(resource_path('tik.png'))
            self.labeltik124.setPixmap(pix)
            self.labeltik124.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik124.move(int(0.42 * width), int(0.83 * height))
            self.labeltik124.show()

            self.window12_ = QWidget(self.main_window12)
            self.window12_.resize(int(0.385 * width), int(NUMBER_OF_DATA_POINTS_MAIN * 0.065 * height + 10))
            self.window12_.show()
            # self.window22.move(int(0.001 * width), int(0.193 * height))
            self.scroll12_ = QScrollArea(self.main_window12)
            self.scroll12_.resize(int(0.4 * width), int(0.59 * height))
            self.scroll12_.move(int(0.022 * width), int(0.9 * height))
            self.scroll12_.setWidget(self.window12_)

            self.edit_list12_ = list()
            for i in range(NUMBER_OF_DATA_POINTS_MAIN):
                label = QLabel(f'{i + 1}', self.window12_)
                label.setStyleSheet(f'font-size: {int(0.013 * width)}px; color:red;'
                                    f' background :burlywood;'
                                    f'border-radius: 10px')
                label.setAlignment(Qt.AlignCenter)
                label.resize(int(0.02 * width), int(0.04 * height))
                label.move(int(0.002 * width), int(i * 0.065 * height + 10))
                label.show()

                edit1 = QLineEdit(self.window12_)
                edit1.setStyleSheet('background: white; color:red')
                edit1.resize(int(0.034 * width), int(0.039 * height))
                edit1.move(int(0.025 * width), int(i * 0.065 * height + 10))
                edit1.show()

                edit2 = QLineEdit(self.window12_)
                edit2.setStyleSheet('background: white')
                edit2.resize(int(0.17 * width), int(0.039 * height))
                edit2.move(int(0.065 * width), int(i * 0.065 * height + 10))
                edit2.show()

                edit3 = QLineEdit(self.window12_)
                edit3.setStyleSheet('background: white; color:red')
                edit3.resize(int(0.04 * width), int(0.039 * height))
                edit3.move(int(0.24 * width), int(i * 0.065 * height + 10))
                edit3.show()

                self.edit_list12_.append([edit1, edit2, edit3])

            self.confirm_btn12_ = QPushButton('Confirm', self.main_window12)
            self.confirm_btn12_.resize(int(0.051 * width), int(0.039 * height))
            self.confirm_btn12_.move(int(0.45 * width), int(1.44 * height))
            self.confirm_btn12_.clicked.connect(self.confirm122)
            self.confirm_btn12_.show()

            self.scroll12_.show()
        except:
            self.labeltik124 = QLabel(self.main_window12)
            pix = QPixmap(exc)
            self.labeltik124.setPixmap(pix)
            self.labeltik124.resize(int(0.026 * width), int(0.04 * height))
            self.labeltik124.move(int(0.42 * width), int(0.83 * height))
            self.labeltik124.show()

    def confirm122(self):
        list_of_first_number = list()
        list_of_first_column_error = list()
        for i in self.edit_list12_:
            if i[0].text():
                try:
                    list_of_first_number.append(int(i[0].text()))
                    if list_of_first_number != natsorted(list_of_first_number) or len(
                            np.unique(list_of_first_number)) != len(list_of_first_number):
                        list_of_first_column_error.append(self.edit_list12_.index(i))
                except:
                    list_of_first_column_error.append(self.edit_list12_.index(i))
            else:
                list_of_first_column_error.append(self.edit_list12_.index(i))

        list_of_text = list()
        list_of_second_column_error = list()
        for i in self.edit_list12_:
            if i[1].text():
                list_of_text.append(i[1].text())
            else:
                list_of_second_column_error.append(self.edit_list12_.index(i))

        list_of_second_number = list()
        list_of_third_column_error = list()
        for i in self.edit_list12_:
            if i[2].text():
                try:
                    list_of_second_number.append(float(i[2].text()))
                except:
                    list_of_third_column_error.append(self.edit_list12_.index(i))
            else:
                list_of_third_column_error.append(self.edit_list12_.index(i))

        if self.list_label_tik12:
            for i in self.list_label_tik12:
                i.close()
        self.list_label_tik12 = list()
        try:
            self.next_btn12.close()
        except:
            pass

        counter = 0
        for i in range(NUMBER_OF_DATA_POINTS_MAIN):
            if i in list_of_first_column_error or i in list_of_second_column_error or i in list_of_third_column_error:
                label = QLabel(self.window12_)
                pix = QPixmap(exc)
                label.setPixmap(pix)
                label.resize(int(0.026 * width), int(0.04 * height))
                label.move(int(0.28 * width), int(i * 0.065 * height + 10))
                label.show()
                self.list_label_tik12.append(label)
            else:
                label = QLabel(self.window12_)
                pix = QPixmap(resource_path('tik.png'))
                label.setPixmap(pix)
                label.resize(int(0.026 * width), int(0.04 * height))
                label.move(int(0.28 * width), int(i * 0.065 * height + 10))
                label.show()
                self.list_label_tik12.append(label)
                counter += 1

        if counter == NUMBER_OF_DATA_POINTS_MAIN and self.number_of_observed_variable_12 != NUMBER_OF_OBSERVED_VARIABLE_MAIN:
            self.next_btn12 = QPushButton('Next', self.main_window12)
            self.next_btn12.resize(int(0.051 * width), int(0.039 * height))
            self.next_btn12.move(int(0.53 * width), int(1.44 * height))
            self.next_btn12.clicked.connect(self.objective_function_type)
            self.next_btn12.show()

    def delete_label_tik121(self):
        try:
            self.labeltik121.close()
        except:
            pass

    def delete_label_tik122(self):
        try:
            self.labeltik123.close()
        except:
            pass

    def delete_label_tik123(self):
        try:
            self.labeltik124.close()
        except:
            pass

    def delete_label_tik124(self):
        try:
            self.labeltik125.close()
        except:
            pass

    def confirm13(self):
        if self.list_label_tik13:
            for i in self.list_label_tik13:
                i.close()

        for i in range(NUMBER_OF_OBSERVED_VARIABLE_MAIN):
            try:
                re.findall(r'(.+)\.txt', self.edit_list13[i].text())[0]

                if self.edit_list13[i].text() and re.findall(r'(.+)\.txt', self.edit_list13[i].text())[0] == \
                        self.list_of_stations12[i] and re.search(r'(.+)\.txt', self.edit_list13[i].text()):
                    label = QLabel(self.window13)
                    pix = QPixmap(resource_path('tik.png'))
                    label.setPixmap(pix)
                    label.resize(int(0.026 * width), int(0.04 * height))
                    label.move(int(0.28 * width), int(i * 0.065 * height + 10))
                    label.show()
                    self.list_label_tik13.append(label)
                else:
                    label = QLabel(self.window13)
                    pix = QPixmap(exc)
                    label.setPixmap(pix)
                    label.resize(int(0.026 * width), int(0.04 * height))
                    label.move(int(0.28 * width), int(i * 0.065 * height + 10))
                    label.show()
                    self.list_label_tik13.append(label)
            except:
                label = QLabel(self.window13)
                pix = QPixmap(exc)
                label.setPixmap(pix)
                label.resize(int(0.026 * width), int(0.04 * height))
                label.move(int(0.28 * width), int(i * 0.065 * height + 10))
                label.show()
                self.list_label_tik13.append(label)

    def create_error_base(self):
        self.error_base_img = QLabel(self.tree)
        pix = QPixmap(exc)
        self.error_base_img.setPixmap(pix)
        self.error_base_img.resize(int(0.026 * width), int(0.04 * height))
        self.error_base_img.move(int(0.03 * width / 5), int(0.6 * height))
        self.error_base_img.show()

        self.error_label_base = QLabel(self.tree)
        self.error_label_base.move(int(0.16 * width / 5), int(0.608 * height))
        self.error_label_base.setText('Click on error to show detail')
        self.error_label_base.setStyleSheet(f'color:orangered;font-size: {int(0.012 * width)}px;')
        self.error_label_base.show()

    # def show_error(self, event):
    #     self.error_comment_img = QLabel(self.tree)
    #     pix = QPixmap(co)
    #     self.error_comment_img.setPixmap(pix)
    #     self.error_comment_img.resize(int(0.35 * width), int(0.25 * height))
    #     self.error_comment_img.move(int(0.03 * width / 5), int(0.6 * height))
    #     self.error_comment_img.show()
    #     QEnterEvent.clone()
    #     print(event.clone())
    #     # self.error_text = QLabel(self.tree)
    #     # self.error_text.setText(text)
    #     # self.error_text.setStyleSheet(f'color:white;font-size: {int(0.012 * width)}px;')
    #     # self.error_text.move(int(0.1 * width / 5), int(0.72 * height))
    #     # self.error_text.show()

    # def delete_error(self):
    #     self.error_comment_img.close()
    #     self.error_text.close()

    # def delete_error_base(self):
        self.error_base_img.close()
        self.error_label_base.close()


def showDialog(self):
        MainWindow = QMainWindow()
        fname, _ = QFileDialog.getOpenFileName(MainWindow, 'Open file', "", 'xlsx Files (*.xlsx)')
        return fname

if __name__ == "__main__":
    app = QApplication()

    w = Widget()
    w.setWindowState(Qt.WindowMaximized)
    # w.resize(1000,700)
    width = w.screen().geometry().width()
    height = w.screen().geometry().height()

    w.show()

    with open('style.qss', 'w') as f:
        f.write("""
        QListWidget {
            color: #FFFFFF;
            background-color: #33373B;
            }

            QListWidget::item {
            height: 50px;
            }

            QListWidget::item:selected {
            background-color: #2ABf9E;
            }

            /*QLabel {*/
            /*    background-color: #FFFFFF;*/
            /*    qproperty-alignment: AlignCenter*/
            /*}*/

            QTreeWidget {
            color: #FFFFFF;
            background-color: #33373B;
            font-size: 18px;
            }

            QTreeWidget::item:selected {
            background-color: #2ABf9E;
            }

            QLabel{
            color: #33373B;
            background-color: None;
            }

            QLineEdit {
            border: 2px solid gray;
            border-radius: 10px;
            padding: 0 8px;
            background: greenyellow;
            selection-background-color: darkgray;
            font-size: 18px;
            }

            QLineEdit[echoMode="2"] {
            lineedit-password-character: 9679;
            }

            QLineEdit:read-only {
            background: lightblue;
            }

            QPushButton {
            border: 2px solid #8f8f91;
            border-radius: 10px;
            background-color: #2ABf9E;
            min-width: 50px;
            }

            QPushButton:pressed {
            background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                              stop: 0 #dadbde, stop: 1 #f6f7fa);
            }

            QPushButton:flat {
            border: none; /* no border for a flat push button */
            }

            QPushButton:default {
            border-color: navy; /* make the default button prominent */
            }

            QScrollBar:vertical {
            border: blue;
            background: orangered;
            border-radius: 10px;
            }

            QScrollBar:horizontal {
            border: blue;
            background: blue;
            border-radius: 10px;
            }
        """)

    with open("style.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)

    sys.exit(app.exec())
