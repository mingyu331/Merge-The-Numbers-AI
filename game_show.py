import PyQt5

import sys
import random
import neat
import pickle
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt

class Main(QtWidgets.QMainWindow):
    def __init__(self, nnet):
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
        # neat
        self.net = nnet
        # PyQt
        self.label = QtWidgets.QLabel()
        self.setCentralWidget(self.label)
        self.draw()
        self.show()

    def draw(self):
        canvas = QtGui.QPixmap(5 + self.blockSize * 5, 5 + self.blockSize * 8)
        self.label.setPixmap(canvas)

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