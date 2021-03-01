# PygameApplication
#
# Copyright (c) 2021 Hajime Saito
#
# Released under the MIT license.
# see https://opensource.org/licenses/MIT
import os
import sys
import pygame

class PygameApplication(object):
    def __init__(self, surfaceWidth, surfaceHeight, fullScreen=False, caption="Pygame Application"):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        pygame.mixer.pre_init(buffer=128)
        pygame.mixer.init()

        pygame.display.set_caption(caption)
        self.surfaceSize = ( surfaceWidth, surfaceHeight )
        self.isFullScreen = False
        self.displayFlags = pygame.DOUBLEBUF | pygame.HWSURFACE
        self.surface = pygame.display.set_mode(self.surfaceSize, flags=self.displayFlags)

        self.backSurfaceSize = None
        self.backSurface = None
        self.hasBackSurface = False

        self.timeClock = pygame.time.Clock()
        self.frameCounter = 0

        # Does not create a fullscreen display directly, for centering a window.
        if fullScreen:
            self.toggleFullScreen()

    def createBackSurface(self, surfaceWidth, surfaceHeight):
        self.backSurfaceSize = ( surfaceWidth, surfaceHeight )
        self.backSurface = pygame.Surface(self.backSurfaceSize)
        self.hasBackSurface = True

    def toggleFullScreen(self):
        self.displayFlags ^= pygame.FULLSCREEN
        self.surface = pygame.display.set_mode(self.surfaceSize, flags=self.displayFlags)
        self.isFullScreen = not self.isFullScreen

        return self.isFullScreen

    def update(self, tick=60):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    self.toggleFullScreen()
                if event.key == pygame.K_ESCAPE:
                    self.quit()
                    sys.exit()

        if self.hasBackSurface:
            self.surface.blit(pygame.transform.scale(self.backSurface, self.surfaceSize), ( 0, 0 ))
        pygame.display.flip()
        self.timeClock.tick(tick)
        self.frameCounter += 1

    def quit(self):
        pygame.quit()
