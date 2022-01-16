import random
import neat
import pickle
import visualize
import multiprocessing


class Main:
    def __init__(self, moves=None):
        super().__init__()
        # const
        self.blockSize = 100
        self.fontSize = 50
        # game stuff
        self.grid = [[-1 for col in range(5)] for row in range(6)]
        self.score = 0
        self.greatestBlockHeight = 10
        self.lowestBlockHeight = 0
        self.nextBlock = 0
        self.nextNextBlock = 0
        self.alive = True

        if moves == None:
            self.setMoves = False
        else:
            self.setMoves = True
            self.moves = moves
        self.blockAmount = 0

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

    def appendblock(self, idx):
        if not self.alive:
            return
        i = 0
        while i <= 5 and self.grid[i][idx] == -1:
            # print(i)
            i += 1
        i -= 1
        self.grid[i][idx] = self.nextBlock
        self.nextBlock = self.nextNextBlock
        if self.setMoves:
            self.nextNextBlock = self.moves[self.blockAmount]
            self.blockAmount += 1
        else:
            self.nextNextBlock = random.randint(min(self.greatestBlockHeight - 10, self.lowestBlockHeight), self.greatestBlockHeight - 6)

        # game over
        if i == 0 and self.grid[0][idx] != self.grid[1][idx]:
            self.alive = False
            return
        self.merge(idx, i)

    def get_data(self):
        ret = [self.nextBlock, self.nextNextBlock]
        for i in self.grid:
            for j in i:
                ret.append(j)
        return ret

    def get_reward(self):
        return self.score / 100


def run(genome, config):
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    game = Main()
    fitness = 0
    for i in range(3):
        while game.alive:
            output = net.activate(game.get_data())
            i = output.index(max(output))
            game.appendblock(i)
        fitness += game.get_reward() ** 2
    return fitness / 3


moves = [random.randint(0, 5) for i in range(100000)]
generation = 0

scores = open("score.txt", "w")

if __name__ == "__main__":
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, "./config.txt")
    p = neat.Population(config)
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    pe = neat.ParallelEvaluator(multiprocessing.cpu_count(), run)
    winner = p.run(pe.evaluate, 1000)
    visualize.draw_net(config, winner, True)
    visualize.plot_stats(stats, view=True)
    visualize.plot_species(stats, view=True)
    with open("winner.pkl", "wb") as f:
        pickle.dump(winner, f)
        f.close()
