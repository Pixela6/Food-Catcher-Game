import pygame
import random
import sys
import os

# Initialize pygame
pygame.init()

# Screen settings
WIDTH = 600
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Food Catcher: Fight Against Hunger")

# Clock
clock = pygame.time.Clock()
FPS = 60

# Font
font = pygame.font.SysFont(None, 40)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load images
def load_image(name, scale=None):
    image = pygame.image.load(os.path.join("assets", name)).convert_alpha()
    if scale:
        image = pygame.transform.scale(image, scale)
    return image

basket_img = load_image("basket.png", (80, 80))
heart_img = load_image("heart.png", (30, 30))

# Food categories
healthy_foods = [
    load_image("apple.png", (40, 40)),
    load_image("banana.png", (40, 40)),
    load_image("carrot.png", (40, 40)),
    load_image("mango.png", (40, 40))
]

junk_foods = [
    load_image("burger.png", (40, 40)),
    load_image("fries.png", (40, 40))
]

spoiled_foods = [
    load_image("rottenapple.png", (40, 40))
]

# Player settings
player_x = WIDTH // 2
player_y = HEIGHT - 100
player_speed = 7

# Food class
class Food:
    def __init__(self, img, type):
        self.img = img
        self.type = type
        self.x = random.randint(0, WIDTH - 40)
        self.y = -40
        self.speed = random.randint(4, 7)

    def move(self):
        self.y += self.speed

    def draw(self):
        screen.blit(self.img, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, 40, 40)

# Food generator
def get_random_food():
    category = random.choice(["healthy", "junk", "spoiled"])
    if category == "healthy":
        return Food(random.choice(healthy_foods), "healthy")
    elif category == "junk":
        return Food(random.choice(junk_foods), "junk")
    else:
        return Food(random.choice(spoiled_foods), "spoiled")

current_food = get_random_food()

# Score and lives
score = 0
lives = 3
import time
start_time = time.time()
game_duration = 60  # Game will last for 60 seconds

# Main game loop
running = True
while running:
    screen.fill(WHITE)
    elapsed_time = time.time() - start_time
    remaining_time = max(0, int(game_duration - elapsed_time))

    # End the game after time runs out
    if remaining_time == 0:
        game_over = True


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    player_x = max(0, min(WIDTH - 80, player_x))

    # Move and draw food
    current_food.move()
    current_food.draw()

    # Draw basket
    screen.blit(basket_img, (player_x, player_y))

    # Collision
    player_rect = pygame.Rect(player_x, player_y, 80, 80)
    if player_rect.colliderect(current_food.get_rect()):
        if current_food.type == "healthy":
            score += 1
        else:
            lives -= 1
        current_food = get_random_food()

    # Missed food logic
    if current_food.y > HEIGHT:
        current_food = get_random_food()

    # Draw score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (20, 20))

    # Draw hearts
    for i in range(lives):
        screen.blit(heart_img, (WIDTH - (i+1)*40, 20))
    timer_text = font.render(f"Time: {remaining_time}s", True, BLACK)
    screen.blit(timer_text, (10, 50))  # Adjust y if it overlaps with hearts

    # Game Over condition
    if lives <= 0:
        running = False

    pygame.display.flip()
    clock.tick(FPS)

# Game Over screen
screen.fill(WHITE)
game_over = font.render("Game Over!", True, BLACK)
final_score = font.render(f"Your Score: {score}", True, BLACK)
screen.blit(game_over, (WIDTH//2 - 100, HEIGHT//2 - 40))
screen.blit(final_score, (WIDTH//2 - 100, HEIGHT//2 + 10))
pygame.display.flip()
pygame.time.wait(3000)

pygame.quit()
sys.exit()
