import random
from typing import List

import numpy

from src.main.python.model.domain import Domain
from src.main.python.solver.constants import QUEEN


class DomainManager:
    def create_domains(self, n: int) -> List[Domain]:
        domains: List[Domain] = []
        for i in range(n):
            domains.append(Domain(n))
        return domains

    def assign_columns(self, domains: List[Domain], values: numpy.array) -> List[Domain]:
        for row, domain in enumerate(domains):
            column = numpy.where(values[row] == QUEEN)[0][0]
            domain.columns = [column]
            domain.placed = True
        return domains

    def count_placed(self, domains: List[Domain]) -> int:
        return sum(1 for row in domains if row.placed)

    def set_placed(self, domains: List[Domain], row: int) -> List[Domain]:
        domains[row].placed = True
        return domains

    def horizontal_constraint(self, domains: List[Domain], row: int, column: int) -> List[Domain]:
        domains[row].columns = [column]
        return domains

    def vertical_constraint(self, domains: List[Domain], row: int, column: int) -> List[Domain]:
        for r in range(len(domains)):
            if r != row:
                if column in domains[r].columns:
                    domains[r].columns.remove(column)
        return domains

    def right_diagonal_constraint(self, domains: List[Domain], row: int, column: int) -> List[Domain]:
        for r in range(len(domains)):
            if r != row:
                diagonal_column = column + (r - row)
                if diagonal_column in domains[r].columns:
                    domains[r].columns.remove(diagonal_column)
        return domains

    def left_diagonal_constraint(self, domains: List[Domain], row: int, column: int) -> List[Domain]:
        for r in range(len(domains)):
            if r != row:
                diagonal_column = column - (r - row)
                if diagonal_column in domains[r].columns:
                    domains[r].columns.remove(diagonal_column)
        return domains

    def all_constraints(self, domains: List[Domain], row: int, column: int) -> List[Domain]:
        self.horizontal_constraint(domains, row, column)
        self.vertical_constraint(domains, row, column)
        self.right_diagonal_constraint(domains, row, column)
        self.left_diagonal_constraint(domains, row, column)
        return domains

    def count_conflicts(self, domains: List[Domain], row: int, column: int) -> int:
        conflict_count = 0
        for other_row, domain in enumerate(domains):
            if other_row != row:
                if column in domain.columns:
                    conflict_count += 1
                if column + (other_row - row) in domain.columns:
                    conflict_count += 1
                if column - (other_row - row) in domain.columns:
                    conflict_count += 1
        return conflict_count