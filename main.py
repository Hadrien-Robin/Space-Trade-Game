# Simple pygame program


# Import and initialize the pygame library

import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    MOUSEBUTTONDOWN,
)
import sys
from menu_functions import *#definition of functions used in menus


pygame.init()


# Set up the drawing window
window_width, window_height = 800, 600
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Your Game Title")


# Run the start screen
start_screen()


# Done! Time to quit.

pygame.quit()
sys.exit()
