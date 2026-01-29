"""
Simple manual test to verify game mechanics
"""

import pygame
from game import BTD6Game, BTD6Renderer
from game.entities import Vector2

pygame.init()

# Create game and renderer
game = BTD6Game(width=800, height=600)
renderer = BTD6Renderer(game)

# Place a tower
game.place_tower(400, 300)

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    dt = clock.tick(60) / 1000.0  # Delta time in seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            game.place_tower(x, y)

    game.update(dt)
    renderer.render()

renderer.close()
pygame.quit()

print("Game test completed!")
print(f"Final state: {game.state}")
print(f"Lives: {game.lives}")
print(f"Balloons killed: {100 - game.lives}")
