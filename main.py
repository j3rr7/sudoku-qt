# -*- coding: utf-8 -*-
import contextlib
import itertools
import os
import sys
import csv
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTimer, QTime, QRegExp, Qt
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import (
    QMessageBox,
    QDialog,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QGridLayout,
    QHBoxLayout,
)
from sudoku import Sudoku
from typing import List, Optional, Union, Tuple


class Scores:
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
        self.player_name = None

        self.game_running = False

        self.timer = None
        self.timer_counter = QTimer()

        self.current_difficulty = 0.0

        self.scores: List[Scores] = []

        # Setup
        self._setup_timer()
        self._setup_buttons()
        self._setup_buttons_events()
        self._setup_game()

        self.toggle_board_enabled()  # disable the game board on start

        self._load_scores()  # Load Scores

        # Setup Line Edit Change Events
        for i, j in itertools.product(range(9), range(9)):
            self.button_matrix[i][j].textChanged[str].connect(
                self._on_line_edit_changed
            )

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
        for i, j in itertools.product(range(9), range(9)):
            le_name = f"le_{i}_{j}"  # find name of line edit based on row and col
            line_edit = self.findChild(QtWidgets.QLineEdit, le_name)
            line_edit.setMaxLength(1)
            line_edit.setValidator(rx)
            self.button_matrix[i][j] = line_edit

    def _setup_buttons_events(self):
        self.btn_start.clicked.connect(self._on_start_clicked)
        self.btn_reset.clicked.connect(self._on_reset_clicked)
        self.btn_cek.clicked.connect(self._on_check_click)

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
        self._setup_buttons_and_timer()
        # if game is not running
        if not self.game_running:
            # reset timer
            self.reset_timer()

            # Show MessageBox
            msgBox = QMessageBox()
            # Reset Board Color
            for i, j in itertools.product(range(9), range(9)):
                self.button_matrix[i][j].setStyleSheet("")

            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText("Game Stopped")
            msgBox.setWindowTitle("Game Over")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()

    def _on_reset_clicked(self):
        self.reset_game()
        self.update_board_text()

    def _on_toggle_difficulty(self):
        if self.current_difficulty == self.get_difficulty():
            return

        self.current_difficulty = self.get_difficulty()
        self.sudoku.board = self.sudoku.get_solution()
        self.sudoku.remove_numbers(self.current_difficulty)

        self.update_board_text()

    def _on_check_click(self):
        solution = self.sudoku.get_solution()

        dialog = QDialog(self)
        dialog.setWindowTitle("Cek")
        dialog.setModal(False)

        main_layout = QVBoxLayout()
        grid_layout = QGridLayout()

        for i, j in itertools.product(range(9), range(9)):
            label = QLabel(str(solution[i][j]))
            label.setAlignment(Qt.AlignCenter)
            grid_layout.addWidget(label, i, j)

        main_layout.addLayout(grid_layout)

        if self.player_name:
            self._show_scores(main_layout)

        dialog.setLayout(main_layout)
        dialog.setMinimumSize(200, 200)
        dialog.show()

    def _show_scores(self, main_layout):
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Your name: {self.player_name}"))
        layout.addWidget(QLabel("=== Scores ==="))
        player_scores = sorted(
            [score for score in self.scores if score.name == self.player_name],
            key=lambda x: x.time,
            reverse=True,
        )
        grouped_scores = itertools.groupby(player_scores, key=lambda x: x.difficulty)
        for difficulty, scores in grouped_scores:
            print(f"Difficulty: {difficulty}")
            top_scores = list(scores)[:5]
            for score in top_scores:
                layout.addWidget(QLabel(f"{score.difficulty} - {score.time}"))
        main_layout.addLayout(layout)

        # Update Color Based on Solution (Optional)
        # for i, j in itertools.product(range(9), range(9)):
        #     if current_board[i][j] != solution[i][j]:
        #         self.button_matrix[i][j].setStyleSheet("background-color: red;")
        #     else:
        #         self.button_matrix[i][j].setStyleSheet("")

    def _on_line_edit_changed(self, text: str):
        # Our Safety Check for empty string
        if (
            not isinstance(text, str)
            or text is None
            or text.isspace()
            or not text.strip()
        ):
            return

        line_edit_id = self.sender().objectName()  #
        _, i, j = line_edit_id.split("_")
        if self.sudoku.is_valid(int(text), (int(i), int(j))):
            self.sudoku.board[int(i)][int(j)] = int(text)
            # ============ ENABLE/DISABLE IF NEEDED ===========
            # Will be used in case of invalid input on current row and cell will be red
            # =========================================
            self.button_matrix[int(i)][int(j)].setStyleSheet("")
        else:
            self.button_matrix[int(i)][int(j)].setStyleSheet("background-color: red;")

        # Check if board and solution are the same
        if self.sudoku.board.all() == self.sudoku.get_solution().all():
            self.game_over()

    def _on_about_clicked(self):
        self.about_window = AboutWindow()
        self.about_window.show()

    def _on_highscore_clicked(self):
        self.score_window = ScoreWindow(self.scores)
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
        # set all button to enabled and disabled based on game_running
        for i, j in itertools.product(range(9), range(9)):
            self.button_matrix[i][j].setEnabled(
                self.game_running if self.button_matrix[i][j].text() == "" else False
            )

        # toggle radio buttons
        self.rb_pemula.setEnabled(not self.game_running)
        self.rb_menengah.setEnabled(not self.game_running)
        self.rb_mahir.setEnabled(not self.game_running)

    def toggle_timer_enabled(self):
        self.timer.start(1000) if self.game_running else self.timer.stop()

    def reset_game(self):
        if self.game_running:
            self._setup_buttons_and_timer()

        # Reset Timer
        self.reset_timer()

        # Reset Board
        self.sudoku.reset_board()
        self.current_difficulty = self.get_difficulty()
        self.sudoku.remove_numbers(self.current_difficulty)

        self.update_board_text()

        # Reset Color
        for i, j in itertools.product(range(9), range(9)):
            self.button_matrix[i][j].setStyleSheet("")

    def _setup_buttons_and_timer(self):
        self.toggle_start_button_text()
        self.toggle_board_enabled()
        self.toggle_timer_enabled()

    def get_difficulty(
        self, include_string: bool = False
    ) -> Union[float, Tuple[float, str]]:
        """
        Get difficulty from radio button

        Args:
        include_string: Whether to include the difficulty string in the return value

        Returns:
        The difficulty as a float. If include_string is True, it also returns the difficulty string.
        """
        if self.rb_pemula.isChecked():
            return (0.2, "Pemula") if include_string else 0.2
        elif self.rb_menengah.isChecked():
            return (0.5, "Menengah") if include_string else 0.5
        elif self.rb_mahir.isChecked():
            return (0.8, "Mahir") if include_string else 0.8

    def update_board_text(self):
        for i, j in itertools.product(range(9), range(9)):
            self.button_matrix[i][j].setText(
                str(self.sudoku.board[i][j]) if self.sudoku.board[i][j] != 0 else ""
            )

    def reset_timer(self):
        self.timer_counter = QTime(0, 0, 0)
        self.lbl_timer.setText(self.timer_counter.toString("HH:mm:ss"))

    def game_over(self):
        # stop timer
        self.timer.stop()

        # Add Prompt to insert name using pyqt
        name_dialog = NameDialog(self)
        if name_dialog.exec_() == QDialog.Accepted:
            name = name_dialog.name_input.text()

            self.player_name = name

            self.scores.append(
                Scores(
                    name=name,
                    difficulty=self.get_difficulty(include_string=True)[1],
                    time=self.timer_counter.toString("HH:mm:ss"),
                )
            )

            self._save_scores()

        self.reset_game()

    # endregion

    # region Highscores Functions

    def _save_scores(self):
        """
        Save highscores to file
        """
        with contextlib.suppress(FileNotFoundError):
            with open("highscores.csv", "w", newline="") as f:
                writer = csv.writer(f)
                if os.fstat(f.fileno()).st_size == 0:
                    writer.writerow(["Name", "Difficulty", "Time"])
                for scores in self.scores:
                    writer.writerow([scores.name, scores.difficulty, scores.time])

    def _load_scores(self):
        """
        Load highscores from file
        """
        with contextlib.suppress(FileNotFoundError):
            with open("highscores.csv", "r") as f:
                reader = csv.reader(f)
                for row in reader:
                    self.scores.append(
                        Scores(name=row[0], difficulty=row[1], time=row[2])
                    )

    # endregion


class AboutWindow(QtWidgets.QDialog):
    def __init__(self):
        super(AboutWindow, self).__init__()
        uic.loadUi("AboutWindow.ui", self)


class ScoreWindow(QtWidgets.QDialog):
    def __init__(self, scores):
        super(ScoreWindow, self).__init__()
        uic.loadUi("ScoreWindow.ui", self)
        self.scores = scores

        self.cb_difficulty.currentIndexChanged.connect(self.update_scores)
        self.cb_difficulty.insertItem(0, "Pemula")
        self.cb_difficulty.insertItem(1, "Menengah")
        self.cb_difficulty.insertItem(2, "Mahir")

    def update_scores(self):
        current_idx = self.cb_difficulty.currentIndex()
        self.list_scores.clear()

        if current_idx == 0:
            self.find_5_highest_score("Pemula")
        elif current_idx == 1:
            self.find_5_highest_score("Menengah")
        elif current_idx == 2:
            self.find_5_highest_score("Mahir")

    def find_5_highest_score(self, difficulty: str):
        diff_scores = [
            scores for scores in self.scores if scores.difficulty == difficulty
        ]
        sorted_scores = sorted(diff_scores, key=lambda x: x.time, reverse=True)[:5]
        for scores in sorted_scores:
            self.list_scores.insertItem(
                0, f"Nama : {scores.name}, Waktu : {scores.time}"
            )


class NameDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Insert Name")

        self.name_label = QLabel("Enter your name:")
        self.name_input = QLineEdit()

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_name)

        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def submit_name(self):
        name = self.name_input.text()
        # Do something with the name, e.g. save it or display it
        self.accept()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
