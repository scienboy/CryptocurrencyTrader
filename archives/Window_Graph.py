from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas_datareader.data as web
from DB_Manager import *
import sqlite3
import pandas as pd
from pandas import Series, DataFrame
# from pandas import DataFrame as df

ui_graph = uic.loadUiType("ui/Graph.ui")[0]

# class Window_Graph(QDialog, ui_graph):
#     def __init__(self, fname):
#         super().__init__()
#         self.setupUi(self)
#         # self.fname = fname
#
#         # self.buttonBox.button(QDialogButtonBox.Cancel).clicked.connect(self.role_cancel)
#         # self.buttonBox.button(QDialogButtonBox.Open).clicked.connect(self.role_open)
#         # self.buttonBox.accepted.connect(self.role_okay)         # Qt Designer 우측하단 '시그널/슬롯 편집기'에 시그널 기준으로 내용이 들어감.
#         # self.buttonBox.rejected.connect(self.role_okay)         # Qt Designer 우측하단 '시그널/슬롯 편집기'에 시그널 기준으로 내용이 들어감.
#         # self.pushButton_01.clicked.connect(self.role_close)
#
#     def role_okay(self):
#         print('okay!!!')
#
#     def role_cancel(self):
#         print('cancel!!!')
#
#     def role_close(self):
#         print('close!!!')
#
#     def role_open(self):
#         print('open!!!')



class Window_Graph(QDialog):
    def __init__(self, fname):
        super().__init__()
        self.dbManager = DB_Manager()
        self.setUi_plus()

    def setUi_plus(self):
        self.setGeometry(600, 200, 1200, 600)
        self.setWindowTitle("PyChart Viewer v0.1")
        self.setWindowIcon(QIcon('icon.png'))

        self.lineEdit = QLineEdit()
        self.btn_drawChart = QPushButton("차트그리기")
        self.btn_drawChart.clicked.connect(self.drawChartClicked)
        self.btn_createDB = QPushButton("DB생성")
        self.btn_createDB.clicked.connect(self.createDBClicked)
        self.btn_insertData = QPushButton("Data 추가")
        self.btn_insertData.clicked.connect(self.insertDataClicked)

        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)

        leftLayout = QVBoxLayout()
        leftLayout.addWidget(self.canvas)

        # Right Layout
        rightLayout = QVBoxLayout()
        rightLayout.addWidget(self.lineEdit)
        rightLayout.addWidget(self.btn_drawChart)   # 버튼 실제 그려주는 부분
        rightLayout.addWidget(self.btn_createDB)
        rightLayout.addWidget(self.btn_insertData)
        rightLayout.addStretch(1)                   # 버튼 위쪽으로 올려 정렬

        layout = QHBoxLayout()
        layout.addLayout(leftLayout)                # Layout에 내용 올리기
        layout.addLayout(rightLayout)               # Layout에 내용 올리기
        # layout.setStretchFactor(leftLayout, 1)
        # layout.setStretchFactor(rightLayout, 0)

        self.setLayout(layout)

    def createDBClicked(self):
        self.dbManager.create_table('test2')

    def insertDataClicked(self):
        self.dbManager.insert_data()

    def drawChartClicked(self):
        code = self.lineEdit.text()
        df = web.DataReader(code + ".KS", "yahoo")
        df['MA20'] = df['Adj Close'].rolling(window=20).mean()
        df['MA60'] = df['Adj Close'].rolling(window=60).mean()

        ax = self.fig.add_subplot(111)                          # fig의 1row 1col 1x 에다가 그림그리기
        ax.plot(df.index, df['Adj Close'], label='Adj Close')
        ax.plot(df.index, df['MA20'], label='MA20')
        ax.plot(df.index, df['MA60'], label='MA60')
        ax.legend(loc='upper right')
        ax.grid()

        self.canvas.draw()