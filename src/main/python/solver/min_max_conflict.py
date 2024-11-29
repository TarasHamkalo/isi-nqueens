from typing import List

import numpy as np
import random

from src.main.python.solver.constants import QUEEN, EMPTY
from src.main.python.service.domain_manager import DomainManager
from src.main.python.solver.solver import Solver
from src.main.python.model.domain import Domain


class MinMaxConflict(Solver):

    def __init__(self, n: int):
        super().__init__(n)
        self.domain_manager = DomainManager()
        self.nodes_expanded = 0
        self.queens: List[int] | None = None
        self.limit = 50000
        self.post_init()

    def solve(self) -> None:
        domains = self.domain_manager.create_domains(self.n)
        self.domain_manager.assign_columns(domains, self.board)
        self.__solve(domains)

    def post_init(self):
        for row in range(self.n):
            column = random.randint(0, self.n - 1)
            self.board[row, column] = QUEEN
            self.steps.append([row, column]) # steps which init the board

    def get_queens(self) -> List[int]:
        if self.queens is None:
            raise ValueError("solve() method was not called")

        return self.queens

    def get_nodes_expanded(self) -> int:
        return self.nodes_expanded

    def reset(self):
        super().reset()
        self.nodes_expanded = 0
        self.queens = None
        self.post_init()

    def __solve(self, domains: list[Domain]) -> bool:
        for i in range(self.limit):
            self.print_board()
            row = self.select_row_with_conflict(domains)
            print(row)
            if row == -1:
                self.queens = [domain.columns[0] for domain in domains]
                return True

            for current_column in domains[row].columns:
                self.board[row][current_column] = EMPTY
                self.steps.append([int(row), int(current_column)])

            column = self.select_column_with_min_conflicts(domains, row)
            domains[row].columns = [column]

            self.nodes_expanded += 1
            self.board[row][column] = QUEEN
            self.steps.append([row, column])

        return False

    def select_row_with_conflict(self, domains: list[Domain]) -> int:
        rows_with_conflicts = []
        for row, domain in enumerate(domains):
            for column in domain.columns:
                if self.have_conflict(domains, row, column):
                    rows_with_conflicts.append(row)

        return random.choice(rows_with_conflicts) if rows_with_conflicts else -1

    def select_column_with_min_conflicts(self, domains: list[Domain], row: int) -> int:
        return min(
            list(range(self.n)),
            key=lambda column: self.domain_manager.count_conflicts(domains, row, column)
        )

    def have_conflict(self, domains: list[Domain], row: int, column: int) -> bool:
        for other_row, other_domain in enumerate(domains):
            if other_row != row:
                if column in other_domain.columns:
                    return True
                if column + (other_row - row) in other_domain.columns:
                    return True
                if column - (other_row - row) in other_domain.columns:
                    return True
        return False