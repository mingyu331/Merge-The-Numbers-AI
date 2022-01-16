import random

class Main:
    def __init__(self):
        super().__init__()
        # game stuff
        self.grid = [[-1 for col in range(5)] for row in range(6)]
        self.score = 0
        self.greatestBlockHeight = 10
        self.lowestBlockHeight = 0
        self.alive = True

    def fall(self, idx):
        for i in range(5, 0, -1):
            if self.grid[i][idx] == -1:
                self.grid[i][idx] = self.grid[i - 1][idx]
                self.grid[i - 1][idx] = -1

    def merge(self, x, y) -> bool:
        if self.grid[y][x] == -1:
            return False
        samecnt = 0
        if y != 0 and self.grid[y - 1][x] == self.grid[y][x] and self.grid[y - 1][x] != -1:
            samecnt += 1
            self.grid[y - 1][x] = -1
        if y != 5 and self.grid[y + 1][x] == self.grid[y][x] and self.grid[y + 1][x] != -1:
            samecnt += 1
            self.grid[y + 1][x] = -1
        if x != 0 and self.grid[y][x - 1] == self.grid[y][x] and self.grid[y][x - 1] != -1:
            samecnt += 1
            self.grid[y][x - 1] = -1
        if x != 4 and self.grid[y][x + 1] == self.grid[y][x] and self.grid[y][x + 1] != -1:
            samecnt += 1
            self.grid[y][x + 1] = -1

        if samecnt == 0:
            return False
        if samecnt == 1:
            self.grid[y][x] += 1
        elif samecnt == 2:
            self.grid[y][x] += 2
        else:
            self.grid[y][x] += 3
        self.greatestBlockHeight = max(self.grid[y][x], self.greatestBlockHeight)
        self.lowestBlockHeight = min(self.grid[y][x], self.lowestBlockHeight)
        self.score += 2 ** self.grid[y][x]
        self.fall(x)
        if x != 0:
            self.fall(x - 1)
        if x != 4:
            self.fall(x + 1)

        for i in range(5, 0, -1):
            self.merge(x, i)
        if x != 0:
            for i in range(5, 0, -1):
                self.merge(x - 1, i)
        if x != 4:
            for i in range(5, 0, -1):
                self.merge(x + 1, i)
        return False

    def appendblock(self, idx, value=-1):
        if not self.alive:
            return
        i = 0
        while i <= 5 and self.grid[i][idx] == -1:
            i += 1
        i -= 1
        
        self.grid[i][idx] = value

        # game over
        if i == 0 and self.grid[0][idx] != self.grid[1][idx]:
            self.alive = False
            return
        self.merge(idx, i)