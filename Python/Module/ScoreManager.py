# ScoreManager
#
# Copyright (c) 2021 Hajime Saito
#
# Released under the MIT license.
# see https://opensource.org/licenses/MIT

class ExtendManager(object):
    def __init__(self):
        self.extendTable = None
        self.extendTableIndex = 0
        self.every = 0
        self.nextExtendScore = 0

    def init(self, extendTable, every=0):
        self.extendTable = extendTable
        self.every = every
        self.reset()

    def clear(self):
        self.extendTable = None
        self.extendTableIndex = 0
        self.every = 0
        self.nextExtendScore = 0

    def reset(self):
        self.extendTableIndex = 0
        self.nextExtendScore = self.extendTable[0]

    def isExtend(self, score):
        if score < self.nextExtendScore:
            return False

        self.extendTableIndex += 1
        if self.extendTableIndex < len(self.extendTable):
            self.nextExtendScore = self.extendTable[self.extendTableIndex]
        else:
            if self.every > 0:
                self.nextExtendScore += self.every
        return True
