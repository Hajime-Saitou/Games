# Repeater
#
# Copyright (c) 2021 Hajime Saito
#
# Released under the MIT license.
# see https://opensource.org/licenses/MIT

class Repeater(object):
    def __init__(self, checker):
        self.repeatCounter = 0
        self.indexOfInterval = 0
        self.intervals = [ 20, 1 ]
        self.defaultValue = 0
        self.prevValue = 0
        self.checker = checker

    def reset(self):
        self.indexOfInterval = 0
        self.repeatCounter = self.intervals[self.indexOfInterval]
        self.prevValue = self.defaultValue

    def setDefaultValue(self, value):
        self.defaultValue = value

    def setRepeatIntervals(self, intervals):
        if not intervals:
            raise ValueError("Error: Interval list is empty.")
        for interval in intervals:
            if interval < 1:
                raise ValueError("Error: Interval sets positive value.")

        self.intervals = intervals

    def update(self, latestValue):
        repeated = self.checker(self.prevValue, latestValue)
        if not repeated:
            self.indexOfInterval = 0
        else:
            self.repeatCounter -= 1
            if self.repeatCounter > 0:
                return self.defaultValue
            else:
                self.indexOfInterval = min(self.indexOfInterval + 1, len(self.intervals) - 1)

        self.repeatCounter = self.intervals[self.indexOfInterval]
        self.prevValue = latestValue

        return latestValue

def xorChecker(prevValue, latestValue):
    return (prevValue ^ latestValue) == 0

class XorRepeater(Repeater):
    def __init__(self):
        super().__init__(xorChecker)
