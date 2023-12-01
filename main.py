# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, uic
import sys
from sudoku import Sudoku


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        self.setFixedSize(650, 450)
        uic.loadUi('MainWindow.ui', self)
        self.show()

        sudoku = Sudoku().mask_numbers(0.5)
        print(sudoku)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()
