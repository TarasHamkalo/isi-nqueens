from typing import List

import numpy
import numpy as np


# Základná trieda pre všetky algoritmy riešenia (solver)
class Solver:

    def __init__(self, n: int):
        self.n = n # predstavuje veľkosť problému n-kráľovien
        self.board: numpy.array = self.initialize_board() # šachovnica, reprezentuje stav problému
        self.steps = [] # používa sa na účely UI (zaznamenávajú sa všetky kroky algoritmu)

    def solve(self) -> None:
        """
        Táto metóda by mala byť volaná, aby solver sa pokúsil vyriešiť problém
        :return: None
        """
        raise NotImplemented("Abstract")

    def get_queens(self) -> List[int]:
        """
        Po volaní solve() by mal solver poskytnúť konečné pozície kráľovien
        vo formáte queens[row] = col
        :return: List[int]
        """
        raise NotImplemented("Abstract")

    def get_nodes_expanded(self) -> int:
        """
        Po volaní solve() by mal solver poskytnúť počet uzlov (stavov),
        ktoré boli skontrolované počas vykonávania
        :return: int
        """
        raise NotImplemented("Abstract")

    def get_steps(self):
        """
        Po volaní solve() by mal solver poskytnúť kroky, ktoré vykonal
        Kroky sú zaznamenané ako dvojice (row, col) a reprezentujú zmenu stavu tejto bunky
        Na strane UI to znamená prepnutie kráľovnej na tejto pozícii
        (ak board[row][col] obsahuje kráľovnú potom board[row][col] <- prázdna a naopak)
        :return: List[List[int]]
        """
        return self.steps

    def reset(self) -> None:
        """
        Táto funkcia by mala vymazať stav solver pred opakovným vykonaním
        :return: None
        """
        self.board = self.initialize_board()
        self.steps = []

    def initialize_board(self) -> numpy.array:
        return np.zeros((self.n, self.n), dtype=int)

    def is_on_board(self, i, j) -> bool:
        return 0 <= i < self.n and 0 <= j < self.n

    def get_diagonal_indexes(self, i, j) -> List[List[int]]:
        """
        Vypočíta indexy diagonál, na ktorých sa nachádza pozícia [i][j]
        """
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
