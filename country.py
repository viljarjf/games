# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 10:48:57 2020

@author: Viljar Femoen
"""
from population import Population
from region import Region
from port import Port

class Country:

    #name: str
    #region: Region
    #population: int
    #airports: list of country names and probabilities ([[A, 0.5], [B, 0.1])
    #seaports: list of country names and probabilities ([[A, 0.5], [B, 0.1])
    #borders: list of names of bordering countries
    def __init__(self, name, region,  population, airports, seaports, borders):
        self.name = name 
        self.region = region 
        self.population = Population(population) 
        self.ports = [] #list of port destinations and probabilities
        self.borders = borders 

        for country in airports+seaports:
            self.ports.append(Port(self.name, country[0], country[1])) #appends a new port route to ports


    def isInfected(self):
        return self.population.isInfected()
    
    