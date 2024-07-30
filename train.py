import pygame
from constants import *
from math import sqrt


class Train:
    width, height = DEFAULT_WIDTH, DEFAULT_HEIGHT

    def __init__(self, name, startPos, direction, next_semaphore, points, rails, semaphores, current_speed=120, max_allowed_speed=120, acceleration=1.1, deceleration=1.5, color=GREEN):
        for rail in rails.values():
            if direction and rail.a.name == startPos:
                self.rail = rail
                self.railep = rail.b
                self.direction = rail.direction
                break
            elif not direction and rail.b.name == startPos:
                self.rail = rail
                self.railep = rail.a
                self.direction = (-1*rail.direction[0], -1*rail.direction[1])
                break
        else:
            raise ValueError("The train is not connected to one of the ends of a rail!")

        
        self.name = name
        self._x = points[startPos]._x
        self._y = points[startPos]._y
        self.acceleration = acceleration*MS_TO_KMH/(300*TRAIN_ACCELERATION_RATE/REFRESH_RATE)
        self.deceleration = deceleration*MS_TO_KMH/(300*TRAIN_ACCELERATION_RATE/REFRESH_RATE)
        self.current_speed = current_speed
        self.max_allowed_speed = max_allowed_speed
        self.color = color

        self.next_semaphore = semaphores[next_semaphore + ("R" if direction else "L")]

        self.target_speed = self.next_semaphore.speed

    def move(self, rails, semaphores):
        self.target_speed = self.next_semaphore.speed

        if self.target_speed > self.current_speed:
            self.current_speed = min(self.current_speed + self.acceleration, self.max_allowed_speed)

        else:
            # using u^2 = v^2 - 2as
            distance_to_next_semaphore = sqrt(abs(self.next_semaphore.point._x-self._x)**2+abs(self.next_semaphore.point._y-self._y)**2)

            optimal_speed = sqrt(self.target_speed**2 + 2*self.deceleration*abs(distance_to_next_semaphore-0.02)/GAME_SPEED)-self.deceleration*0.6

            if optimal_speed < self.current_speed - self.deceleration:
                raise ValueError("The train is going too fast to stop at the next semaphore!")
            
            if optimal_speed < self.current_speed:
                self.current_speed = max(0, optimal_speed)

            else:
                self.current_speed = min(optimal_speed, self.current_speed + self.acceleration, self.max_allowed_speed)


        #move_train
        distance_to_move = self.current_speed*GAME_SPEED

        while distance_to_move > 0:
            self._x += self.direction[0]*distance_to_move
            self._y += self.direction[1]*distance_to_move

            # if the train is still on the rail: exit
            if self.direction[0] < 0 and self._x > self.railep._x or \
                self.direction[0] > 0 and self._x < self.railep._x:
                    return
                    
            #reevalute distance to move
            distance_to_move = sqrt(abs(self.railep._x-self._x)**2+abs(self.railep._y-self._y)**2)

            self._x = self.railep._x
            self._y = self.railep._y
            self.rail.unlock()

            #if the train went past a semaphore
            if self._x == self.next_semaphore.point._x and self._y == self.next_semaphore.point._y:
                #if the semaphore is always green, we exited the playing field
                if self.next_semaphore.isAlwaysGreen:
                    return True
                
                self.max_allowed_speed = self.next_semaphore.speed
                self.next_semaphore.speed = 0
                self.next_semaphore = semaphores[self.next_semaphore.next_semaphore.name]
                self.target_speed = self.next_semaphore.speed

            if self.direction[0] > 0:                
                self.rail = rails[self.rail.next]
                self.railep = self.rail.b
                self.direction = self.rail.direction
            else:
                self.rail = rails[self.rail.previous]
                self.railep = self.rail.a
                self.direction = (-1*self.rail.direction[0], -1*self.rail.direction[1])

    @property
    def X(self):
        return self._x * self.width

    @property
    def Y(self):
        return self._y * self.height

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.X, self.Y), 10)

        font = pygame.font.Font(None, 20)
        
        speed_text = font.render(f"{self.current_speed:.0f}km/h", True, YELLOW)
        speed_rect = speed_text.get_rect()

        if self._x > 1:
            text = font.render(f"{round(abs(self._x-1)*830)}m", True, YELLOW if self.direction[0] > 0 else RED)
            text_rect = text.get_rect()
            text_rect.center = (self.width-25, self.Y + 15)
            speed_rect.center = (self.width-25, self.Y + 30)

        elif self._x < 0:
            text = font.render(f"{round(abs(self._x)*830)}m", True, YELLOW if self.direction[0] < 0 else RED)
            text_rect = text.get_rect()
            text_rect.center = (25, self.Y - 20)
            speed_rect.center = (25, self.Y + 20)


        else:
            text = font.render(f"ID: {self.name}", True, YELLOW)
            text_rect = text.get_rect()
            text_rect.center = (self.X, self.Y - 20)
            speed_rect.center = (self.X, self.Y + 20)

        surface.blit(text, text_rect)
        surface.blit(speed_text, speed_rect)

    def __repr__(self):
        return f"Train(rail={repr(self.rail)}, startPos=Point({self._x}, {self._y}), current_speed={self.current_speed})"


