# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 16:57:15 2020

@author: Viljar Femoen
"""
from population import Population
from building import Building
from route import Route
from room import Room
import random

rooms = []

vrimleRoutes = [["R7", 5], ["R1", 5], ["Nanolab", 1], ["F1", 10], ["KJL1", 5], ["R3", 6]]
Vrimle = Room("Vrimle", Building.Kjemiblokkene, 50, vrimleRoutes)
rooms.append(Vrimle)

def getRoom(roomName):
    for room in rooms:
        if room.name == roomName:
            return room
    

def move(room):
    for route in room.routes:
        fracInf = room.population.getFractionInfected()
        infected = route.amount*fracInf
        getRoom(route.destination).infect(int(infected*random.random()))