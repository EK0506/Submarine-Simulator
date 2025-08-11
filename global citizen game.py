"""Notes:
 - Requires the 'assets' folder with images and sounds at the relative paths used.
 - Save file: "high_score.txt" is used for storing the high score in the working directory.
 - Some assets are loaded inside a function (inefficient) — see inline comments.
"""
import pygame
import random
import time

# Initialize pygame modules
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
# Images are loaded and scaled once at the top to avoid repeated scaling during the game loop
# Menu Backgrounds
menubg_image = pygame.image.load('assets/img/menubg.png')
menubg = pygame.transform.smoothscale(menubg_image, (screen_width, screen_height))

#Intro Background for intro screen
introbg_image = pygame.image.load('assets/img/introbg.png')
introbg = pygame.transform.smoothscale(introbg_image, (screen_width, screen_height)) #intro before level 1
lv2introbg_image = pygame.image.load('assets/img/lv2_intro.png')
lv2introbg = pygame.transform.smoothscale(lv2introbg_image, (screen_width, screen_height)) #intro before level 2
lv3introbg_image = pygame.image.load('assets/img/lv3_intro.png') 
lv3introbg = pygame.transform.smoothscale(lv3introbg_image, (screen_width, screen_height)) #intro before level 3

# Game Backgrounds (3 levels)
bg_image = pygame.image.load('assets/img/bg.png')
bg = pygame.transform.smoothscale(bg_image, (screen_width, screen_height))
bg_image2 = pygame.image.load('assets/img/bg2.png')
bg2 = pygame.transform.smoothscale(bg_image2, (screen_width, screen_height))
bg_image3 = pygame.image.load('assets/img/bg3.png')
bg3 = pygame.transform.smoothscale(bg_image3, (screen_width, screen_height))

# Tutorial Image
tutorial_image_raw = pygame.image.load('assets/img/tutorial.png')
tutorial_image = pygame.transform.smoothscale(tutorial_image_raw, (screen_width, screen_height)) #full screen size
tutorial_image2_raw = pygame.image.load('assets/img/tutorial2.png')
tutorial2_image = pygame.transform.smoothscale(tutorial_image2_raw, (screen_width, screen_height))

# Buttons (images + hover states)
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

# Button Hitboxes for mouse collision
play_button_rect = pygame.Rect(screen_width // 2 - playbtn_width // 2, screen_height // 2 + 50, playbtn_width, playbtn_height)
ready_button_rect = pygame.Rect(screen_width - readybtn_width - 30, screen_height - readybtn_height - 30, readybtn_width, readybtn_height)

# Score Panel
score_panel_image = pygame.image.load("assets/img/score_panel.png").convert_alpha()
score_panel_width = 220
score_panel_height = 110
scaled_score_panel = pygame.transform.smoothscale(score_panel_image, (score_panel_width, score_panel_height))

# Submarine Image (scaled)
sub_image_raw = pygame.image.load("assets/img/submarine.png").convert_alpha()
submarine_image = pygame.transform.smoothscale(sub_image_raw, [150, 150]) # Scaled once

# Fish images: load all fish variants and scale them uniformly
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

# Rubbish Images
plastic_width = 80
plastic_height = 65
plastic_images = [
    pygame.image.load("assets/img/rubbish/p1.png").convert_alpha(),
    pygame.image.load("assets/img/rubbish/p2.png").convert_alpha(),
    pygame.image.load("assets/img/rubbish/p3.png").convert_alpha(),
    pygame.image.load("assets/img/rubbish/p4.png").convert_alpha(),
]
scaled_plastic_images = [pygame.transform.smoothscale(img, (plastic_width, plastic_height)) for img in plastic_images]

# SFX
btn_sound = pygame.mixer.Sound("assets/sound/sound_effect/button.mp3")
collect_sound = pygame.mixer.Sound("assets/sound/sound_effect/collect.wav")
level_complete_sound = pygame.mixer.Sound("assets/sound/sound_effect/level_complete.mp3")
text_sound = pygame.mixer.Sound("assets/sound/sound_effect/text_sound.mp3")
damage_sound = pygame.mixer.Sound("assets/sound/sound_effect/damage.mp3")


# --- Game Variables ---
# Submarine hitbox
ship_width = 60
ship_height = 40
ship_velocity = 7 # pixels per frame

plastic_speed = 5
fish_speed = 6

# Plastic and fish spawn probabilities
# These are dictionaries where the key is the level number and the value is the spawn chance per frame.
# It works by genereating a random number between 1 and 100 (1 and 200 for fish), and if it is less than or equal to the value in the dictionary,
# the item spawns. For example, plastic_chance[1] = 0 means no plastics spawn in level 1.
# You can adjust these values to change the difficulty of each level.

plastic_chance = {1: 0, 2: 1, 3: 3} 
fish_chance = {1: 8, 2: 6, 3: 3} 

clock = pygame.time.Clock()

# --- Dialogue Content ---
# Intro dialogue before the game starts
intro_dialogue = [
    "Hey there, explorer! Welcome aboard.",
    "You're on a mission to study the ocean's wonders.",
    "Your goal is to collect fish data using the submarine.",
    "But keep your eyes open. The ocean is always changing...",
]
# Story dialogues for each level
# Level 1
story_dialogue_1 = [
    "Construction of new factories has begun.",
    "Waste from the site is being dumped into the ocean.",
    "Plastic are starting to appear in the water.",
    "Avoid them at all costs!"
]
# Level 2
story_dialogue_2 = [
    "More factories have been built near the coast.",
    "This is having a serious impact on the ecosystem.",
    "You'll encounter more plastics now. Stay focused!"
]

# --- Functions ---
def typewriter_text(surface, text, font, colour, x, y, speed=5, background_image=None): #Lowering speed increases text display speed
    """
    Displays text with a typewriter animation on the provided surface.
    - surface: pygame.Surface to draw on (usually the main window)
    - text: the full string to display
    - font: pygame.font.Font object
    - colour: text color
    - x, y: top-left coordinates to render the text surface
    - speed: number of milliseconds between character reveals (lower = faster)
    - background_image: optional background image to draw each frame (keeps story background)
    """
    displayed_text = ''
    last_update = pygame.time.get_ticks()
    index = 0
    full_text_displayed = False
    
    # Play sound effect for typing
    pygame.mixer.Sound.play(text_sound, loops=-1)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    if not full_text_displayed:
                        # Skip to the end of the text
                        displayed_text = text
                        index = len(text)
                        full_text_displayed = True
                        pygame.mixer.Sound.stop(text_sound)
                    else:
                        # Text is already displayed, so a second key press exits the function and continue next catalogue
                        return
        # Typewriter animation logic
        if not full_text_displayed:
            current_time = pygame.time.get_ticks()
            if current_time - last_update >= speed: # Reveal 1 character every 'speed' milliseconds
                displayed_text += text[index]
                index += 1
                last_update = current_time
                if index >= len(text):
                    full_text_displayed = True
                    pygame.mixer.Sound.stop(text_sound)

        # Drawing the screen
        if background_image:
            draw_story_screen_background(surface, background_image)
            
        text_surface = font.render(displayed_text, True, colour)
        surface.blit(text_surface, (x, y))
        
        # After full text displayed, prompt user to continue
        if full_text_displayed:
            continue_text = small_font.render("(Press space to continue)", True, white)
            window.blit(continue_text, (screen_width - continue_text.get_width() - 70, screen_height - 65))
            
        pygame.display.update()

        # This is where your original wait_for_key_press() would have been.
        # Now it's integrated, so we don't need a separate call.

def draw_menu():
    """
    Draws the main menu background and the Play button with hover effect.
    - If background music is not already playing, loads and starts the menu music loop.
    - Uses play_button_rect to check hover/click.
    """
    window.blit(menubg, (0, 0))
    mouse_pos = pygame.mouse.get_pos()

    # Start background music for the menu if nothing is playing.
    # music.get_busy() returns True if the music mixer is currently playing.
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load("assets/sound/bgm/menu.mp3")
        pygame.mixer.music.play(-1)

    # Hover effect drawing: blit a different surface when the mouse is on the button.
    if play_button_rect.collidepoint(mouse_pos):
        window.blit(playbtn_hover, play_button_rect.topleft)
    else:
        window.blit(playbtn, play_button_rect.topleft)

    pygame.display.flip()

def draw_story_screen_background(surface, background_image):
    """
    Draws a standard story screen layout:
    - fills background with black then draws the provided background_image
    - draws the captain portrait and a framed rectangle for the text area
    """
    surface.fill(black)
    surface.blit(background_image, (0, 0))
    captain_img = pygame.image.load("assets/img/captain.png").convert_alpha()
    captain_scaled = pygame.transform.smoothscale(captain_img, (180, 250))
    surface.blit(captain_scaled, (screen_width - 280, screen_height - 300))

    pygame.draw.rect(surface, black, (50, screen_height - 120, screen_width - 100, 80))
    pygame.draw.rect(surface, white, (50, screen_height - 120, screen_width - 100, 80), 2)

def run_story_dialogue(dialogues, story_image):
    """
    Iterate through a list of dialogue strings and show each with the typewriter effect.
    - dialogues: list of strings to show
    - story_image: background image to render during the story
    The typewriter_text() function handles user input to move between lines.
    """
    for line in dialogues:
        draw_story_screen_background(window, story_image)
        
        # Handles both the animation and waiting for user input
        typewriter_text(window, line, context_font, white, 60, screen_height - 100, background_image=story_image)
        

def wait_for_key_press():
    """
    Blocks until the user presses any key or mouse button.
    Used for simple 'press any key to continue' interactions outside of the typewriter.
    """
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

def draw_tutorial1():
    """
    Draws the first tutorial image and the ready button (with hover).
    Designed to be used inside a loop so the ready button can be clicked.
    """
    window.blit(tutorial_image, (0, 0))
    mouse_pos = pygame.mouse.get_pos()

    if ready_button_rect.collidepoint(mouse_pos):
        window.blit(readybtn_hover, ready_button_rect.topleft)
    else:
        window.blit(readybtn, ready_button_rect.topleft)
    pygame.display.flip()

def draw_tutorial2():
    """
    Draws the second tutorial screen used between levels.
    Same pattern as draw_tutorial1.
    """
    window.blit(tutorial2_image, (0, 0))
    mouse_pos = pygame.mouse.get_pos()
    if ready_button_rect.collidepoint(mouse_pos):
        window.blit(readybtn_hover, ready_button_rect.topleft)
    else:
        window.blit(readybtn, ready_button_rect.topleft)
    pygame.display.flip()

def draw_game_over(score):
    """
    Draws a simple game over screen showing the final score.
    Music is stopped, the screen is shown for 3 seconds using pygame.time.wait.
    """
    pygame.mixer.music.stop()
    window.fill(white)
    game_over_text = title_font.render("Game Over", True, black)
    score_text = score_font.render(f"Your Score: {score}", True, black)
    window.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, 150))
    window.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, 250))
    pygame.display.flip()
    pygame.time.wait(3000) # Pause for 3 seconds so player can read the score

def display_score(score, high_score, fuel_percent):
    """
    Draw a score panel in the top-right corner:
    - Score, Best Score, and Fuel % printed on a panel image.
    Positioning is anchored to the right edge of the screen.
    """
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
    """
    Create a new plastic rectangle positioned at the right edge of the screen
    with a random vertical position. The returned object is a pygame.Rect which
    is used for positioning and collision detection.
    """
    x = screen_width
    y = random.randint(0, screen_height - plastic_height)
    return pygame.Rect(x, y, plastic_width, plastic_height)

def spawn_fish():
    """
    Create a new fish rectangle positioned at the right edge of the screen
    with a random vertical position (ensures it fits within the screen height).
    """
    x = screen_width
    y = random.randint(0, screen_height - fish_height)
    return pygame.Rect(x, y, fish_width, fish_height)

def load_high_score():
    """
    Load the stored high score from "high_score.txt".
    If the file is not present or contains invalid content, return 0.
    Using try/except makes loading robust against missing/corrupt files.
    """
    try:
        with open("high_score.txt", 'r') as f:
            return int(f.read())
    except (FileNotFoundError, ValueError):
        return 0

def save_high_score(high_score):
    """
    Save the high score to "high_score.txt".
    """
    with open("high_score.txt", "w") as f:
        f.write(str(high_score))

def wait_for_button_click(button_rect, screen_drawing_function):
    """
    Generic blocking helper that:
    - Calls screen_drawing_function() each frame to render the UI
    - Waits until the user clicks inside button_rect, or quits
    - Plays a button sound when the button is clicked
    Returns:
    - True if the button was clicked
    - False if the user quit the game
    """
    waiting = True
    while waiting:
        screen_drawing_function() # Draw the provided screen so hover states and UI remain responsive
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
    """
    Visual and audio feedback for completing a level.
    Stops any currently playing music, plays a completion SFX, shows the message,
    and waits 3 seconds.
    """
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(level_complete_sound)
    window.fill(white)
    complete_text = title_font.render(f"Level {level} Complete!", True, black)
    window.blit(complete_text, (screen_width // 2 - complete_text.get_width() // 2, screen_height // 2 - 50))
    pygame.display.flip()
    pygame.time.wait(3000)

def run_game(level):
    """
    Core game loop for a given level.
    """
    current_score = 0 #Set initial score to 0
    pygame.mixer.music.stop() # Stop any music from previous levels

    # Choose background music according to level
    if level == 1:
        pygame.mixer.music.load("assets/sound/bgm/lv1.mp3")
    elif level == 2:
        pygame.mixer.music.load("assets/sound/bgm/lv2.mp3")
    elif level == 3:
        pygame.mixer.music.load("assets/sound/bgm/lv3.mp3")
    pygame.mixer.music.play(-1)

    # total_fuel_time is the time in seconds that corresponds to 100% fuel.
    total_fuel_time = 40
    ship_x = 50
    ship_y = screen_height // 2
    plastics = []
    fish_list = []

    high_score = load_high_score()
    start_time = time.time()
    running = True

    while running:  # Draw level-specific background
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
        #Ship movement controls
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

        window.blit(submarine_image, (ship_x, ship_y)) # Draw the submarine at the new position
        ship_hitbox = pygame.Rect(ship_x + 20, ship_y + 45, 110, 60) # Create a hitbox for collision detection
        #pygame.draw.rect(window, green, ship_hitbox, 2)  # Draw hitbox for debugging

        if random.randint(1, 100) <= plastic_chance.get(level, 0): # Spawn plastics based on level chance
            plastics.append((spawn_plastic(), random.choice(scaled_plastic_images)))

        # Update plastics: move left, draw, check collision with player, and removal
        for i, (plastic_rect, plastic_img) in enumerate(plastics[:]):
            plastic_rect.x -= plastic_speed
            window.blit(plastic_img, plastic_rect.topleft)
            if ship_hitbox.colliderect(plastic_rect): # Collision detection
                pygame.mixer.Sound.play(damage_sound)
                total_fuel_time -= 3
                plastics.pop(i) # Remove plastic on collision
        plastics = [(r, img) for (r, img) in plastics if r.x + plastic_width > 0] # Keep plastics on screen

        if random.randint(1, 200) <= fish_chance.get(level, 0): # Spawn fish based on level chance
            fish_list.append((spawn_fish(), random.choice(scaled_fish_images))) 

        for i, (fish_rect, fish_img) in enumerate(fish_list[:]): # Move fish left, draw, check collision with player, and removal
            fish_rect.x -= fish_speed
            window.blit(fish_img, fish_rect.topleft) # Draw fish at its position
            if ship_hitbox.colliderect(fish_rect):
                pygame.mixer.Sound.play(collect_sound)
                current_score += 1 # Increment score on fish collection
                fish_list.pop(i) # Remove fish on collection
        fish_list = [f for f in fish_list if f[0].x + fish_width > 0] # Keep fish on screen

        elapsed_time = time.time() - start_time # Calculate elapsed time since the level started
        fuel_left = max(0, 100 - int((elapsed_time / total_fuel_time) * 100)) # Calculate fuel left as a percentage

        if fuel_left <= 0: # If fuel runs out, end the game
            pygame.mixer.music.stop()
            if current_score > high_score: # Check if new high score
                save_high_score(current_score) # Save new high score
            return current_score

        display_score(current_score, high_score, fuel_left) # Display score panel
        level_text = score_font.render("Year " + str(level), True, white) # Draw level text
        window.blit(level_text, [screen_width//2, 50]) # Draw level text at the top center

        pygame.display.flip()
        clock.tick(60) # Limit to 60 FPS

def run_all_levels():
    total_score = 0 # Initialize total score for all levels
    max_level = 3
    for level in range(1, max_level + 1): # Loop through each level
        score = run_game(level)
        if score is None:
            return
        total_score += score
        if level < max_level:
            draw_level_complete(level) # Show level complete screen before next level
            if level == 1:
                run_story_dialogue(story_dialogue_1, lv2introbg) # Intro before level 2
                
                draw_tutorial2()
                if not wait_for_button_click(ready_button_rect, draw_tutorial2): # If user clicks ready button, continue to next level
                    return None
                
            elif level == 2:
                run_story_dialogue(story_dialogue_2, lv3introbg) # Intro before level 3
        else:
            draw_game_over(total_score) # Final game over screen after last level

# --- Main Game Loop / Flow ---
game_state = "menu"

while True:
    if game_state == "menu":
        draw_menu()
        if wait_for_button_click(play_button_rect, draw_menu): # User clicked Play button
            game_state = "intro" # Start the game intro
        else:
            break
    elif game_state == "intro":
        pygame.mixer.music.stop() # Stop any music from the menu
        run_story_dialogue(intro_dialogue, introbg) # Intro dialogue before the game starts
        game_state = "tutorial" # Move to tutorial state
    elif game_state == "tutorial":
        draw_tutorial1()
        if wait_for_button_click(ready_button_rect, draw_tutorial1): # User clicked Ready button
            game_state = "game" # Start the game
        else:
            break
    elif game_state == "game":
        run_all_levels()
        game_state = "quit" # After all levels, exit the game
    elif game_state == "quit":
        break
    
pygame.quit()