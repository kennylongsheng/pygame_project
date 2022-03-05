# refers to https://www.youtube.com/watch?v=jO6qQDNa2UY
import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) # Set Window Size
pygame.display.set_caption("First Game") # Set Window Title 
WHITE = (127, 127, 127)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
FPS = 60
VELOCITY = 5
BULLET_VEL = 7
MAX_BULLET = 3
BORDER = pygame.Rect((WIDTH // 2) - 5, 0 , 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound('Asset/Grenade+1.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound('Asset/Gun+Silencer.mp3')

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

SPACESHIP_SCALE_X, SPACESHIP_SCALE_Y = (50, 50)

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Asset', 'spaceship_yellow.png'))
YELLOW_SPACESHIP_IMAGE = pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_SCALE_X, SPACESHIP_SCALE_Y))
YELLOW_SPACESHIP_IMAGE = pygame.transform.rotate(YELLOW_SPACESHIP_IMAGE, (90))

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Asset', 'spaceship_red.png'))
RED_SPACESHIP_IMAGE = pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_SCALE_X, SPACESHIP_SCALE_Y))
RED_SPACESHIP_IMAGE = pygame.transform.rotate(RED_SPACESHIP_IMAGE, (-90))

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Asset', 'space.png')), (WIDTH, HEIGHT))

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0, 0)) # WIN.fill(WHITE)
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text =  HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text =  HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, ((WIDTH - red_health_text.get_width() - 10), 10))
    WIN.blit(yellow_health_text, (10, 10))
    
    WIN.blit(YELLOW_SPACESHIP_IMAGE, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP_IMAGE, (red.x, red.y))

    for bullets in red_bullets:
        pygame.draw.rect(WIN, RED, bullets)

    for bullets in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullets)

    pygame.display.update() # Ask Window to Update

def yellow_handle_movements(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and (yellow.x - VELOCITY > 0): # left
        yellow.x -= VELOCITY
    if keys_pressed[pygame.K_d] and (yellow.x + VELOCITY + yellow.width < BORDER.x): # right
        yellow.x += VELOCITY
    if keys_pressed[pygame.K_w] and (yellow.y - VELOCITY > 0): # up
        yellow.y -= VELOCITY
    if keys_pressed[pygame.K_s] and (yellow.y + VELOCITY + yellow.height < HEIGHT): # down
        yellow.y += VELOCITY

def red_handle_movements(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and (red.x - VELOCITY > BORDER.x + BORDER.width): # left
        red.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT] and (red.x + VELOCITY + red.width < WIDTH): # right
        red.x += VELOCITY
    if keys_pressed[pygame.K_UP] and (red.y - VELOCITY > 0): # up
        red.y -= VELOCITY
    if keys_pressed[pygame.K_DOWN] and (red.y + VELOCITY + red.height < HEIGHT): # down
        red.y += VELOCITY

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullets in yellow_bullets:
        bullets.x += BULLET_VEL
        if red.colliderect(bullets):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullets)
        elif bullets.x > WIDTH:
            yellow_bullets.remove(bullets)


    for bullets in red_bullets:
        bullets.x -= BULLET_VEL
        if yellow.colliderect(bullets):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullets)
        elif bullets.x < 0:
            red_bullets.remove(bullets)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1 , WHITE)
    WIN.blit(draw_text, (WIDTH / 2 - draw_text.get_width() /2 , HEIGHT / 2 - draw_text.get_height() / 2))
    
    pygame.display.update()
    pygame.time.delay(1000)

def main():
    red = pygame.Rect(700, 300, SPACESHIP_SCALE_X, SPACESHIP_SCALE_Y)
    yellow = pygame.Rect(100, 300, SPACESHIP_SCALE_X, SPACESHIP_SCALE_Y)
    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS) # Set Clock Tick to 60 times a Second 
        for event in pygame.event.get(): # Get event in pygame
            if event.type == pygame.QUIT: # If user quit pygame
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLET:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2 , 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLET:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2 , 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_test = ""

        if red_health <= 0:
            winner_test = "Yellow Wins!"

        if yellow_health <= 0:
            winner_test = "Red Wins!"

        if winner_test != "":
            draw_winner(winner_test) # Someone WON
            break

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movements(keys_pressed, yellow)
        red_handle_movements(keys_pressed, red)
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
    main()

if __name__ == "__main__":
    main()