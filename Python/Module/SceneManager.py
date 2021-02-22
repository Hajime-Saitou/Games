# SceneManager
#
# Copyright (c) 2021 Hajime Saito
#
# Released under the MIT license.
# see https://opensource.org/licenses/MIT
class SceneManager(object):
    def __init__(self):
        self.currentScene = None
        self.nextScene = None
        self.frameCounter = 0

    def reset(self):
        self.currentScene = None
        self.nextScene = None
        self.frameCounter = 0

    def change(self, nextScene):
        self.nextScene = nextScene

    def update(self):
        if self.currentScene != self.nextScene:
            self.currentScene = self.nextScene
            self.frameCounter = 0
        else:
            self.frameCounter += 1
