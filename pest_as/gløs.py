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
VrimleDesc = "Studentene ved MTNANO\nsitter her og jobber. Mye\nsamarbeid på tvers av\ntrinnene, men få folk."
Vrimle = Room("Vrimle", Building.Kjemiblokkene, 50, vrimleRoutes, vrimleCoords, VrimleDesc)
rooms.append(Vrimle)

R7Routes = [["Vrimle", 5], ["Realfagbiblioteket", 25], ["R1", 8], ["F1", 10], ["R3", 10]]
R7Coords = [142, 496]
R7Desc = "Medium stort auditorium,\nkjent for takbelysningen"
R7 = Room("R7", Building.Realfagbygget, 342, R7Routes, R7Coords, R7Desc)
rooms.append(R7)

R1Routes = [["Vrimle", 5], ["R7", 15], ["Realfagbiblioteket", 25], ["F1", 17], ["R3", 8]]
R1Coords = [523, 494]
R1Desc = "Det største auditoriet i \nRealfagbygget, med plass\ntil nesten 500."
R1 = Room("R1", Building.Realfagbygget, 478, R1Routes, R1Coords, R1Desc)
rooms.append(R1)

R3Routes = [["Vrimle", 2], ["R7", 5], ["Realfagbiblioteket", 15], ["F1", 10], ["R1", 8]]
R3Coords = [492, 621]
R3Desc = "Stort for undervisningsrom\nå være, men lite i forhold\ntil auditorier."
R3 = Room("R3", Building.Realfagbygget, 66, R3Routes, R3Coords, R3Desc)
rooms.append(R3)

RealfagbiblioteketRoutes = []
RealfagbiblioteketCoords = [275, 493]
RealfagbiblioteketDesc = "Her sitter folk fra nesten\nalle studieretninger i\nstillhet og jobber for seg\nselv. Her sitter man for å\njobbe etter forelesninger."
Realfagbiblioteket = Room("Realfagbiblioteket", Building.Realfagbygget, 700, RealfagbiblioteketRoutes, RealfagbiblioteketCoords, RealfagbiblioteketDesc)
rooms.append(Realfagbiblioteket)

F1Routes = [["Vrimle", 5], ["R7", 15], ["Realfagbiblioteket", 35], ["R1", 15], ["R3", 7]]
F1Coords = [25, 20]
F1Desc = "Det største auditoriet på\nGløshaugen, brukt i mange\nav de grunnleggende fagene."
F1 = Room("F1", Building.ITbygget, 500, F1Routes, F1Coords, F1Desc)
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