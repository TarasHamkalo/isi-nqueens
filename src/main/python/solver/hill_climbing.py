import logging
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
        self.updates_count = 0
        self.solution_score = -1
        self.limit = int(1e12)
        self.side_moves = 100
        self.post_init()

    def post_init(self):
        for row in range(self.n):
            col = random.randint(0, self.n - 1)
            self.board[row][col] = QUEEN
            self._put_queen(row, col)
            # append steps to track start position
            self.steps.append((row, col))

    def solve(self):
        self._solve(self.limit, self.side_moves)

    def get_queens(self) -> List[int]:
        return self.queens

    def get_nodes_expanded(self) -> int:
        return self.updates_count

    def reset(self):
        super().reset()
        self.queens = [-1] * self.n
        self.columns = [0] * self.n
        self.diag = [0] * (2 * self.n - 1)
        self.anti_diag = [0] * (2 * self.n - 1)
        self.updates_count = 0
        self.solution_score = -1
        self.post_init()

    def _solve(self, limit: int, side_moves: int):
        side_moves_copy = side_moves

        self.solution_score = self.get_number_of_attacking_queens()
        for i in range(limit):
            if self.solution_score == 0:
                logging.debug("Solution was found!")
                return

            neighbors = self.get_neighbors()

            logging.debug(f"Iteration {i}: Evaluating neighbors...")

            best_neighbor: Neighbor = min(neighbors, key=lambda n: n.heuristic_score)
            logging.debug([neighbor.heuristic_score for neighbor in neighbors])
            logging.debug(f"Best score is {best_neighbor.heuristic_score}."
                  f" Move Queen {best_neighbor.queen} to Column {best_neighbor.next_col}")

            # self.print_board()
            # self.print_neighbors(neighbors)

            if best_neighbor.heuristic_score < self.solution_score:
                side_moves_copy = side_moves
                self.solution_score = self.update_state(self.solution_score, best_neighbor)
            elif best_neighbor.heuristic_score == self.solution_score and side_moves_copy > 0:
                logging.debug("Making side move!")
                side_moves_copy -= 1
                self.solution_score = self.update_state(self.solution_score, best_neighbor)
            else:
                logging.debug("No improvement possible.")

                return

    def update_state(self, current_score, best_neighbor):
        logging.debug(f"Updating score from {current_score} to {best_neighbor.heuristic_score}")
        self.updates_count += 1
        # Update the queen's position
        self._remove_queen(best_neighbor.queen)
        self._put_queen(best_neighbor.queen, best_neighbor.next_col)

        # Update the board
        self.board[best_neighbor.queen][best_neighbor.orig_col] = EMPTY
        self.board[best_neighbor.queen][best_neighbor.next_col] = QUEEN

        # Record steps
        self.steps.append((best_neighbor.queen, best_neighbor.orig_col))
        self.steps.append((best_neighbor.queen, best_neighbor.next_col))

        return best_neighbor.heuristic_score

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

                # print(f"Move queen {queen} from {orig_col} to {next_col}")
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
        logging.debug(f"Columns: {self.columns}, attacks {col_attacking_queens}")
        logging.debug(f"Diagonals: {self.diag}, attacks {diag_attacking_queens}")
        logging.debug(f"Anti-diagonals:: {self.anti_diag}, attacks {anti_diag_attacking_queens}")

        return col_attacking_queens + diag_attacking_queens + anti_diag_attacking_queens

    def print_neighbors(self, neighbors):
        for i, neighbor in enumerate(neighbors):
            print(neighbor.heuristic_score, end=" ")
            if (i + 1) % (self.n - 1) == 0:
                print()
        print()

