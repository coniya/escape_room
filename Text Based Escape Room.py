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

        #instance variables
        #assign name and image
        self.name = name
        self.image = image
        
        #add dictionaries
        self.answers = {}
        self.items = {}
        self.grabbables = []


    #getters and setters
    #name
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value

    #image
    @property
    def image(self):
        return self._image
    @image.setter
    def image(self, value):
        self._image = value

    #answers to riddles
    @property
    def answers(self):
        return self._answers
    @answers.setter
    def answers(self, value):
        self._answers = value

    #items
    @property
    def items(self):
        return self._items
    @items.setter
    def items(self, value):
        self._items = value
        
    #grabbables
    @property
    def grabbables(self):
        return self._grabbables
    @grabbables.setter
    def grabbables(self, value):
        self._grabbables = value

    #add answers
    def addAnswer(self, answer, room):
        #add the room to the dictionary
        #answers will be keys, rooms will be values
        self._answers[answer] = room

    #add items
    def addItem(self, item, desc):
        #add the item and its description
        self._items[item] = desc

    #add grabbables
    def addGrabbable(self, item):
        self._grabbables.append(item)

    #del grabbables
    def delGrabbable(self, item):
        self._grabbables.remove(item)

    #introduction of the game
    #player name, rules, etc.
    def intro(self):
        #ask player name
        self.playerName = input("What is your name? ")
        #describe the rules
        return("Welcome to the Haunted Asylum {}. We would like to explain how you will be able to escape.\n\nYou will have 15 minutes to escape 3 rooms:\n\n".format(self.playerName) +\
              "the Starting Room, the Haunted Hallway, and your Final destination.\nIf you can escape before the time runs out you win, if not...\n\nGOOD LUCK!")

    #custom __str__()
    def __str__(self):
        #where you are
        s = "Currently in {}\n".format(self.name)
        #what you see
        s += "\nYou see: \n"
        for item in self.items.keys():
            s += item + " "
        return s

class Game(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        
    #create rooms
    def createRooms(self):
        #create the rooms
        r1 = Room("Intro", "intro.gif")
        r2 = Room("Haunted Office", "hauntedOffice.gif")
        r3 = Room("Haunted Hall", "hauntedHall.gif")
        r4 = Room("Final Destination... almost", "finalRoom.gif")
        r5 = Room("Final Destination... closer", "finalRoom.gif")
        r6 = Room("Final Destination... right there", "finalRoom.gif")
        r7 = Room("CONGRADULATIONS", "winner.gif")
        #r8 = Room("LOSER", "loser.gif")

        
        #add any items
        #r1 just intro page with rules
        r1.intro()
        r1.addAnswer("continue", r2)
        
        #r2 items
        r2.addItem("bookshelf", "Very dusty. It has 3 books sitting on it.")
        r2.addItem("red_book", "This book has 816 written on it.")
        r2.addItem("blue_book", "This book has 311 written on it.")
        r2.addItem("orange_book", "This book has 514 written on it.")
        r2.addItem("mirror", "In this mirror you see someone standing behind you. There is also a map taped to it.")
        #r2 answer
        r2.addAnswer("816", r3)
        #r2 grabbables
        r2.addGrabbable("map")
        
        #r3 items
        r3.addItem("corpse", "This is what you'll look like if you don't escape in time.")
        r3.addItem("medical_cart", "It is a metal cart with something red oozing down it. There also seems to be a scalpel sitting on top.")
        r3.addItem("broken_door", "It is lying on the floor. There is a message written here in something red:'Get out!'")
        #r3 answer
        r3.addAnswer("", r4)
        r3.addGrabbable("scalpel")

        #r4 items
        r4.addItem("picture", "This picture is hanging on the wall. It seems to be a picture of the previous owner of the asylum.")
        r4.addItem("exit", "If you look ahead you can see the way out!")
        #r4 answers
        r4.addAnswer("leaves", r5)
        r5.addAnswer("nothing", r6)
        r6.addAnswer("", r7)

        #set the current room to r1
        Game.currentRoom = r1

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

    #process input
    def process(self, event):
        
        #set default response
        response = "I don't understand. Try noun verb. Valid verbs are escape, look, and take."

        #get the command input from the GUI
        action = Game.player_input.get()
        action = action.lower()
        
        #handle exits
        if(action == "quit" or action == "exit"):
            exit(0)

        #handle end of game (death)
        if(Game.currentRoom == None):
            Game.player_input.delete(0, END)
            return

        #handle verbs and nouns
        words = action.split()

        if(len(words) == 2):
            verb = words[0]
            noun = words[1]

            #process go
            if(verb == "escape"):
                #default response
                response = "Invalid answer."

                #check the currentRoom's exits
                if(noun in Game.currentRoom.answers):
                    #if it's valid, update currentRoom
                    Game.currentRoom = Game.currentRoom.answers[noun]
                    #notify user that room has changed
                    response = "Next room."
                    
            #process look
            elif(verb == "look"):
                #default response
                response = "I don't see that item."

                #check the currentRoom's items
                if(noun in Game.currentRoom.items):
                    response = Game.currentRoom.items[noun]

                        
                                
            #process take
            elif(verb == "take"):
                #default response
                response = "I don't see that item."

                #check currentRoom's grabbables
                for grabbable in Game.currentRoom.grabbables:
                    if(noun == grabbable):
                        #add it to inventory
                        Game.inventory.append(grabbable)
                        #set the response
                        response = "{} grabbed".format(grabbable)
                        #remove it from the room's grabbables
                        Game.currentRoom.delGrabbable(grabbable)
                        #exit the loop
                        break
                    
        #call the updates for display
        self.setStatus(response)
        self.setRoomImage()
        Game.player_input.delete(0, END)


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
