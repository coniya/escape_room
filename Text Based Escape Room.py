from tkinter import *
import time

#Room class
class Room:
    #constructor
    def __init__(self, name, image):
        #rooms have:
        #a name ("room1", ...)
        #an image
        #items and item descriptions
        #grabbables
        #riddles/ tasks
        self.name = name
        self.image = image
        #
        self.answer = {}
        self.items = {}
        self.grabbables = []        

class Game(Frame):
    def __init__(self, parent):
        #create the rooms
        r1 = Room("Start", "start.")
        r2 = Room("Haunted Office", "hauntedOffice.jpeg")
        r3 = Room("Haunted Hall", "hauntedHall.JPG")
        r4 = Room("Final Destination... almost", "finalRoom.jpeg")
        

        #add any items
        r1.intro()

        #set the current room to r1
        Game.currentRoom

        #initialize player's inventory
        Game.inventory = []

    #set up GUI
    def setupGUI(self):
        #organize and pack the GUI
        self.pack(fill = BOTH, expand = 1)
        
        #setup player input(bottom)
        Game.player_input = Entry(self, bg = "white")
        Game.player_input.bind("<Return>", self.process)
        Game.player_input.pack(side=BOTTOM, fill = X)
        Game.player_input.focus()

        #setup image on the left of the display
        img = None
        Game.image = Label(self, width = WIDTH//2, image = img)
        Game.image.pack(side=LEFT, fill = Y)
        Game.image.pack_propagate(False) #don't let the img change the widgets size

        #setup text output on the right of the display
        text_frame = Frame(self, width = WIDTH//2)
        Game.text = Text(text_frame, bg = "lightgrey", state = DISABLED)
        Game.text.pack(fill = Y, expand = 1)
        text_frame.pack(side = RIGHT, fill = Y)
        text_frame.pack_propagate(False)

        #update current room image
    def setRoomImage(self):
        if(Game.currentRoom == None):
            Game.img = PhotoImage(file="skull.gif")
        else:
            Game.img = PhotoImage(file=Game.currentRoom.image)

        Game.image.config(image = Game.img)
        Game.image.image = Game.img

    #update status
    def setStatus(self, status):
        #clear the text widget
        Game.text.config(state = NORMAL)
        Game.text.delete("1.0", END)

        #if dead, say so, otherwise set the text to __str__
        if(Game.currentRoom == None):
            Game.text.insert(END, "You are dead. You may quit.\m")
        else:
            Game.text.insert(END, str(Game.currentRoom)+\
                             "\nYou are carrying: " +str(Game.inventory) +\
                             "\n\n" + status)
            Game.text.config(state = DISABLED)

    #introduction of the game
    #player name, rules, etc.
    def intro(self):
        #ask player name
        playerName = input("What is your name? ")
        #describe the rules
        print("Welcome to the Haunted Asylum {}. We would like to explain how you will be able to escape.\nYou will have 15 minutes to escape 3 rooms:\n" +\
              "the Starting Room, the Haunted Hallway, and your Final destination. If you can escape before the time runs out you win, if not...\n GOOD LUCK!".format(playerName))
        
    #play the game
    def play(self):
        #add rooms
        self.createRooms()
        #setup GUI
        self.setupGUI()
        #set room image
        self.setRoomImage()
        #set status
        self.setStatus("")


#################################################
#main code( construct the display and begin game)
#################################################

#define default screen size
WIDTH = 800
HEIGHT = 600

#create the window
window = Tk()
window.title("Room Adventure")

#create the GUI as a Tkinter canvas within the window
g = Game(window)

#begin the game

g.play()

#wait until the main window closes
window.mainloop()
