"""
This module contains the various states that the game can be in. Each state is a class that inherits from the State class.

The State class is a base class that contains the basic functionality that every state should have. It is not meant to be used directly.

The State class has the following methods:
    boot: called when the state is first initialized
    update: called on every frame
    enter: called when the state becomes the current state
    exit: called when the state is no longer the current state
    draw: called on every frame

The State class has the following attributes:
    game: the game object
    all_sprites: a sprite group that contains all the sprites in the state
"""

import os
import pygame as pg
from components import *
from settings import *
import memory as mry
import random 

class State:
    """
    Base class for all states
    """
    def __init__(self, game):
        """
        game: game object
        """
        self.game = game
        # all sprites in the state
        self.all_sprites = pg.sprite.Group()
        self.all_buttons = pg.sprite.Group()
        self.all_frames = pg.sprite.Group()
        self.boot()

    def boot(self):
        """
        Called when the state is first initialized
        """
        # override this method to add logic that happens when the state is first initialized
        pass

    def update(self):
        """
        Called on every frame
        """
        # override this method to add logic that happens on every frame
        self.all_sprites.update()

    def enter(self):
        """
        Called when the state becomes the current state
        """
        # override this method to add logic that happens when this state becomes the current state
        pass

    def exit(self):
        """
        Called when the state is no longer the current state
        """
        # override this method to add logic that happens when changing
        # from this state to some other state
        pass

    def draw(self, screen):
        """
        Called on every frame
        """
        self.all_sprites.draw(screen)
        self.all_buttons.draw(screen)
        self.all_frames.draw(screen)


class Intro(State):
    """
    Intro state
    """
    def boot(self):
        assets_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets'))
        # load the intro sound
        self.game.audio.load_sound('intro', os.path.join(assets_dir, 'sounds', 'start_screen_st.mp3'))

        # add a background image
        rand_bg = random.randint(1,3)
        bg = ImageSprite(self.game, os.path.join(assets_dir, 'images', 'start_screen', 'start_screen_bg'+str(rand_bg)+'.png'))
        bg.rect.topleft = (0,0)
        self.all_sprites.add(bg)

        # add the starfield overlays
        SF_WIDTH = 4096
        self.all_starfields = pg.sprite.Group()
        rand_sf = random.randint(1,4)
        starfield1 = ImageSprite(self.game, os.path.join(assets_dir, 'images', 'start_screen', 'Starfield'+str(rand_sf)+'.png'))
        starfield1.rect.topleft = (0,0)
        self.all_sprites.add(starfield1)
        self.all_starfields.add(starfield1)
        
        starfield2 = ImageSprite(self.game, os.path.join(assets_dir, 'images', 'start_screen', 'Starfield'+str(rand_sf)+'.png'))
        starfield2.rect.topleft = (SF_WIDTH,0)
        self.all_sprites.add(starfield2)
        self.all_starfields.add(starfield2)

        #add a spaceship sprite
        spaceship = ImageSprite(self.game, os.path.join(assets_dir, 'images', 'Player_sprite.png'))
        spaceship.rect.center = (0.2*SCREEN_WIDTH,0.5*SCREEN_HEIGHT)
        self.all_sprites.add(spaceship)
        
        # add some text
        # center text on screen
        # add the text to the all_sprites group
        title = TextSprite(self.game, os.path.join(assets_dir, 'fonts', 'PressStart2P-Regular.ttf'),
                GAME_TITLE, 48, color = WHITE)
        title.rect.center = self.game.screen.get_rect().center
        title.rect.centery = SCREEN_HEIGHT*0.2
        self.all_sprites.add(title)

        
        # add some more text
        new_game_text = TextSprite(self.game,
                os.path.join(assets_dir, 'fonts', 'PressStart2P-Regular.ttf'),
                "New Game", 24, color = (255,255,255),tag='NewGame')
        new_game_text.rect.center = title.rect.center
        new_game_text.rect.centery += SCREEN_HEIGHT*0.2
        # add the text to the all_sprites group
        self.all_sprites.add(new_game_text)
        self.all_buttons.add(new_game_text)

        # add some more text
        load_text = TextSprite(self.game,
                os.path.join(assets_dir, 'fonts', 'PressStart2P-Regular.ttf'),
                "Load Game", 24, color = (255,255,255),tag='Load')
        load_text.rect.center = title.rect.center
        load_text.rect.centery += SCREEN_HEIGHT*0.4
        # add the text to the all_sprites group
        self.all_sprites.add(load_text)
        self.all_buttons.add(load_text)

        # add some more text
        settings_text = TextSprite(self.game,
                os.path.join(assets_dir, 'fonts', 'PressStart2P-Regular.ttf'),
                "Settings", 24, color = (255,255,255),tag='Settings')
        settings_text.rect.center = title.rect.center
        settings_text.rect.centery += SCREEN_HEIGHT*0.6
        # add the text to the all_sprites group
        self.all_sprites.add(settings_text)
        self.all_buttons.add(settings_text)
        
    def enter(self):
        # when the state becomes the current state, play the intro sound
        self.game.audio.play('intro')

    def update(self):
        # on every frame, call the update method of the base class
        super().update()
       
       # check if any key is pressed
        if self.game.input.is_mouse_pressed(1):
                print("Mouse press")
                mouse_pos = pg.mouse.get_pos()
                # Check if the mouse click is within the region of Option 1
                for button in self.all_buttons:
                    if button.rect.collidepoint(mouse_pos) and button.tag == 'NewGame':
                        self.game.change_state('Pilote')
                        print("New Game")
                    # Check for Option 2
                    elif button.rect.collidepoint(mouse_pos) and button.tag == 'Load':
                        #load_menu()
                        print("Load")
                    # Check for Option 3
                    elif button.rect.collidepoint(mouse_pos) and button.tag == 'Settings':
                        #self.game.change_state('Outro')
                        print("Settings")
        sf_speed = SCREEN_WIDTH/(60*5)
        for sf in self.all_starfields:
            sf.rect.x -= sf_speed
            if sf.rect.right < 0:
                sf.rect.x += 4096
        
class Pilote(State):
    """
    Pilote game state
    """
    def boot(self):
        self.game.memory.move_player(list(self.game.memory.Galaxy.stars.values())[0])
        print(list(self.game.memory.Galaxy.stars.keys())[0])
        assets_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets'))

        #Draw map
        size_drw = (SCREEN_WIDTH*0.4, SCREEN_HEIGHT*0.8)
        map_bg = ShapeSprite(self.game,"rect", color = BLACK,size = size_drw)
        map_bg.rect.topleft = (0.05*SCREEN_WIDTH, 0.125*SCREEN_HEIGHT)
        self.all_sprites.add(map_bg)
        self.all_frames.add(map_bg.generate_frame())

        #Draw right menu
        menu_shape = ShapeSprite(self.game, "rect", color = BLACK, size = size_drw)
        menu_shape.rect.topright = (0.95*SCREEN_WIDTH, 0.125*SCREEN_HEIGHT)
        menu_background = menu_shape.generate_frame(Background=True)
        self.all_sprites.add(menu_background)
        print(menu_background.rect.bottom, menu_background.rect.top)
        
    def enter(self):
        # when the state becomes the current state
        #set the current submenu to main
        self.menu_state = 'main'
        print('enter')

    def update(self):
        # on every frame, call the update method of the base class
        super().update()
        assets_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets'))
        
       # check which menu is currently display
        match self.menu_state:
            case 'main':
               title_button = TextSprite(self.game,
                os.path.join(assets_dir, 'fonts', 'PressStart2P-Regular.ttf'),
                self.game.memory.Player["System"].name, 12, color = (255,255,255))
               size = (SCREEN_WIDTH*0.4*0.9,title_button.rect.h)
               title_button.make_button(size)
               title_button.rect.centerx = 0.75*SCREEN_WIDTH
               title_button.rect.top = 0.15*SCREEN_HEIGHT
               self.all_buttons.add(title_button)     
               
               enter_button = TextSprite(self.game,
                os.path.join(assets_dir, 'fonts', 'PressStart2P-Regular.ttf'),
                "Enter system", 12, color = (255,255,255),tag='enter')
               enter_button.make_button(size)
               enter_button.rect.center = title_button.rect.center
               enter_button.rect.centery += 0.175*SCREEN_HEIGHT
               self.all_buttons.add(enter_button)
               
               travel_button = TextSprite(self.game,
                os.path.join(assets_dir, 'fonts', 'PressStart2P-Regular.ttf'),
                "Leave the system", 12, color = (255,255,255),tag='travel')
               travel_button.make_button(size)
               travel_button.rect.center = title_button.rect.center
               travel_button.rect.centery += 0.325*SCREEN_HEIGHT
               self.all_buttons.add(travel_button)
               
               logs_button = TextSprite(self.game,
                os.path.join(assets_dir, 'fonts', 'PressStart2P-Regular.ttf'),
                "Check logs", 12, color = (255,255,255),tag='logs')
               logs_button.make_button(size)
               logs_button.rect.center = title_button.rect.center
               logs_button.rect.centery += 0.475*SCREEN_HEIGHT
               self.all_buttons.add(logs_button) 

               inventory_button = TextSprite(self.game,
                os.path.join(assets_dir, 'fonts', 'PressStart2P-Regular.ttf'),
                "Check inventory", 12, color = (255,255,255),tag='inventory')
               inventory_button.make_button(size)
               inventory_button.rect.center = title_button.rect.center
               inventory_button.rect.centery += 0.625*SCREEN_HEIGHT
               self.all_buttons.add(inventory_button)

        # check if any key is pressed                   

class Loading(State):
    """
    Outro state
    """
    def boot(self):
        assets_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets'))
        # add the loading text
        text = TextSprite(self.game,
                os.path.join(assets_dir, 'fonts', 'PressStart2P-Regular.ttf'),
                "Loading", 24, color = (255,255,255))
        # center text on screen
        text.rect.center = self.game.screen.get_rect().center
        # add the text to the all_sprites group
        self.all_sprites.add(text)

# add the states to the __all__ list
# this is needed so that the states can be imported using the * syntax
# the first item in the list is the default state
__all__ = ['Intro', 'Pilote','Loading'] #exclude loading
