import random
from typing import List

from solver.constants import QUEEN, EMPTY
from solver.solver import Solver


# track number of queens on each diagonal/anti-diagonal and column
# count attacking pairs for each possible state
class Neighbor:
    def __init__(self, queen: int, orig_col: int, next_col: int, heuristic_score: int = int(-1e32)):
        self.queen: int = queen
        self.orig_col: int = orig_col
        self.next_col: int = next_col
        self.heuristic_score: int = heuristic_score

class HillClimbing(Solver):
    def __init__(self, n):
        super().__init__(n)
        self.queens = [-1] * self.n  # track which queen and where (row: col)
        self.columns = [0] * self.n  # track number of queens in each column
        self.diag = [0] * (2 * self.n - 1)  # track number of queens in each main diagonals
        self.anti_diag = [0] * (2 * self.n - 1)  # track number of queens in each reverse diagonal
        self.post_init()

    def post_init(self):
        for row in range(self.n):
            col = random.randint(0, self.n - 1)
            self.board[row][col] = QUEEN
            self._put_queen(row, col)

    def solve(self):
        self._solve(limit=500)

    def _solve(self, limit):
        current_score = self.get_number_of_attacking_queens()
        for i in range(limit):
            neighbors = self.get_neighbors()

            print(f"Iteration {i}: Evaluating neighbors...")
            best_neighbor: Neighbor = min(neighbors, key=lambda n: n.heuristic_score)
            print(f"Best score is {best_neighbor.heuristic_score}. Move Queen {best_neighbor.queen} to Column {best_neighbor.next_col}")

            if best_neighbor.heuristic_score < current_score:
                print(f"Updating score from {current_score} to {best_neighbor.heuristic_score}")
                current_score = best_neighbor.heuristic_score

                # Update the queen's position
                self._remove_queen(best_neighbor.queen)
                self._put_queen(best_neighbor.queen, best_neighbor.next_col)

                # Update the board
                self.board[best_neighbor.queen][best_neighbor.orig_col] = EMPTY
                self.board[best_neighbor.queen][best_neighbor.next_col] = QUEEN

                # Record steps
                self.steps.append((best_neighbor.queen, best_neighbor.orig_col))
                self.steps.append((best_neighbor.queen, best_neighbor.next_col))
            else:
                print("No improvement possible. Stopping.")
                return

    def _put_queen(self, queen: int, col: int) -> bool:
        self.queens[queen] = col
        self.columns[col] += 1
        self.diag[queen - col + self.n - 1] += 1
        self.anti_diag[queen + col] += 1
        return True

    def _remove_queen(self, queen: int) -> bool:
        col = self.queens[queen]
        if col == -1:
            return False

        self.queens[queen] = -1
        self.columns[col] -= 1
        self.diag[queen - col + self.n - 1] -= 1
        self.anti_diag[queen + col] -= 1
        return True

    def get_neighbors(self) -> List[Neighbor]:
        neighbors: List[Neighbor] = []
        for queen, orig_col in enumerate(self.queens):
            for next_col in range(self.n):
                if orig_col == next_col:
                    continue

                self._remove_queen(queen)
                self._put_queen(queen, next_col)
                heuristic_score = self.get_number_of_attacking_queens()

                neighbors.append(Neighbor(
                    queen=queen,
                    orig_col=orig_col,
                    next_col=next_col,
                    heuristic_score=heuristic_score
                ))

                # Restore the original position
                self._remove_queen(queen)
                self._put_queen(queen, orig_col)

        return neighbors

    def get_number_of_attacking_queens(self) -> int:
        # taking 2 from n = n * (n - 1) / 2 (for queens in col, diag and antidiag)
        col_attacking_queens = sum(q * (q - 1) // 2 for q in self.columns)
        diag_attacking_queens = sum(q * (q - 1) // 2 for q in self.diag)
        anti_diag_attacking_queens = sum(q * (q - 1) // 2 for q in self.anti_diag)
        return col_attacking_queens + diag_attacking_queens + anti_diag_attacking_queens
