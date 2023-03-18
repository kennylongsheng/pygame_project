from defines import *
from machine_learning import *

# Some Global Variables
game_run = True
game_start = False
ate_flag = False
dead_flag = False
machine_learninig_flag = False
score = 0
cur_snake = snake_struct()
cur_food = food_struct()
keyboard_buff = []

# Functions
def game_init():
    global game_start, ate_flag, dead_flag, score, cur_snake, cur_food
    output_text = "Hit Enter to Continue!"
    output_text_render = FONT_60.render(output_text, 1, WHITE_COLOR)
    WIN.fill(BLACK_COLOR)
    WIN.blit(output_text_render, ((WINDOW_SIZE[0] / 2) - (output_text_render.get_width() / 2) , (WINDOW_SIZE[1] / 2) - (output_text_render.get_height() / 2)))
    
    game_start = False
    ate_flag = False
    dead_flag = False
    score = 0
    cur_snake.reset()
    cur_food.reset()
    pygame.display.update() # Ask Window to Update

def game_calculate(buff):
    global ate_flag, dead_flag, score, machine_learninig_flag
    # Food
    cur_food.food_update(ate_flag)
    
    # Snake
    cur_snake.update_postition(ate_flag, buff)

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
    elif ((snake_head[0][0] < 0) or (snake_head[0][0] > FIELD_SIZE[0] - BLOCK_SIZE) or (snake_head[0][1] < 0) or (snake_head[0][1] > FIELD_SIZE[1] - BLOCK_SIZE)):
        #print("Snake Head Collide to Boundary")
        dead_flag = True
    elif(set(cur_food.loc) & set(cur_snake.body)):
        #print("Food Ate")
        ate_flag = True
        score += 1
        cur_snake.temp_append.append(cur_snake.body[len(cur_snake.body) - 1])

def machine_learninig_flow():
    # Update Distances
    cur_snake.calculate_distance(cur_food.loc)

def win_draw():
    global score, machine_learninig_flag
    snake_head_flag = True
    WIN.fill(BLACK_COLOR)
    pygame.draw.rect(WIN, FIELD_COLOR, FIELD_RECT)
    
    #CHECK LOCATION
    #print(snake_struct.body)
    #print(food_struct.loc)

    # Field Area
    food_R = pygame.Rect(cur_food.loc[0][0], cur_food.loc[0][1], BLOCK_SIZE, BLOCK_SIZE)
    pygame.draw.rect(WIN, BLACK_COLOR, food_R)

    # Field Area Draw
    for body_rect_idx  in cur_snake.body:
        snake_R = pygame.Rect(body_rect_idx[0], body_rect_idx[1], BLOCK_SIZE, BLOCK_SIZE)
        if snake_head_flag == True:
            snake_head_flag = False
            pygame.draw.rect(WIN, DARKG_COLOR, snake_R)
        else:
            pygame.draw.rect(WIN, GREEN_COLOR, snake_R)

    if machine_learninig_flag:
        for idx in range(4):
            if(cur_snake.draw_head_to_body[idx] != (-1, -1)):
                dis_R = pygame.Rect(cur_snake.draw_head_to_body[idx][0], cur_snake.draw_head_to_body[idx][1], BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(WIN, RED_COLOR, dis_R)
                # dis_text = (str(cur_snake.distance_head_to_body[idx]))
                # dis_text_R = FONT_BLOCK.render(dis_text, 1, WHITE_COLOR)
                # WIN.blit(dis_text_R, (cur_snake.draw_head_to_body[idx]))

    # Expanded Area
    x_axis = FIELD_SIZE[0] + BLOCK_SIZE
    y_axis = BLOCK_SIZE
    score_text = ("Score: " + str(score))
    score_R = FONT_30.render(score_text, 1, WHITE_COLOR)
    WIN.blit(score_R, (x_axis, y_axis))
    y_axis += (BLOCK_SIZE + score_R.get_height())

    if machine_learninig_flag:
        dis_text = ("Head2Food " + str(cur_snake.distance_head_to_food))
        dis_text_R = FONT_30.render(dis_text, 1, WHITE_COLOR)
        WIN.blit(dis_text_R, (x_axis, y_axis))
        y_axis += (BLOCK_SIZE + dis_text_R.get_height())

        dis_text = ("Head2Wall " + str(cur_snake.distance_head_to_wall))
        dis_text_R = FONT_30.render(dis_text, 1, WHITE_COLOR)
        WIN.blit(dis_text_R, (x_axis, y_axis))
        y_axis += (BLOCK_SIZE + dis_text_R.get_height())

        dis_text = ("Head2Body " + str(cur_snake.distance_head_to_body))
        dis_text_R = FONT_30.render(dis_text, 1, WHITE_COLOR)
        WIN.blit(dis_text_R, (x_axis, y_axis))
        y_axis += (BLOCK_SIZE + dis_text_R.get_height())


    # Ask Window to Update
    pygame.display.update()

def main():
    global game_run, game_start, machine_learninig_flag
    clock = pygame.time.Clock()
    while game_run:
        clock.tick(FPS + (score / 2)) # Set Window FPS

        # Mode Setting
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Close Window
                game_run = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and game_start == False:
                    # Press Enter to Start Game
                    game_start = True
                elif event.key == pygame.K_l:
                    # Press l to For Machine Learning Flag
                    if(machine_learninig_flag == True):
                        machine_learninig_flag = False
                        print("ML Flag FALSE")
                    else:
                        machine_learninig_flag = True
                        print("ML Flag TRUE")
                elif event.key == pygame.K_UP:
                    if (keyboard_buff):
                        keyboard_buff.pop()
                    keyboard_buff.append(0)
                elif event.key == pygame.K_DOWN:
                    if (keyboard_buff):
                        keyboard_buff.pop()
                    keyboard_buff.append(1)
                elif event.key == pygame.K_LEFT:
                    if (keyboard_buff):
                        keyboard_buff.pop()
                    keyboard_buff.append(2)
                elif event.key == pygame.K_RIGHT:
                    if (keyboard_buff):
                        keyboard_buff.pop()
                    keyboard_buff.append(3)

        # Start Normal Game / Training
        if game_start == False or dead_flag == True:
            game_init()
        else:
            game_calculate(keyboard_buff)

            if machine_learninig_flag == True:
                # Machine Learning Flow
                machine_learninig_flow()

            # Update Window
            win_draw()


if __name__ == "__main__":
    main()
