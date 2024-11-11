class Solver:

  def __init__(self, n: int):
    self.n = n
    self.board = [[0] * n ] * n
    self.steps = [] #

  def solve(self):
    raise NotImplemented("Abstract")

  def get_steps(self):
    return self.steps

  def reset(self):
    self.board = [[0] * self.n ] * self.n

  def print_board(self):
    for i in range(self.n):
      for j in range(self.n):
        if self.board[i][j] == 1:
          print("Q")
        else:
          print(".")

