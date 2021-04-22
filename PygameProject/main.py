#loading in the library
import pygame
pygame.font.init()
pygame.mixer.init()



#loading in the images:
RED_SPACESHIP_IMAGE = pygame.image.load("Assets/spaceship_red.png")
YELLOW_SPACESHIP_IMAGE = pygame.image.load("Assets/spaceship_yellow.png")
ICON = pygame.image.load("Assets/Battleplane.png")
SPACE = pygame.image.load("Assets/spacebackground.jpeg")


#making the width, height, caption, and icon of the game screen
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooters")
pygame.display.set_icon(ICON)



WHITE = (255, 255, 255)
BLACK = 0
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

HEALTH_FONT = pygame.font.SysFont("comicsans", 40)
WINNER_FONT = pygame.font.SysFont("comicsans", 100)

FPS = 60
VEL = 5
MAX_BULLETS = 3
BULLET_VEL = 10

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# BULLET_FIRE_SOUND = pygame.mixer.Sound("Assets/blasterSound.mp3")


#the height and width of the spaceships are being defined here
SSWIDTH, SSHEIGHT = 50, 50


#making the images the proper size
RED_SPACESHIP_IMAGE = pygame.transform.scale(RED_SPACESHIP_IMAGE, (SSWIDTH, SSHEIGHT))
YELLOW_SPACESHIP_IMAGE = pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SSWIDTH, SSHEIGHT))
SPACE = pygame.transform.scale(SPACE, (WIDTH, HEIGHT))

#rotating the images
RED_SPACESHIP_IMAGE = pygame.transform.rotate(RED_SPACESHIP_IMAGE, 270)
YELLOW_SPACESHIP_IMAGE = pygame.transform.rotate(YELLOW_SPACESHIP_IMAGE, 90)





#This function draws all you need to draw
#for example, the background colour, and the surfaces that I have made in the program
#It is also important for it to constantly do this, hence the .update method
def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))
    WIN.blit(YELLOW_SPACESHIP_IMAGE, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP_IMAGE, (red.x, red.y))

    
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


def moving_the_yellow_spaceship(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0 : #LEFT
            yellow.x -= VEL        
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x: #RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: #UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT: #DOWN
        yellow.y += VEL


def moving_the_red_spaceship(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: #LEFT
            red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL < WIDTH - red.width: #RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: #UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL < HEIGHT - red.height: #DOWN
        red.y += VEL


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        if bullet.x > WIDTH:
            yellow_bullets.remove(bullet)


    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        if bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():

    #considers the spaceships as rectangles
    red = pygame.Rect(700, 300, SSWIDTH, SSHEIGHT) 
    yellow = pygame.Rect(100, 300, SSWIDTH, SSHEIGHT) 

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    # BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    # BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                # BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                # BULLET_HIT_SOUND.play()


        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"
        
        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break
            


        keys_pressed = pygame.key.get_pressed()    


        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
        moving_the_yellow_spaceship(keys_pressed, yellow)
        moving_the_red_spaceship(keys_pressed, red)

    main()
    

if __name__ == "__main__":
    main()