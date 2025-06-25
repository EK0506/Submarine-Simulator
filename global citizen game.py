"""Version 1 only contain the core game mechanics, including
Player control, spawning of fish and plastics, score and fuel display"""
import pygame
import random
import time
pygame.init()

# Set screen size
screen_width = 800
screen_height = 500
window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Submarine Simulator")

# Colours
light_blue = (173, 216, 230)
brown = (102, 51, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
white = (255, 255, 255)

# Fonts and timing
score_font = pygame.font.Font(None, 36)

# Score amd fuel variables
total_fuel_time = 60
current_score = 0
high_score = 0  # 60 seconds of total run time

# Ship properties
ship_width = 50
ship_height = 30
ship_x = 50
ship_y = screen_height // 2
ship_velocity = 4

# Plastics properties
plastic_width = plastic_height = 30
plastic_speed = 3
#Fish properties
fish_width = fish_height = 30
fish_speed = 4


def load_high_score():
    try:
        with open("high_score.txt", 'r') as f:
            return int(f.read())
    except (FileNotFoundError, ValueError):
        return 0

def save_high_score(high_score):
    with open("high_score.txt", "w") as f:
        f.write(str(high_score))

def display_score(score, high_score, fuel_percent):
    score_text = score_font.render("Score: " + str(score), True, white)
    high_score_text = score_font.render("High Score: " + str(high_score), True, white)
    fuel_text = score_font.render("Fuel: " + str(int(fuel_percent)) + "%", True, white)
    window.blit(score_text, [screen_width - 200, 10])
    window.blit(high_score_text, [screen_width - 200, 40])
    window.blit(fuel_text, [screen_width - 200, 70])

def spawn_plastic():
    x = screen_width
    y = random.randint(0, screen_height - plastic_height)
    return pygame.Rect(x, y, plastic_width, plastic_height)

def spawn_fish():
    x = screen_width
    y = random.randint(0, screen_height - fish_height)
    return pygame.Rect(x, y, fish_width, fish_height)

running = True
clock = pygame.time.Clock()
plastics = []
fish_list = []
high_score = load_high_score()
start_time = time.time()

while running:
    window.fill(light_blue)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and ship_y > 0:
        ship_y -= ship_velocity
    if keys[pygame.K_DOWN] and ship_y + ship_height < screen_height:
        ship_y += ship_velocity

    ship_rect = pygame.Rect(ship_x, ship_y, ship_width, ship_height)
    pygame.draw.rect(window, brown, ship_rect)

    # Spawn and move plastic
    if random.randint(1, 100) == 1:
        plastics.append(spawn_plastic())

    for plastic in plastics[:]:
        plastic.x -= plastic_speed
        if ship_rect.colliderect(plastic):
            plastics.remove(plastic)
            total_fuel_time -= 3  # Lose 3 seconds of total run time (~5% fuel)
        else:
            pygame.draw.rect(window, red, plastic)

    plastics = [p for p in plastics if p.x + plastic_width > 0]

    # Spawn and move fish
    if random.randint(1, 80) == 1:
        fish_list.append(spawn_fish())

    for fish in fish_list[:]:
        fish.x -= fish_speed
        if ship_rect.colliderect(fish):
            current_score += 1
            fish_list.remove(fish)
        else:
            pygame.draw.rect(window, blue, fish)
    #Remove fish when out of the screen
    fish_list = [f for f in fish_list if f.x + fish_width > 0]

    # Calculate fuel percentage
    elapsed_time = time.time() - start_time
    fuel_left = max(0, 100 - int((elapsed_time / total_fuel_time) * 100))
    if fuel_left <= 0:  # End game when fuel runs out
        fuel_left = 0
        running = False  
    #Update high score to file if current score is higher
    if current_score > high_score:
        high_score = current_score
        save_high_score(high_score)

    #Display current score, high score and fuel left on top right
    display_score(current_score, high_score, fuel_left)

    pygame.display.flip()
    clock.tick(100)

pygame.quit()
