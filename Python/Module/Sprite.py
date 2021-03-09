# Sprite
#
# Copyright (c) 2021 Hajime Saito
#
# Released under the MIT license.
# see https://opensource.org/licenses/MIT
import pygame
import math
import numpy as np
from enum import IntFlag, auto

class SpriteFlip(IntFlag):
    default = 0
    horizontal = auto()
    vertical = auto()

class SpriteBase(object):
    def __init__(self):
        pass

    def draw(self, surface, x, y, angle, scale):
        pass

class Sprite(SpriteBase):
    def __init__(self, image, left, top, width, height, flipFlag=SpriteFlip.default):
        self.width = width
        self.height = height
        self.rect = pygame.Rect(left, top, width, height)
        self.image = image.subsurface(self.rect)
        self.flipFlag = flipFlag

    def draw(self, surface, x, y, angle=0, scale=1.0, flipFlag=SpriteFlip.default):
        flipFlag ^= self.flipFlag
        if flipFlag != SpriteFlip.default:
            render_image = pygame.transform.flip(self.image, flipFlag & SpriteFlip.horizontal, flipFlag & SpriteFlip.vertical)
        else:
            render_image = self.image

        if angle != 0 or scale != 1.0:
            render_image = pygame.transform.rotozoom(render_image, angle, scale)

        surface.blit(render_image, [ int(x - render_image.get_width() // 2), int(y - render_image.get_height() // 2) ])

class LinkedSprite(SpriteBase):
    def __init__(self):
        self.sprites = []
    
    def append(self, sprite, x, y):
        self.sprites.append(( sprite, x, y ))

    def draw(self, surface, x, y, angle=0, scale=1.0, flipFlag=SpriteFlip.default):
        for sprite, sx, sy in self.sprites:
            cos = math.cos(math.radians(-angle))
            sin = math.sin(math.radians(-angle))
            rotate = np.matrix([ [ cos, -sin ], [ sin, cos ] ])
            point = np.matrix( [ [ sx * scale ], [ sy * scale ] ])
            rotatedPoint = rotate * point

            sprite.draw(surface, int(rotatedPoint[0] + x), int(rotatedPoint[1] + y), angle, scale, flipFlag)

class AnimationSprite(SpriteBase):
    def __init__(self):
        self.sprites = []
        self.animeFrameCounter = 0
        self.animeIndex = 0
        self.totalanimeFrameCounter = 0
        self.currentanimeFrameCounter = 0

    def append(self, sprite, animeFrameCounter):
        if animeFrameCounter < 0:
            raise ValueError("Invalid animation frame counter")
        self.sprites.append(( sprite, animeFrameCounter ))
        self.totalanimeFrameCounter += animeFrameCounter

    def next(self):
        around = False
        _, animeFrameCounter = self.sprites[self.animeIndex]

        self.animeFrameCounter += 1
        self.currentanimeFrameCounter += 1
        if self.animeFrameCounter >= animeFrameCounter:
            self.animeIndex += 1
            if self.animeIndex >= len(self.sprites):
                self.animeIndex = 0
                self.currentanimeFrameCounter = 0
                around = True
            self.animeFrameCounter = 0

        return around

    def prev(self):
        around = False

        _, animeFrameCounter = self.sprites[self.animeIndex]

        self.animeFrameCounter -= 1
        self.currentanimeFrameCounter -= 1
        if self.animeFrameCounter < 0:
            self.animeIndex -= 1
            if self.animeIndex <= 0:
                self.animeIndex = len(self.sprites) - 1
                self.currentanimeFrameCounter = self.totalanimeFrameCounter - 1
                around = True
            _, animeFrameCounter = self.sprites[self.animeIndex]
            self.animeFrameCounter = animeFrameCounter

        return around

    def reset(self):
        self.animeFrameCounter = 0
        self.animeIndex = 0
        self.currentanimeFrameCounter = 0

    def draw(self, surface, x, y, angle=0, scale=1.0, flipFlag=SpriteFlip.default):
        sprite, _ = self.sprites[self.animeIndex]
        if sprite is not None:
            sprite.draw(surface, x, y, angle, scale, flipFlag)
