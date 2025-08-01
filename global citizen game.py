import pygame
import random
import time

pygame.init()
pygame.font.init()
pygame.mixer.init() # Initialize the mixer for sound effects and music

# --- Screen Setup ---
screen_width = 900
screen_height = 506
window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Submarine Simulator")

# --- Colours ---
light_blue = (173, 216, 230)
brown = (102, 51, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)

# --- Fonts ---
cour = "assets/font/courier_new.ttf"
premier = "assets/font/premier2019.ttf"
title_font = pygame.font.Font(cour, 60)
score_font = pygame.font.Font(premier, 30)
context_font = pygame.font.Font(cour, 22)
small_font = pygame.font.Font(cour, 18)

# --- Images ---
# Menu Backgrounds
menubg_image = pygame.image.load('assets/img/menubg.png')
menubg = pygame.transform.smoothscale(menubg_image, (screen_width, screen_height))
introbg_image = pygame.image.load('assets/img/introbg.png')
introbg = pygame.transform.smoothscale(introbg_image, (screen_width, screen_height))

# Game Backgrounds
bg_image = pygame.image.load('assets/img/bg.png')
bg = pygame.transform.smoothscale(bg_image, (screen_width, screen_height))
bg_image2 = pygame.image.load('assets/img/bg2.png')
bg2 = pygame.transform.smoothscale(bg_image2, (screen_width, screen_height))
bg_image3 = pygame.image.load('assets/img/bg3.png')
bg3 = pygame.transform.smoothscale(bg_image3, (screen_width, screen_height))

# Tutorial Image
tutorial_image_raw = pygame.image.load('assets/img/tutorial.png')
tutorial_image = pygame.transform.smoothscale(tutorial_image_raw, (screen_width, screen_height))

# Buttons
playbtn_image = pygame.image.load("assets/img/playbutton.png").convert_alpha()
playbtn_hover_image = pygame.image.load("assets/img/playbutton_hover.png").convert_alpha()
readybtn_image = pygame.image.load("assets/img/readybutton.png").convert_alpha()
readybtn_hover_image = pygame.image.load("assets/img/readybutton_hover.png").convert_alpha()

# Button Dimensions
playbtn_width = 250
playbtn_height = 80
readybtn_width = 230
readybtn_height = 80

# Scaled Buttons
playbtn = pygame.transform.smoothscale(playbtn_image, (playbtn_width, playbtn_height))
playbtn_hover = pygame.transform.smoothscale(playbtn_hover_image, (playbtn_width, playbtn_height))
readybtn = pygame.transform.smoothscale(readybtn_image, (readybtn_width, readybtn_height))
readybtn_hover = pygame.transform.smoothscale(readybtn_hover_image, (readybtn_width, readybtn_height))

# Button Rectangles
play_button_rect = pygame.Rect(screen_width // 2 - playbtn_width // 2, screen_height // 2 + 50, playbtn_width, playbtn_height)
ready_button_rect = pygame.Rect(screen_width - readybtn_width - 30, screen_height - readybtn_height - 30, readybtn_width, readybtn_height)

# Score Panel
score_panel_image = pygame.image.load("assets/img/score_panel.png").convert_alpha()
score_panel_width = 220
score_panel_height = 110
scaled_score_panel = pygame.transform.smoothscale(score_panel_image, (score_panel_width, score_panel_height))

# Submarine
sub_image_raw = pygame.image.load("assets/img/submarine.png").convert_alpha()
submarine_image = pygame.transform.smoothscale(sub_image_raw, [150, 150]) # Scaled once

# Fish Images
fish_width = 85
fish_height = 60
fish_images = [
    pygame.image.load("assets/img/fish/f1.png").convert_alpha(),
    pygame.image.load("assets/img/fish/f2.png").convert_alpha(),
    pygame.image.load("assets/img/fish/f3.png").convert_alpha(),
    pygame.image.load("assets/img/fish/f4.png").convert_alpha(),
    pygame.image.load("assets/img/fish/f5.png").convert_alpha(),
    pygame.image.load("assets/img/fish/f6.png").convert_alpha(),
    pygame.image.load("assets/img/fish/f7.png").convert_alpha(),
    pygame.image.load("assets/img/fish/f8.png").convert_alpha(),
]
scaled_fish_images = [pygame.transform.smoothscale(img, (fish_width, fish_height)) for img in fish_images]

# Rubbish Images (Plastics)
plastic_width = 80
plastic_height = 65
plastic_images = [
    pygame.image.load("assets/img/rubbish/p1.png").convert_alpha(),
    pygame.image.load("assets/img/rubbish/p2.png").convert_alpha(),
    pygame.image.load("assets/img/rubbish/p3.png").convert_alpha(),
    pygame.image.load("assets/img/rubbish/p4.png").convert_alpha(),
]
scaled_plastic_images = [pygame.transform.smoothscale(img, (plastic_width, plastic_height)) for img in plastic_images]

# --- Sound Effects & Music ---
# BGM 
# Note: For continuous looping BGM, it's often better to use pygame.mixer.music
# menubgm = pygame.mixer.Sound("assets/sound/bgm/menu.mp3")
# lv1bgm = pygame.mixer.Sound("assets/sound/bgm/lv1.mp3")
# lv2bgm = pygame.mixer.Sound("assets/sound/bgm/lv2.mp3")
# lv3bgm = pygame.mixer.Sound("assets/sound/bgm/lv3.mp3")

# SFX
btn_sound = pygame.mixer.Sound("assets/sound/sound_effect/button.mp3")
collect_sound = pygame.mixer.Sound("assets/sound/sound_effect/collect.wav")


# --- Game Variables ---
ship_width = 60 
ship_height = 40 
ship_velocity = 7

plastic_speed = 5
fish_speed = 6

# Spawning probabilities per level (out of 100 for plastic, out of 200 for fish)
plastic_chance = {1: 0, 2: 1, 3: 3}
fish_chance = {1: 8, 2: 6, 3: 3} # For fish, probability is checked against 200

clock = pygame.time.Clock()

intro_dialogue = [
    "Ahoy, explorer! Welcome aboard.",
    "You're on a mission to study the ocean's wonders.",
    "Your goal is to collect fish data using the submarine.",
    "But keep your eyes open. The ocean is always changing...",
]

# --- Functions ---

def typewriter_text(surface, text, font, colour, x, y, speed=5):
    displayed_text = ''
    last_update = pygame.time.get_ticks()
    index = 0

    while index < len(text):
        current_time = pygame.time.get_ticks()
        if current_time - last_update >= speed:
            displayed_text += text[index]
            index += 1
            last_update = current_time

        draw_story_screen_background(surface) # Redraw background
        text_surface = font.render(displayed_text, True, colour)
        surface.blit(text_surface, (x, y))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

def draw_menu():
    window.blit(menubg, (0, 0))
    mouse_pos = pygame.mouse.get_pos()

    # Play menu BGM if not already playing
    # Using pygame.mixer.music for continuous background music
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load("assets/sound/bgm/menu.mp3")
        pygame.mixer.music.play(-1) # Loop indefinitely

    if play_button_rect.collidepoint(mouse_pos):
        window.blit(playbtn_hover, play_button_rect.topleft)
    else:
        window.blit(playbtn, play_button_rect.topleft)

    pygame.display.flip()

def draw_story_screen_background(surface):
    surface.fill(black)
    surface.blit(introbg, (0, 0))
    captain_img = pygame.image.load("assets/img/captain.png").convert_alpha()
    captain_scaled = pygame.transform.smoothscale(captain_img, (180, 250))
    surface.blit(captain_scaled, (screen_width - 280, screen_height - 300))

    pygame.draw.rect(surface, black, (50, screen_height - 120, screen_width - 100, 80))
    pygame.draw.rect(surface, white, (50, screen_height - 120, screen_width - 100, 80), 2)

def run_intro_dialogue(dialogues):
    for line in dialogues:
        typewriter_text(window, line, context_font, white, 60, screen_height - 100)
        continue_text = small_font.render("(Press any key to continue)", True, white)
        window.blit(continue_text, (screen_width - continue_text.get_width() - 70, screen_height - 65))
        pygame.display.update()
        wait_for_key_press()

def wait_for_key_press():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

def draw_tutorial():
    window.blit(tutorial_image, (0, 0))
    mouse_pos = pygame.mouse.get_pos()

    if ready_button_rect.collidepoint(mouse_pos):
        window.blit(readybtn_hover, ready_button_rect.topleft)
    else:
        window.blit(readybtn, ready_button_rect.topleft)
    pygame.display.flip()

def draw_game_over(score):
    pygame.mixer.music.stop() # Stop any background music
    window.fill(white)
    game_over_text = title_font.render("Game Over", True, black)
    score_text = score_font.render(f"Your Score: {score}", True, black)
    window.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, 150))
    window.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, 250))
    pygame.display.flip()
    pygame.time.wait(3000)

def display_score(score, high_score, fuel_percent):
    panel_x = screen_width - scaled_score_panel.get_width() - 10
    panel_y = 10
    window.blit(scaled_score_panel, (panel_x, panel_y))
    score_text = score_font.render("Score      " + str(score), True, white)
    high_score_text = score_font.render("Best Score " + str(high_score), True, white)
    fuel_text = score_font.render("Fuel       " + str(int(fuel_percent)) + "%", True, white)
    window.blit(score_text, [screen_width - 200, 14])
    window.blit(high_score_text, [screen_width - 200, 44])
    window.blit(fuel_text, [screen_width - 200, 74])

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

def wait_for_button_click(button_rect, screen_drawing_function):
    waiting = True
    while waiting:
        screen_drawing_function()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    pygame.mixer.Sound.play(btn_sound)
                    waiting = False
        clock.tick(60)
    return True

def draw_level_complete(level):
    pygame.mixer.music.stop() # Stop current level BGM
    window.fill(white)
    complete_text = title_font.render(f"Day {level} Complete!", True, black)
    next_day_text = score_font.render("Preparing for the next dive...", True, black)
    window.blit(complete_text, (screen_width // 2 - complete_text.get_width() // 2, 150))
    window.blit(next_day_text, (screen_width // 2 - next_day_text.get_width() // 2, 250))
    pygame.display.flip()
    pygame.time.wait(3000)

def run_game(level):
    pygame.mixer.music.stop() # Stop any previous BGM (e.g., menu music)

    # Load and play BGM for the current level
    if level == 1:
        pygame.mixer.music.load("assets/sound/bgm/lv1.mp3")
    elif level == 2:
        pygame.mixer.music.load("assets/sound/bgm/lv2.mp3")
    elif level == 3:
        pygame.mixer.music.load("assets/sound/bgm/lv3.mp3")
    pygame.mixer.music.play(-1) # Loop indefinitely

    total_fuel_time = 40
    ship_x = 50
    ship_y = screen_height // 2
    current_score = 0
    plastics = []
    fish_list = []

    high_score = load_high_score()
    start_time = time.time()
    running = True

    while running:
        # Draw background based on level
        if level == 1:
            window.blit(bg, (0, 0))
        elif level == 2:
            window.blit(bg2, (0, 0))
        elif level == 3:
            window.blit(bg3, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None

        # Submarine Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if ship_y > -50 :
                ship_y -= ship_velocity
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if ship_y + ship_height < screen_height - 60:
                ship_y += ship_velocity
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if ship_x > 0:
                ship_x -= ship_velocity
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if ship_x + ship_width < screen_width // 3:
                ship_x += ship_velocity

        # Draw submarine (using the pre-scaled image)
        window.blit(submarine_image, (ship_x, ship_y))

        # Ship hitbox for collisions
        ship_hitbox = pygame.Rect(ship_x + 20, ship_y + 45, 110, 60)
        # pygame.draw.rect(window, (0, 255, 0), ship_hitbox, 2) # Debug outline

        # Plastic spawning and collision
        if random.randint(1, 100) <= plastic_chance.get(level, 0):
            plastics.append((spawn_plastic(), random.choice(scaled_plastic_images)))

        # Move plastics and check for collisions
        for i, (plastic_rect, plastic_img) in enumerate(plastics[:]):
            plastic_rect.x -= plastic_speed
            window.blit(plastic_img, plastic_rect.topleft)
            if ship_hitbox.colliderect(plastic_rect):
                total_fuel_time -= 3
                plastics.pop(i)
        plastics = [(r, img) for (r, img) in plastics if r.x + plastic_width > 0] # Remove off-screen plastics

        # Fish spawning and collision
        if random.randint(1, 200) <= fish_chance.get(level, 0):
            fish_list.append((spawn_fish(), random.choice(scaled_fish_images)))

        for i, (fish_rect, fish_img) in enumerate(fish_list[:]):
            fish_rect.x -= fish_speed
            window.blit(fish_img, fish_rect.topleft)
            if ship_hitbox.colliderect(fish_rect):
                pygame.mixer.Sound.play(collect_sound)
                current_score += 1
                fish_list.pop(i)
        fish_list = [f for f in fish_list if f[0].x + fish_width > 0] # Remove off-screen fish

        # Fuel calculations
        elapsed_time = time.time() - start_time
        fuel_left = max(0, 100 - int((elapsed_time / total_fuel_time) * 100))

        if fuel_left <= 0:
            pygame.mixer.music.stop() # Stop BGM when fuel runs out
            if current_score > high_score:
                save_high_score(current_score)
            return current_score

        # Player Stats Display
        display_score(current_score, high_score, fuel_left)
        level_text = score_font.render("Day " + str(level), True, white)
        window.blit(level_text, [screen_width//2 - 50, 50])

        pygame.display.flip()
        clock.tick(60) # Limit to 60 FPS

def run_all_levels():
    total_score = 0
    max_level = 3
    for level in range(1, max_level + 1):
        score = run_game(level)
        if score is None: # Game quit during a level
            return
        total_score += score
        if level < max_level:
            draw_level_complete(level)
        else:
            draw_game_over(total_score)


# --- Main Game Loop / Flow ---
game_state = "menu"

while True:
    if game_state == "menu":
        draw_menu()
        if wait_for_button_click(play_button_rect, draw_menu):
            game_state = "intro"
        else:
            break
    elif game_state == "intro":
        pygame.mixer.music.stop() # Stop menu music before intro
        run_intro_dialogue(intro_dialogue)
        game_state = "tutorial"
    elif game_state == "tutorial":
        draw_tutorial()
        if wait_for_button_click(ready_button_rect, draw_tutorial):
            game_state = "game"
        else:
            break
    elif game_state == "game":
        run_all_levels()
        game_state = "quit"
    elif game_state == "quit":
        break

pygame.quit()