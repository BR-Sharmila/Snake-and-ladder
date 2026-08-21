import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen
WIDTH = 900
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodge")

clock = pygame.time.Clock()
FPS = 60

# Colors
BLACK = (10, 10, 25)
WHITE = (255, 255, 255)
BLUE = (50, 150, 255)
CYAN = (50, 240, 255)
RED = (255, 70, 70)
YELLOW = (255, 220, 50)
GREEN = (70, 255, 120)
GRAY = (100, 100, 120)

# Fonts
title_font = pygame.font.Font(None, 80)
big_font = pygame.font.Font(None, 55)
font = pygame.font.Font(None, 32)


# -------------------------------------------------------
# PLAYER
# -------------------------------------------------------

class Player:

    def __init__(self):
        self.width = 50
        self.height = 60

        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - 100

        self.speed = 7

    def reset(self):
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - 100

    def update(self, keys):

        # Keyboard controls
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed

        # Keep player inside screen
        if self.x < 0:
            self.x = 0

        if self.x + self.width > WIDTH:
            self.x = WIDTH - self.width

        if self.y < 70:
            self.y = 70

        if self.y + self.height > HEIGHT:
            self.y = HEIGHT - self.height

    def get_rect(self):
        return pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height
        )

    def draw(self):

        # Spaceship
        points = [
            (self.x + self.width // 2, self.y),
            (self.x, self.y + self.height),
            (self.x + self.width // 2, self.y + 42),
            (self.x + self.width, self.y + self.height)
        ]

        pygame.draw.polygon(
            screen,
            CYAN,
            points
        )

        # Cockpit
        pygame.draw.circle(
            screen,
            WHITE,
            (
                self.x + self.width // 2,
                self.y + 25
            ),
            7
        )

        # Engine flames
        pygame.draw.polygon(
            screen,
            RED,
            [
                (self.x + 12, self.y + self.height),
                (self.x + 25, self.y + self.height),
                (self.x + 18, self.y + self.height + 15)
            ]
        )

        pygame.draw.polygon(
            screen,
            YELLOW,
            [
                (self.x + 25, self.y + self.height),
                (self.x + 38, self.y + self.height),
                (self.x + 31, self.y + self.height + 15)
            ]
        )


# -------------------------------------------------------
# ENEMY
# -------------------------------------------------------

class Enemy:

    def __init__(self, speed):

        self.size = random.randint(30, 55)

        self.x = random.randint(
            0,
            WIDTH - self.size
        )

        self.y = random.randint(
            -300,
            -50
        )

        self.speed = speed

    def update(self):
        self.y += self.speed

    def get_rect(self):
        return pygame.Rect(
            self.x,
            self.y,
            self.size,
            self.size
        )

    def draw(self):

        center_x = int(self.x + self.size / 2)
        center_y = int(self.y + self.size / 2)

        pygame.draw.circle(
            screen,
            RED,
            (center_x, center_y),
            self.size // 2
        )

        pygame.draw.circle(
            screen,
            YELLOW,
            (center_x, center_y),
            self.size // 5
        )


# -------------------------------------------------------
# COIN
# -------------------------------------------------------

class Coin:

    def __init__(self):

        self.radius = 12

        self.x = random.randint(
            20,
            WIDTH - 20
        )

        self.y = -30

        self.speed = 4

    def update(self):
        self.y += self.speed

    def get_rect(self):

        return pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )

    def draw(self):

        pygame.draw.circle(
            screen,
            YELLOW,
            (int(self.x), int(self.y)),
            self.radius
        )

        pygame.draw.circle(
            screen,
            WHITE,
            (int(self.x - 4), int(self.y - 4)),
            3
        )


# -------------------------------------------------------
# STAR BACKGROUND
# -------------------------------------------------------

stars = []

for i in range(100):

    stars.append([
        random.randint(0, WIDTH),
        random.randint(0, HEIGHT),
        random.randint(1, 3)
    ])


def draw_background():

    screen.fill(BLACK)

    for star in stars:

        pygame.draw.circle(
            screen,
            WHITE,
            (star[0], star[1]),
            star[2]
        )

        star[1] += star[2]

        if star[1] > HEIGHT:

            star[0] = random.randint(0, WIDTH)
            star[1] = 0


# -------------------------------------------------------
# TEXT
# -------------------------------------------------------

def draw_text(text, font_type, color, x, y):

    image = font_type.render(
        text,
        True,
        color
    )

    rectangle = image.get_rect(
        center=(x, y)
    )

    screen.blit(
        image,
        rectangle
    )


# -------------------------------------------------------
# GAME VARIABLES
# -------------------------------------------------------

player = Player()

enemies = []
coins = []

score = 0
level = 1
lives = 3

enemy_timer = 0
coin_timer = 0

game_state = "menu"


# -------------------------------------------------------
# RESET GAME
# -------------------------------------------------------

def reset_game():

    global score
    global level
    global lives
    global enemy_timer
    global coin_timer

    score = 0
    level = 1
    lives = 3

    enemy_timer = 0
    coin_timer = 0

    enemies.clear()
    coins.clear()

    player.reset()


# -------------------------------------------------------
# MENU
# -------------------------------------------------------

def draw_menu():

    draw_background()

    draw_text(
        "SPACE DODGE",
        title_font,
        CYAN,
        WIDTH // 2,
        150
    )

    draw_text(
        "Keyboard Game",
        big_font,
        WHITE,
        WIDTH // 2,
        220
    )

    # Start button
    pygame.draw.rect(
        screen,
        BLUE,
        (WIDTH // 2 - 150, 280, 300, 70),
        border_radius=15
    )

    draw_text(
        "PRESS ENTER",
        big_font,
        WHITE,
        WIDTH // 2,
        315
    )

    draw_text(
        "Arrow Keys / W A S D = Move",
        font,
        GRAY,
        WIDTH // 2,
        410
    )

    draw_text(
        "Avoid RED enemies",
        font,
        RED,
        WIDTH // 2,
        450
    )

    draw_text(
        "Collect YELLOW coins",
        font,
        YELLOW,
        WIDTH // 2,
        490
    )

    draw_text(
        "ESC = Quit",
        font,
        WHITE,
        WIDTH // 2,
        540
    )


# -------------------------------------------------------
# GAME OVER
# -------------------------------------------------------

def draw_game_over():

    draw_background()

    draw_text(
        "GAME OVER",
        title_font,
        RED,
        WIDTH // 2,
        180
    )

    draw_text(
        f"Your Score: {score}",
        big_font,
        WHITE,
        WIDTH // 2,
        280
    )

    pygame.draw.rect(
        screen,
        GREEN,
        (WIDTH // 2 - 170, 350, 340, 70),
        border_radius=15
    )

    draw_text(
        "PRESS R TO RESTART",
        font,
        BLACK,
        WIDTH // 2,
        385
    )

    draw_text(
        "Press ESC for Menu",
        font,
        WHITE,
        WIDTH // 2,
        470
    )


# -------------------------------------------------------
# MAIN GAME LOOP
# -------------------------------------------------------

running = True

while running:

    clock.tick(FPS)

    # ---------------------------------------------------
    # EVENTS
    # ---------------------------------------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        if event.type == pygame.KEYDOWN:

            # ESC
            if event.key == pygame.K_ESCAPE:

                if game_state == "playing":
                    game_state = "menu"

                elif game_state == "game_over":
                    game_state = "menu"

                else:
                    running = False

            # MENU
            if game_state == "menu":

                if event.key in (
                    pygame.K_RETURN,
                    pygame.K_SPACE
                ):

                    reset_game()
                    game_state = "playing"

            # GAME OVER
            elif game_state == "game_over":

                if event.key == pygame.K_r:

                    reset_game()
                    game_state = "playing"

    # ---------------------------------------------------
    # PLAYING
    # ---------------------------------------------------

    if game_state == "playing":

        keys = pygame.key.get_pressed()

        player.update(keys)

        # Enemy timer
        enemy_timer += 1

        enemy_delay = max(
            18,
            55 - level * 4
        )

        if enemy_timer >= enemy_delay:

            enemy_speed = 4 + level * 0.5

            enemies.append(
                Enemy(enemy_speed)
            )

            enemy_timer = 0

        # Coin timer
        coin_timer += 1

        if coin_timer >= 100:

            coins.append(
                Coin()
            )

            coin_timer = 0

        # Update enemies
        for enemy in enemies[:]:

            enemy.update()

            if enemy.y > HEIGHT:

                enemies.remove(enemy)

        # Update coins
        for coin in coins[:]:

            coin.update()

            if coin.y > HEIGHT:

                coins.remove(coin)

        # Enemy collision
        player_rect = player.get_rect()

        for enemy in enemies[:]:

            if player_rect.colliderect(
                enemy.get_rect()
            ):

                enemies.remove(enemy)

                lives -= 1

                if lives <= 0:

                    game_state = "game_over"

                break

        # Coin collision
        for coin in coins[:]:

            if player_rect.colliderect(
                coin.get_rect()
            ):

                coins.remove(coin)

                score += 25

        # Score
        score += 1

        # Level
        level = 1 + score // 500

    # ---------------------------------------------------
    # DRAW
    # ---------------------------------------------------

    if game_state == "menu":

        draw_menu()

    elif game_state == "playing":

        draw_background()

        # Draw coins
        for coin in coins:
            coin.draw()

        # Draw enemies
        for enemy in enemies:
            enemy.draw()

        # Draw player
        player.draw()

        # HUD

        pygame.draw.rect(
            screen,
            (15, 15, 40),
            (0, 0, WIDTH, 60)
        )

        draw_text(
            f"Score: {score}",
            font,
            WHITE,
            100,
            30
        )

        draw_text(
            f"Level: {level}",
            font,
            CYAN,
            300,
            30
        )

        draw_text(
            f"Lives: {lives}",
            font,
            RED,
            500,
            30
        )

        draw_text(
            "ESC: Menu",
            font,
            WHITE,
            750,
            30
        )

    elif game_state == "game_over":

        draw_game_over()

    # Update screen
    pygame.display.flip()


# -------------------------------------------------------
# EXIT
# -------------------------------------------------------

pygame.quit()
sys.exit()