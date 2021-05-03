from tkinter import *
import time
import LCD_driver
from threading import Thread

start_min = 0
start_sec = 10
isIntro = True

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
        r3 = Room("Haunted Morgue", "hauntedMorgue.gif")
        r4 = Room("Final Destination... almost", "finalRoom.gif")
        r5 = Room("Final Destination... closer", "finalRoom.gif")
        r6 = Room("Final Destination... right there", "finalRoom.gif")
        r7 = Room("CONGRADULATIONS", "winner.gif")


        
        #add any items
        #r1 just intro page with rules
        r1.addAnswer("continue", r2)
        
        #r2 items
        r2.addItem("bookshelf", "Very dusty. It has 5 books sitting on it.")
        r2.addItem("red_book", "This book has 1 written on it.")
        r2.addItem("blue_book", "This book has 23 written on it.")
        r2.addItem("orange_book", "This book has 22 written on it.")
        r2.addItem("black_book", "This book has 13 written on it.")
        r2.addItem("grey_book", "This book has 26 written on it.")
        r2.addItem("mirror", "On here is written message: 'Sophie was murdered in her room. The Suspects were Julie, Zdena, David, Nicky, and Frank. Who killed her?'")
        r2.addItem("calendar", "There is a calendar with only the month of February and the last 2 days are torn off. The calendar also seems to be upside down.")
        #r2 answer
        r2.addAnswer("zdena", r3)
        #r2 grabbables
        r2.addGrabbable("map")
        
        #r3 items #add body parts and answer to riddle
        r3.addItem("corpse", "You notice that several body parts have been marked for incisions")
        r3.addItem("arm", "There's an x on it.")
        r3.addItem("foot", "There's an x on it.")
        r3.addItem("stomach", "There's an x on it.")
        r3.addItem("medical_cart", "It is a metal cart with something red oozing down it. There also seems to be a scalpel sitting on top.")
        r3.addItem("filing_cabinet", "It is locked. Maybe there is something that could unlock it.")
        #r3 answer
        r3.addAnswer("3;4", r4)
        r3.addGrabbable("scalpel")
        r3.addGrabbable("key")

        #r4 items #add answer to 
        r4.addItem("picture", "There is a picture hanging on the wall. It seems to be a picture of the previous owner of the asylum.")
        r4.addItem("exit", "If you look ahead you can see the way out!")
        r4.addItem("wall", "On the wall there is a message written in blood: 'I am the darkness that fills your mind, I am the reason you keep your light on at night, I can make children not sleep, I am what makes grown men weep, what am I?'")
        #r4 answers
        r4.addAnswer("fear", r5)
        r5.addItem("ghost", "The ghost is asking you a question: 'x is a 7 letter word. x is impossible for God. Babies like x better than milk. If you eat x you will die. x is more important than your life. I will give you x if you get the answer. what is x?'")    
        r5.addAnswer("nothing", r6)
        r6.addItem("leaves", "There are leaves on the ground and they seem to write a question: 'Walk on the living, they don’t even mumble. Walk on the dead, they mutter and grumble. What are they?'")
        r6.addAnswer("leaves", r7)

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
            Game.img = PhotoImage(file="loser.gif")
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
            Game.text.insert(END, status)
        elif(Game.currentRoom.name == "CONGRADULATIONS"):
            Game.text.insert(END, "You won! You may exit.\m")

        elif(Game.currentRoom.name == "Intro"):
            Game.text.insert(END, "Welcome to the Haunted Asylum. We would like to explain how you will be able to escape.\n\nYou will have 15 minutes to escape 3 rooms:\n\n the Starting Room, the Haunted Hallway, and your Final destination.\nIf you can escape before the time runs out you win, if not...\n\nGOOD LUCK!")
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
        response = "I don't understand. Try noun verb. Valid verbs are answer, use, look, and take."

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
            if(verb == "answer"):
                #default response
                response = "Invalid answer."

                #check the currentRoom's exits
                if(noun in Game.currentRoom.answers):
                    if(noun == "continue"):
                        global isIntro
                        isIntro = False
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

            #process use
            elif(verb == "use" and noun == "scalpel"):
                #set default response
                response = "I don't see that item in your inventory."
                #check inventory for valid item
                for i in range(len(Game.inventory)):
                    #a valid item is found
                    if(Game.inventory[i] == "scalpel"):
                        #check for valid item in room
                        for i in range(len(Game.currentRoom.items)):
                            #valid item is found
                            if("corpse" in Game.currentRoom.items.keys()):
                                #change description
                                Game.currentRoom.items["foot"] = "Inside is a key"
                                Game.currentRoom.items["arm"] = "There is nothing in here but blood and tissue."
                                Game.currentRoom.items["stomach"] = "Nothing but guts in here"
                                #set response(success)
                                response = "Item used."
                                Game.inventory.remove("key")
            elif(verb == "use" and noun == "key"):
                #set default response
                response = "I don't see that item in your inventory."
                #check inventory for valid item
                for i in range(len(Game.inventory)):
                    #a valid item is found
                    if(Game.inventory[i] == "key"):
                        #check for valid item in room
                        for i in range(len(Game.currentRoom.items)):
                            #valid item is found
                            if("filing_cabinet" in Game.currentRoom.items.keys()):
                                #change description
                                Game.currentRoom.items["filing_cabinet"] = "Inside is a file folder that has a piece of paper with a riddle written on it: 'Leonard works in the morgue,  When he tries to put each cadaver in its own gurney, he has one cadaver too many. But if he puts two cadavers per gurney, he has one gurney too many. How many cadavers and how many gurneys does Leonard have?'"
                                #set response(success)
                                response = "Item used."
                                Game.inventory.remove("key")

                        
                                
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

    def timer(self, minutes, seconds):
        while(isIntro):
            pass

        mylcd.lcd_display_string(str(minutes)+" minutes",1, 1)
        mylcd.lcd_display_string(str(seconds)+" seconds", 2, 1)
        
        if(seconds == 0 and minutes != 0):
            #window.after(1000, timer, minutes-1, 59)
            time.sleep(1)
            start_min = minutes
            start_sec = seconds
            g.timer(minutes-1, 59)
        elif(seconds > 0 and seconds < 60):
            #window.after(1000, timer, minutes, seconds-1)
            time.sleep(1)
            start_min = minutes
            start_sec = seconds
            g.timer(minutes, seconds-1)
        elif(minutes ==0 and seconds == 0):
            start_min = 0
            start_sec = 0
            #Tells the player they lose if their time runs out
            deathRoom = Game.currentRoom.name
            Game.currentRoom = None
            response = "You died in {}".format(deathRoom)
            self.setStatus(response)
            self.setRoomImage()
            Game.player_input.delete(0, END)
            
            #flashes the lcd to say "Times Up!"
            for i in range(10):
                mylcd.lcd_clear()
                mylcd.lcd_display_string("Times Up!")
                time.sleep(1)
                mylcd.lcd_clear()
                time.sleep(1)



#################################################
#main code( construct the display and begin game)
#################################################

#define default screen size
WIDTH = 800
HEIGHT = 600

#create the window
window = Tk()
window.title("Escape Room")

#create the GUI as a Tkinter canvas within the window
g = Game(window)

#begin the game
mylcd = LCD_driver.lcd() 
if __name__ == '__main__':
    Thread(target = g.play).start()
    Thread(target = g.timer, args=[start_min, start_sec]).start()
#g.play()

#wait until the main window closes
window.mainloop()
