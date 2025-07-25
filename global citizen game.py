import pygame
import random
import time

pygame.init()

# Screen setup
screen_width = 900
screen_height = 506
window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Submarine Simulator")
menubg_image = pygame.image.load('menubg.png')
menubg = pygame.transform.smoothscale(menubg_image, (screen_width, screen_height))
bg_image = pygame.image.load('bg.png') # Load background image
bg = pygame.transform.smoothscale(bg_image, (screen_width, screen_height)) # Scale background image to fit screen sizeresize background image to fit screen size
playbtn_image = pygame.image.load("playbutton.png").convert_alpha()
playbtn = pygame.transform.smoothscale(playbtn_image, (250, 80))  # Match original button size
playbtnhover_image = pygame.image.load("playbutton_hover.png").convert_alpha()
playbtn_hover = pygame.transform.smoothscale(playbtnhover_image, (250, 80))  
 
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
# Adjusted button rects to match the scaled image size
menu_play_button_rect = pygame.Rect(screen_width // 2 - 170, screen_height // 2 - 20 + 70, 250, 80) 
instructions_play_button_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 180, 200, 60)

# Game variables
ship_width = 60
ship_height = 40
ship_velocity = 10

plastic_width = 65
plastic_height = 65
plastic_speed = 5

fish_width = 90
fish_height = 60
fish_speed = 7

#Fish Image
fish_images = [
    pygame.image.load("f1.png").convert_alpha(),
    pygame.image.load("f2.png").convert_alpha(),
    pygame.image.load("f3.png").convert_alpha(),
    pygame.image.load("f4.png").convert_alpha(),    
    pygame.image.load("f5.png").convert_alpha(),    
    pygame.image.load("f6.png").convert_alpha(),    
]

#Resize fish images
scaled_fish_images = [pygame.transform.smoothscale(img, (fish_width, fish_height)) for img in fish_images]

#Rubbish Image
plastic_image = [
    pygame.image.load("p1.png").convert_alpha(),
    pygame.image.load("p2.png").convert_alpha(),
    pygame.image.load("p3.png").convert_alpha(),
    pygame.image.load("p4.png").convert_alpha(),      
]

scaled_plastic_images = [pygame.transform.smoothscale(img, (plastic_width, plastic_height)) for img in plastic_image]


# Spawning probabilities per level
plastic_chance = {1: 0, 2: 1, 3: 3}
fish_chance = {1: 8, 2: 6, 3: 3}
clock = pygame.time.Clock()

def draw_menu():
    window.blit(menubg, (0, 0))  # Background
    mouse_pos = pygame.mouse.get_pos()
    
    # Check if mouse is over the play button
    if menu_play_button_rect.collidepoint(mouse_pos):
        window.blit(playbtn_hover, menu_play_button_rect.topleft) # Blit at the rect's top-left
    else:
        window.blit(playbtn, menu_play_button_rect.topleft) # Blit at the rect's top-left

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
    
    # You might want to make the instructions play button also have a hover effect
    # For simplicity, keeping it as a colored rect for now.
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

def wait_for_play_click(button_rect, screen_drawing_function):
    """
    Waits for a click on the given button, continuously drawing the screen
    using the provided screen_drawing_function.
    """
    waiting = True
    while waiting:
        screen_drawing_function() # Continuously draw the current screen (menu or instructions)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    waiting = False
        clock.tick(60) # Control the frame rate

    return True

def draw_level_complete(level):
    window.fill(white)
    complete_text = title_font.render(f"Day {level} Complete!", True, black)
    next_day_text = score_font.render("Preparing for the next dive...", True, black)
    window.blit(complete_text, (screen_width // 2 - complete_text.get_width() // 2, 150))
    window.blit(next_day_text, (screen_width // 2 - next_day_text.get_width() // 2, 250))
    pygame.display.flip()
    pygame.time.wait(3000)

def run_game(level):
    total_fuel_time = 40 #time(s) of fuel lasts
    ship_x = 50 #Initial submarine x position
    ship_y = screen_height // 2 #Initial submarine y position
    current_score = 0 #initial score
    plastics = []
    fish_list = []

    high_score = load_high_score()
    start_time = time.time()
    running = True

    while running:
        window.blit(bg, (0, 0)) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None

        # Sub movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if ship_y > -50 :
                ship_y -= ship_velocity
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if ship_y + ship_height < screen_height - 60:
                ship_y += ship_velocity

        # Load & draw submarine
        sub_image = pygame.image.load("submarine.png").convert_alpha()
        resized_ship = pygame.transform.smoothscale(sub_image, [150, 150])
        window.blit(resized_ship, (ship_x, ship_y))

        # Custom hitbox — adjust to match vector shape
        # ship_hitbox = pygame.Rect(ship_x + 23, ship_y + 43, 110, 63) # Original hitbox
        ship_hitbox = pygame.Rect(ship_x + 35, ship_y + 60, 90, 40) # A bit tighter hitbox
        # pygame.draw.rect(window, (0, 255, 0), ship_hitbox, 2)  # Debug outline - uncomment to see

        # Plastic spawning and collision
        if random.randint(1, 100) <= plastic_chance.get(level, 0):
            plastics.append((spawn_plastic(), random.choice(scaled_plastic_images)))  # Store rect and image

        # Move plastics and check for collisions
        for i, (plastic_rect, plastic_img) in enumerate(plastics[:]):
            plastic_rect.x -= plastic_speed
            window.blit(plastic_img, plastic_rect.topleft)
            if ship_hitbox.colliderect(plastic_rect):
                total_fuel_time -= 3
                plastics.pop(i)
        # Remove plastics that moved off-screen
        plastics = [(r, img) for (r, img) in plastics if r.x + plastic_width > 0]

        # Fish spawning and collision
        if random.randint(1, 200) <= fish_chance.get(level, 0):
            fish_list.append((spawn_fish(), random.choice(scaled_fish_images))) # Store rect and image
        for i, (fish_rect, fish_img) in enumerate(fish_list[:]):
            fish_rect.x -= fish_speed
            window.blit(fish_img, fish_rect.topleft) # Draw the fish image
            if ship_hitbox.colliderect(fish_rect):
                current_score += 1
                fish_list.pop(i) # Remove by index as it's a list of tuples
        fish_list = [f for f in fish_list if f[0].x + fish_width > 0] # Filter by the rect's x-coordinate


        # Fuel calculations
        elapsed_time = time.time() - start_time
        fuel_left = max(0, 100 - int((elapsed_time / total_fuel_time) * 100))

        if fuel_left <= 0:
            if current_score > high_score:
                save_high_score(current_score)
            return current_score

        # HUD
        display_score(current_score, high_score, fuel_left)
        level_text = score_font.render("Day " + str(level), True, white)
        window.blit(level_text, [screen_width//2 - 50, 50])

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


# Main Game Loop / Flow
# Loop to handle the menu state continuously
game_state = "menu" # "menu", "instructions", "game"

while True:
    if game_state == "menu":
        draw_menu()
        if wait_for_play_click(menu_play_button_rect, draw_menu):
            game_state = "instructions"
        else: # User quit during menu
            break
    elif game_state == "instructions":
        draw_instructions()
        if wait_for_play_click(instructions_play_button_rect, draw_instructions):
            game_state = "game"
        else: # User quit during instructions
            break
    elif game_state == "game":
        run_all_levels()
        game_state = "quit" 
    elif game_state == "quit":
        break

pygame.quit()