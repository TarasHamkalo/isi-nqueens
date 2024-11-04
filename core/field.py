import numpy as np

class Field:
    def __init__(self):
        self.board = np.zeros((8, 8))

    def get_board(self):
        return self.board

    def is_solved(self) -> bool:
        pass

    def print(self):
        for row in self.board:
            print(" ".join("Q" if col else "." for col in row))
        print("\n")