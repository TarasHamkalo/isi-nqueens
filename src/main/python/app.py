from typing import Dict

from solver.dfs_backtracking import DfsBacktracking
from solver.solver import Solver


class App:

  solvers: Dict[str, Solver] = {
    'dfs-backtracking': DfsBacktracking(4),
  }

  def __init__(self):
    self.solver: Solver = self.solvers['dfs-backtracking']

  def solve(self):
    self.steps = self.solver.solve()

  def get_board(self):
    return self.solver.get_board()

  def set_solver(self, solver_name):
    self.solver = self.solvers[solver_name]

  def reset(self):
    self.solver.reset()