import pygame 
import os 
import random 
import math 
from os import listdir
from os.path import isfile, join

pygame.init()

pygame.display.set_caption("SODAS") # title for the screen

# Dimensions of the window including player's abilities and frames the game is playing at
width = 800
height = 600
FPS = 60
Player_VEL = 5
GROUND_LEVEL = height - 10
JUMP_VEL = -10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

window = pygame.display.set_mode((width, height))


#Obstacle
class Obstacle(pygame.sprite.Sprite):
    COLOR = BLUE  # Blue color for obstacles

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, win, offset_x):
        adjusted_rect = self.rect.copy()
        adjusted_rect.x -= offset_x
        pygame.draw.rect(win, self.COLOR, adjusted_rect)

        

    
# Fonts 
TITLE_FONT = pygame.font.SysFont('comicsans', 70) 
BUTTON_FONT = pygame.font.SysFont('comicsans', 50)
msg_FONT = pygame.font.SysFont('comicsans', 20)

# Player
class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    GRAVITY = 1

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.is_jumping = False

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.y_vel = JUMP_VEL
            self.fall_count = 0

    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)

        if self.rect.bottom >= GROUND_LEVEL:
            self.rect.bottom = GROUND_LEVEL
            self.y_vel = 0
            self.fall_count = 0
            self.is_jumping = False

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > GROUND_LEVEL:
            self.rect.bottom = GROUND_LEVEL

        self.fall_count += 1

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, self.rect)


#Enemy 
class Enemy(pygame.sprite.Sprite):
    COLOR = (GREEN)
    GRAVITY = 1

    def __init__(self, x, y, width, height,): #initialising the enemy 
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.move_timer = 0

    def move(self, dx, dy): #movement x and y position
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self, vel): #movement left 
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel): #movement right
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    
    
    def random_move(self):
        if self.move_timer <= 0:
            directions = ['left', 'right', 'up', 'down']
            direction = random.choice(directions)
            if direction == 'left':
                self.move_left(random.randint(1, 5))
            elif direction == 'right':
                self.move_right(random.randint(1, 5))
            
            self.move_timer = random.randint(30, 60)
        else:
            self.move_timer -= 1

    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)
        self.random_move()

        if self.rect.bottom >= GROUND_LEVEL:
            self.rect.bottom = GROUND_LEVEL
            self.y_vel = 0
            self.fall_count = 0
            
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > GROUND_LEVEL:
            self.rect.bottom = GROUND_LEVEL

        self.fall_count += 1

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, self.rect)


    


# Background and creating the tiles for game
def get_background(name):
    image = pygame.image.load(join("Assets", "Background", name))
    image = pygame.transform.scale(image, (800, 600))
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(width // width + 1):
        for x in range(height // height + 1):
            pos = (i * width, x * height)
            tiles.append(pos)
    
    return tiles, image

# Drawing everything on window
def draw(window, background, bg_image, player, offset_x, obstacles, enemies):
    for tile in background:
        adjusted_tile = (tile[0] - offset_x, tile[1])
        window.blit(bg_image, adjusted_tile)

    player.draw(window)

    pygame.draw.rect(window, RED, player.rect, 2)
    

    for obstacle in obstacles:
        obstacle.draw(window, offset_x)
       #pygame.draw.rect(window, BLUE, obstacle.rect, 2)


    for enemy in enemies:
        enemy.draw(window)
        pygame.draw.rect(window, GREEN, enemy.rect, 2)
    

    pygame.draw.rect(window, (139, 69, 19), (0, GROUND_LEVEL, width, height - GROUND_LEVEL))

    pygame.display.update()

# Handling player movements
def handle_move(player, offset_x):
    keys = pygame.key.get_pressed()
    player.x_vel = 0
    if keys[pygame.K_a]: #move left
        player.move_left(Player_VEL)
        offset_x -= Player_VEL  
    if keys[pygame.K_d]: #move right
        player.move_right(Player_VEL)
        offset_x += Player_VEL  
    if keys[pygame.K_SPACE]: #jump
        player.jump()
    return offset_x

def check_collision1(player, obstacles, enemies):
    for obstacle in obstacles:
        if player.rect.colliderect(obstacle.rect):
            # Handle collision with the top of the obstacle
            if player.y_vel > 0 and player.rect.bottom <= obstacle.rect.top + player.y_vel:
                player.rect.bottom = obstacle.rect.top
                player.y_vel = 0
                player.is_jumping = False
             # Handle collision from the bottom (e.g., jumping into the obstacle)
            elif player.y_vel < 0 and player.rect.top >= obstacle.rect.bottom - abs(player.y_vel):
                player.rect.top = obstacle.rect.bottom
                player.y_vel = 0
            # Handle collision from the left
            elif player.x_vel > 0 and player.rect.right >= obstacle.rect.left:
                player.rect.right = obstacle.rect.left
                player.x_vel = 0
            # Handle collision from the right
            elif player.x_vel < 0 and player.rect.left <= obstacle.rect.right:
                player.rect.left = obstacle.rect.right
                player.x_vel = 0

    # Check collision with enemies
    for enemy in enemies:
        if player.rect.colliderect(enemy.rect):
            gameover()
        
        for enemy in enemies:
            if player.rect.colliderect(enemy.rect):
                gameover()


#main menu for the game
def menu():
    run = True
    while run: 
        window.fill(WHITE)
        title_text = TITLE_FONT.render('SODAS', 1, BLACK)
        start_button = BUTTON_FONT.render('Start World', 1, GREEN)
        settings_button = BUTTON_FONT.render('SETTINGS', 1, GREEN)
        exit_button = BUTTON_FONT.render('EXIT', 1, RED)

        start_button_rect = pygame.Rect(width // 2 - start_button.get_width() // 2, 250, start_button.get_width(), start_button.get_height())
        settings_button_rect = pygame.Rect(width // 2 - settings_button.get_width() // 2, 350, settings_button.get_width(), settings_button.get_height())
        exit_button_rect = pygame.Rect(width // 2 - exit_button.get_width() // 2, 450, exit_button.get_width(), exit_button.get_height())

        window.blit(title_text, (width // 2 - title_text.get_width() // 2, 100))
        window.blit(start_button, (width // 2 - start_button.get_width() // 2, 250))
        window.blit(settings_button, (width // 2 - settings_button.get_width() // 2, 350))
        window.blit(exit_button, (width // 2 - exit_button.get_width() // 2, 450))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if start_button_rect.collidepoint(mouse_x, mouse_y):
                    main(window)
                if settings_button_rect.collidepoint(mouse_x, mouse_y):
                    Settings()
                if exit_button_rect.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    quit()

#display screen for the game over        
def gameover():
    # Display the game over screen
    window.fill(WHITE)
    Gameover_text1 = TITLE_FONT.render('GAME OVER', 1, BLACK)
    restart_text = BUTTON_FONT.render('Press R to Restart', 1, GREEN)
    quit_text = BUTTON_FONT.render('Press Q to Quit', 1, RED)

    window.blit(Gameover_text1, (width // 2 - Gameover_text1.get_width() // 2, 100))
    window.blit(restart_text, (width // 2 - restart_text.get_width() // 2, 300))
    window.blit(quit_text, (width // 2 - quit_text.get_width() // 2, 400))

    pygame.display.update()

    # Wait for user input to restart or quit
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_r:
                    main(window)  # Restart the game


def Settings():
    # Display the game over screen
    window.fill(WHITE)
    Howitworks_text1 = msg_FONT.render('How does this Game work: left = A key, right = D key , jump = space Bar', 1, BLACK)
    menu_text = BUTTON_FONT.render('Press m to go to menu', 1, BLACK)


    window.blit(Howitworks_text1, (width // 2 - Howitworks_text1.get_width() // 2, 200))
    window.blit(menu_text, (width // 2 - menu_text.get_width() // 2, 300))
   

    pygame.display.update()

    # Wait for user input to restart or quit
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    menu()
                elif event.key == pygame.K_r:
                    main(window)  # Restart the game

    

def main(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("Yellow.png")
    player = Player(50, 50, 25, 25)
    offset_x = 0

    enemies = [
        Enemy(200, GROUND_LEVEL - 25, 25, 25),  # Enemy 1 at a different position
        Enemy(400, GROUND_LEVEL - 25, 25, 25),  # Enemy 2
        Enemy(600, GROUND_LEVEL - 25, 25, 25),  # Enemy 3
    ]
    obstacles = [
        Obstacle(200, GROUND_LEVEL - 50, 100, 20),
        Obstacle(400, GROUND_LEVEL - 100, 100, 20),
        Obstacle(600, GROUND_LEVEL - 150, 100, 20)
    ]

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        offset_x = handle_move(player, offset_x)
        player.loop(FPS)

        check_collision1(player, obstacles, enemies)

        for enemy in enemies:
            enemy.loop(60)
            enemy.draw(window)
    


        draw(window, background, bg_image, player, offset_x, obstacles, enemies )
    
    pygame.quit() 
    quit()

if __name__ == "__main__":
    menu()
