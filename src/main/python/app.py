from typing import Dict

from flask import Flask

from solver.dfs_backtracking import DfsBacktracking
from solver.solver import Solver


class App:

  solvers: Dict[str, Solver] = {
    'dfs': DfsBacktracking(8),
  }

  def __init__(self):
    self.solver: Solver = self.solvers['dfs']

  def get_steps(self, solver_name: str):
    if solver_name not in self.solvers:
      raise ValueError(f'Solver "{solver_name}" is not supported')

    self.solver = self.solvers[solver_name]
    self.solver.reset()
    self.solver.solve()
    return self.solver.get_steps()