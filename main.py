# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTimer, QTime, QRegExp
from PyQt5.QtGui import QRegExpValidator
from sudoku import Sudoku


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        self.about_window = None
        self.score_window = None
        uic.loadUi('MainWindow.ui', self)
        self.show()

        # region Setup Buttons Matrix
        pattern = QRegExp("[1-9]")
        rx = QRegExpValidator(pattern)
        self.button_matrix = [[None for _ in range(9)] for _ in range(9)]

        for i in range(9):
            for j in range(9):
                le_name = f"le_{i}_{j}"
                line_edit = self.findChild(QtWidgets.QLineEdit, le_name)
                line_edit.setMaxLength(1)
                line_edit.setValidator(rx)
                self.button_matrix[i][j] = line_edit
        # endregion

        # region Fields
        self.game_running = False

        self.timer = None
        self.timer_counter = 0

        # endregion

        self.setup_timer()
        self.setup_buttons()
        # self.setup_game()

    def setup_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer_label)
        self.timer_counter = QTime(0, 0, 0)

    def setup_buttons(self):
        self.btn_start.clicked.connect(self.toggle_start_stop)
        self.btn_reset.clicked.connect(self.reset_game)
        self.btn_about.clicked.connect(self.open_about_window)
        self.btn_highscore.clicked.connect(self.open_score_window)

    def setup_game(self):
        sudoku = Sudoku().mask_numbers(0.5)
        print(sudoku)

    # region Timer Functions
    def update_timer_label(self):
        self.timer_counter = self.timer_counter.addSecs(1)
        self.lbl_timer.setText(self.timer_counter.toString("HH:mm:ss"))

    def toggle_start_stop(self):
        if self.game_running:
            self.timer.stop()
            self.btn_start.setText("Start")
            self.game_running = False
        else:
            self.reset_game()
            self.timer.start(1000)
            self.btn_start.setText("Stop")
            self.game_running = True

    def reset_game(self):
        self.timer.stop()
        self.timer_counter = QTime(0, 0)
        self.btn_start.setText("Start")
        self.lbl_timer.setText("00:00:00")
        self.game_running = False

    def open_about_window(self):
        self.about_window = AboutWindow()
        print(self.about_window)
        print(dir(self.about_window))
        print(help(self.about_window))
        self.about_window.show()

    def open_score_window(self):
        self.score_window = ScoreWindow()
        self.score_window.show()
    # endregion


class AboutWindow(QtWidgets.QDialog):
    def __init__(self):
        super(AboutWindow, self).__init__()
        uic.loadUi('AboutWindow.ui', self)


class ScoreWindow(QtWidgets.QDialog):
    def __init__(self):
        super(ScoreWindow, self).__init__()
        uic.loadUi('ScoreWindow.ui', self)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec()
