import pygame
import random
import time

pygame.init()

# Screen setup
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
black = (0, 0, 0)

# Fonts
title_font = pygame.font.Font(None, 74)
score_font = pygame.font.Font(None, 36)

# Game assets
play_text = title_font.render("PLAY", True, black)
menu_play_button_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 100, 200, 60)
instructions_play_button_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 180, 200, 60)


# Game variables
ship_width = 50
ship_height = 30
ship_velocity = 4

plastic_width = plastic_height = 30
plastic_speed = 3

fish_width = fish_height = 30
fish_speed = 4


# Spawning probabilities per level
plastic_chance = {1: 0, 2: 1, 3: 3}
fish_chance = {1: 8, 2: 6, 3: 3}
clock = pygame.time.Clock()


def draw_menu():
    window.fill(white)
    title_text = title_font.render("Submarine Game", True, black)
    window.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 150))
    pygame.draw.rect(window, blue, menu_play_button_rect)
    play_text = title_font.render("PLAY", True, black)
    play_button_rect = pygame.Rect(screen_width // 2 - 100, (screen_height + 100) // 2 + 60, 200, 50)
    window.blit(play_text, (play_button_rect.centerx - play_text.get_width() // 2,
                            play_button_rect.centery - play_text.get_height() // 2))
    pygame.display.flip()

def draw_instructions():
    window.fill(white)
    institle_text = title_font.render("Instructions", True, black)
    window.blit(institle_text, (screen_width // 2 - institle_text.get_width() // 2, 50))
    
    lines = [
        "Use UP and DOWN arrow keys to move.",
        "Avoid plastic waste (red) — it reduces fuel.",
        "Catch fish (blue) — it gives you points!",
        "Catch as much fish as possible before fuel runs out!",
        "Click PLAY to begin!"
    ]
    for i, line in enumerate(lines):
        text = score_font.render(line, True, black)
        window.blit(text, (100, 150 + i * 40))
    
    pygame.draw.rect(window, blue, instructions_play_button_rect)
    window.blit(play_text, (instructions_play_button_rect.centerx - play_text.get_width() // 2,
                            instructions_play_button_rect.centery - play_text.get_height() // 2))
    pygame.display.flip()


def draw_game_over(score):
    window.fill(white)
    game_over_text = title_font.render("Game Over", True, black)
    score_text = score_font.render(f"Your Score: {score}", True, black)
    window.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, 150))
    window.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, 250))
    pygame.display.flip()
    pygame.time.wait(3000)

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

def load_high_score():
    try:
        with open("high_score.txt", 'r') as f:
            return int(f.read())
    except (FileNotFoundError, ValueError):
        return 0

def save_high_score(high_score):
    with open("high_score.txt", "w") as f:
        f.write(str(high_score))

def wait_for_play_click(button_rect):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return True
        clock.tick(60)

def draw_level_complete(level):
    window.fill(white)
    complete_text = title_font.render(f"Day {level} Complete!", True, black)
    next_day_text = score_font.render("Preparing for the next dive...", True, black)
    window.blit(complete_text, (screen_width // 2 - complete_text.get_width() // 2, 150))
    window.blit(next_day_text, (screen_width // 2 - next_day_text.get_width() // 2, 250))
    pygame.display.flip()
    pygame.time.wait(3000)

def run_game(level):
    total_fuel_time = 60
    ship_x = 50
    ship_y = screen_height // 2
    current_score = 0
    plastics = []
    fish_list = []

    high_score = load_high_score()
    start_time = time.time()
    running = True

    while running:
        window.fill(light_blue)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None  # Exit signal

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and ship_y > 0:
            ship_y -= ship_velocity
        if keys[pygame.K_DOWN] and ship_y + ship_height < screen_height:
            ship_y += ship_velocity

        ship_rect = pygame.Rect(ship_x, ship_y, ship_width, ship_height)
        pygame.draw.rect(window, brown, ship_rect)

        if random.randint(1, 100) <= plastic_chance.get(level, 0):
            plastics.append(spawn_plastic())
        for plastic in plastics[:]:
            plastic.x -= plastic_speed
            if ship_rect.colliderect(plastic):
                plastics.remove(plastic)
                total_fuel_time -= 3
            else:
                pygame.draw.rect(window, red, plastic)
        plastics = [p for p in plastics if p.x + plastic_width > 0]

        if random.randint(1, 200) <= fish_chance.get(level, 0):
            fish_list.append(spawn_fish())
        for fish in fish_list[:]:
            fish.x -= fish_speed
            if ship_rect.colliderect(fish):
                current_score += 1
                fish_list.remove(fish)
            else:
                pygame.draw.rect(window, blue, fish)
        fish_list = [f for f in fish_list if f.x + fish_width > 0]

        elapsed_time = time.time() - start_time
        fuel_left = max(0, 100 - int((elapsed_time / total_fuel_time) * 100))

        if fuel_left <= 0:
            if current_score > high_score:
                save_high_score(current_score)
            return current_score  # Level complete

        display_score(current_score, high_score, fuel_left)
        level_text = score_font.render("Day: " + str(level), True, white)
        window.blit(level_text, [screen_width - 200, 100])

        pygame.display.flip()
        clock.tick(100)

def run_all_levels():
    total_score = 0
    max_level = 3
    for level in range(1, max_level + 1):
        score = run_game(level)
        if score is None:
            return  # Quit early
        total_score += score
        if level < max_level:
            draw_level_complete(level)
        else:
            draw_game_over(total_score)


# Flow: Menu → Instructions → Game
draw_menu()
if wait_for_play_click(menu_play_button_rect):
    draw_instructions()
    if wait_for_play_click(instructions_play_button_rect):
        run_all_levels()
pygame.quit()



pygame.quit()
