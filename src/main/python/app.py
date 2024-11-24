from typing import Dict

from solver.dfs import Dfs
from solver.dfs_backtracking import DfsBacktracking
from solver.min_max_conflict import MinMaxConflict
from solver.solver import Solver
from src.main.python.solver.forward_checking import ForwardChecking


class App:
    solvers: Dict[str, Solver] = {
        'dfs': Dfs(8),
        'backtracking': DfsBacktracking(8),
        'forwardchecking': ForwardChecking(8),
        'minmax': MinMaxConflict(8),
    }

    def __init__(self):
        self.solver: Solver = self.solvers['dfs']

    def get_steps(self, solver_name: str):
        if solver_name not in self.solvers:
            raise ValueError(f'Solver "{solver_name}" is not supported')

        self.solver = self.solvers[solver_name]
        self.solver.reset()
        self.solver.solve()
        print(self.solver.get_steps())
        return self.solver.get_steps()
