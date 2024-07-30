from track import *

#adjust these variables:
TRAIN_SPEED_COEFFICIENT = 1 # don't set above 1
REFRESH_RATE = 10 # in ms
TRAIN_FEED_RATE = 1 # on average 1 train every x seconds
TRAIN_ACCELERATION_RATE = 1

DEFAULT_WIDTH, DEFAULT_HEIGHT = 800, 600

#end of adjustable variables


GAME_SPEED = TRAIN_SPEED_COEFFICIENT/3000*(REFRESH_RATE/1000)
MS_TO_KMH = 3.6

RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)