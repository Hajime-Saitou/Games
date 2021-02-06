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
        self.every = False
        self.nextExtendScore = 0

    def init(self, extendTable, every=False):
        self.extendTable = extendTable
        self.every = every
        self.reset()

    def clear(self):
        self.extendTable = None
        self.extendTableIndex = 0
        self.every = False
        self.nextExtendScore = 0

    def reset(self):
        self.extendTableIndex = 0
        self.nextExtendScore = self.extendTable[0]

    def isExtend(self, score):
        print("next: " + str(self.nextExtendScore))

        if self.extendTableIndex == len(self.extendTable):
            return False

        if score < self.nextExtendScore:
            return False

        self.extendTableIndex += 1
        print("index: " + str(self.extendTableIndex))
        if self.extendTableIndex == len(self.extendTable):
            if self.every:
                self.extendTableIndex = min(self.extendTableIndex, len(self.extendTable) - 1)
                self.nextExtendScore += self.extendTable[self.extendTableIndex]
        else:
            self.nextExtendScore = self.extendTable[self.extendTableIndex]

        return True
