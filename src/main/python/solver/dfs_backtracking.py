from typing import List

from .constants import QUEEN, EMPTY
from .solver import Solver


class DfsBacktracking(Solver):

  def solve(self):
    # i = randint(0, self.n - 1)
    # j = randint(0, self.n - 1)
    # self.steps.append([i, j])
    # візьми одну позицію
    # додай до стаку усі позиції на рядок вище
    # пройди кожною та якщо можеш поставити - рекурсія
    # інакше назад
    self.dfs(0)

  def dfs(self, i):
    if i == self.n:
      return True

    for j in range(0, self.n):
      if not self.is_queen_placeable(i, j):
        continue

      self.board[i][j] = QUEEN
      self.steps.append([i, j])
      if self.dfs(i + 1):
        return True

      self.steps.append([i, j])
      self.board[i][j] = 0

    return False

  def is_queen_placeable(self, i, j):
    if self.board[i, :].sum() > 0:
      return False

    if self.board[:, j].sum() > 0:
      return False

    for di, dj in self.get_diagonal_indexes(i, j):
      if self.board[di][dj] == QUEEN:
        return False

    return True