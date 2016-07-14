#!/usr/bin/env python
# -*- coding: utf-8 -*-
from linepoints import *
from Tkinter import *

class GUI(Tk):
    """GUI portion of plotID"""
    file_name = None
    manipulator = None
    displayed_image = None
    
    width = 800
    height = 800
    def __init__(self):
        #Inherits from Tkinter.Tk, initialize window
        Tk.__init__(self)
        
        #GUI setup (set title, size, and disallow resizing)
        self.title("Testing and stuff")
        self.geometry("%sx%s+0+0" % (self.width,self.height))
        self.resizable(0,0)
        
        #prepare canvas
        self.canvas = Canvas(self)
        self.canvas.config(width=self.width,height=self.height)
        self.canvas.pack()
    
        
        #begin GUI event loop
        self.test()
        self.mainloop()
        
    def test(self):
        p1 = Point(0,0)
        p2 = Point(100,100)
        
        segment = Segment(p1,p2)
        
        for (x,y) in points_on(segment):
            print (x,y)
            
            
            
            
            
            
            
            
            
            
            
            
            
            
        
        
g = GUI()