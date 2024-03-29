# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 12:13:32 2020

@author: Viljar Femoen
"""

class Population:

    def __init__(self, total, healthy=0, infected=0, dead=0):
        self.__total=total
        self.__healthy=total
        self.__infected=infected
        self.__dead=dead
    
    def getHealthy(self):
        return self.__healthy
    
    def getTotal(self):
        return self.__total

    def getInfected(self):
        return self.__infected
    
    def getDead(self):
        return self.__dead
    
    def isInfected(self):
        return self.__infected > 0
    
    def isDead(self):
        return self.__dead == self.__total

    def getFractionInfected(self):
        if self.__dead != self.__total:
            return self.__healthy/(self.__total-self.__dead)
        return 0

    def infect(self, amount):
        if self.__healthy == 0:
            return
        elif self.__infected+amount <= self.__healthy:
            self.__infected += amount
            self.__healthy -= amount
        else:
            self.__healthy = 0
            self.__infected = self.__total-self.__dead
        