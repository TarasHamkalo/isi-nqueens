import numpy
import numpy as np


class Solver:

  def __init__(self, n: int):
    self.n = n
    self.board: numpy.array = self.initialize_board()
    self.steps = []

  def solve(self):
    raise NotImplemented("Abstract")

  def get_steps(self):
    return self.steps

  def reset(self):
    self.board = np.zeros((self.n, self.n), dtype=int)
    self.steps = []

  def print_board(self):
    for i in range(self.n):
      for j in range(self.n):
        if self.board[i][j] == 1:
          print("Q", end="")
        else:
          print(".", end="")

      print("")

  def initialize_board(self) -> numpy.array:
    return np.zeros((self.n, self.n), dtype=int)