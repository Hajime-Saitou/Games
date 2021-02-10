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

class HighScoreRankingManager(object):
    def __init__(self, validKeys, maxRecordCount=10):
        if not "Score" in validKeys:
            raise KeyError("Error: Do not have the key 'Score'.")

        self.validKeys = validKeys
        self.highScoreRecords = []

        if maxRecordCount < 1:
            raise ValueError("Error: Max record count sets positive value.")
        self.maxRecordCount = maxRecordCount

    def append(self, newRecord):
        if newRecord.keys() ^ self.validKeys:
            raise KeyError("Error: The number of keys does not match.")
        if not self.isRankIn(newRecord["Score"]):
            return -1

        self.highScoreRecords.append(newRecord)
        self.sortDesendingByScore()
        return self.getNewRecordPosition(newRecord)

    def sortDesendingByScore(self):
        self.highScoreRecords = sorted(self.highScoreRecords, key=lambda k: k["Score"], reverse=True)[:self.maxRecordCount]

    def getNewRecordPosition(self, newRecord):
        for position, record in enumerate(self.highScoreRecords):
            if record == newRecord:
                return position

        return -1

    def isExceedTopScore(self, score):
        return score >= self.highScoreRecords[0]["Score"]

    def isRankIn(self, score):
        if len(self.highScoreRecords) < self.maxRecordCount:
            return True
        return score >= self.highScoreRecords[-1]["Score"]

    def getPrivisionalRanks(self, records):
        provisionalRanks = [ None ] * len(records)
        provisionalRecords = sorted(self.highScoreRecords + records, key=lambda k: k["Score"], reverse=True)[:self.maxRecordCount]
        for index, record in enumerate(records):
            provisionalRanks[index] = provisionalRecords.index(record) if record in provisionalRecords else -1

        return provisionalRanks
