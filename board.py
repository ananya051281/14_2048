import random

SIZE = 4


class Board:
    def __init__(self):
        self.grid = [[0] * SIZE for _ in range(SIZE)]
        self.score = 0
        self.add_random_tile()
        self.add_random_tile()

    def add_random_tile(self):
        empty = [(r, c) for r in range(SIZE) for c in range(SIZE) if self.grid[r][c] == 0]
        if empty:
            r, c = random.choice(empty)
            self.grid[r][c] = 4 if random.random() < 0.1 else 2

    @staticmethod
    def slide_line(line):
        values = [x for x in line if x]
        result = []
        merged = False
        i = 0

        while i < len(values):
            if i + 1 < len(values) and values[i] == values[i + 1]:
                result.append(values[i] * 2)
                merged = True
                i += 2
            else:
                result.append(values[i])
                i += 1

        return result + [0] * (SIZE - len(result)), merged

    def move_left(self):
        changed = False
        merged = False

        for r in range(SIZE):
            old = self.grid[r][:]
            self.grid[r], line_merged = self.slide_line(old)
            changed |= old != self.grid[r]
            merged |= line_merged

        return changed, merged

    def move_right(self):
        changed = False
        merged = False

        for r in range(SIZE):
            old = self.grid[r][:]
            new, line_merged = self.slide_line(list(reversed(old)))
            self.grid[r] = list(reversed(new))
            changed |= old != self.grid[r]
            merged |= line_merged

        return changed, merged

    def move_up(self):
        changed = False
        merged = False

        for c in range(SIZE):
            old = [self.grid[r][c] for r in range(SIZE)]
            new, column_merged = self.slide_line(old)

            for r in range(SIZE):
                self.grid[r][c] = new[r]

            changed |= old != new
            merged |= column_merged

        return changed, merged

    def move_down(self):
        changed = False
        merged = False

        for c in range(SIZE):
            old = [self.grid[r][c] for r in range(SIZE)]
            new, column_merged = self.slide_line(list(reversed(old)))
            new = list(reversed(new))

            for r in range(SIZE):
                self.grid[r][c] = new[r]

            changed |= old != new
            merged |= column_merged

        return changed, merged

    def has_won(self):
        return any(2048 in row for row in self.grid)

    def can_move(self):
        if any(0 in row for row in self.grid):
            return True
        for r in range(SIZE):
            for c in range(SIZE):
                if c + 1 < SIZE and self.grid[r][c] == self.grid[r][c + 1]:
                    return True
                if r + 1 < SIZE and self.grid[r][c] == self.grid[r + 1][c]:
                    return True
        return False
