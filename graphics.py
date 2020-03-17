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
    info_pad = 20
    start_date = "02.03.2020"
    start_time = "08:15"

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
        self.root.update()
        self.date_box_label = tkinter.Label(self.root, width = 5, height = 1, text = "Dato:")
        self.date_box_label.place(x = self.root.winfo_width() -self.padX -self.box_pad - self.date_box.winfo_width(), y = self.root.winfo_height()-self.padY, anchor = tkinter.SE)

        #time box
        self.time_box = tkinter.Text(self.root, width = 10, height = 1)
        self.time_box.insert('0.0', self.start_time)
        self.time_box.configure(state = "disabled")
        self.time_box.place(x = self.root.winfo_width() -self.padX, y = self.root.winfo_height()-self.padY-self.box_pad-self.date_box.winfo_height(), anchor = tkinter.SE)
        self.root.update() #updates are necessary for reading the widget size later
        self.time_box_label = tkinter.Label(self.root, width = 5, height = 1, text = "Klokka:")
        self.time_box_label.place(x = self.root.winfo_width() -self.padX -self.box_pad - self.time_box.winfo_width(), y = self.root.winfo_height()-self.padY-self.box_pad-self.date_box.winfo_height(), anchor = tkinter.SE)

        #info canvas
        self.info = tkinter.Canvas(self.root, width = self.info_width, height = self.info_height)
        self.info.place(x = self.bg_map.width()+2*self.padX, y = self.padY, anchor = tkinter.NW)

        #### info canvas initial content ####

        #title
        self.info_title = tkinter.StringVar()
        self.info_title.set("Instruksjon")
        self.info_title_label = tkinter.Label(self.info, width = 20, height = 1, text = self.info_title, textvariable = self.info_title, anchor = tkinter.NW)
        self.info_title_label.config(font=("Courier", 26))
        self.info_title_label.place(x=self.info_pad, y=self.info_pad, anchor = tkinter.NW)
        self.root.update() 
        
        #healthy
        self.info_healthy_label = tkinter.Label(self.info, width = 10, height = 1, text = "Friske:", anchor = tkinter.NW)
        self.info_healthy_label.config(font=("Courier", 16))
        healthy_y_pos = self.info_pad + self.padY + self.info_title_label.winfo_height()
        self.info_healthy_label.place(x = self.info_pad, y = healthy_y_pos, anchor = tkinter.NW)
        self.root.update()
        self.info_healthy_count = tkinter.Text(self.info, width = 4, height = 1)
        self.info_healthy_count.insert('0.0', 0)
        self.info_healthy_count.configure(state = "disabled")
        self.info_healthy_count.place(x = self.info_width - self.info_pad, y = healthy_y_pos, anchor = tkinter.NE)

        #infected
        self.info_infected_label = tkinter.Label(self.info, width = 10, height = 1, text = "Syke:", anchor = tkinter.NW)
        self.info_infected_label.config(font=("Courier", 16))
        infected_y_pos = self.info_pad + 2*self.padY + self.info_title_label.winfo_height() + self.info_healthy_label.winfo_height()
        self.info_infected_label.place(x = self.info_pad, y = infected_y_pos, anchor = tkinter.NW)
        self.info_infected_count = tkinter.Text(self.info, width = 4, height = 1)
        self.info_infected_count.insert('0.0', 0)
        self.info_infected_count.configure(state = "disabled")
        self.info_infected_count.place(x = self.info_width - self.info_pad, y = infected_y_pos, anchor = tkinter.NE)

        #dead
        self.info_dead_label = tkinter.Label(self.info, width = 10, height = 1, text = "Karantene:", anchor = tkinter.NW)
        self.info_dead_label.config(font=("Courier", 16))
        dead_y_pos = self.info_pad + 3*self.padY + self.info_title_label.winfo_height() + 2*self.info_healthy_label.winfo_height()
        self.info_dead_label.place(x = self.info_pad, y = dead_y_pos, anchor = tkinter.NW)
        self.info_dead_count = tkinter.Text(self.info, width = 4, height = 1)
        self.info_dead_count.insert('0.0', 0)
        self.info_dead_count.configure(state = "disabled")
        self.info_dead_count.place(x = self.info_width - self.info_pad, y = dead_y_pos, anchor = tkinter.NE)

        #tutorial text
        tutorial_text = "Velkommen til Pest A.S \nMålet er å infisere alle rommene ved Realfagbygget.\nSpillet forutsetter generell kjennskap til rommene.\nKlikk på et rom for å begynne."
        self.info_tutorial_label = tkinter.Label(self.info, width = 50, height = 10, text = tutorial_text, justify = tkinter.LEFT, anchor = tkinter.NW)
        self.info_tutorial_label.place(x = self.info_pad, y = healthy_y_pos, anchor = tkinter.NW)

        #### End of info section ####



        #### Room Buttons ####

        #create buttons dict
        self.roomButtons = dict()

        #create button image dict
        btn_images = dict()

        #create command dict
        command_dict = dict()

        #fill the dicts
        for room in self.rooms:
            self.roomButtons[room.name] = tkinter.Button(self.bg)
            btn_images[room.name] = tkinter.PhotoImage(file = self.graphicspath + room.name + ".png")
            command_dict[room.name] = lambda: updateInfoScreen(self, room)
        
        #configure all buttons
        for room in self.rooms:
            self.roomButtons[room.name].configure(image = btn_images[room.name], command = lambda room=room: updateInfoScreen(self, room), borderwidth = 0) 
            # in the lambda command, room=room because otherwise all buttons point to the last
            self.roomButtons[room.name].image = btn_images[room.name] #these need to be stored becaused of garbage collection
            self.roomButtons[room.name].place(x = room.coordinates[0], y = room.coordinates[1], anchor = tkinter.NW)

            

    def show(self):
        self.root.mainloop()
    
def updateInfoScreen(win, room):
    #first infection removed tutorial and infects 1 person
    if win.info_tutorial_label.winfo_exists():
        room.infect(1)
        win.info_tutorial_label.destroy()

    #change title text
    win.info_title.set(room.name)
    if len(room.name) > 12: #resize if text is too big
        win.info_title_label.config(font=("Courier", 37-len(room.name)))
        
    else:
        win.info_title_label.config(font=("Courier", 26))

    #healthy
    win.info_healthy_count.configure(state = "normal")
    win.info_healthy_count.delete('0.0', tkinter.END)
    win.info_healthy_count.insert('0.0', room.population.getHealthy())
    win.info_healthy_count.configure(state = "disabled")

    #infected
    win.info_infected_count.configure(state = "normal")
    win.info_infected_count.delete('0.0', tkinter.END)
    win.info_infected_count.insert('0.0', room.population.getInfected())
    win.info_infected_count.configure(state = "disabled")

    #dead
    win.info_dead_count.configure(state = "normal")
    win.info_dead_count.delete('0.0', tkinter.END)
    win.info_dead_count.insert('0.0', room.population.getDead())
    win.info_dead_count.configure(state = "disabled")

test = Window()
test.show()
