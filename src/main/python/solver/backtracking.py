import logging
from typing import List

from .solver import Solver


class Backtracking(Solver):
    """
    Rozširuje základný algoritmus 'backtracking' o mrv a lcv metody
    """

    def __init__(self, n):
        super().__init__(n)
        self.queens: List[
                         int] | None = None  # pole predstavuje stav problému (rozloženie kráľovných) queens[row] = col
        self.nodes_expanded = 0  # počet prejdených stavov (uzlov)

    def solve(self):
        queens = [-1] * self.n  # inicializuje problém
        self._solve(queens)
        self.queens = queens

    def get_queens(self) -> List[int]:
        if self.queens is None:
            raise ValueError("solve() method was not called")

        return self.queens

    def get_nodes_expanded(self) -> int:
        return self.nodes_expanded

    def reset(self):
        super().reset()
        self.nodes_expanded = 0
        self.queens = None

    def _solve(self, queens: List[int]) -> bool:
        if all(queen != -1 for queen in queens):
            # ak sú všetke kráľovne umiestnené, tak najdené riešenie
            return True

        queen = self.select_queen_mrv(queens)
        if queen == -1:
            # ak nie je možné umiestniť žiadnu kráľovnú (všetky pozície sú napadnuté inými),
            # potom návrat
            print("all domains empty")
            return False

        logging.info(f"Queen selected {queen}")
        ordered_domain = self.order_domain_with_lcv(queens, queen)

        for col in ordered_domain:
            logging.info(f"Col selected with LCV: {col}")
            if not self.is_safe(queens, queen, col):
                # ak sa kráľovná nedá bezpečne umiestniť
                continue

            # záznam kráľovnej a krokov
            self.nodes_expanded += 1
            self.steps.append((queen, col))
            queens[queen] = col

            if self._solve(queens):
                return True

            self.steps.append((queen, col))
            queens[queen] = -1

        return False

    def select_queen_mrv(self, queens) -> int:
        """
        Z množiny kráľovien (premenných problému) vyberte kráľovnú,
        ktorá má najmenší počet možných umiestnení v danom riadku (najmenšia oblasť)

        :param queens: kráľovny vo formate queens[row] = col
        :return vráti číslo dámy s najmenšou neprázdnou množinou ťahov
        """
        domain_lengths = {}
        for queen in range(self.n):
            if queens[queen] != -1:
                # preskočte tie, ktoré sú už nainštalované
                continue

            domain_lengths[queen] = self.count_safe(queens, queen)

        sorted_domain = sorted(domain_lengths.items(), key=lambda item: item[1])

        for queen, d_len in sorted_domain:
            if d_len > 0:
                return queen

        return -1

    def count_safe(self, queens, queen) -> int:
        """
        Vypočíta počet bezpečných pozícií v danom riadku (row = queen)
        """
        count = 0
        for col in range(self.n):
            if self.is_safe(queens, queen, col):
                count += 1

        return count

    def is_safe(self, queens, queen, col) -> bool:
        """
        Kontrola, či je dáma v pozícii (queen, col) v konflikte s inou dámou
        Používa sa pritom diagonálne číslovanie (priamych aj vedľajsich)
        """
        if col in queens:
            # v tomto stĺpci je umiestnená kráľovná
            return False

        for other in range(self.n):
            other_col = queens[other]
            if other == queen or other_col == -1:
                continue

            if other + other_col == queen + col:
                # dve dámy sú na rovnakej vedľajšej diagonále
                return False

            other_diag = other - other_col + self.n - 1
            queen_diag = queen - col + self.n - 1
            if other_diag == queen_diag:
                # dve dámy sú na rovnakej diagonále
                return False

        return True

    def order_domain_with_lcv(self, queens, queen):
        heuristic_scores = [-1] * self.n
        for col in range(self.n):
            # heuristic_scores[col] = self.count_locked(queen, col) # 89 steps for 8*8
            heuristic_scores[col] = self.count_remaining(queens, queen, col)  # 56 steps for 8*8

        domain_with_scores = [(col, heuristic_scores[col]) for col in range(self.n)]
        logging.debug(domain_with_scores)

        # heuristika vráti množstvo voľných políčok,
        # pričom najlepší ťah je ten, ktorý ich ponechá najviac,
        # takže triedenie vzhľadom na score * -1
        ordered_domain = [col for col, _ in sorted(domain_with_scores, key=lambda x: -1 * x[1])]

        return ordered_domain

    def count_remaining(self, queens, queen, col) -> int:
        """
        Vypočíta, koľko hodnôt domény zostane pre ostatné premenné,
        keď umiestnime kráľovnú na pozíciu (queen, col)
        """
        remaining_values = 0

        queens[queen] = col

        # skontrolujte, ako toto umiestnenie ovplyvňuje ostatné nepriradené kráľovné.
        for other in range(self.n):
            if other == queen or queens[other] != -1:
                # len nepriradené kráľovné a zaroveň nie vstupná
                continue

            remaining_values += self.count_safe(queens, other)

        queens[queen] = -1
        return remaining_values

    def count_locked(self, queen, col) -> int:
        """
        Vypočita, koľko buniek bude zamknutých umiestnením kráľovnej na poziciu (queen, col)
        *Táto heuristika vykazovala horšie výsledky, preto sa nepoužila
        """

        cells_locked = self.n - 1  # whole column

        diag = queen - col + self.n - 1  # diagonal on which this queen located
        anti_diag = queen + col  # anti diagonal on which this queen located
        if diag <= self.n - 1:
            # interesting that the index of diag corresponds to number of elements in it -1
            cells_locked += diag
        else:
            # and this corresponds for diags which are after main diag
            cells_locked += self.n - abs((self.n - 1) - diag) - 1

        if anti_diag <= self.n - 1:
            # interesting that the index of diag corresponds to number of elements in it -1
            cells_locked += anti_diag
        else:
            # and this corresponds for diags which are after main diag
            cells_locked += self.n - abs((self.n - 1) - anti_diag) - 1

        return cells_locked

    def select_queen_mrv_old(self, queens) -> int:
        # для кожної королеви перевір скільки існує варіантів розстановки
        min_queen = -1
        min_domain_len = float('inf')

        for queen in range(self.n):
            if queens[queen] != -1:
                # select each only once
                continue

            domain_len = self.count_safe(queens, queen)

            if domain_len < min_domain_len:
                min_domain_len = domain_len
                min_queen = queen

        return min_queen
