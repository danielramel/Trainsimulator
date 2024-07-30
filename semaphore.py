import pygame
from constants import *


class Semaphore:
    def __init__(self, name, point, direction, isAlwaysGreen=False):
        self.name = name
        self.point = point
        self.direction = 1 if direction else -1

        self.speed = 0
        self.next_speed = 0
        self.path = None
        self.next_semaphore = None

        self.isAlwaysGreen = isAlwaysGreen
        if isAlwaysGreen:
            self.speed = 160
            self.next_speed = 160

    def set(self, path):
        if self.isAlwaysGreen:
            raise ValueError("Cannot set always green semaphore!")
        
        self.path = path
        mini = min([rail.speed for rail in self.path])
        self.speed = mini

        self.next_semaphore = self.path[-1].b.rightSemaphore if self.direction==1 else self.path[-1].a.leftSemaphore

    @property
    def Colors(self):
        if self.isAlwaysGreen:
            return [BLACK, BLACK, GREEN, BLACK, BLACK]
        
        if self.speed == 0:
            return [BLACK, BLACK, RED, BLACK, BLACK]
        
        c = [None, None, None, None, None]
        
        if self.speed == 40:
            c[2:] = [BLACK, YELLOW, BLACK]
        elif self.speed == 80:
            c[2:] = [BLACK, YELLOW, GREEN]
        else:
            c[2:] = [BLACK, BLACK, BLACK]

        next_speed = self.next_semaphore.speed

        if next_speed == 0 or next_speed == 40 and pygame.time.get_ticks() % 1000 < 500:
            c[:2] = [BLACK, YELLOW]
        elif next_speed == 40:
            c[:2] = [BLACK, BLACK]
        elif next_speed == 80 and pygame.time.get_ticks() % 1000 > 500:
            c[:2] = [BLACK, BLACK]
        else:
            c[:2] = [GREEN, BLACK]

        return c

    def __repr__(self):
        return f"Semaphore(name={self.name}, point={repr(self.point)}, direction={self.direction})"
    
    def draw(self, surface):
        pygame.draw.circle(surface, WHITE, (self.point.X - (self.direction*10), self.point.Y-30), 3)
        pygame.draw.circle(surface, self.Colors[0], (self.point.X - (self.direction*10), self.point.Y-30), 2)

        pygame.draw.circle(surface, WHITE, (self.point.X - (self.direction*10), self.point.Y-25), 3)
        pygame.draw.circle(surface, self.Colors[1], (self.point.X - (self.direction*10), self.point.Y-25), 2)

        pygame.draw.circle(surface, WHITE, (self.point.X - (self.direction*10), self.point.Y-15), 3)
        pygame.draw.circle(surface, self.Colors[2], (self.point.X - (self.direction*10), self.point.Y-15), 2)

        pygame.draw.circle(surface, WHITE, (self.point.X - (self.direction*10), self.point.Y-10), 3)
        pygame.draw.circle(surface, self.Colors[3], (self.point.X - (self.direction*10), self.point.Y-10), 2)

        pygame.draw.line(surface, self.Colors[4], (self.point.X  - (self.direction*10)-4, self.point.Y-5), (self.point.X- (self.direction*10)+4, self.point.Y-5), 2)


class AutoSemaphore(Semaphore):
    def __init__(self, name, point, direction):
        self.name = name
        self.point = point
        self.direction = 1 if direction else -1

        



    def set(self, path):
        raise ValueError("Cannot set auto semaphore!")