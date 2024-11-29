import time
from typing import Dict

from solver.backtracking import Backtracking
from solver.dfs import Dfs
from solver.hill_climbing import HillClimbing
from solver.min_max_conflict import MinMaxConflict
from solver.solver import Solver
from src.main.python.solver.forward_checking import ForwardChecking


class App:

    solvers: Dict[str, Solver] = {
        'dfs': Dfs(8),
        'forwardchecking': ForwardChecking(8),
        'minmax': MinMaxConflict(8),
        'hillclimbing': HillClimbing(8),
        'backtracking': Backtracking(8),
    }

    def __init__(self):
        self.solver: Solver = self.solvers['dfs']
        self.solve_duration: float = 0.0  # Store duration of solving

    def get_steps(self, solver_name: str):
        if solver_name not in self.solvers:
            raise ValueError(f'Solver "{solver_name}" is not supported')

        self.solver = self.solvers[solver_name]
        self.solver.reset()

        start_time = time.time()
        self.solver.solve()
        end_time = time.time()
        self.solve_duration = end_time - start_time

        print(f"{self.solver}: {self.solver.get_steps()}")
        return self.solver.get_steps()

    def get_solve_duration(self):
        return self.solve_duration

    def get_nodes_expanded(self):
        return self.solver.get_nodes_expanded()

    def get_queens(self):
        return self.solver.get_queens()

    def set_limit(self, limit):
        self.solvers['minmax'].limit = limit
        self.solvers['hillclimbing'].limit = limit

    def set_side_moves(self, side_moves):
        self.solvers['hillclimbing'].side_moves = side_moves
