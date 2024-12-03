from typing import List

from .constants import QUEEN
from .solver import Solver

class DfsBacktracking(Solver):
    """
    Implementuje základný algoritmus 'backtracking'
    """

    def __init__(self, n):
        super().__init__(n)
        self.nodes_expanded = 0
        self.queens = []

    def solve(self):
        """
        Prejde riadky počnúc riadkom 0, umiestni kráľovnú na pozíciu (stĺpec zľava doprava),
        kde nie je ohrozená, a opakuje pre ďalší riadok, kým nie sú umiestnené všetky kráľovné.
        """
        self.dfs(0)

    def reset(self):
        super().reset()
        self.nodes_expanded = 0
        self.queens = []

    def get_queens(self) -> List[int]:
        if len(self.queens) == 0:
            raise ValueError("solve() method was not called")

        queens = [-1] * self.n
        for i, j in self.queens:
            queens[i] = j

        return queens

    def get_nodes_expanded(self):
        return self.nodes_expanded

    def dfs(self, queen):
        if queen == self.n:
            # ak sú všetke kráľovne umiestnené, tak najdené riešenie
            return True

        for col in range(0, self.n):
            if not self.is_safe(queen, col):
                # ak sa kráľovná nedá bezpečne umiestniť
                continue

            # záznam kráľovnej a krokov
            self.nodes_expanded += 1
            self.board[queen][col] = QUEEN
            self.steps.append([queen, col])

            if self.dfs(queen + 1):
                # záznam kráľovnej, po vyriešení problemu
                self.queens.append((queen, col))
                return True

            self.steps.append([queen, col])
            self.board[queen][col] = 0

        return False

    def is_safe(self, queen, col):
        """
        Kontrola, či je dáma v pozícii (queen, col) v konflikte s inou dámou
        """

        if self.board[:, col].sum() > 0:
            return False

        for di, dj in self.get_diagonal_indexes(queen, col):
            if self.board[di][dj] == QUEEN:
                return False

        return True
