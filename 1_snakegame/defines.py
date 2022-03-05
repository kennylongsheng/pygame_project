import pygame
from random import randint

FPS = 10
WINDOW_SIZE = (1000, 500)
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (  0,   0,   0)
GREEN_COLOR = (  0, 255,   0)
BLOCK_SIZE = 10

WIN = pygame.display.set_mode(WINDOW_SIZE) # Set Window Size
pygame.display.set_caption("Snake Game") # Set Window Title

pygame.font.init()
WELCOME_FONT = pygame.font.SysFont('comicsans',60)
SCORE_FONT = pygame.font.SysFont('comicsans',30)

def new_location():
    temp_rand = []
    x_rand = randint(0, ((WINDOW_SIZE[0] / BLOCK_SIZE) - 1)) * BLOCK_SIZE
    y_rand = randint(0, ((WINDOW_SIZE[1] / BLOCK_SIZE) - 1)) * BLOCK_SIZE
    temp_rand.append((x_rand, y_rand))

    if(set(temp_rand) & set(snake_struct.body) or set(temp_rand) & set(food_struct.loc)):
        print("Repeated")
        return(new_location())
    else:
        return ((x_rand, y_rand))

class snake_struct():
    direction = 0 # Up(0), Down(1), Left(2), Right(3)
    snake_init_length = 3
    body = []
    temp_append = []

    def update_postition(self, ate_flag, key_pressed):
        # Update Direction
        if key_pressed[pygame.K_UP] and self.direction != 1:
            self.direction = 0
        elif key_pressed[pygame.K_DOWN] and self.direction != 0:
            self.direction = 1
        elif key_pressed[pygame.K_LEFT] and self.direction != 3:
            self.direction = 2
        elif key_pressed[pygame.K_RIGHT] and self.direction != 2:
            self.direction = 3

        # Update Body
        for i in range(len(self.body)-1, -1, -1):
            if (i ==  0):
                (x,y) = self.body[i]
                if (self.direction == 0):
                    self.body[i] = (x,y-BLOCK_SIZE)
                elif (self.direction == 1):
                    self.body[i] = (x,y+BLOCK_SIZE)
                elif (self.direction == 2):
                    self.body[i] = (x-BLOCK_SIZE,y)
                elif (self.direction == 3):
                    self.body[i] = (x+BLOCK_SIZE,y)
            else:
                self.body[i] = self.body[i-1]
        if  ate_flag:
            self.body.append(self.temp_append.pop())

    def reset(self):
        self.body.clear()
        self.temp_append.clear()
        self.direction = randint(0, 3)
        self.body.append(new_location())
        for i in range(self.snake_init_length):
            x = self.body[i][0]
            y = self.body[i][1]
            if self.direction == 0 :
                self.body.append((x    , y + BLOCK_SIZE))
            elif self.direction == 1 :
                self.body.append((x    , y - BLOCK_SIZE))
            elif self.direction == 2 :
                self.body.append((x + BLOCK_SIZE, y    ))
            elif self.direction == 3 :
                self.body.append((x - BLOCK_SIZE, y    ))

    def __init__(self):
        self.reset()


class food_struct():
    loc = []

    def food_update(self, ate_flag):
        if ate_flag == True:
            self.loc.pop()
            self.loc.append(new_location())

    def reset(self):
        self.loc.clear()
        self.loc.append(new_location())


    def __init__(self):
        self.reset()