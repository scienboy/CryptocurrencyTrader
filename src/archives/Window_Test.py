import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from src.archives.Worker import *
from src.archives.Window_Graph import *
from src.dbs.db_manager import *

ui_tester = uic.loadUiType("ui/Tester.ui")[0]

class Window_Test(QMainWindow, ui_tester):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # layout = QVBoxLayout()
        # layout.addWidget(self.label)

        self.tickers = ["BTC", "ETH", "BCH", "ETC"]
        self.tableWidget.setRowCount(len(self.tickers))

        self.worker = Worker(self.tickers)
        self.worker.customized_signal_fill_table.connect(self.update_table_widget)
        self.worker.start()
        self.pushButton.clicked.connect(self.inquiry)
        self.pushButton_2.clicked.connect(self.create_db(self.lineEdit_2))
        self.pushButton_3.clicked.connect(self.create_table(self.lineEdit_3))

    @pyqtSlot(dict)
    def update_table_widget(self, data):
        try:
            for ticker, infos in data.items():
                index = self.tickers.index(ticker)

                self.tableWidget.setItem(index, 0, QTableWidgetItem(ticker))
                self.tableWidget.setItem(index, 1, QTableWidgetItem(str(infos[0])))
                self.tableWidget.setItem(index, 2, QTableWidgetItem(str(infos[1])))
                self.tableWidget.setItem(index, 3, QTableWidgetItem(str(infos[2])))
        except:
            pass

    def inquiry(self):
        fname = QFileDialog.getOpenFileName(self)   # 탐색기 열어 파일지정해서 fname에 담음
        self.lineEdit.setText(str(fname[0]))        # 네모칸에 경로 출력

        dlg = Window_Graph(fname[0])    # 다이얼로그 인스턴스 생성
        dlg.exec_()             # 다이얼로그 띄움


        # price = pykorbit.get_current_price("BTC")
        # self.lineEdit.setText(str(price))
        print("조회 버튼 클릭")

    def create_db(self, db_name):
        self.dbManager = DB_Manager(db_name)
        self.dbManager.create_db(db_name)

    def create_table(self, db_name, table_name):
        self.dbManager = DB_Manager(db_name)
        self.dbManager.create_table(table_name)


    # def open_url(self):
    #     QDesktopServices::openUrl
    #     print("조회 버튼 클릭")


