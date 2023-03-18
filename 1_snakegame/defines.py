import pygame
from random import randint

FPS = 8
FIELD_SIZE  = (500, 500)
WINDOW_SIZE = (1000, 500)
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (  0,   0,   0)
FIELD_COLOR = (100, 255, 100)
GREEN_COLOR = (  0, 255,   0)
DARKG_COLOR = (  0, 100,   0)
RED_COLOR   = (100,   0,   0)
BLOCK_SIZE = 20

WIN = pygame.display.set_mode(size = (WINDOW_SIZE)) # Set Window Size
pygame.display.set_caption("Snake Game") # Set Window Title

pygame.font.init()
FONT_60 = pygame.font.SysFont('comicsans',60)
FONT_30 = pygame.font.SysFont('comicsans',30)
FONT_BLOCK = pygame.font.SysFont('comicsans',BLOCK_SIZE)
DISTANCE_FONT = pygame.font.SysFont('comicsans',BLOCK_SIZE)
FIELD_RECT = pygame.Rect(0, 0, FIELD_SIZE[0], FIELD_SIZE[1])

def new_location():
    temp_rand = []
    x_rand = randint(0, ((FIELD_SIZE[0] / BLOCK_SIZE) - 1)) * BLOCK_SIZE
    y_rand = randint(0, ((FIELD_SIZE[1] / BLOCK_SIZE) - 1)) * BLOCK_SIZE
    temp_rand.append((x_rand, y_rand))

    if(set(temp_rand) & set(snake_struct.body) or set(temp_rand) & set(food_struct.loc)):
        # print("Repeated")
        return(new_location())
    else:
        return ((x_rand, y_rand))

class snake_struct():
    direction = 0 # Up(0), Down(1), Left(2), Right(3)
    snake_init_length = 3
    body = []
    temp_append = []
    distance_head_to_food = [0, 0, 0, 0] # Up(0), Down(1), Left(2), Right(3)
    distance_head_to_wall = [0, 0, 0, 0] # Up(0), Down(1), Left(2), Right(3)
    distance_head_to_body = [0, 0, 0, 0] # Up(0), Down(1), Left(2), Right(3)
    draw_head_to_body = [(0,0),(0,0),(0,0),(0,0)] # Up(0), Down(1), Left(2), Right(3)

    def calculate_distance(self, food_loc):
        snake_head = []
        snake_head.append(self.body[0])
        snake_head_x = snake_head[0][0]
        snake_head_y = snake_head[0][1]
        snake_body_x = sorted(sorted(self.body[1:], key = lambda s:s[1]), key = lambda s:s[0])
        snake_body_x_r = sorted(sorted(self.body[1:], key = lambda s:s[1]), key = lambda s:s[0], reverse = True)
        snake_body_y = sorted(sorted(self.body[1:], key = lambda s:s[0]), key = lambda s:s[1])
        snake_body_y_r = sorted(sorted(self.body[1:], key = lambda s:s[0]), key = lambda s:s[1], reverse = True)
        food_loc_x = food_loc[0][0]
        food_loc_y = food_loc[0][1]

        # Up(0), Down(1), Left(2), Right(3)
        for dir_idx in range(4):
            if dir_idx == 0:
                # head2wall
                self.distance_head_to_wall[dir_idx] = ((snake_head_y - 0) / BLOCK_SIZE)

                # head2food
                if (snake_head_x == food_loc_x) and (food_loc_y < snake_head_y):
                    self.distance_head_to_food[dir_idx] = ((food_loc_y - snake_head_y) / BLOCK_SIZE)
                else:
                    self.distance_head_to_food[dir_idx] = -1

                # head2body
                body = snake_body_y_r
                for body_idx in body:
                    if (body_idx[0] == snake_head_x) and (body_idx[1] < snake_head_y):
                        self.draw_head_to_body[dir_idx] = body_idx
                        self.distance_head_to_body[dir_idx] = ((snake_head_y - body_idx[1]) / BLOCK_SIZE)
                        break
                    else:
                        self.draw_head_to_body[dir_idx] = (-1, -1)
                        self.distance_head_to_body[dir_idx] = -1
                #print("DIR: UP; HEAD: " + str(snake_head[0][0]) + "," + str(snake_head[0][1]) + " ; BODY: " + str(self.draw_head_to_body[dir_idx][0]) + "," + str(self.draw_head_to_body[dir_idx][1]) + " ; DIS: " + str(self.distance_head_to_body[dir_idx]) + " ;")
            elif dir_idx == 1:
                # head2wall
                self.distance_head_to_wall[dir_idx] = ((FIELD_SIZE[1] - snake_head_y) / BLOCK_SIZE)

                # head2food
                if (snake_head_x == food_loc_x) and (food_loc_y > snake_head_y):
                    self.distance_head_to_food[dir_idx] = ((snake_head_y - food_loc_y) / BLOCK_SIZE)
                else:
                    self.distance_head_to_food[dir_idx] = -1

                body = snake_body_y
                for body_idx in body:
                    if (body_idx[0] == snake_head_x) and (body_idx[1] > snake_head_y):
                        self.draw_head_to_body[dir_idx] = body_idx
                        self.distance_head_to_body[dir_idx] = ((body_idx[1] - snake_head_y) / BLOCK_SIZE)
                        break
                    else:
                        self.draw_head_to_body[dir_idx] = (-1, -1)
                        self.distance_head_to_body[dir_idx] = -1
                #print("DIR: DOWN; HEAD: " + str(snake_head[0][0]) + "," + str(snake_head[0][1]) + " ; BODY: " + str(self.draw_head_to_body[dir_idx][0]) + "," + str(self.draw_head_to_body[dir_idx][1]) + " ; DIS: " + str(self.distance_head_to_body[dir_idx]) + " ;")
            elif dir_idx == 2:
                # head2wall
                self.distance_head_to_wall[dir_idx] = ((snake_head_x - 0) / BLOCK_SIZE)

                # head2food
                if (snake_head_y == food_loc_y) and (food_loc_x < snake_head_x):
                    self.distance_head_to_food[dir_idx] = ((snake_head_x - food_loc_x) / BLOCK_SIZE)
                else:
                    self.distance_head_to_food[dir_idx] = -1

                body = snake_body_x_r
                for body_idx in body:
                    if (body_idx[1] == snake_head_y) and (body_idx[0] < snake_head_x):
                        self.draw_head_to_body[dir_idx] = body_idx
                        self.distance_head_to_body[dir_idx] = ((snake_head_x - body_idx[0]) / BLOCK_SIZE)
                        break
                    else:
                        self.draw_head_to_body[dir_idx] = (-1, -1)
                        self.distance_head_to_body[dir_idx] = -1
                #print("DIR: LEFT; HEAD: " + str(snake_head[0][0]) + "," + str(snake_head[0][1]) + " ; BODY: " + str(self.draw_head_to_body[dir_idx][0]) + "," + str(self.draw_head_to_body[dir_idx][1]) + " ; DIS: " + str(self.distance_head_to_body[dir_idx]) + " ;")
            elif dir_idx == 3:
                # head2wall
                self.distance_head_to_wall[dir_idx] = ((FIELD_SIZE[0] - snake_head_x) / BLOCK_SIZE)

                # head2food
                if (snake_head_y == food_loc_y) and (food_loc_x > snake_head_x):
                    self.distance_head_to_food[dir_idx] = ((food_loc_x - snake_head_x) / BLOCK_SIZE)
                else:
                    self.distance_head_to_food[dir_idx] = -1

                body = snake_body_x
                for body_idx in body:
                    if (body_idx[1] == snake_head_y) and (body_idx[0] > snake_head_x):
                        self.draw_head_to_body[dir_idx] = body_idx
                        self.distance_head_to_body[dir_idx] = ((body_idx[0] - snake_head_x) / BLOCK_SIZE)
                        break
                    else:
                        self.draw_head_to_body[dir_idx] = (-1, -1)
                        self.distance_head_to_body[dir_idx] = -1
                #print("DIR: LEFT; HEAD: " + str(snake_head[0][0]) + "," + str(snake_head[0][1]) + " ; BODY: " + str(self.draw_head_to_body[dir_idx][0]) + "," + str(self.draw_head_to_body[dir_idx][1]) + " ; DIS: " + str(self.distance_head_to_body[dir_idx]) + " ;")

    def update_postition(self, ate_flag, buff):
        key_pressed = -1;

        # Update Direction
        if(buff):
            key_pressed = (buff.pop())
        if key_pressed == 0 and self.direction != 1:
            self.direction = 0
        elif key_pressed == 1 and self.direction != 0:
            self.direction = 1
        elif key_pressed == 2 and self.direction != 3:
            self.direction = 2
        elif key_pressed == 3 and self.direction != 2:
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
        if ate_flag:
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
