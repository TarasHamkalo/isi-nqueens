from typing import List

from .constants import QUEEN, EMPTY
from .solver import Solver


class DfsBacktracking(Solver):
  def __init__(self, n):
    super().__init__(n)
    self.nodes_expanded = 0
    self.queens = []

  def solve(self):
    # i = randint(0, self.n - 1)
    # j = randint(0, self.n - 1)
    # self.steps.append([i, j])
    # візьми одну позицію
    # додай до стаку усі позиції на рядок вище
    # пройди кожною та якщо можеш поставити - рекурсія
    # інакше назад
    self.dfs(0)

  def reset(self):
    super().reset()
    self.nodes_expanded = 0
    self.queens = []

  def get_queens(self) -> List[int]:
    if len(self.queens) == 0:
      raise ValueError("solve() method was not called")

    queens = [-1] * self.n
    for i, j in self.queens:
      queens[i] = j

    return queens

  def get_nodes_expanded(self):
    return self.nodes_expanded

  # Прикольно вважати що королеви це змінні (числа рядки) а значення це колонки де стоять
  # кожен рівень рекурсії пробує підібрати значення з домени, для королев, в цьому випадку
  # королева преставляє змінну (знаходиться на якомусь рядку) та домена це колонки де може стояти
  def dfs(self, i):
    if i == self.n:
      return True

    for j in range(0, self.n):
      if not self.is_queen_placeable(i, j):
        continue

      self.nodes_expanded += 1

      self.board[i][j] = QUEEN
      self.steps.append([i, j])
      if self.dfs(i + 1):
        self.queens.append((i, j))
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