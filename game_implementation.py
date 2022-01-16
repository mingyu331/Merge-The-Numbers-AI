import sys
import random
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt

class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # const
        self.blockSize = 100
        self.fontSize = 50
        # game stuff
        self.grid = [[-1 for col in range(5)] for row in range(6)]
        self.keys = [QtCore.Qt.Key_1, QtCore.Qt.Key_2, QtCore.Qt.Key_3, QtCore.Qt.Key_4, QtCore.Qt.Key_5]
        self.score = 0
        self.greatestBlockHeight = 10
        self.lowestBlockHeight = 0
        self.nextBlock = 0
        self.nextNextBlock = 0
        self.points = 0
        self.bestScore = 0
        # PyQt
        self.label = QtWidgets.QLabel()
        canvas = QtGui.QPixmap(5 + self.blockSize * 5, 5 + self.blockSize * 8)
        self.label.setPixmap(canvas)
        self.setCentralWidget(self.label)
        self.draw()
        self.show()

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.key() in self.keys:
            self.appendblock(event.key() - 49)
            self.label.setPixmap(QtGui.QPixmap(5 + self.blockSize * 5, 5 + self.blockSize * 8))
            self.draw()
            self.show()
        event.accept()

    def draw(self):

        # setup
        painter = QtGui.QPainter(self.label.pixmap())
        # background
        painter.setBrush(QtGui.QBrush(QtGui.QColor("#FFFFFF"), Qt.SolidPattern))
        painter.drawRect(-1, -1, 6 + self.blockSize * 5, 6 + self.blockSize * 8)
        # information
        painter.setBrush(QtGui.QBrush(QtGui.QColor("#FF2054"), Qt.SolidPattern))
        painter.setPen(QtGui.QColor("#FF2054"))
        painter.drawRect(5, 5, self.blockSize * 5 - 5, self.blockSize - 5)
        painter.drawRect(5, 5 + self.blockSize, self.blockSize * 5 - 5, self.blockSize - 5)
        painter.setPen(QtGui.QColor("#FFFFFF"))
        painter.setFont(QtGui.QFont("Cascadia Code", int(self.fontSize / 2)))
        painter.drawText(QtCore.QPoint(10, 10 + int(self.fontSize / 2)), str(self.points))
        painter.drawText(QtCore.QPoint(10 + int(self.blockSize * 2.5), 10 + int(self.fontSize / 2)), str(self.bestScore))
        painter.setFont(QtGui.QFont("Cascadia Code", self.fontSize))
        painter.drawText(QtCore.QPoint(10, 10 + self.fontSize + self.blockSize),
                         "cur:" + str(self.nextBlock) + " nxt:" + str(self.nextNextBlock))
        # grid
        painter.setPen(QtGui.QColor("#FF2054"))

        for i in range(5, 5 + self.blockSize * 5, self.blockSize):
            for j in range(5, 5 + self.blockSize * 6, self.blockSize):
                painter.drawRect(i, j + self.blockSize * 2, self.blockSize - 5, self.blockSize - 5)

        painter.setPen(QtGui.QColor("#FFFFFF"))

        for i in range(10, 10 + self.blockSize * 5, self.blockSize):
            for j in range(10, 10 + self.blockSize * 6, self.blockSize):
                if self.grid[int((j - 10) / self.blockSize)][int((i - 10) / self.blockSize)] != -1:
                    painter.drawText(QtCore.QPoint(i, j + self.blockSize * 2 + self.fontSize),
                                     str(self.grid[int((j - 10) / self.blockSize)][int((i - 10) / self.blockSize)]))
        # painter.drawLine(10, 10, 300, 200)
        painter.end()

    def reset(self):
        for i in range(6):
            for j in range(5):
                self.grid[i][j] = -1
        self.greatestBlockHeight = 10
        self.lowestBlockHeight = 0
        print(self.points)
        self.bestScore = max(self.points, self.bestScore)
        self.points = 0

    def fall(self, idx):
        for i in range(5, 0, -1):
            if self.grid[i][idx] == -1:
                self.grid[i][idx] = self.grid[i - 1][idx]
                self.grid[i - 1][idx] = -1
        for i in range(5, 0, -1):
            self.merge(idx, i)

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
        self.points += 2 ** self.grid[y][x]
        self.fall(x)
        if x != 0:
            self.fall(x - 1)
        if x != 4:
            self.fall(x + 1)
        return False

    def appendblock(self, idx):
        i = 0
        while i <= 5 and self.grid[i][idx] == -1:
            # print(i)
            i += 1
        i -= 1
        self.grid[i][idx] = self.nextBlock
        self.nextBlock = self.nextNextBlock
        self.nextNextBlock = random.randint(min(self.greatestBlockHeight - 10, self.lowestBlockHeight), self.greatestBlockHeight - 6)

        # game over
        if i == 0 and self.grid[0][idx] != self.grid[1][idx]:
            self.reset()
            return
        self.merge(idx, i)





app = QtWidgets.QApplication(sys.argv)
window = Main()
window.show()
app.exec_()
