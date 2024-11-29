import logging
from typing import List

from solver.solver import Solver

class Backtracking(Solver):
    def __init__(self, n):
        super().__init__(n)
        self.nodes_expanded = 0

    def solve(self):
        queens = [-1] * self.n
        self._solve(queens)
        print(queens)
        print(self.nodes_expanded)

    def _solve(self, queens: List[int]):
        if all(queen != -1 for queen in queens):
            return True

        queen = self.select_queen_mrv(queens)
        logging.info(f"Queen selected {queen}")
        ordered_domain = self.order_domain_with_lcv(queens, queen)

        for col in ordered_domain:
            logging.info(f"Col selected with LCV: {col}")
            if not self.is_safe(queens, queen, col):
                continue

            queens[queen] = col
            self.nodes_expanded += 1
            if self._solve(queens):
                return True

            queens[queen] = -1

    def select_queen_mrv(self, queens) -> int:
        # для кожної королеви перевір скільки існує варіантів розстановки
        min_queen = -1
        min_domain_len = float('inf')
        for queen in range(self.n):
            if queens[queen] != -1:
                # select each only once
                continue

            domain_len = self.count_safe(queens, queen)
            if domain_len < min_domain_len:
                min_domain_len = domain_len
                min_queen = queen

        return min_queen

    def count_safe(self, queens, queen) -> bool:
        count = 0
        for col in range(self.n):
            if self.is_safe(queens, queen, col):
               count += 1
        return count

    def is_safe(self, queens, queen, col) -> bool:
        if col in queens:
            # there is queen placed inside this column
            return False

        for other in range(self.n):
            other_col = queens[other]
            if other == queen or other_col == -1:
                continue

            if other + other_col == queen + col:
                # two queens have same anti-diag
                return False

            other_diag = other - other_col + self.n - 1
            queen_diag = queen - col + self.n - 1
            if other_diag == queen_diag:
                # two queens have same diag
               return False

        return True

    def order_domain_with_lcv(self, queens, queen):
        # count how many cells will be locked by placing queen there
        heuristic_scores = [-1] * self.n
        for col in range(self.n):
            heuristic_scores[col] = self.count_locked(queens, queen, col)

        domain_with_scores = [(col, heuristic_scores[col]) for col in range(self.n)]
        ordered_domain = [col for col, _ in sorted(domain_with_scores, key=lambda x: x[1])]
        print(ordered_domain)
        return ordered_domain

    def count_locked(self, queens, queen, col) -> int:
        cells_locked = self.n - 1 # init to whole column (this queen not counted)

        # for diags <= self.n - 1
        diag = queen - col + self.n - 1 # diagonal on which this queen located
        anti_diag = queen + col # anti diagonal on which this queen located
        if diag <= self.n - 1:
            # interesting that the index of diag corresponds to number of elements in it -1
            cells_locked += diag
        else:
            # and this corresponds for diags which are after main diag
            cells_locked += self.n - abs((self.n - 1) - diag) - 1

        if anti_diag <= self.n - 1:
            # interesting that the index of diag corresponds to number of elements in it -1
            cells_locked += anti_diag
        else:
            # and this corresponds for diags which are after main diag
            cells_locked += self.n - abs((self.n - 1) - anti_diag) - 1

        return cells_locked