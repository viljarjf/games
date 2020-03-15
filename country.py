# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 10:48:57 2020

@author: Viljar Femoen
"""
from population import Population

class Country:

    def __init__(self, name, region,  population, airports, ports, borders):
        self.name = name #str
        self.region = region #region
        self.population = Population(population) # int
        self.airports = airports #list of airports
        self.ports = ports # list of ports
        self.borders = borders #list of countries

    def isInfected(self):
        return self.population.isInfected()
    
     