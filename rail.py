import pygame
from math import sqrt
from constants import *

class Rail:
    def __init__(self, name, a, b, previous, next, isTunnel=False, speed=120):
        self.name = name
        self.a = a
        self.b = b
        self.previous = previous
        self.next = next

        self.isTunnel = isTunnel
        self.speed = speed
        
        self.isLocked = False
        self.length = sqrt((self.b._x-self.a._x)**2+(self.b._y-self.a._y)**2)
        self.direction = ((self.b._x-self.a._x)/self.length, (self.b._y-self.a._y)/self.length)

    def lock(self):
        self.isLocked = True

    def unlock(self):
        self.isLocked = False

    def draw(self, surface):
        pygame.draw.line(surface, RED if self.isLocked else PURPLE if self.isTunnel else BLUE, (self.a.X, self.a.Y), (self.b.X, self.b.Y), 2)

    def __repr__(self):
        return f"Rail(name={self.name}, a={repr(self.a)}, b={repr(self.b)})"