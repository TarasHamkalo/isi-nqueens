from typing import List

import numpy
import numpy as np


class Solver:

    def __init__(self, n: int):
        self.n = n
        self.board: numpy.array = self.initialize_board()
        self.steps = []

    def solve(self):
        raise NotImplemented("Abstract")

    def get_queens(self) -> List[int]:
        # sequence of queens columns queens[row] -> col
        raise NotImplemented("Abstract")

    def get_nodes_expanded(self) -> int:
        raise NotImplemented("Abstract")

    def get_steps(self):
        return self.steps

    def reset(self):
        self.board = self.initialize_board()
        self.steps = []

    def initialize_board(self) -> numpy.array:
        return np.zeros((self.n, self.n), dtype=int)

    def is_on_board(self, i, j) -> bool:
        return 0 <= i < self.n and 0 <= j < self.n

    def get_diagonal_indexes(self, i, j) -> List[List[int]]:
        indexes = [[i, j]]
        for k in range(1, self.n):
            if self.is_on_board(i + k, j + k):
                indexes.append([i + k, j + k])

            if self.is_on_board(i - k, j - k):
                indexes.append([i - k, j - k])

            if self.is_on_board(i - k, j + k):
                indexes.append([i - k, j + k])

            if self.is_on_board(i + k, j - k):
                indexes.append([i + k, j - k])

        return indexes

    def print_board(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.board[i][j] == 1:
                    print("Q", end="")
                else:
                    print(".", end="")

            print("")
