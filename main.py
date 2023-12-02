# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTimer, QTime, QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QRadioButton, QMessageBox
from sudoku import Sudoku
from typing import List, Optional


class Highscore:
    def __init__(self, name, difficulty, time):
        self.name = name
        self.difficulty = difficulty
        self.time = time


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi("MainWindow.ui", self)

        # Local Variables
        self.sudoku = None
        self.about_window = None
        self.score_window = None

        self.game_running = False

        self.timer = None
        self.timer_counter = QTimer()

        self.current_difficulty = 0.0

        self.highscores: List[Highscore] = []

        # Setup
        self._setup_timer()
        self._setup_buttons()
        self._setup_buttons_events()
        self._setup_game()

        self.toggle_board_enabled()  # disable the game board on start

    # region Setup Functions

    def _setup_timer(self) -> None:
        self.timer = QTimer()
        self.timer.timeout.connect(self._on_update_timer)
        self.timer_counter = QTime(0, 0, 0)

    def _setup_buttons(self):
        pattern = QRegExp("[1-9]")
        rx = QRegExpValidator(pattern)
        self.button_matrix: List[List[Optional[QtWidgets.QLineEdit]]] = [
            [None for _ in range(9)] for _ in range(9)
        ]

        # setup line edits and set input validation to one numerical character from 1 to size + 1
        for i in range(9):
            for j in range(9):
                le_name = f"le_{i}_{j}"  # find name of line edit based on row and col
                line_edit = self.findChild(QtWidgets.QLineEdit, le_name)
                line_edit.setMaxLength(1)
                line_edit.setValidator(rx)
                self.button_matrix[i][j] = line_edit

    def _setup_buttons_events(self):
        self.btn_start.clicked.connect(self._on_start_clicked)
        self.btn_reset.clicked.connect(self._on_reset_clicked)

        self.rb_pemula.toggled.connect(self._on_toggle_difficulty)
        self.rb_menengah.toggled.connect(self._on_toggle_difficulty)
        self.rb_mahir.toggled.connect(self._on_toggle_difficulty)

        self.btn_about.clicked.connect(self._on_about_clicked)
        self.btn_highscore.clicked.connect(self._on_highscore_clicked)

    def _setup_game(self):
        self.sudoku = Sudoku(size=9)

        # set difficulty to the lowest = 0.2 # hardcoded
        self.current_difficulty = 0.2
        self.sudoku.remove_numbers(self.current_difficulty)

        # Populate buttons with puzzle
        self.update_board_text()

    # endregion

    # region Events Functions

    def _on_start_clicked(self):
        self.toggle_start_button_text()
        self.toggle_board_enabled()
        self.toggle_timer_enabled()

        # if game is not running
        if not self.game_running:
            # reset timer
            self.reset_timer()

            # Show MessageBox
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText("Game Stopped")
            msgBox.setWindowTitle("Game Over")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()

    def _on_reset_clicked(self):
        self.reset_game()
        self.update_board_text()

    def _on_toggle_difficulty(self):
        # check if current difficulty is the same as get_difficulty()
        # if not, remove numbers
        # if yes, do nothing

        if self.current_difficulty == self.get_difficulty():
            return

        self.current_difficulty = self.get_difficulty()
        self.sudoku.board = self.sudoku.get_solved_board()
        self.sudoku.remove_numbers(self.current_difficulty)

        self.update_board_text()

    def _on_check_click(self):
        # ToDo: Check if the answer is correct and find the number of wrong answers
        pass

    def _on_line_edit_changed(self):
        # ToDo: Add Event every time a line edit value is changed ( gameover )
        pass

    def _on_about_clicked(self):
        self.about_window = AboutWindow()
        self.about_window.show()

    def _on_highscore_clicked(self):
        self.score_window = ScoreWindow()
        self.score_window.show()

    def _on_update_timer(self):
        self.timer_counter = self.timer_counter.addSecs(1)
        self.lbl_timer.setText(self.timer_counter.toString("HH:mm:ss"))

    # endregion

    # region UI Functions

    def toggle_start_button_text(self):
        self.game_running = not self.game_running
        self.btn_start.setText("Stop" if self.game_running else "Start")

    def toggle_board_enabled(self):
        for i in range(9):
            for j in range(9):
                self.button_matrix[i][j].setEnabled(
                    self.game_running
                    if self.button_matrix[i][j].text() == ""
                    else False
                )

    def toggle_timer_enabled(self):
        self.timer.start(1000) if self.game_running else self.timer.stop()

    def reset_game(self):
        if self.game_running:
            self.toggle_start_button_text()
            self.toggle_board_enabled()
            self.toggle_timer_enabled()

        # Reset Timer
        self.reset_timer()

        # Reset Board
        self.sudoku.reset_board()
        self.current_difficulty = self.get_difficulty()
        self.sudoku.remove_numbers(self.current_difficulty)

    def get_difficulty(self) -> float:
        """
        Get difficulty from radio button
        """
        if self.rb_pemula.isChecked():
            return 0.2
        elif self.rb_menengah.isChecked():
            return 0.5
        elif self.rb_mahir.isChecked():
            return 0.8

    def update_board_text(self):
        for i in range(9):
            for j in range(9):
                self.button_matrix[i][j].setText(
                    str(self.sudoku.board[i][j]) if self.sudoku.board[i][j] != 0 else ""
                )

    def reset_timer(self):
        self.timer_counter = QTime(0, 0, 0)
        self.lbl_timer.setText(self.timer_counter.toString("HH:mm:ss"))

    # endregion

    # region Highscores Functions

    def _save_scores(self):
        """
        Save highscores to file

        ToDo: Implement
        """
        pass

    def _load_scores(self):
        """
        Load highscores from file

        ToDo: Implement
        """
        pass

    # endregion


class AboutWindow(QtWidgets.QDialog):
    def __init__(self):
        super(AboutWindow, self).__init__()
        uic.loadUi("AboutWindow.ui", self)


class ScoreWindow(QtWidgets.QDialog):
    def __init__(self):
        super(ScoreWindow, self).__init__()
        uic.loadUi("ScoreWindow.ui", self)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
