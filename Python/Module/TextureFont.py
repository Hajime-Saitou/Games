# TextureFont
#
# Copyright (c) 2021 Hajime Saito
#
# Released under the MIT license.
# see https://opensource.org/licenses/MIT
import pygame

class TextureFont(object):
    def __init__(self, texture, fontSize, pixelOffset=( 0, 0 ), rows=16, lines=16):
        self.texture = texture
        self.fontSize = fontSize
        self.pixelOffset = pixelOffset
        self.rows = rows
        self.lines = lines
        self.cacheRects = self.createCacheRects()

    def createCacheRects(self):
        rects = []
        for y in range(self.lines):
            top = y * self.fontSize[1] + self.pixelOffset[1]
            for x in range(self.rows):
                left = x * self.fontSize[0] + self.pixelOffset[0]
                rects.append(self.createRects(left, top))
        return rects

    def createRects(self, left, top):
        return pygame.Rect(left, top, self.fontSize[0], self.fontSize[1])

    def drawChar(self, surface, left, top, ch):
        surface.blit(self.texture, ( left, top ), self.cacheRects[ch])

    def drawString(self, surface, left, top, string):
        for i in range(len(string)):
            self.drawChar(surface, i * self.fontSize[0] + left, top, ord(string[i]) & 0xff)
