import pygame
from math import sqrt
import sys
import random
from constants import *
from rail import Rail
from switch import Switch
from route import Route
from train import Train
from point import Point



def main():
    semaphores = {}
    points = {name: Point(name, *point, semaphores=semaphores) for name, point in POINTS.items()}
    rails = {name: Rail(name, points[rail[0]], points[rail[1]], *rail[2:]) for name, rail in RAILS.items()}
    switches = {name: Switch(*switch) for name, switch in SWITCHES.items()}

    pygame.init()

    screen = pygame.display.set_mode((DEFAULT_WIDTH, DEFAULT_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption(TRACK_NAME)


    MOVE_TRAIN_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(MOVE_TRAIN_EVENT, REFRESH_RATE)

    paused = False
    firstPoint = None
    c = 1
    command = []
    trains = {}

    while True:
        screen.fill((0, 0, 0))

        if paused:
            font = pygame.font.SysFont("Arial", 50)
            text = font.render("PAUSED", True, WHITE)
            text_rect = text.get_rect(center=(DEFAULT_WIDTH/2, DEFAULT_HEIGHT/2))
            screen.blit(text, text_rect)

        for rail in rails.values():
            rail.draw(screen)

        for train in trains.values():
            train.draw(screen)

        for semaphore in semaphores.values():
            semaphore.draw(screen)
        
        for point in points.values():
            point.draw(screen, firstPoint)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.VIDEORESIZE:
                Train.width, Train.height = event.w, event.h
                Point.width, Point.height = event.w, event.h

                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            elif event.type == MOVE_TRAIN_EVENT and not paused:
                toBeRemoved = []
                for train in trains.values():
                    if train.move(rails, semaphores):
                        toBeRemoved.append(train.name)
                for name in toBeRemoved:
                    del trains[name]
                
                # generate trains
                if random.random() < 1/(TRAIN_FEED_RATE*1000/REFRESH_RATE):
                    point = random.choice(("ZB", "ZD", "ZE", "TF", "TH"))

                    direction = point.startswith("T")

                    if not direction and not rails[point].isLocked or direction and not rails[point[1]+"1"].isLocked:
                        
                        trains[str(c)] = Train(str(c), point, direction, ("B" if direction else "E") + point[1], points, rails, semaphores)
                        rails[point].lock()
                        if direction:
                            rails[point[1]+"1"].lock()
                        c += 1
                  
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused

                #reverse a train
                elif event.key == pygame.K_c:
                    command = []
                elif event.key == pygame.K_e:
                    train_to_reverse = "".join(command)
                    if train_to_reverse not in trains:
                        print("Train not found!")
                        continue
                    if trains[train_to_reverse].current_speed != 0:
                        print("Cannot reverse a moving train!")
                        continue

                    train = trains[train_to_reverse]
                    train.direction = (-1*train.direction[0], -1*train.direction[1])
                    train.max_allowed_speed = 40
                    train.next_semaphore = semaphores["B"+train.next_semaphore.name[1]+"R"]
                    train.railep = train.rail.a if train.direction[0] < 0 else train.rail.b

                else:
                    command.append(event.unicode)
                    
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for point in points.values():
                        if sqrt((point.X-event.pos[0])**2+(point.Y-event.pos[1])**2) < 15 and point.connectable:
                            if firstPoint is None:
                                firstPoint = point
                                break
                        
                            if firstPoint == point:
                                if firstPoint.name.startswith("E"):
                                    point = points["Z"+firstPoint.name[1]]
                                elif firstPoint.name.startswith("S") and "T"+firstPoint.name[1] in points:
                                    point = points["T"+firstPoint.name[1]]
                            
                        
                            direction = firstPoint._x < point._x

                            if direction and (firstPoint.rightSemaphore is None or point.rightSemaphore is None) or \
                                not direction and (firstPoint.leftSemaphore is None or point.leftSemaphore is None):
                                print("It is not possible to set a route between these two points!")
                                break
                            
                            r = Route(firstPoint, point, rails)

                            if r.path is None:
                                print("It is not possible to set a route between these two points!")
                                break

                            try:
                                r.set(rails, semaphores, switches)
                            except ValueError as e:
                                print(e)
                                break
                            
                            firstPoint = None

                #mouse right click
                elif event.button == 3:
                    firstPoint = None

if __name__ == "__main__":
    main()
          
    # todo
    # optimal speed when two semaphores are close, the second one is stop, cbig shows when you set the TRAIN_SPEED_COEFFICIENT too high
    # make other types of semaphores
    # auto switch creation
