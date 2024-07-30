import pygame
from constants import *
from semaphore import Semaphore


class Point:
    width, height = DEFAULT_WIDTH, DEFAULT_HEIGHT

    def __init__(self, name, x, y, semaphore=None, semaphores=None):
        self.name = name
        self._x = x / 100
        self._y = y / 100
        self.connectable = semaphore is not None

        self.rightSemaphore = None
        self.leftSemaphore = None

        if not self.connectable: return
        if "right" in semaphore:
            semaphores[self.name+"R"] = Semaphore(self.name+"R", self, True, "auto" in semaphore)
            self.rightSemaphore = semaphores[self.name+"R"]

        if "left" in semaphore:
            semaphores[self.name+"L"] = Semaphore(self.name+"L", self, False, "auto" in semaphore)
            self.leftSemaphore = semaphores[self.name+"L"]

    @property
    def X(self):
        return self._x * self.width

    @property
    def Y(self):
        return self._y * self.height
    
    def draw(self, surface, firstPoint):
        if not self.connectable: return
    
        if self==firstPoint:
            pygame.draw.circle(surface, RED, (self.X, self.Y), 6)
        else:
            pygame.draw.circle(surface, YELLOW, (self.X, self.Y), 6)

    def __repr__(self) -> str:
        return f"Point({self.name}, x={self._x}, y={self._y})"
