from defines import *

# Some Global Variables
game_run = True
game_start = False
ate_flag = False
dead_flag = False
score = 0
cur_snake = snake_struct()
cur_food = food_struct()

# Functions
def game_init():
    global game_start, ate_flag, dead_flag, score, cur_snake, cur_food
    output_text = "Hit Enter to Continue!"
    output_text_render = WELCOME_FONT.render(output_text, 1, BLACK_COLOR)
    WIN.fill(WHITE_COLOR)
    WIN.blit(output_text_render, ((WINDOW_SIZE[0] / 2) - (output_text_render.get_width() / 2) , (WINDOW_SIZE[1] / 2) - (output_text_render.get_height() / 2)))
    
    game_start = False
    ate_flag = False
    dead_flag = False
    score = 0
    cur_snake.reset()
    cur_food.reset()
    pygame.display.update() # Ask Window to Update

def game_calculate(key_pressed):
    global ate_flag, dead_flag, score
    # Food
    cur_food.food_update(ate_flag)
    
    # Snake
    cur_snake.update_postition(ate_flag, key_pressed)

    if (ate_flag == True):
        ate_flag = False

    # Check Collide
    snake_head = []
    snake_head.append(cur_snake.body[0])
    if (set(snake_head) & set(cur_snake.body[1:])):
        #print("Snake Head Collide")
        #print(snake_struct.body)
        #print(snake_struct.direction)
        dead_flag = True
    elif ((snake_head[0][0] < 0) or (snake_head[0][0] > WINDOW_SIZE[0] - BLOCK_SIZE) or (snake_head[0][1] < 0) or (snake_head[0][1] > WINDOW_SIZE[1] - BLOCK_SIZE)):
        #print("Snake Head Collide to Boundary")
        dead_flag = True
    elif(set(cur_food.loc) & set(cur_snake.body)):
        #print("Food Ate")
        ate_flag = True
        score += 1
        cur_snake.temp_append.append(cur_snake.body[len(cur_snake.body) - 1])

def win_draw():
    global score
    WIN.fill(WHITE_COLOR)
    
    #CHECK LOCATION
    #print(snake_struct.body)
    #print(food_struct.loc)

    score_text = ("Score: " + str(score))
    score_R = SCORE_FONT.render(score_text, 1, BLACK_COLOR)
    WIN.blit(score_R, (BLOCK_SIZE, BLOCK_SIZE))

    food_R = pygame.Rect(cur_food.loc[0][0], cur_food.loc[0][1], BLOCK_SIZE, BLOCK_SIZE)
    pygame.draw.rect(WIN, BLACK_COLOR, food_R)

    for body_rect_idx  in cur_snake.body:
        snake_R = pygame.Rect(body_rect_idx[0], body_rect_idx[1], BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(WIN, GREEN_COLOR, snake_R)

    pygame.display.update() # Ask Window to Update

def main():
    global game_run, game_start
    clock = pygame.time.Clock()
    while game_run:
        clock.tick(FPS) # Set Window FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_run = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and game_start == False:
                    game_start = True
        if game_start == False or dead_flag == True:
            game_init()
        else:
            game_calculate(pygame.key.get_pressed())
            win_draw()


if __name__ == "__main__":
    main()