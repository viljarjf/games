# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 10:48:57 2020

@author: Viljar Femoen
"""
from population import Population
from building import Building
from route import Route
import random
import weakref

class Room:

    #name: str
    #building: Building
    #population: int
    #routes: list of route names and amount ([[A, 5], [B, 85], [C, 10]])
    #coords: x and y pos for top right corner ([100,150])
    #(relative to bg image)
    #desc: str, linebreaks every 27 chars
    def __init__(self, name, building,  population, routes, coords, desc):
        self.name = name 
        self.building = building 
        self.population = Population(population) 
        self.routes = [] #list of routes  
        self.coordinates = coords 
        self.desc = desc

        for room in routes:
            self.routes.append(Route(room[0], room[1])) #appends a new route to self.routes

    def isInfected(self):
        return self.population.isInfected()

    def infect(self, amount):
        self.population.infect(amount)

