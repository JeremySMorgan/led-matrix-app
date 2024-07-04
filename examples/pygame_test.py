import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 500, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Draw Square")

# Set up the square parameters
square_size = 50
square_color = (255, 0, 0)  # Red

# Set up the initial position of the square
square_x = (width - square_size) // 2
square_y = (height - square_size) // 2

line_color = (0, 0, 255)  # Blue
line_start = (500, 0)
line_end = (450, 450)
line_width = 3

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Draw the square on the screen
    screen.fill((255, 255, 255))  # Fill the screen with white background
    pygame.draw.rect(
        screen,
        square_color,
        (square_x, square_y, square_size, square_size),
    )

    pygame.draw.line(screen, line_color, line_start, line_end, line_width)

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    pygame.time.Clock().tick(60)
