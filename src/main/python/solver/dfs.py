from solver.constants import QUEEN, EMPTY
from solver.solver import Solver


class Dfs(Solver):

    def __init__(self, n: int):
        super().__init__(n)
        self.queens = []

    def solve(self):
        # візьми як перший стан, перший рядок
        # додай усі клітинки наступного рядку
        # вибери одну і йди далі

        # if frontier is empty -> false
        # вибери позицію, постав королеву
        # if row == 8 and valid -> true
        # додай усіх сусідів та рекурсія
        self._solve(0)

    def _solve(self, i) -> bool:
        if i == self.n:
            # frontier can not be expanded, no other child nodes
            return False

        for j in range(0, self.n):
            self.board[i][j] = QUEEN
            self.queens.append((i, j))
            self.steps.append((i, j))

            if self.is_goal_state():
                return True

            # expand frontier with adjacent cells
            if self._solve(i + 1):
                return True

            self.board[i][j] = EMPTY
            self.steps.append((i, j))
            self.queens.pop()

        return False

    def is_goal_state(self):
        return len(self.queens) == self.n and self.no_queens_attack()

    def no_queens_attack(self):
        for i, j in self.queens:
            if not self.is_safe(i, j):
                # this queen attack some other
                return False

        return True

    def is_safe(self, i, j):
        if self.board[i, :].sum() - QUEEN > 0:
            return False

        if self.board[:, j].sum() - QUEEN > 0:
            return False

        for di, dj in self.get_diagonal_indexes(i, j):
            if di == i and dj == j:
                continue

            if self.board[di][dj] == QUEEN:
                return False

        return True
