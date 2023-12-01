# -*- coding: utf-8 -*-
import numpy as np


# def generate_board(self):
#     for i in range(9):
#         for j in range(9):
#             if self.board[i][j] == 0:
#                 for num in range(1, 10):
#                     if self.is_valid(i, j, num):
#                         self.board[i][j] = num
#                         if self.generate_board():
#                             return True
#                         self.board[i][j] = 0
#                 return False
#     return True

class Sudoku:
    def __init__(self):
        self.board = np.zeros((9, 9), dtype=int)
        self._rows = np.arange(9)
        self._cols = np.arange(9)

        self.generate_board()

    def generate_board(self):
        for i in self._rows:
            for j in self._cols:
                if self.board[i][j] == 0:
                    valid_nums = [num for num in range(1, 10) if self.is_valid(i, j, num)]
                    if valid_nums:
                        for num in valid_nums:
                            self.board[i][j] = num
                            if self.generate_board():
                                return True
                            self.board[i][j] = 0
                    return False
        return True

    def regenerate_board(self):
        self.board = np.zeros((9, 9), dtype=int)
        self.generate_board()

    def is_valid(self, row, col, num):
        if np.any(self.board[row] == num):
            return False
        if np.any(self.board[:, col] == num):
            return False
        start_row = row - row % 3
        start_col = col - col % 3
        if np.any(self.board[start_row:start_row + 3, start_col:start_col + 3] == num):
            return False
        return True

    def mask_numbers(self, difficulty):
        num_to_mask = int(91 * difficulty)
        num_to_mask = min(num_to_mask, 81)  # Ensure num_to_mask does not exceed 81
        flattened_board = self.board.flatten()
        masked_indices = np.random.choice(np.arange(81), size=num_to_mask, replace=False)
        flattened_board[masked_indices] = 0
        # self.board = flattened_board.reshape(9, 9)
        return flattened_board.reshape(9, 9)

    def print_board(self):
        print(self.board)


if __name__ == '__main__':
    sudoku = Sudoku()
    sudoku.print_board()
    new_board = sudoku.mask_numbers(0.5)
    print(new_board)

    sudoku.generate_board()
    sudoku.print_board()



