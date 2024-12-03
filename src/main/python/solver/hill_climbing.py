import logging
import random
from typing import List

from solver.constants import QUEEN, EMPTY
from solver.solver import Solver

"""
Reprezentuje možný krok algoritmu, stav, do ktorého sa môže presunúť pole
"""
class Neighbor:
    def __init__(self, queen: int, orig_col: int, next_col: int, heuristic_score: int = int(-1e32)):
        self.queen: int = queen  # reprezentuje kráľovnú (jej riadkovú pozíciu na poli)
        self.orig_col: int = orig_col  # pozícia, z ktorej sa má kráľovná presunúť
        self.next_col: int = next_col  # pozícia, na ktorú sa má kráľovná presunúť
        self.heuristic_score: int = heuristic_score  # heuristické skóre, ako dobrý je daný ťah


class HillClimbing(Solver):

    def __init__(self, n):
        super().__init__(n)
        self.queens = [-1] * self.n  # sleduje, ktorá kráľovná a kde (queens[row] = col)
        self.columns = [0] * self.n  # sleduje počet kráľovien v každom stĺpci
        self.diag = [0] * (2 * self.n - 1)  # sleduje počet kráľovien na každej hlavnej diagonále
        self.anti_diag = [0] * (2 * self.n - 1)  # sleduje počet kráľovien na každej vedľajšej diagonále
        self.updates_count = 0  # sleduje počet navštívených stavov
        self.solution_score = -1  # sleduje heuristické skóre tohto stavu
        self.limit = int(1e12)  # limit na zastavenie algoritmu
        self.side_moves = 100  # keď sa dosiahne lokálne minimum, predstavuje max počet krokov medzi stavmi s rovnakým skóre
        self.post_init()  # náhodne inicializuje pole

    def post_init(self):
        """
        Náhodne zaplní pole kráľovnami
        :return: None
        """
        for row in range(self.n):
            col = random.randint(0, self.n - 1)
            self.board[row][col] = QUEEN
            self._put_queen(row, col)
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

        self.solution_score = self.get_number_of_attacking_queens()  # ulož heuristické skóre pre aktuálne pole
        for i in range(limit):
            if self.solution_score == 0:
                logging.debug("Solution was found!")
                return

            neighbors = self.get_neighbors()  # vypočíta všetky možné susedné stavy (ťahy) z aktuálneho stavu

            logging.debug(f"Iteration {i}: Evaluating neighbors...")

            best_neighbor: Neighbor = min(neighbors,
                key=lambda n: n.heuristic_score)  # zvol najlepsieho
            logging.debug([neighbor.heuristic_score for neighbor in neighbors])
            logging.debug(f"Best score is {best_neighbor.heuristic_score}."
                          f" Move Queen {best_neighbor.queen} to Column {best_neighbor.next_col}")

            # self.print_board()
            # self.print_neighbors(neighbors)
            if best_neighbor.heuristic_score < self.solution_score:
                # ak je heuristické skóre lepšie ako naše aktuálne, zmeň stav na tento
                side_moves_copy = side_moves
                self.solution_score = self.update_state(self.solution_score, best_neighbor)
            elif best_neighbor.heuristic_score == self.solution_score and side_moves_copy > 0:
                # dosiahlo sa lokálne minimum, pokus o výstup s neho, náhodným výberom stavu
                # s rovnakým heuristickým skóre ako náš
                logging.debug("Making side move!")
                side_moves_copy -= 1
                best_neighbors = filter(
                    lambda x: x.heuristic_score == best_neighbor.heuristic_score, neighbors
                )
                random_neighbor = random.choice(list(best_neighbors))

                self.solution_score = self.update_state(self.solution_score, random_neighbor)
            else:
                logging.debug("No improvement possible.")
                return

    def update_state(self, current_score, best_neighbor):
        """
        Zmena stavu a zaznamenanie pozícií kráľovien, krokov algoritmu a počítadla
        :param current_score:
        :param best_neighbor:
        :return:
        """
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
        """
        Aktualizuje počet kráľovien na jej diagonálach a stĺpcoch
        """
        self.queens[queen] = col
        self.columns[col] += 1
        self.diag[queen - col + self.n - 1] += 1
        self.anti_diag[queen + col] += 1
        return True

    def _remove_queen(self, queen: int) -> bool:
        """
        Aktualizuje počet kráľovien na jej diagonálach a stĺpcoch
        """
        col = self.queens[queen]
        if col == -1:
            return False

        self.queens[queen] = -1
        self.columns[col] -= 1
        self.diag[queen - col + self.n - 1] -= 1
        self.anti_diag[queen + col] -= 1
        return True

    def get_neighbors(self) -> List[Neighbor]:
        neighbors: List[Neighbor] = []  # sleduje všetky nasledujúce možné stavy z aktuálneho stavu
        for queen, orig_col in enumerate(self.queens):  # queen = row
            for next_col in range(self.n):
                if orig_col == next_col:
                    continue

                # vykoná sa na sledovanie počtu kráľovien na každom stĺpci/diagonále po pohybe (queen, next_col)
                self._remove_queen(queen)  # odstráň kráľovnú z jej pôvodnej pozície
                self._put_queen(queen, next_col)  # pridaj kráľovnú na novú pozíciu
                heuristic_score = self.get_number_of_attacking_queens()

                neighbors.append(Neighbor(
                    queen=queen,
                    orig_col=orig_col,
                    next_col=next_col,
                    heuristic_score=heuristic_score
                ))

                # Po výpočte heuristického skóre obnov pôvodnú pozíciu
                self._remove_queen(queen)
                self._put_queen(queen, orig_col)

        return neighbors

    def get_number_of_attacking_queens(self) -> int:
        """
        Pre jednoduchší výpočet počtu konfliktov na poli
        sleduje sa počet kráľoven na každej diagonále a stĺpci
        Potom možno vypočítať počet útočiacich párov pre každý stĺpec/diagonálu
        vzrocom pre kombináciou: n * (n - 1) -- pre počet kombinácií (výber 2 z n)
        Vysledkom je počet parov, ale počíta sa (q1, q2) a (q2, q1), takže deleno 2
        """

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
