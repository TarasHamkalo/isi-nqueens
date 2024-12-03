from typing import List

from .constants import QUEEN, EMPTY
from .solver import Solver


class Dfs(Solver):
    """
    Implementuje algoritmus 'dfs'
    """

    def __init__(self, n: int):
        super().__init__(n)
        self.queens = []  # sleduje pozície kráľovien
        self.nodes_expanded = 0  # sleduje počet krokov

    def solve(self):
        """
        Prechádza riadok po riadku, začínajúc od riadku 0,
        umiestňuje kráľovnú na nejakú pozíciu (stľpec, zľava doprava)
        a kontroluje, či je daný stav cieľovým stavom.
        """
        self._solve(0)

    def reset(self):
        super().reset()
        self.queens = []
        self.nodes_expanded = 0

    def get_queens(self) -> List[int]:
        if len(self.queens) == 0:
            raise ValueError("solve() method was not called")

        queens = [-1] * self.n
        for i, j in self.queens:
            queens[i] = j
        return queens

    def get_nodes_expanded(self):
        return self.nodes_expanded

    def _solve(self, i) -> bool:
        if i == self.n:
            # ak bol dosiahnutý posledný riadok, stop DFS
            return False

        for j in range(0, self.n):
            # sleduje pozície kráľovien a kroky
            self.board[i][j] = QUEEN

            self.queens.append((i, j))
            self.steps.append((i, j))

            self.nodes_expanded += 1 # počítadlo krokov

            if self.is_goal_state():
                # ak bol nájdený cieľový stav, vrátiť
                return True

            # prejsť do iných stavov, začínajúc od ďalšieho riadku
            if self._solve(i + 1):
                return True

            # ak cieľový stav nebol nájdený pri aktuálnom umiestnení, odstrániť
            self.board[i][j] = EMPTY
            self.steps.append((i, j))
            self.queens.pop()

        return False

    def is_goal_state(self):
        """
         Cieľový stav: Všetky kráľovné sú umiestnené a žiadna z nich sa nenapadá.
        :return:
        """
        return len(self.queens) == self.n and self.no_queens_attack()

    def no_queens_attack(self):
        for i, j in self.queens:
            # pre každú umiestnenú kráľovnú skontrolovať, či sa nekonfliktuje s inou
            if not self.is_safe(i, j):
                return False

        return True

    def is_safe(self, i, j):
        """
        Skontrolovať, či sa nachádza iná kráľovná okrem tejto v stĺpci alebo diagonále
        :param i: queen row
        :param j: queen column
        :return:
        """

        # skontrolovať súčet stĺpca, ak > QUEEN, potom je umiestnených viac ako jedna kráľovná
        if self.board[:, j].sum() - QUEEN > 0:
            return False

        for di, dj in self.get_diagonal_indexes(i, j):
            if di == i and dj == j:
                continue

            if self.board[di][dj] == QUEEN:
                return False

        return True
