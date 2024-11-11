from typing import Dict

from flask import Flask

from solver.dfs_backtracking import DfsBacktracking
from solver.solver import Solver

flask = Flask(__name__)

class App:

  solvers: Dict[str, Solver] = {
    'dfs-backtracking': DfsBacktracking(4),
  }

  def __init__(self):
    self.solver: Solver = self.solvers['dfs-backtracking']

  def set_solver(self, solver_name):
    self.solver = self.solvers[solver_name]

  def solve(self):
    self.solver.solve()

  def get_steps(self):
    return self.get_steps()

  def reset(self):
    self.solver.reset()