# -*- coding: utf-8 -*-
import numpy as np
from random import sample


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

# class Sudoku:
#     def __init__(self):
#         self.board = np.zeros((9, 9), dtype=int)
#         self._rows = np.arange(9)
#         self._cols = np.arange(9)
#
#         self.generate_board()
#
#     def generate_board(self):
#         for i in self._rows:
#             for j in self._cols:
#                 if self.board[i][j] == 0:
#                     valid_nums = [num for num in range(1, 10) if self.is_valid(i, j, num)]
#                     if valid_nums:
#                         for num in valid_nums:
#                             self.board[i][j] = num
#                             if self.generate_board():
#                                 return True
#                             self.board[i][j] = 0
#                     return False
#         return True
#
#     def regenerate_board(self):
#         self.board = np.zeros((9, 9), dtype=int)
#         self.generate_board()
#
#     def is_valid(self, row, col, num):
#         if np.any(self.board[row] == num):
#             return False
#         if np.any(self.board[:, col] == num):
#             return False
#         start_row = row - row % 3
#         start_col = col - col % 3
#         if np.any(self.board[start_row:start_row + 3, start_col:start_col + 3] == num):
#             return False
#         return True
#
#     def mask_numbers(self, difficulty):
#         num_to_mask = int(91 * difficulty)
#         num_to_mask = min(num_to_mask, 81)  # Ensure num_to_mask does not exceed 81
#         flattened_board = self.board.flatten()
#         masked_indices = np.random.choice(np.arange(81), size=num_to_mask, replace=False)
#         flattened_board[masked_indices] = 0
#         # self.board = flattened_board.reshape(9, 9)
#         return flattened_board.reshape(9, 9)
#
#     def print_board(self):
#         print(self.board)
#


class Sudoku:
    def __init__(self, base=3):
        self.board = None
        self.base = base
        self.side = base * base

    def pattern(self, r, c):
        return (self.base * (r % self.base) + r // self.base + c) % self.side

    def shuffle(self, s):
        return sample(s, len(s))

    def generate_board(self):
        rBase = range(self.base)
        rows = [g * self.base + r for g in self.shuffle(rBase) for r in self.shuffle(rBase)]
        cols = [g * self.base + c for g in self.shuffle(rBase) for c in self.shuffle(rBase)]
        nums = self.shuffle(range(1, self.base * self.base + 1))

        # produce board using randomized baseline pattern
        board = [[nums[self.pattern(r, c)] for c in cols] for r in rows]

        squares = self.side * self.side
        empties = squares * 3 // 4
        for _ in sample(range(squares), empties):
            r, c = divmod(_, self.side)
            board[r][c] = 0

        self.board = np.array(board)

    def print_board(self):
        print(self.board)


if __name__ == '__main__':
    sudoku = Sudoku(base=3)
    sudoku.generate_board()

    print(sudoku.board)
