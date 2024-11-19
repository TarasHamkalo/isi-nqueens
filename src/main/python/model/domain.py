class Domain:
    def __init__(self, n: int):
        self.columns: list[int] = list(range(n))
        self.placed: bool = False