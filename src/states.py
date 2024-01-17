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
        self.all_sprites.empty()
        self.all_buttons.empty()
        self.all_frames.empty()
        
        pass

    def draw(self, screen):
        """
        Called on every frame
        """
        self.all_sprites.draw(screen)
        self.all_buttons.draw(screen)
        self.all_frames.draw(screen)
        
    def draw_PiloteUI(self):
        self.menu_drawn = False
        
        #Draw map
        size_drw = (SCREEN_WIDTH*0.4, SCREEN_HEIGHT*0.8)
        map_bg = ShapeSprite(self.game,"rect", color = BLACK,size = size_drw)
        map_bg.rect.topleft = (0.05*SCREEN_WIDTH, 0.125*SCREEN_HEIGHT)
        if isinstance(self, Inventory):
            self.make_grid(map_bg, 7,6)      
        else:
            self.all_sprites.add(map_bg)
        self.all_frames.add(map_bg.generate_frame())


        #Draw right menu
        menu_shape = ShapeSprite(self.game, "rect", color = BLACK, size = size_drw)
        menu_shape.rect.topright = (0.95*SCREEN_WIDTH, 0.125*SCREEN_HEIGHT)
        menu_background = menu_shape.generate_frame(Background=True)
        self.all_sprites.add(menu_background)  

    def make_grid(self,background,row,column):
        size = background.rect.size
        square_size = size[0]/column    
        print("grid")
        for y in range(row):
            for x in range(column):
                square = ShapeSprite(self.game, "rect", color = WHITE, size = (square_size,square_size))
                square.rect.topleft = (
                    background.rect.topleft[0]+square_size*x, background.rect.topleft[1]+square_size*y)
                square.tag = x + column*y
                self.all_sprites.add(square.make_square())
                
    def draw_inventory_content(self, row, column):
        page_numb = self.inventory_page
        curr_slot = self.inv_slot
        size = SCREEN_WIDTH*0.4/column
        assets_dir = ressource_path()
        for sprite in self.all_frames:
            if sprite.tag == "inv":
                sprite.kill()   

        x_slot, y_slot = curr_slot
        for sprite in self.all_sprites:
            if sprite.tag == 'activated':
                sprite.kill()
            if sprite.tag == x_slot + column*y_slot:
                self.all_sprites.add(sprite.make_square(active = True))

    
        inventory_sheet = pg.image.load(os.path.join(assets_dir, 'images', 'sprite_sheet', 'inventory.png'))
        Inventory = self.game.memory.Player["Inventory"]
        Iron_Ore = pg.Surface.subsurface(inventory_sheet, (24*8,24*3, 24, 24))
        for y in range(row):
            for x in range(column):
                if Inventory[page_numb][y][x] != -1:
                    square = ShapeSprite(
                        self.game, "rect", color=BLACK, size=(24, 24),tag="inv")
                    square.image.fill( (255,255,255,0) )
                    match Inventory[page_numb][y][x].name:
                        case "Iron Ore":
                            square.image = Iron_Ore
                    square.image = pg.transform.scale(square.image, (size, size))
                    square.image.get_rect()
                    square.rect.topleft = (x*size + 0.05*SCREEN_WIDTH, y*size + 0.125*SCREEN_HEIGHT)

                    self.all_frames.add(square)               
        
class Intro(State):
    """
    Intro state
    """
    def boot(self):
        assets_dir = ressource_path()
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

        
    def enter(self):
        # when the state becomes the current state
        #set the current submenu to main
        self.menu_state = 'main'
        self.menu_page = 0
        self.menu_obj = 0
        self.draw_PiloteUI()
        print('enter')

    def update(self):
        # on every frame, call the update method of the base class
        super().update()
        assets_dir = ressource_path()
        
       # check which menu is currently display
        if self.menu_drawn == False:
            print(self.menu_drawn)
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
               
                   inventory_button = TextSprite(self.game,
                    os.path.join(assets_dir, 'fonts', 'PressStart2P-Regular.ttf'),
                    "Check inventory", 12, color = (255,255,255),tag='inventory')
                   inventory_button.make_button(size)
                   inventory_button.rect.center = title_button.rect.center
                   inventory_button.rect.centery += 0.475*SCREEN_HEIGHT
                   self.all_buttons.add(inventory_button) 

                   logs_button = TextSprite(self.game,
                    os.path.join(assets_dir, 'fonts', 'PressStart2P-Regular.ttf'),
                    "Check logs", 12, color = (255,255,255),tag='logs')
                   logs_button.make_button(size)
                   logs_button.rect.center = title_button.rect.center
                   logs_button.rect.centery += 0.625*SCREEN_HEIGHT
                   self.all_buttons.add(logs_button)

                   self.menu_drawn = True
               
                case 'system':
                    # Title button is not printed, but serves as an anchor and size reference for other sprites.
                    title_button = TextSprite(self.game,
                        os.path.join(assets_dir, 'fonts', 'PressStart2P-Regular.ttf'),
                        self.game.memory.Player["System"].name, 12, color = (255,255,255))
                    size = (SCREEN_WIDTH*0.4*0.9,title_button.rect.h)
                    title_button.make_button(size)
                    title_button.rect.centerx = 0.75*SCREEN_WIDTH
                    title_button.rect.top = 0
                    
                    Objects_list = self.game.memory.Galaxy.stars[self.game.memory.Player["System"].name].objects
                    nbr_planets = len(Objects_list)
                    # You can only print 4 objects at a time                 
                    
                    first_button = TextSprite(self.game,
                        os.path.join(assets_dir, 'fonts', 'PressStart2P-Regular.ttf'),
                        Objects_list[self.menu_obj].name, 12, color = (255,255,255),tag='first')
                    first_button.make_button(size)
                    first_button.rect.center = title_button.rect.center
                    first_button.rect.centery += 0.175*SCREEN_HEIGHT
                    self.all_buttons.add(first_button)                                            

                    if nbr_planets >= 2+self.menu_obj:
                        second_button = TextSprite(self.game,
                            os.path.join(assets_dir, 'fonts', 'PressStart2P-Regular.ttf'),
                            Objects_list[self.menu_obj +1].name, 12, color = (255,255,255),tag='second')
                        second_button.make_button(size)
                        second_button.rect.center = title_button.rect.center
                        second_button.rect.centery += 0.325*SCREEN_HEIGHT
                        self.all_buttons.add(second_button)
                    
                    if nbr_planets >= 3+self.menu_obj:
                        third_button = TextSprite(self.game,
                            os.path.join(assets_dir, 'fonts', 'PressStart2P-Regular.ttf'),
                            Objects_list[self.menu_obj +2].name, 12, color = (255,255,255),tag='third')
                        third_button.make_button(size)
                        third_button.rect.center = title_button.rect.center
                        third_button.rect.centery += 0.475*SCREEN_HEIGHT
                        self.all_buttons.add(third_button) 
                    
                    if nbr_planets >= 4+self.menu_obj:
                        fourth_button = TextSprite(self.game,
                            os.path.join(assets_dir, 'fonts', 'PressStart2P-Regular.ttf'),
                            Objects_list[self.menu_obj +3].name, 12, color = (255,255,255),tag='fourth')
                        fourth_button.make_button(size)
                        fourth_button.rect.center = title_button.rect.center
                        fourth_button.rect.centery += 0.625*SCREEN_HEIGHT
                        self.all_buttons.add(fourth_button)

                    size_arrow = (title_button.rect.h,title_button.rect.h)
                    if self.menu_obj > 0:
                        left_arrow = make_arrow(self.game, 'left', size_arrow)
                        
                        left_arrow.rect.center = title_button.rect.center
                        left_arrow.rect.centery += 0.775*SCREEN_HEIGHT
                        left_arrow.rect.centerx -= 0.125*SCREEN_WIDTH
                                                
                        self.all_buttons.add(left_arrow)
                        
                    if self.menu_obj +3 < nbr_planets-1:
                        right_arrow = make_arrow(self.game, 'right',size_arrow)
                        
                        right_arrow.rect.center = title_button.rect.center
                        right_arrow.rect.centery += 0.775*SCREEN_HEIGHT
                        right_arrow.rect.centerx += 0.125*SCREEN_WIDTH

                        self.all_buttons.add(right_arrow)   

                    back_arrow = make_arrow(self.game, 'back',size_arrow)
                        
                    back_arrow.rect.center = title_button.rect.center
                    back_arrow.rect.centery += 0.775*SCREEN_HEIGHT
                    
                    self.all_buttons.add(back_arrow)                    

                    self.menu_drawn = True
                    
                    

       # check if any key is pressed
        if self.game.input.is_mouse_pressed(1):
                print("Mouse press")
                mouse_pos = pg.mouse.get_pos()
                # Check case
                match self.menu_state:
                    case 'main':
                        for button in self.all_buttons:
                            if button.rect.collidepoint(mouse_pos) and button.tag == 'enter':
                                self.menu_state = 'system'
                                self.all_buttons.empty()
                                self.menu_drawn = False
                            # Check for Option 2
                            elif button.rect.collidepoint(mouse_pos) and button.tag == 'travel':
                                print("Travel")
                            # Check for Option 3
                            elif button.rect.collidepoint(mouse_pos) and button.tag == 'logs':
                                print("Logs")    
                            elif button.rect.collidepoint(mouse_pos) and button.tag == 'inventory':
                                self.game.change_state('Inventory')
                                print("Inventory")         

                    case 'system':
                        for button in self.all_buttons:
                            Objects_list = self.game.memory.Galaxy.stars[self.game.memory.Player["System"].name].objects
                            if button.rect.collidepoint(mouse_pos) and button.tag == 'first':
                                print("first")
                                self.game.memory.move_player(self.game.memory.Player["System"], obj = Objects_list[self.menu_obj])
                                self.game.change_state('Surface')
                                
                            # Check for Option 2
                            elif button.rect.collidepoint(mouse_pos) and button.tag == 'second':
                                print("second")
                                self.game.memory.move_player(self.game.memory.Player["System"], obj=Objects_list[self.menu_obj + 1])
                                self.game.change_state('Surface')
                                
                            # Check for Option 3
                            elif button.rect.collidepoint(mouse_pos) and button.tag == 'third':
                                print("third")
                                self.game.memory.move_player(
                                    self.game.memory.Player["System"], obj=Objects_list[self.menu_obj + 2])
                                self.game.change_state('Surface')
                                
                            elif button.rect.collidepoint(mouse_pos) and button.tag == 'fourth':
                                #self.game.change_state('Outro')
                                print("fourth")
                                self.game.memory.move_player(
                                    self.game.memory.Player["System"], obj=Objects_list[self.menu_obj + 3])
                                self.game.change_state('Surface')
                                
                            elif button.rect.collidepoint(mouse_pos) and button.tag == 'back':
                                print("Back")
                                self.menu_state = 'main'
                                self.all_buttons.empty()
                                self.menu_obj = 0
                                self.menu_drawn = False
                                
                            elif button.rect.collidepoint(mouse_pos) and button.tag == 'left':
                                print("Left")
                                self.all_buttons.empty()
                                self.menu_drawn = False
                                self.menu_obj -= 4
                                
                            elif button.rect.collidepoint(mouse_pos) and button.tag == 'right':
                                print("right")
                                self.all_buttons.empty()
                                self.menu_drawn = False
                                self.menu_obj += 4

class Surface(State):
    """
    Surface state
    """

    def boot(self):
        print("Surface")


    def enter(self):
        # when the state becomes the current state
        #set the current submenu to main
        self.menu_state = 'main'
        self.menu_square = 0
        print('surface')
        self.draw_PiloteUI()
        print(self.game.memory.Player["Object"].name)
        
    def update(self):
        # on every frame, call the update method of the base class
        super().update()
        assets_dir = ressource_path()
        
       # check which menu is currently display
        if self.menu_drawn == False:
            match self.menu_state:
                case 'main':
                    # Title button is
                    title_button = TextSprite(self.game,
                        os.path.join(assets_dir, 'fonts', 'PressStart2P-Regular.ttf'),
                        self.game.memory.Player["Object"].name, 12, color = (255,255,255))
                    size = (SCREEN_WIDTH*0.4*0.9,title_button.rect.h)
                    title_button.make_button(size)
                    title_button.rect.centerx = 0.75*SCREEN_WIDTH
                    title_button.rect.top = 0.15*SCREEN_HEIGHT
                    self.all_sprites.add(title_button)
                    
                    obj = self.game.memory.Player["Object"]
                    Checkboard = obj.grid
                    build_button = TextSprite(self.game,
                            os.path.join(assets_dir, 'fonts', 'PressStart2P-Regular.ttf'),
                            "Scan surface", 12, color=(255, 255, 255),tag='build')
                    build_button.make_button(size)
                    build_button.rect.center = title_button.rect.center
                    build_button.rect.centery += 0.175*SCREEN_HEIGHT
                    
                    leave_button = TextSprite(self.game,
                        os.path.join(assets_dir, 'fonts', 'PressStart2P-Regular.ttf'),
                        "Leave orbit", 12, color=(255, 255, 255),tag='leave')
                    leave_button.make_button(size)
                    leave_button.rect.center = title_button.rect.center
                    leave_button.rect.centery += 0.325*SCREEN_HEIGHT
                    
                    inventory_button = TextSprite(self.game,
                        os.path.join(assets_dir, 'fonts', 'PressStart2P-Regular.ttf'),
                        "Inventory", 12, color=(255, 255, 255),tag='inventory')
                    inventory_button.make_button(size)
                    inventory_button.rect.center = title_button.rect.center
                    inventory_button.rect.centery += 0.475*SCREEN_HEIGHT

                    if obj.populated == True:
                        trade_button = TextSprite(self.game,
                            os.path.join(assets_dir, 'fonts', 'PressStart2P-Regular.ttf'),
                            "Trade", 12, color=(255, 255, 255),tag='trade')
                        trade_button.make_button(size)
                        trade_button.rect.center = title_button.rect.center
                        trade_button.rect.centery += 0.175*SCREEN_HEIGHT
                        build_button.rect.centery += 0.150*SCREEN_HEIGHT
                        leave_button.rect.centery += 0.150*SCREEN_HEIGHT
                        inventory_button.rect.centery += 0.150*SCREEN_HEIGHT
                        self.all_buttons.add(trade_button)
                    
                    self.all_buttons.add(build_button)
                    self.all_buttons.add(leave_button)
                    self.all_buttons.add(inventory_button)
                    self.menu_drawn = True
                    
       # check if any key is pressed
        if self.game.input.is_mouse_pressed(1):
            print("Mouse press")
            mouse_pos = pg.mouse.get_pos()
            # Check if the mouse click is within the region of Option 1
            for button in self.all_buttons:
                if button.rect.collidepoint(mouse_pos) and button.tag == 'build':
                    self.menu_state = 'build'
                    self.menu_drawn = False
                    self.all_buttons.empty()
                    print("Scan surface")
                # Check for Option 2
                elif button.rect.collidepoint(mouse_pos) and button.tag == 'leave':
                    print("Leave orbit")
                    self.game.change_state('Pilote')
                # Check for Option 3
                elif button.rect.collidepoint(mouse_pos) and button.tag == 'inventory':
                    self.game.change_state('Inventory')
                elif button.rect.collidepoint(mouse_pos) and button.tag == 'trade':
                    self.menu_state = 'trade'
                    self.menu_drawn = False
                    self.all_buttons.empty()
                    print("Trade")

class Inventory(State):
    """
    Inventory state
    """
    def enter(self):
        # when the state becomes the current state
        self.menu_state = 'main'
        self.inventory_page = 0
        self.menu_square = 0
        self.draw_PiloteUI()
        self.inv_slot = [0,0]
        print('inventory')
        
    def update(self):
        # on every frame, call the update method of the base class
        super().update()
        assets_dir = ressource_path()
        

        if self.menu_drawn == False:
            Inventory = self.game.memory.Player["Inventory"]
            self.draw_inventory_content(7, 6)
            match self.menu_state:
                case 'main':
                    # Check what is the selected item
                    text = Inventory[self.inventory_page][self.inv_slot[1]][self.inv_slot[0]].name
                    title_button = TextSprite(self.game,
                        os.path.join(assets_dir, 'fonts', 'PressStart2P-Regular.ttf'),
                        text, 12, color = (255,255,255))
                    size = (SCREEN_WIDTH*0.4*0.9,title_button.rect.h)
                    title_button.make_button(size)
                    title_button.rect.centerx = 0.75*SCREEN_WIDTH
                    title_button.rect.top = 0.15*SCREEN_HEIGHT
                    
                    self.all_sprites.add(title_button)
                    
                    size_arrow = (title_button.rect.h,title_button.rect.h)
                    if self.inventory_page > 0:
                        left_arrow = make_arrow(self.game, 'left', size_arrow)
                        
                        left_arrow.rect.center = title_button.rect.center
                        left_arrow.rect.centery += 0.65*SCREEN_HEIGHT
                        left_arrow.rect.centerx -= 0.625*SCREEN_WIDTH      
                        
                        self.all_buttons.add(left_arrow)
                        
                    if self.inventory_page < len(Inventory)-1:
                        print(len(Inventory))
                        right_arrow = make_arrow(self.game, 'right',size_arrow)
                        right_arrow.rect.center = title_button.rect.center
                        right_arrow.rect.centery += 0.65*SCREEN_HEIGHT
                        right_arrow.rect.centerx -= 0.375*SCREEN_WIDTH

                        self.all_buttons.add(right_arrow)   

                    back_arrow = make_arrow(self.game, 'back',size_arrow)   
                    back_arrow.rect.center = title_button.rect.center
                    back_arrow.rect.centery += 0.65*SCREEN_HEIGHT
                    back_arrow.rect.centerx -= 0.5*SCREEN_WIDTH
                    
                    self.all_buttons.add(back_arrow)                    

            self.menu_drawn = True  
        # check if any key is pressed
        if self.game.input.is_key_pressed('any'):
            if self.game.input.is_key_down('left') and self.inv_slot[0] > 0:
                self.inv_slot[0] -= 1
                self.menu_drawn = False
            if self.game.input.is_key_down('right') and self.inv_slot[0] < 5:
                self.inv_slot[0] += 1
                self.menu_drawn = False   
            if self.game.input.is_key_down('up') and self.inv_slot[1] > 0:
                self.inv_slot[1] -= 1
                self.menu_drawn = False
            if self.game.input.is_key_down('down') and self.inv_slot[1] < 6:
                self.inv_slot[1] += 1
                self.menu_drawn = False
        
        if self.game.input.is_mouse_pressed(1):
            pos = pg.mouse.get_pos()
            for sprite in self.all_sprites:
                if sprite.tag in range(0, 42) and sprite.rect.collidepoint(pos):
                    self.menu_drawn = False
                    self.inv_slot = [sprite.tag % 6, sprite.tag//6]
            for sprite in self.all_buttons:
                if sprite.tag == 'back' and sprite.rect.collidepoint(pos):
                    self.menu_drawn = False
                    print('back')
                    self.game.change_state('Pilote')
                    

            

class Loading(State):
    """
    Loading screen state (Unused yet)
    """
    def boot(self):
        assets_dir = ressource_path()
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
__all__ = ['Intro', 'Pilote','Surface','Inventory'] #exclude loading
