# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 18.05.43 2020

@author: Viljar Femoen
"""
from gløs import rooms, getRoom, move
import tkinter
from PIL import Image 



class Window():

    graphicspath = "graphics/"
    bg_map_filename = graphicspath+"map.png"
    info_width = 300
    info_height = 400
    padX = 30
    padY = 30
    box_pad = 10
    start_date = "02.03.2020"
    start_time = "08:00"

    def __init__(self):
        #Initial variables and main tkinter window
        self.rooms = rooms
        self.root = tkinter.Tk()
        self.root.title("Pest A.S.")

        #map image
        self.bg_map = tkinter.PhotoImage(file = self.bg_map_filename)

        #main window size
        self.root.geometry(str(self.bg_map.width()+self.info_width+3*self.padX)+"x"+str(self.bg_map.height()+2*self.padY))
        self.root.update()

        #placing the map image
        self.bg = tkinter.Canvas(self.root, width = self.bg_map.width(), height = self.bg_map.height())
        self.bg.create_image(0, 0, image = self.bg_map, anchor = tkinter.NW)
        self.bg.place(x=self.padX, y=self.padY)

        #date box
        self.date_box = tkinter.Text(self.root, width = 10, height = 1)
        self.date_box.insert('0.0', self.start_date)
        self.date_box.configure(state = "disabled")
        self.date_box.place(x = self.root.winfo_width() -self.padX, y = self.root.winfo_height()-self.padY, anchor = tkinter.SE)
        self.date_box_label = tkinter.Label(self.root, width = 5, height = 1, text = "Dato:")
        self.date_box_label.place(x = self.root.winfo_width() -self.padX -self.box_pad - 8*len(self.start_date)-2, y = self.root.winfo_height()-self.padY, anchor = tkinter.SE)

        #time box
        self.time_box = tkinter.Text(self.root, width = 10, height = 1)
        self.time_box.insert('0.0', self.start_time)
        self.time_box.configure(state = "disabled")
        self.time_box.place(x = self.root.winfo_width() -self.padX, y = self.root.winfo_height()-self.padY-self.box_pad-20, anchor = tkinter.SE)
        self.time_box_label = tkinter.Label(self.root, width = 5, height = 1, text = "Klokka:")
        self.time_box_label.place(x = self.root.winfo_width() -self.padX -self.box_pad - 8*len(self.start_date)-2, y = self.root.winfo_height()-self.padY-self.box_pad-20, anchor = tkinter.SE)

        #info canvas
        self.info = tkinter.Canvas(self.root, width = self.info_width, height = self.info_height)
        self.info.place(x = self.bg_map.width()+2*self.padX, y = self.padY, anchor = tkinter.NW)

    def show(self):
        self.root.mainloop()
    

test = Window()
test.show()
