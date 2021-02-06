# PriorityLayer
#
# Copyright (c) 2021 Hajime Saito
#
# Released under the MIT license.
# see https://opensource.org/licenses/MIT
import pygame

class PriorityLayer(object):
    def __init__(self):
        self.layerDatas = []

    def append(self, name, priority):
        if self.isDuplicated(name):
            raise ValueError("Error: duplicated layer name {}.".format(name))
        else:
            self.layerDatas.append({ "Name": name, "Priority": priority, "Objects": [] })

    def remove(self, name):
        layer = self.searchLayerDataByName(name)
        self.layerDatas.remove(layer)

    def appendObject(self, name, obj):
        layer = self.searchLayerDataByName(name)
        if len(layer) != 0:
            layer["Objects"].append(obj)

    def removeObject(self, name, obj):
        layer = self.searchLayerDataByName(name)
        if len(layer) != 0:
            layer["Objects"].remove(obj)

    def getObjects(self, name):
        layerDatas = self.searchLayerDataByName(name)
        return layerDatas["Objects"]

    def getAllObjects(self):
        return [ dic["Objects"] for dic in self.layerDatas ]

    def changeLayer(self, fromLayerName, toLayerName, obj):
        self.removeObject(fromLayerName, obj)
        self.appendObject(toLayerName, obj)

    def isDuplicated(self, name):
        return len(self.searchLayerDataByName(name)) != 0

    def searchLayerDataByName(self, name):
        layerDatas = [ dic for dic in self.layerDatas if dic.get("Name") == name ]
        return layerDatas[0] if len(layerDatas) != 0 else []

    def sortByPriority(self):
        self.layerDatas = sorted(self.layerDatas, key=lambda k: k["Priority"])

    def clearObjects(self, name):
        layer = self.searchLayerDataByName(name)
        layer["Objects"].clear()

    def clearAllObjects(self):
        for obj in [ dic["Objects"] for dic in self.layerDatas ]:
            obj.clear()
