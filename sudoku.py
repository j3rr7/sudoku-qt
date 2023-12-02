# -*- coding: utf-8 -*-
import numpy as np
import time


# region Utility Decorator For Timing
def timer_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Execution time of {func.__name__}: {end_time - start_time} seconds")
        return result

    return wrapper


# endregion


class Sudoku:
    @timer_decorator
    def __init__(self, size: int = 9):
        self.memo = {}  # memoization

        self.size = size
        self.board = np.zeros((size, size), dtype=int)

        self.reset_board()

        # save the original board to solve it
        self.solved_board = self.board.copy()

    @timer_decorator
    def reset_board(self):
        if self.size is None:
            return

        self.board = np.zeros((self.size, self.size), dtype=int)

        # Fill the first index with shuffled numbers
        numbers = np.arange(1, self.size + 1)
        np.random.shuffle(numbers)
        self.board[:, 0] = numbers

        self.solve_board()

        self.solved_board = self.board.copy()  # save the original board to solve it

    def is_valid(self, num, pos):
        # Check row
        for i in range(len(self.board[0])):
            if self.board[pos[0]][i] == num and pos[1] != i:
                return False

        # Check column
        for i in range(len(self.board)):
            if self.board[i][pos[1]] == num and pos[0] != i:
                return False

        # Check box
        box_x = pos[1] // 3
        box_y = pos[0] // 3
        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if self.board[i][j] == num and (i, j) != pos:
                    return False
        return True

    def solve_board(self):
        key = tuple(map(tuple, self.board))
        if key in self.memo:
            return self.memo[key]

        find = self.find_empty()
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, self.size + 1):
            if self.is_valid(i, (row, col)):
                self.board[row][col] = i

                if self.solve_board():
                    self.memo[key] = True
                    return True

                self.board[row][col] = 0

        self.memo[key] = False
        return False

    def find_empty(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == 0:
                    return i, j  # row, col
        return None

    @timer_decorator
    def print_board(self):
        for i in range(len(self.board)):
            if i % 3 == 0 and i != 0:
                print("- - - - - - - - - - - - - ")
            for j in range(len(self.board[0])):
                if j % 3 == 0 and j != 0:
                    print(" | ", end="")
                if j == 8:
                    print(self.board[i][j])
                else:
                    print(str(self.board[i][j]) + " ", end="")

    @timer_decorator
    def remove_numbers(self, difficulty: float = 1, replace: bool = True):
        masked_board = self.board if replace else self.board.copy()

        # sorry, need to cap the difficulty between 0.2 and 0.8
        difficulty = max(0.2, min(difficulty, 0.8))
        for i in range(int(self.size * self.size * difficulty)):
            row = np.random.randint(0, self.size)
            col = np.random.randint(0, self.size)
            masked_board[row][col] = 0

        return masked_board

    def get_solved_board(self):
        return self.solved_board.copy()


def test_sudoku():
    sudoku = Sudoku()
    sudoku.remove_numbers(0)
    print(sudoku.board)
    print(sudoku.get_solved_board())


if __name__ == "__main__":
    test_sudoku()
