import random
from typing import List

import numpy as np

from solver.constants import QUEEN, EMPTY
from solver.solver import Solver


# track number of queens on each diagonal/anti-diagonal and column
# count attacking pairs for each possible state
class Neighbor:
    def __init__(self, queen: int, orig_col: int, next_col: int, heuristic_score: int = int(-1e32)):
        self.queen: int = queen
        self.orig_col: int = orig_col
        self.next_col: int = next_col
        self.heuristic_score: int = heuristic_score

class HillClimbing(Solver):

    def __init__(self, n):
        super().__init__(n)
        # self.queens = {i: Domain(self.n) for i in range(self.n)}
        self.queens = [-1] * self.n # track which queen and where (row: col)
        self.columns = [0] * self.n # track number of queens in each column
        self.diag = [0] * (2 * self.n - 1) # track number of queens in each main diagonals
        self.anti_diag = [0] * (2 * self.n - 1) # track number of queens in each reverse diagonal
        # self.columns = {i: 0 for i in range(n)}
        # self.diag = {i: 0 for i in range(n)}
        # self.anti_diag = {i: 0 for i in range(n)}
        self.post_init()

    def post_init(self):
        for row in range(self.n):
            col = random.randint(0, self.n - 1)
            self.board[row][col] = QUEEN
            self._put_queen(row, col)

    def solve(self):
        self._solve(limit=500)

    def _solve(self, limit):
        current_score = self.get_number_of_attacking_queens()
        for i in range(limit):
            neighbors = self.get_neighbors()
            print(len(neighbors))
            best_neighbor: Neighbor = min(neighbors, key=lambda n: n.heuristic_score)
            print(f"Best score is {best_neighbor.heuristic_score}. Move {best_neighbor.queen}: {best_neighbor.next_col}")
            if best_neighbor.heuristic_score < current_score:
                print(f"Updating score from {current_score} to {best_neighbor.heuristic_score}")
                current_score = best_neighbor.heuristic_score

                # tracking queen conflicts
                self._remove_queen(best_neighbor.queen)
                self._put_queen(best_neighbor.queen, best_neighbor.next_col)

                # board update
                self.board[best_neighbor.queen][best_neighbor.orig_col] = EMPTY
                self.board[best_neighbor.queen][best_neighbor.next_col] = QUEEN

                # steps record
                self.steps.append((best_neighbor.queen, best_neighbor.orig_col))
                self.steps.append((best_neighbor.queen, best_neighbor.next_col))

            if current_score == best_neighbor.heuristic_score:
                print('Score can not be updated')
                return

    def _put_queen(self, queen: int, col: int) -> bool:
        # puts queen on given column, updates counts for heuristic calculation
        self.queens[queen] = col

        self.columns[col] += 1
        self.diag[queen - col + self.n - 1] += 1
        self.anti_diag[queen + col] += 1
        # TODO: should be counted here... attacking
        return True

    def _remove_queen(self, queen: int) -> bool:
        col = self.queens[queen]
        if col == -1:
            return False

        self.queens[queen] = -1

        self.columns[col] -= 1
        self.diag[queen - col + self.n - 1] -= 1
        self.anti_diag[queen + col] -= 1

        return True

    def get_neighbors(self) -> List[Neighbor]:
        # для кожного могжливого руху королеви в рядку, порахуй еврестичний скор
        # та додай до листа
        neighbors: List[Neighbor] = []
        for queen, orig_col in enumerate(self.queens):
            for next_col in range(self.n):
                if orig_col == next_col:
                    continue

                self._remove_queen(queen)
                self._put_queen(queen, next_col)
                heuristic_score = self.get_number_of_attacking_queens() # TODO: reverse, to penalize

                neighbor = Neighbor(
                    queen=queen,
                    orig_col=orig_col,
                    next_col=next_col,
                    heuristic_score=heuristic_score
                )
                neighbors.append(neighbor)

            # put the queen back
            self._remove_queen(queen)
            self._put_queen(queen, orig_col)

        return neighbors

    def get_number_of_attacking_queens(self) -> int:
        # n * (n - 1) / 2 (for queens in col, diag and antidiag)
        col_attacking_queens = 0
        for queens in self.columns:
            col_attacking_queens += queens * (queens - 1) // 2

        diagonal_attacking_queens = 0
        for queens in self.diag:
            diagonal_attacking_queens += queens * (queens - 1) // 2

        anti_diagonal_attacking_queens = 0
        for queens in self.anti_diag:
            anti_diagonal_attacking_queens += queens * (queens - 1) // 2

        return col_attacking_queens + diagonal_attacking_queens + anti_diagonal_attacking_queens
