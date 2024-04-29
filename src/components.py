"""
This file contains the classes for the components of the game
"""

import pygame as pg
import os
import sys
import math 

def ressource_path():
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, "assets")

class CustomSprite(pg.sprite.Sprite):
    
    def generate_frame(self, Background = False):
        assets_dir = ressource_path()
        if Background == False:
            frame = ImageSprite(self.game, os.path.join(assets_dir, 'images','UI', 'frame_map.png'))
        elif Background == True:
            frame = ImageSprite(self.game, os.path.join(assets_dir, 'images','UI','background_menu.png'))
        size = (self.image.get_width() + 32,self.image.get_height() + 32)
        frame.image = slice_sprite(frame.image, 32, 32, 27, 38, size[0],size[1])    
        frame.rect = frame.image.get_rect()
        frame.rect.center = self.rect.center
        frame.rect.centery += 5
        return frame
    
    def make_square(self,active=False):
        assets_dir = ressource_path()
        if active == True:
            square = ImageSprite(self.game, os.path.join(
                assets_dir, 'images', 'UI', 'square_A.png'),tag="activated")
        else:
            square = ImageSprite(self.game, os.path.join(
                assets_dir, 'images', 'UI', 'square_I.png'))
        square.image.convert_alpha()
        size = self.rect.size
        square.image = slice_sprite(square.image, 7, 7, 1, 7, size[0], size[1])
        square.rect = square.image.get_rect()
        square.rect.center = self.rect.center
        if active == False:
            square.tag = self.tag
        return square

class ImageSprite(CustomSprite):
    """
    Sprite class for loading and displaying images
    """
    def __init__(self, game, path,tag=''):
        """
        game: game object
        path: path to the image file
        """

        super().__init__()
        self.game = game
        # load the image
        self.image = pg.image.load(path).convert_alpha()
        # set the colorkey to black
        self.image.set_colorkey((0,0,0))
        # get the rect
        self.rect = self.image.get_rect()
        self.tag = tag
    
class ShapeSprite(CustomSprite):
    """
    Sprite class for loading and displaying images
    """
    def __init__(self, game, shape, color = (0,0,0), size = (10,10),tag=''):
        """
        game: game object
        shape: a 
        """

        super().__init__()
        self.game = game
        # draw the shape
        if shape == "rect":
            self.image = pg.Surface(size, pg.SRCALPHA)
            self.image.fill(color)

        # get the rect
        self.rect = self.image.get_rect() 
        self.tag = tag
    
class TextSprite(pg.sprite.Sprite):
    """
    Sprite class for displaying text
    """
    def __init__(self, game, font_path, text="", size = 10, color = (0, 0, 0),tag=''):
        """
        game: game object
        font_path: path to the font file
        text: text to display
        size: font size
        color: font color
        tag: a tag to identify the sprite easily
        """
        super().__init__()
        self.game = game
        self.font_path = font_path
        self.draw_text(text, size, color)
        self.tag = tag

    def draw_text(self, text, size = 10, color = (0,0,0), alias = True):
        """
        Draw the text

        text: text to display
        size: font size
        color: font color
        alias: whether to use anti-aliasing
        """
        self.text = text
        self.image = self.get_font_size(size).render(text, alias, color)
        self.rect = self.image.get_rect()

    def get_font_size(self, size):
        """
        Get the font object with the given size
        """
        return pg.font.Font(self.font_path, size)

    def make_button(self, size):
        shape = ShapeSprite(self.game,'rect',size=size)
        button_bg = shape.generate_frame(Background=True)
        button_bg.image.blit(self.image,((button_bg.rect.w - self.rect.w)*0.5,(button_bg.rect.h - self.rect.h)*0.5 -5), special_flags=pg.BLEND_PREMULTIPLIED)
        self.image = button_bg.image
        self.image.set_colorkey((0,0,0))
        self.rect = button_bg.image.get_rect()
        
class MapSprite(CustomSprite):
    def __init__(self, game, map_bg):
        super().__init__()
        self.game = game
        self.rect = map_bg.rect.copy()
        self.rect.h = map_bg.rect.w
        self.draw_map()
        self.tag = "map overlay"

    def draw_map(self):
        surface = pg.Surface(self.rect.size, pg.SRCALPHA)
        camera_pos = self.game.memory.Galaxy.camera_pos
        starSprite = TextSprite(self.game, os.path.join(ressource_path(), 'fonts', 'PressStart2P-Regular.ttf'), "*", 10, color = (255,255,255))
        CurStarSprite = TextSprite(self.game, os.path.join(ressource_path(), 'fonts', 'PressStart2P-Regular.ttf'), "[*]", 10, color = (255,255,255))

        ind = 0
        self.game.memory.Galaxy.select_visible_star()
        PrevStars = []
        print(self.game.memory.Galaxy.visible_stars)
        for star in self.game.memory.Galaxy.stars.values():
            if self.game.memory.Galaxy.visible_stars[ind]:
                pos = [(star.coordinates[0] - self.game.memory.Galaxy.camera_pos[0])*(self.rect.w/self.game.memory.Galaxy.current_zoom), (star.coordinates[1] - self.game.memory.Galaxy.camera_pos[1])*(self.rect.w/self.game.memory.Galaxy.current_zoom)]
                if star != self.game.memory.Player["System"]:
                    printpos = [pos[0] - starSprite.rect.w/2, pos[1] - starSprite.rect.h/2]
                    surface.blit(starSprite.image, printpos, special_flags=pg.BLEND_PREMULTIPLIED)
                else:
                    printpos = [pos[0] - CurStarSprite.rect.w/2, pos[1] - CurStarSprite.rect.h/2]
                    surface.blit(CurStarSprite.image, printpos, special_flags=pg.BLEND_PREMULTIPLIED)
                PrevStars.append(star)
                for i in range(0, ind):
                    if self.game.memory.Galaxy.vs_way[ind][i]:
                        pos2 = [(PrevStars[i].coordinates[0] - self.game.memory.Galaxy.camera_pos[0])*(self.rect.w/self.game.memory.Galaxy.current_zoom), (PrevStars[i].coordinates[1] - self.game.memory.Galaxy.camera_pos[1])*(self.rect.w/self.game.memory.Galaxy.current_zoom)]
                        #pg.draw.line(surface, "White", pos,pos2)
                        draw_dashed_line(surface, "White", pos, pos2, 0)
            ind += 1

        self.image = surface
        
    


#From Kokoko @stackoverflow

def slice_sprite(sprite, left, right, top, bottom, width, height, draw_mode="SLICED"):
    # get the size of the sprite
    sprite_width = sprite.get_width()
    sprite_height= sprite.get_height()

    if height < top + bottom:
        height = top+bottom
    if width < top + bottom:
        width = top+bottom
    

    # create a new surface to draw the sliced sprite on
    sliced_sprite = pg.Surface((width, height),pg.SRCALPHA)

    # draw the top left side of the sprite
    sliced_sprite.blit(sprite, (0, 0), (0, 0, left, top),special_flags = pg.BLEND_PREMULTIPLIED)

    # draw the top right side of the sprite
    sliced_sprite.blit(sprite, (width - right, 0),
                       (sprite_width - right, 0, right, top),special_flags = pg.BLEND_PREMULTIPLIED)

    # draw the bottom left side of the sprite
    sliced_sprite.blit(sprite, (0, height - bottom),
                       (0, sprite_height - bottom, left, bottom),special_flags = pg.BLEND_PREMULTIPLIED)

    # draw the bottom right side of the sprite
    sliced_sprite.blit(sprite, (width - right, height - bottom),
                       (sprite_width - right, sprite_height - bottom, right, bottom),special_flags = pg.BLEND_PREMULTIPLIED)

    match draw_mode:
        case "SLICED":
            # scale top and bottom sides of the sprite
            sliced_sprite.blit(pg.transform.scale(sprite.subsurface(
                left, 0, sprite_width - left - right, top), (width - left - right, top)), (left, 0),special_flags = pg.BLEND_PREMULTIPLIED)
            sliced_sprite.blit(pg.transform.scale(sprite.subsurface(left, sprite_height - bottom,
                               sprite_width - left - right, bottom), (width - left - right, bottom)), (left, height - bottom),special_flags = pg.BLEND_PREMULTIPLIED)

            # scale the center of the sprite
            sliced_sprite.blit(pg.transform.scale(sprite.subsurface(left, top, sprite_width - left - right,
                               sprite_height - top - bottom), (width - left - right, height - top - bottom)), (left, top),special_flags = pg.BLEND_PREMULTIPLIED)

            # scale left and right sides of the sprite
            sliced_sprite.blit(pg.transform.scale(sprite.subsurface(
                0, top, left, sprite_height - top - bottom), (left, height - top - bottom)), (0, top),special_flags = pg.BLEND_PREMULTIPLIED)
            sliced_sprite.blit(pg.transform.scale(sprite.subsurface(sprite_width - right, top, right,
                               sprite_height - top - bottom), (right, height - top - bottom)), (width - right, top),special_flags = pg.BLEND_PREMULTIPLIED)

        case "TILED":
            # tile the center of the sprite
            for x in range(left, width - right, sprite_width - left - right):
                for y in range(top, height - bottom, sprite_height - top - bottom):
                    sliced_sprite.blit(sprite.subsurface(
                        left, top, sprite_width - left - right, sprite_height - top - bottom), (x, y),special_flags = pg.BLEND_PREMULTIPLIED)

            # tile top and bottom sides of the sprite
            for x in range(left, width - right, sprite_width - left - right):
                sliced_sprite.blit(sprite.subsurface(
                    left, 0, sprite_width - left - right, top), (x, 0),special_flags = pg.BLEND_PREMULTIPLIED)
                sliced_sprite.blit(sprite.subsurface(
                    left, sprite_height - bottom, sprite_width - left - right, bottom), (x, height - bottom),special_flags = pg.BLEND_PREMULTIPLIED)

            # tile left and right sides of the sprite
            for y in range(top, height - bottom, sprite_height - top - bottom):
                sliced_sprite.blit(sprite.subsurface(
                    0, top, left, sprite_height - top - bottom), (0, y),special_flags = pg.BLEND_PREMULTIPLIED)
                sliced_sprite.blit(sprite.subsurface(
                    sprite_width - right, top, right, sprite_height - top - bottom), (width - right, y),special_flags = pg.BLEND_PREMULTIPLIED)

            # draw the corners of the sprite
            sliced_sprite.blit(sprite.subsurface(0, 0, left, top), (0, 0),special_flags = pg.BLEND_PREMULTIPLIED)
            sliced_sprite.blit(sprite.subsurface(
                sprite_width - right, 0, right, top), (width - right, 0),special_flags = pg.BLEND_PREMULTIPLIED)
            sliced_sprite.blit(sprite.subsurface(
                0, sprite_height - bottom, left, bottom), (0, height - bottom),special_flags = pg.BLEND_PREMULTIPLIED)
            sliced_sprite.blit(sprite.subsurface(
                sprite_width - right, sprite_height - bottom, right, bottom), (width - right, height - bottom),special_flags = pg.BLEND_PREMULTIPLIED)

    return sliced_sprite

def make_arrow(game, direction, size):
    assets_dir = ressource_path()
    button = ImageSprite(game, os.path.join(assets_dir, 'images', 'UI', direction+'.png'), tag=direction)
    button.image = slice_sprite(button.image, 34, 34, 29, 39, 1.5*size[0],1.5*size[1])
    button.image.set_colorkey((0,0,0))
    button.rect = button.image.get_rect()
    return button


#Adapted from galatolofederico @Github 
def blit_text(surface, text, pos, font, color=pg.Color('white')):
    words = [word.split(' ') for word in text.splitlines()] 
    space = font.size(' ')[0]
    max_width, max_height = surface.get_width(), surface.get_height()
    x, y = pos
    rects = []
    row_rects = []
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]
                rects.append(row_rects)
                row_rects = []
            row_rects.append(word)
            x += word_width + space
        x = pos[0]
        rects.append(row_rects)
        row_rects = []

    max_vertical_rects = math.floor(max_height / font.size(' ')[1])
    printable_rects = rects[-max_vertical_rects:]
    for line in printable_rects:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]
        y += word_height*1.1
 

#Adapted from Rabbid76 @ StackOverflow
def draw_dashed_line(surf, color, p1, p2, prev_line_len, dash_length=8):
    dx, dy = p2[0]-p1[0], p2[1]-p1[1]
    if dx == 0 and dy == 0:
        return 
    dist = math.hypot(dx, dy)
    dx /= dist
    dy /= dist

    step = dash_length*2
    start = (int(prev_line_len) // step) * step
    end = (int(prev_line_len + dist) // step + 1) * step
    for i in range(start, end, dash_length*2):
        s = max(0, start - prev_line_len + i)
        e = min(start - prev_line_len + dash_length + i, dist)
        if s < e:
            ps = p1[0] + dx * s, p1[1] + dy * s 
            pe = p1[0] + dx * e, p1[1] + dy * e 
            pg.draw.line(surf, color, pe, ps)


def draw_dashed_lines(surf, color, points, dash_length=8):
    p1, p2 = points[0], points[1]
    line_len = 0
    dist = dash_length*2
    while line_len < math.hypot(points[0][0] - points[1][0],points[0][1]-points[1][1]):
        print(math.hypot(p1[0] - p2[0],p1[1]-p2[1]), line_len)
        draw_dashed_line(surf, color, p1, p2, line_len, dash_length)
        line_len += dist