"""
This file contains the classes for the components of the game
"""

import pygame as pg
import os

class CustomSprite(pg.sprite.Sprite):
    
    def generate_frame(self, Background = False):
        assets_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets'))
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

class ImageSprite(CustomSprite):
    """
    Sprite class for loading and displaying images
    """
    def __init__(self, game, path):
        """
        game: game object
        path: path to the image file
        """

        super().__init__()
        self.game = game
        # load the image
        self.image = pg.image.load(path)
        # set the colorkey to black
        self.image.set_colorkey((0,0,0))
        # get the rect
        self.rect = self.image.get_rect()
        

    
class ShapeSprite(CustomSprite):
    """
    Sprite class for loading and displaying images
    """
    def __init__(self, game, shape, color = (0,0,0), size = (10,10)):
        """
        game: game object
        shape: a 
        """

        super().__init__()
        self.game = game
        # draw the shape
        if shape == "rect":
            self.image = pg.Surface(size)
            self.image.fill(color)

        # get the rect
        self.rect = self.image.get_rect()        
    
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
        button_bg.image.blit(self.image,((button_bg.rect.w - self.rect.w)*0.5,(button_bg.rect.h - self.rect.h)*0.5), special_flags=pg.BLEND_PREMULTIPLIED)
        self.image = button_bg.image
        self.rect = button_bg.image.get_rect()
        

    


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

