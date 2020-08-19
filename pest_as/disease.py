# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 21:38:20 2020

@author: Viljar Femoen
"""

#making abstract classes in python seems strange. 
#This will therefore be a base class, but not abstract. 
class Disease:


    def __init__(self, infectivity, severity, lethality):
        self.infectivity = infectivity
        self.severity = severity
        self.lethality = lethality
        self.upgrades = []

    def upgrade(self, infectivity, severity, lethality):
        self.infectivity += infectivity
        self.severity += severity
        self.lethality += lethality

class Upgrade:

    def __init__(self):
    
    