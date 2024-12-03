import copy
from typing import List

from src.main.python.model.domain import Domain
from src.main.python.solver.constants import QUEEN, EMPTY
from src.main.python.service.domain_manager import DomainManager
from src.main.python.solver.solver import Solver


class ForwardChecking(Solver):
    def __init__(self, n: int):
        super().__init__(n)
        self.domain_manager = DomainManager()
        self.nodes_expanded = 0
        self.queens: List[int] | None = None

    def solve(self) -> None:
        domains = self.domain_manager.create_domains(self.n)
        print(f"Initial domains: {domains}")
        self.__solve(domains)

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

    def __solve(self, domains: list[Domain]) -> bool:
        self.print_board()
        print(f"Current domains: {domains}")

        if (self.existsEmptyDomain(domains)):
            return False

        if self.domain_manager.count_placed(domains) == self.n:
            print("All queens are placed.")
            self.queens = [domain.columns[0] for domain in domains]
            return True

        row = self.select_row_with_mrv(domains)
        if row == -1:
            return False
        print(f"Selected row with MRV: {row}")
        columns = self.select_columns_with_lcv(row, domains)
        print(f"Columns with LCV for row {row}: {columns}")

        for column in columns:
            print(f"Trying to place queen at row {row}, column {column}")
            self.board[row][column] = QUEEN
            self.steps.append([row, column])

            new_domains = copy.deepcopy(domains)
            new_domains = self.domain_manager.set_placed(new_domains, row)
            new_domains = self.domain_manager.all_constraints(new_domains, row, column)

            self.nodes_expanded += 1

            if self.__solve(new_domains):
                return True

            print(f"Backtracking from row {row}, column {column}")
            self.board[row][column] = EMPTY
            self.steps.append([row, column])

        return False

    def select_row_with_mrv(self, domains: list[Domain]) -> int:
        selected_row = min(
            (row for row, domain in enumerate(domains) if domain.columns and not domain.placed),
            key=lambda r: len(domains[r].columns),
            default=-1
        )
        print(f"MRV selected row: {selected_row}")
        return selected_row

    def select_columns_with_lcv(self, row: int, domains: list[Domain]) -> list[int]:
        columns = sorted(
            domains[row].columns,
            key=lambda column: self.domain_manager.count_conflicts(domains, row, column)
        )
        print(f"LCV sorted columns for row {row}: {columns}")
        return columns

    def existsEmptyDomain(self, domains: list[Domain]) -> bool:
        for domain in domains:
            if not domain.columns:
                return True
        return False
