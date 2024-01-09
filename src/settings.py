"""
This file contains all the settings for the game.

You can change the settings here instead of changing them in the main file.

You can also add more settings here and use them in the main file.

Example:
    In this file:
        GAME_TITLE = "My Game"
    In the main file:
        import settings
        print(settings.GAME_TITLE) # prints "My Game"
"""



# Colors (R, G , B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
DARKGRAY = (40, 40, 40)
LIGHTGRAY = (100, 100, 100)

# Game settings
GAME_TITLE = "Space Trade Game"
SCREEN_WIDTH = 800  #Overided when in fullscreen mode
SCREEN_HEIGHT = 600 #Overided when in fullscreen mode
FULLSCREEN = False
FPS = 60
BACKGROUND_COLOR = DARKGRAY



if FULLSCREEN == True:
    import pyautogui
    SCREEN_WIDTH,SCREEN_HEIGHT = pyautogui.size()
