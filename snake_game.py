import pygame
import random
import sys
import os

# Initialize Pygame
pygame.init()

# Constants
TILE_SIZE = 20
GRID_SIZE = 20
WIDTH = HEIGHT = TILE_SIZE * GRID_SIZE
FPS = 10

# Colors
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
RED = (220, 20, 60)
BLACK = (0, 0, 0)
YELLOW = (255, 215, 0)
BLUE = (30, 144, 255)

# Set up screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🐍 Snake Game - CSC221 Final Project")

# Fonts
font = pygame.font.SysFont('consolas', 24)
big_font = pygame.font.SysFont('consolas', 40)

# Clock
clock = pygame.time.Clock()

# Sound setup (optional)
pygame.mixer.init()
eat_sound = pygame.mixer.Sound(pygame.mixer.SoundType)
try:
    eat_sound = pygame.mixer.Sound(pygame.mixer.Sound(os.path.join('eat.wav')))
except:
    eat_sound = None

def draw_text(text, color, x, y, center=True, size='small'):
    if size == 'large':
        surface = big_font.render(text, True, color)
    else:
        surface = font.render(text, True, color)
    rect = surface.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(surface, rect)

def draw_snake(snake):
    for i, segment in enumerate(snake):
        color = GREEN if i == 0 else BLUE
        pygame.draw.rect(screen, color, (*segment, TILE_SIZE, TILE_SIZE))

def draw_food(position):
    pygame.draw.rect(screen, RED, (*position, TILE_SIZE, TILE_SIZE))

def generate_food(snake):
    while True:
        x = random.randint(0, GRID_SIZE - 1) * TILE_SIZE
        y = random.randint(0, GRID_SIZE - 1) * TILE_SIZE
        if (x, y) not in snake:
            return (x, y)

def welcome_screen():
    screen.fill(BLACK)
    draw_text("Welcome to Snake Game", YELLOW, WIDTH // 2, HEIGHT // 3, size='large')
    draw_text("Use Arrow Keys to Move", WHITE, WIDTH // 2, HEIGHT // 2)
    draw_text("Press ENTER to Start", WHITE, WIDTH // 2, HEIGHT // 2 + 40)
    draw_text("Press Q to Quit", WHITE, WIDTH // 2, HEIGHT // 2 + 80)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def show_game_over(score, high_score):
    screen.fill(BLACK)
    draw_text("Game Over", RED, WIDTH // 2, HEIGHT // 3, size='large')
    draw_text(f"Your Score: {score}", WHITE, WIDTH // 2, HEIGHT // 2)
    draw_text(f"High Score: {high_score}", YELLOW, WIDTH // 2, HEIGHT // 2 + 40)
    draw_text("Press R to Restart or Q to Quit", WHITE, WIDTH // 2, HEIGHT // 1.5)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def draw_grid():
    for x in range(0, WIDTH, TILE_SIZE):
        pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, TILE_SIZE):
        pygame.draw.line(screen, (40, 40, 40), (0, y), (WIDTH, y))

def game_loop():
    snake = [(100, 100), (80, 100), (60, 100)]
    direction = (TILE_SIZE, 0)
    food = generate_food(snake)
    score = 0
    high_score = 0

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Controls
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, TILE_SIZE):
                    direction = (0, -TILE_SIZE)
                elif event.key == pygame.K_DOWN and direction != (0, -TILE_SIZE):
                    direction = (0, TILE_SIZE)
                elif event.key == pygame.K_LEFT and direction != (TILE_SIZE, 0):
                    direction = (-TILE_SIZE, 0)
                elif event.key == pygame.K_RIGHT and direction != (-TILE_SIZE, 0):
                    direction = (TILE_SIZE, 0)

        # Update snake position
        head_x, head_y = snake[0]
        new_head = (head_x + direction[0], head_y + direction[1])

        # Collision with walls
        if (
            new_head[0] < 0 or new_head[0] >= WIDTH or
            new_head[1] < 0 or new_head[1] >= HEIGHT
        ):
            break

        # Collision with self
        if new_head in snake:
            break

        snake.insert(0, new_head)

        # Eating food
        if new_head == food:
            score += 1
            food = generate_food(snake)
            if eat_sound:
                eat_sound.play()
        else:
            snake.pop()

        # Drawing
        screen.fill(BLACK)
        draw_grid()
        draw_food(food)
        draw_snake(snake)
        draw_text(f"Score: {score}", WHITE, 10, 10, center=False)

        pygame.display.flip()

    high_score = max(score, high_score)
    return score, high_score

# Main game execution
if __name__ == "__main__":
    while True:
        welcome_screen()
        score, high_score = game_loop()
        restart = show_game_over(score, high_score)
        if not restart:
            break
