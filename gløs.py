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
import math

rooms = []
#Vrimle
#R7
#R1
#R3
#Realfagbiblioteket
#F1
#Fysikkland

vrimleRoutes = [["R7", 5], ["R1", 5], ["Nanolab", 1], ["F1", 10], ["R3", 6]] #["KJL1", 5]?
Vrimle = Room("Vrimle", Building.Kjemiblokkene, 50, vrimleRoutes)
rooms.append(Vrimle)

R7Routes = [["Vrimle", 5], ["Realfagbiblioteket", 25], ["R1", 8], ["F1", 10], ["R3", 10], ["Fysikkland", 10]]
R7 = Room("R7", Building.Realfagbygget, 342, R7Routes)
rooms.append(R7)

R1Routes = [["Vrimle", 5], ["R7", 15], ["Realfagbiblioteket", 25], ["F1", 17], ["R3", 8], ["Fysikkland", 10]]
R1 = Room("R1", Building.Realfagbygget, 478, R1Routes)
rooms.append(R1)

R3Routes = [["Vrimle", 2], ["R7", 5], ["Realfagbiblioteket", 15], ["F1", 10], ["R1", 8], ["Fysikkland", 10]]
R3 = Room("R3", Building.Realfagbygget, 66, R3Routes)
rooms.append(R3)

RealfagbiblioteketRoutes = []
Realfagbiblioteket = Room("Realfagbiblioteket", Building.Realfagbygget, 700, RealfagbiblioteketRoutes)
rooms.append(Realfagbiblioteket)

F1Routes = [["Vrimle", 5], ["R7", 15], ["Realfagbiblioteket", 35], ["R1", 15], ["Fysikkland", 20], ["R3", 7]]
F1 = Room("F1", Building.ITbygget, 500, F1Routes)
rooms.append(F1)

FysikklandRoutes = [["F1", 10], ["R1", 10], ["R7", 7], ["R3", 4]]
Fysikkland = Room("Fysikkland", Building.Realfagbygget, 120, FysikklandRoutes)
rooms.append(Fysikkland)

def getRoom(roomName):
    for room in rooms:
        if room.name == roomName:
            return room
    

def move(room):
    for route in room.routes:
        fracInf = room.population.getFractionInfected()
        infected = route.amount*fracInf
        getRoom(route.destination).infect(math.ceil(infected*random.random()*random.random()/3)) #random*random/3 for each infected