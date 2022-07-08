from copy import deepcopy
import pygame
from .constants import SQUARE_SIZE

class Piece:

    def __init__(self, name= None, color: tuple= None, row= 0, col= 0, image: pygame.Surface= None):
        self.name = name
        self.color = color
        self.row = row
        self.col = col
        self.image = image
        self.moved = 0
        self.moveLen = (0, 0)
        self.x = 0
        self.y = 0
        if self.image: self.calcPos()

    def calcPos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE//2 - self.image.get_width()//2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE//2 - self.image.get_height()//2

    def copy(self):
        copyObj = Piece()
        for name, attr in self.__dict__.items():
            if hasattr(attr, 'copy') and callable(getattr(attr, 'copy')):
                copyObj.__dict__[name] = attr.copy()
            else:
                copyObj.__dict__[name] = deepcopy(attr)
        return copyObj

    def promote(self, other):
        self.name = other.name
        self.image = other.image.copy()
        
    def move(self, row, col):
        self.moved += 1
        self.moveLen = (self.col - col, self.row - row)
        self.row = row
        self.col = col
        self.calcPos()

    def __repr__(self) -> str:
        return self.name + "  " + str(self.color) + "  (" + str(self.row) + ", " + str(self.col) + ")"