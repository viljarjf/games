# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 10:48:57 2020

@author: Viljar Femoen
"""
from population import Population
from building import Building
from route import Route
import random

class Room:

    #name: str
    #region: Region
    #population: int
    #routes: list of route names and amount ([[A, 5], [B, 100])
    def __init__(self, name, building,  population, routes):
        self.name = name 
        self.building = building 
        self.population = Population(population) 
        self.routes = [] #list of routes  

        for room in routes:
            self.routes.append(Route(self.name, room[0], room[1])) #appends a new route to self.routes


    def isInfected(self):
        return self.population.isInfected()
    