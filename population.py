# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 12:13:32 2020

@author: Viljar Femoen
"""

class Population:

    def __init__(self, total, healthy=0, infected=0, dead=0):
        self.total=total
        self.healthy=total
        self.infected=infected
        self.dead=dead
    
    def getHealthy(self):
        return self.healthy
    
    def getTotal(self):
        return self.total

    def getInfected(self):
        return self.infected
    
    def getDead(self):
        return self.dead
    
    def isInfected(self):
        return self.infected>0
    
