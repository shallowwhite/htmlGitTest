import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Drawing with Code")

# Set up colors
white = (255, 255, 255)
black = (0, 0, 0)

# Set up drawing variables
drawing = False
radius = 5

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False
        elif event.type == pygame.MOUSEMOTION and drawing:
            x, y = event.pos
            pygame.draw.circle(screen, white, (x, y), radius)

    # Update the display
    pygame.display.flip()