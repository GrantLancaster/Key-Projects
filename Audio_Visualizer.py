# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 13:11:59 2021

@author: Grant Young, Payton O'Brien, Grant Lancaster

This code creates an audio visualizer the reacts to .wav file that is found in
the sounds folder. The visualizer is mostly just meant to be watched, but it 
does have a little bit of intereactivity for the user to explore. Try playing 
with the left and right arrow keys as well as the spacebar while running the 
code to see what they do!

LINK:
    https://drive.google.com/file/d/1yH3rzHzPv-cwk81d3UoJLFS8Dfxb5YM_/view?usp=sharing
    Use this link to get to the zip file for the code, module, and sound file!
    I recommend using the .py file stored in the zip file to run the program. That way, you shouldn't have to change
    the path that the computer looks at to find the music file.
    
CONTROlS:
    left arrow key - left side stretch
    right arrow key - right side stretch
    space bar - return to center
    
RESOURCES:
    the module soundResponseDrZ was made by Dr. Shaz Zamore, and we were allowed
    access to use it for this project. Theyre code uses pydub and some other 
    libraries to analyze the audio track that is playing, take audio samples,
    turn those samples into values for frequency and amplitude, and store 
    the frequency and amplitude into an array to be used.
    
ACKNOWlEDGMENTS:
    Song: Slash by Tokyo Machine - NCS Release
    
NOTES:
    - To get the song to stop playing, use the hamburger menu in the python console
        to restart the kernel. This will stop the audio track.
    - The only audio files that will be properly read are .wav files. Make sure 
        that if you want to use a different song, that it is in this format.
    - you also have to go into the soundResponseDrZ.py file and change the name
        to the name of the audio file you want to use
    - You have to also put the audio file into the 'sounds' folder.
    
We hope you enjoy seeing music come to life, in our own chaotic little way!!

"""
import soundResponseDrZ as SR
import turtle
import pygame
import os
import random
import time

class SystemSetup:
    """Sets up the base screen and some general turtle setup. Instanciates 
    the class that runs the animation for the audio."""
    def __init__(self):
        turtle.colormode(255)
        turtle.tracer(0)
        self.panel = turtle.Screen()
        self.panelHeight = 600
        self.panelWidth = 800
        
        self.panel.setup(width=self.panelWidth, height=self.panelHeight)
        self.setupComplete = SystemRunning(self.panel)  

class SystemRunning:
    """This runs the animation by calling the method playVis()."""
    def __init__(self, panel):
        self.panel = panel
        self.run = True
        self.music = SR.Ctrlr()
        self.playVis()
    
    def stopVis(self):
        """Stops the visual. *not called in code yet*"""
        self.run = False
    
    def playVis(self):
        """Starts the animation. *called in line 68*
        contains the While Loop as well as the instanciation of the classes
        that create the animation."""
        self.music.start() #Starts the music track
        self.soundBarsBottom = SoundBars(-400,-300) #instance of the bottom sound bar
        self.soundBarsTop = SoundBars(-400,300) #instance of the top sound bar
        #Uncomment line 81 and line 108 for a cool line effect
        # self.soundBarsMid = SoundBars(200,-300)
        self.soundSquares = SpinningSquare() #instance of the spinning squares
        while self.run: #The animation while loop.
            self.amp = self.music.getCurrAmp()[0]/1000
            self.freq = self.music.getCurrFreq()[0]/8000
            self.soundBarsBottom.reacting(self.amp, self.freq)
            self.soundBarsTop.reacting(self.amp, self.freq)
            # self.soundBarsMid.reacting(self.amp, self.freq)
            self.soundSquares.dancing(self.amp, self.freq, self.panel)
        turtle.listen()
        turtle.update()
            
class SoundBars:
    """This is the class that creates a line of turtles that generate an audio
    specturm. By changeing the parameters for the startPosX and startPosY, you
    can create lines of turtles that start in different locations."""
    def __init__(self, startPosX, startPosY):
        self.barTurtList = []
        self.barTurtIncrement = 40
        self.barTurtStartPosX = -400
        self.barTurtStartPosY = -300
        for i in range(21): #This loop creates all the turtles for SoundBars, stuffs them into a list, and gives them their starting position through indexing.
            self.barTurtle = turtle.Turtle(shape="turtle")
            self.barTurtList.append(self.barTurtle)
            self.barTurtList[-1].penup()
            self.barTurtList[-1].goto(startPosX, startPosY)
            startPosX = startPosX + self.barTurtIncrement
            # startPosY = startPosY + self.barTurtIncrement
            
    def reacting(self, amp, freq):
        """This method causes the turtles in this class to change their shape
        size based on the amplitude and frequency of the audio that is playing.
        There are conditionals that change how turtles look if the amplitude
        and frequency hit certian values."""
        for i in range(21): #This loop gives the SoundBar turtles their size changes and color changes.
            self.barTurtList[i].shapesize(abs((amp)*(random.uniform(0.5,1.5)))+0.1, 2)
            if freq >= 7:
                self.barTurtList[i].right(abs(freq))
            else:
                self.barTurtList[i].right(-1)
            if amp >= 12:
                self.barTurtList[i].color("blue")
            if amp >= 17:
                self.barTurtList[i].color("red")
            if amp >= 21:
                self.barTurtList[i].color("orange")
        turtle.update()
        
class SpinningSquare:
    """This class generates the 5 spinning squares that rotate in the middle
    of the animation. You can change the size of the squares and the speed at
    which they rotate by altering the values in self.squareSizeList and
    self.rotationalMultiplierList."""
    def __init__(self):
        self.squareWidth = 3
        self.squareHeight = 3
        self.squareSizeMult = [5,4,3,2,1] #Multipliers that make the up front square small and back square big.
        self.squareTurtleList = []
        self.squareGhostList = []
        self.rotationalMultiplierList = [0.2,0.4,0.6,0.8,1.0]
        for i in range (5): #Creates the square turtles, sets their shape size, and changes their color
            self.squareGhost = turtle.Turtle(shape="square")
            self.squareTurtle = turtle.Turtle(shape="square")
            self.squareTurtleList.append(self.squareTurtle)
            self.squareGhostList.append(self.squareGhost)
            self.squareTurtleList[i].shapesize(self.squareWidth*self.squareSizeMult[i],
                                               self.squareHeight*self.squareSizeMult[i])
            self.squareGhostList[i].shapesize(self.squareWidth*self.squareSizeMult[i],
                                               self.squareHeight*self.squareSizeMult[i])
            self.squareTurtleList[i].color("red","black")
            self.squareGhostList[i].color("red","white")
            
    def dancing(self, amp, freq, panel):
        """This method simply makes the squares react to the amplitude and 
        frequency of the audio that is playing. The squares will spin and change
        their shape size when the conditions for the amp and freq are met.
        The multipliers are just to keep the values to a reasonable size so it 
        doesn't take over the whole panel."""
        self.panel = panel
        if amp >= 0.1:
            for i in range(5): #makes the squares spin with the amount of amplitude
                self.squareTurtleList[i].right(amp*self.rotationalMultiplierList[i])
                self.squareGhostList[i].right(amp*self.rotationalMultiplierList[i]*(0.5))
        if freq >= 8.7:
            for i in range(5): #makes the ghost squares changes their size when freq is above a certain amount.
                self.squareGhostList[i].shapesize((abs(freq))*(self.squareSizeMult[i])*(0.4),
                                                  (self.squareWidth)*(self.squareSizeMult[i]))
        self.panel.onkey(self.horizontalShiftRight, "Right")
        self.panel.onkey(self.horizontalShiftLeft, "Left")
        self.panel.onkey(self.centerSquares, "space")
        self.panel.listen()
        
    def horizontalShiftRight(self):
        """When the right arrow key is pressed, the squares will spread out
        with the smallest square being the leader. The smallest square moves
        to the right, hense the name horizontatShiftRight."""
        self.panelWidth = -200
        self.shiftRight = []
        for i in range(5): #creates the locations for the squares to move to
            self.shiftRight.append(self.panelWidth)
            self.panelWidth += 100
        for i in range(5): #moves the squares to the previously created positions
            self.squareTurtleList[i].goto(self.shiftRight[i],0)
            self.squareGhostList[i].goto(self.shiftRight[i],0)
        turtle.update()
    
    def horizontalShiftLeft(self):
        """When the left arrow key is pressed, the squares will spsread out
        with the smallest square being the leader. The smallest square moves 
        to the left, hence the name horizontalShiftLeft."""
        self.panelWidth = 200
        self.shiftLeft = []
        for i in range(5): #creates the locations for the square to move to
            self.shiftLeft.append(self.panelWidth)
            self.panelWidth -= 100
        for i in range(5): #moves the squares to the previously created positions
            self.squareTurtleList[i].goto(self.shiftLeft[i],0)
            self.squareGhostList[i].goto(self.shiftLeft[i],0)
        turtle.update()
    
    def centerSquares(self):
        """When the space bar is pressed, the squares return the origin, reverting
        back to their original stacked positions."""
        for turt in range(5): #resets the squares back to their origin.
            self.squareTurtleList[turt].goto(0,0)
            self.squareGhostList[turt].goto(0,0)
        turtle.update()
        
if __name__ == "__main__":
    go = SystemSetup()
    turtle.mainloop()
        
        


