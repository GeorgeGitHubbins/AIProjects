#Dont forget to pip install pygame!

import pygame
from pygame.locals import *
import random

# Initialize Pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SCALE = 0.10  # Scale factor for the player
FIRE_SPRITES_HEIGHT = 100  # Desired height for fire sprites, initialized value

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Esteban Adventures")

# Load the sprite sequences for movement and collision
movement_sprites = [
    pygame.image.load("Esteban.png").convert_alpha(),
    pygame.image.load("EstebanSkew1.png").convert_alpha(),
    pygame.image.load("EstebanSkew2.png").convert_alpha(),
]

collision_sprites = [
    pygame.image.load("Esteban_ow.png").convert_alpha(),
    pygame.image.load("Esteban_owSkew1.png").convert_alpha(),
    pygame.image.load("Esteban_owSkew2.png").convert_alpha(),
]

# Load fire sprites
fire_sprites = [
    pygame.image.load("fire1.png").convert_alpha(),
    pygame.image.load("fire2.png").convert_alpha(),
    pygame.image.load("fire3.png").convert_alpha(),
    pygame.image.load("fire4.png").convert_alpha(),
]

# Function to scale sprites
def scale_sprites(sprites, height):
    scaled_sprites = []
    for sprite in sprites:
        aspect_ratio = sprite.get_width() / sprite.get_height()
        width = int(height * aspect_ratio)  # Maintain aspect ratio
        scaled_sprites.append(pygame.transform.smoothscale(sprite, (width, height)))
    return scaled_sprites

# Scale all sprites
movement_sprites = scale_sprites(movement_sprites, int(movement_sprites[0].get_height() * PLAYER_SCALE))
collision_sprites = scale_sprites(collision_sprites, int(collision_sprites[0].get_height() * PLAYER_SCALE))
fire_sprites = scale_sprites(fire_sprites, FIRE_SPRITES_HEIGHT)

# Create player and fire obstacle
player = pygame.Rect(400, 300, movement_sprites[0].get_width(), movement_sprites[0].get_height())
fire_obstacle = pygame.Rect(200, 200, fire_sprites[0].get_width(), FIRE_SPRITES_HEIGHT)
fire_size_ratio = fire_sprites[0].get_width() / FIRE_SPRITES_HEIGHT

# Colors
white = (255, 255, 255)
blue = (0, 0, 255)

# Game loop
running = True
sprite_index = 0  # To track current sprite in the sequence
sprite_cycle_speed = 0.01  # Adjust this to control sprite cycling speed
cycle_counter = 0  # Used to control sprite cycling
fire_cycle_counter = 0  # Used to control fire sprite cycling
fire_sprite_index = 0  # To cycle through fire sprites
blue_squares = []  # List of blue squares to track projectiles

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        # Shooting mechanism
        if event.type == KEYDOWN and event.key == K_SPACE:
            # Create a blue square projectile
            blue_squares.append(pygame.Rect(player.x, player.y + 75, 10, 10))

    # Player movement
    keys = pygame.key.get_pressed()
    dx = dy = 0  # Movement delta
    if keys[K_LEFT]:
        dx = -1
    if keys[K_RIGHT]:
        dx = 1
    if keys[K_UP]:
        dy = -1
    if keys[K_DOWN]:
        dy = 1

    # Move the player
    player.x += dx
    player.y += dy


    # Update the sprite cycle
    cycle_counter += sprite_cycle_speed * max(abs(dx), abs(dy), abs(dx) + abs(dy))
    if cycle_counter >= 1:
        sprite_index = (sprite_index + 1) % len(movement_sprites)  # Loop through sprites
        cycle_counter = 0

    fire_cycle_counter += 0.005
    if fire_cycle_counter >= 1:
        # Update fire obstacle cycle
        fire_sprite_index = (fire_sprite_index + 1) % len(fire_sprites)
        fire_obstacle.x += random.choice(range(-1, 2, 1))
        fire_obstacle.y += random.choice(range(-1, 2, 1))
        fire_cycle_counter = 0

    # Update blue squares
    to_remove = []
    for square in blue_squares:
        square.x -= 1  # Move left
        if square.x < -1000:
            to_remove.append(square)  # Mark for removal after a total movement of 1000 units
        elif square.colliderect(fire_obstacle):
            # If the square collides with the fire obstacle, grow the obstacle
            FIRE_SPRITES_HEIGHT += 10
            fire_obstacle.height = FIRE_SPRITES_HEIGHT
            fire_obstacle.width += 10*fire_size_ratio
            fire_sprites = scale_sprites(fire_sprites, FIRE_SPRITES_HEIGHT)  # Rescale the fire sprites
            to_remove.append(square)  # Remove the square after collision

    for square in to_remove:
        blue_squares.remove(square)  # Remove squares from list

    # Check for collisions
    if player.colliderect(fire_obstacle):
        current_sprite = collision_sprites[sprite_index]  # Colliding sprite
        cycle_counter += sprite_cycle_speed
    else:
        current_sprite = movement_sprites[sprite_index]  # Moving sprite

    # Draw everything
    screen.fill(white)  # Set the background to white
    screen.blit(fire_sprites[fire_sprite_index], (fire_obstacle.x, fire_obstacle.y))  # Cycle through fire sprites

    screen.blit(current_sprite, (player.x, player.y))  # Draw the player sprite

    # Draw blue squares
    for square in blue_squares:
        pygame.draw.rect(screen, blue, square)

    pygame.display.update()

pygame.quit()

