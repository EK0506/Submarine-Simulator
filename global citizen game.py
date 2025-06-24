#Version 1 only incldes basic 
import pygame
import random

pygame.init()  # Initialize all imported Pygame modules

# Set screen size
screen_width = 800
screen_height = 500

# Set up the display window
window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Submarine Simulator")  # Title for the game window

# Game control flag
running = True

# Define RGB color values
light_blue = (173, 216, 230) 
brown = (102, 51, 0)        
red = (255, 0, 0)            
blue = (0, 0, 255)
green = (188, 227, 199)
black = (0, 0, 0)
white = (255, 255, 255)       

#Score Display
score_font = pygame.font.Font(None, 36) 

# Ship setup
ship_width = 50
ship_height = 30
ship_x = 50                                # Submarine starts on the left
ship_y = screen_height // 2                # Centered vertically
ship_velocity = 4                          # Speed at which the submarine moves

# Plastic object setup
plastic_width = 30
plastic_height = 30
plastic_speed = 3                          # Speed of plastic objects

# fish object setup
fish_width = 30
fish_height = 30
fish_speed = 4                           # Slightly faster than plastic

# Function to generate a new plastic object
def spawn_plastic():
    x = screen_width                      # Start off-screen on the right
    y = random.randint(0, screen_height - plastic_height)
    return pygame.Rect(x, y, plastic_width, plastic_height)

# Function to generate a new fish object
def spawn_fish():
    x = screen_width
    y = random.randint(0, screen_height - fish_height)
    return pygame.Rect(x, y, fish_width, fish_height)

# Object containers
plastics = []
fish_list = []

clock = pygame.time.Clock()  # Controls how fast the game loop updates

# Main game loop
while running:
    window.fill(light_blue)  # Clear the screen and fill it with background color

    # Event handler for quitting the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Keyboard input for moving the submarine
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and ship_y > 0:
        ship_y -= ship_velocity
    if keys[pygame.K_DOWN] and ship_y + ship_height < screen_height:
        ship_y += ship_velocity

    # Draw the submarine
    pygame.draw.rect(window, brown, [ship_x, ship_y, ship_width, ship_height])

    # Random chance to spawn a plastic object
    if random.randint(1, 100) == 1: #Spawn plastic when the random number is 1
        plastics.append(spawn_plastic())

    # Move and draw plastics
    for plastic in plastics:
        plastic.x -= plastic_speed
    plastics = [p for p in plastics if p.x + plastic_width > 0]  # Keep only visible ones
    for plastic in plastics:
        pygame.draw.rect(window, red, plastic)

    # Random chance to spawn a fish object
    if random.randint(1, 80) == 1: #Spawn fish when the random number is 1
        fish_list.append(spawn_fish())

    # Move and draw fish
    for fish in fish_list:
        fish.x -= fish_speed
    fish_list = [d for d in fish_list if d.x + fish_width > 0]
    for fish in fish_list:
        pygame.draw.rect(window, blue, fish)

    # Refresh the screen to show new frame
    pygame.display.flip()

    # Control the frame rate (lower for smoother movement)
    clock.tick(100)