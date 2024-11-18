from typing import Dict

from flask import Flask

from solver.dfs_backtracking import DfsBacktracking
from solver.solver import Solver


class App:

  solvers: Dict[str, Solver] = {
    'dfs': DfsBacktracking(4),
  }

  def __init__(self):
    self.solver: Solver = self.solvers['dfs']

  def get_steps(self, solver_name: str):
    self.solver.reset()
    self.solver.solve()
    return self.solver.get_steps()