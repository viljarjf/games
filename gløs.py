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
#Vrimle \coords
#R7 \coords
#R1 \coords
#R3 \coords
#Realfagbiblioteket \coords
#F1 
tempCoords = [0,0] #for temporarily adding coords to rooms

vrimleRoutes = [["R7", 5], ["R1", 5], ["Nanolab", 1], ["F1", 10], ["R3", 6]] #["KJL1", 5]?
vrimleCoords = [57, 409]
Vrimle = Room("Vrimle", Building.Kjemiblokkene, 50, vrimleRoutes, vrimleCoords)
rooms.append(Vrimle)

R7Routes = [["Vrimle", 5], ["Realfagbiblioteket", 25], ["R1", 8], ["F1", 10], ["R3", 10]]
R7Coords = [142, 496]
R7 = Room("R7", Building.Realfagbygget, 342, R7Routes, R7Coords)
rooms.append(R7)

R1Routes = [["Vrimle", 5], ["R7", 15], ["Realfagbiblioteket", 25], ["F1", 17], ["R3", 8]]
R1Coords = [523, 494]
R1 = Room("R1", Building.Realfagbygget, 478, R1Routes, R1Coords)
rooms.append(R1)

R3Routes = [["Vrimle", 2], ["R7", 5], ["Realfagbiblioteket", 15], ["F1", 10], ["R1", 8]]
R3Coords = [492, 621]
R3 = Room("R3", Building.Realfagbygget, 66, R3Routes, R3Coords)
rooms.append(R3)

RealfagbiblioteketRoutes = []
RealfagbiblioteketCoords = [275, 493]
Realfagbiblioteket = Room("Realfagbiblioteket", Building.Realfagbygget, 700, RealfagbiblioteketRoutes, RealfagbiblioteketCoords)
rooms.append(Realfagbiblioteket)

F1Routes = [["Vrimle", 5], ["R7", 15], ["Realfagbiblioteket", 35], ["R1", 15], ["R3", 7]]
F1Coords = [25, 20]
F1 = Room("F1", Building.ITbygget, 500, F1Routes, F1Coords)
rooms.append(F1)


def getRoom(roomName):
    for room in rooms:
        if room.name == roomName:
            return room
    

def move(room):
    for route in room.routes:
        fracInf = room.population.getFractionInfected()
        infected = route.amount*fracInf
        getRoom(route.destination).infect(math.ceil(infected*random.random()*random.random()/3)) #random*random/3 for each infected