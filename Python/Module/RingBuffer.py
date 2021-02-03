# RingBuffer
#
# Copyright (c) 2021 Hajime Saito
#
# Released under the MIT license.
# see https://opensource.org/licenses/MIT
import copy

class RingBuffer(object):
    def __init__(self, size):
        self.size = size
        self.buffer = [ None ] * size
        self.index = 0

    def setValue(self, value):
        self.index = (self.index + 1) % self.size
        self.buffer[self.index] = value

    def getValue(self, index):
        return self.buffer[(self.index + index) % self.size]
