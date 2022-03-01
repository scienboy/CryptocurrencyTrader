import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from src.archives.Window_Test import *


class Tester():
    def __init__(self):
        self.generate_window()

    def generate_window(self):
        app = QApplication(sys.argv)  # QApplication 객체 생성

        window = Window_Test()
        window.show()

        app.exec_()  # 이벤트 루프 생성