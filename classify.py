#!/usr/bin/env python2.7
from Tkinter import *
import os
import math
from functools import partial
from PIL import Image, ImageTk



print """
Click or drag an image to use the magnifying glass tool.
Increase or decrease the radius of the selection circle with the up and down arrows.
"""

class GUI(Tk):
    """An aid for visual classification of events"""
    width  = 820
    height = 600
    
    cursor_radius = 35 #this has to be odd, don't ask me why, I'm ashamed. I'll fix it later.
    mouse_position = (0,0)
    magnification = 3
    
    current_image = None
    current_index = -1
    image_list = []
    source = ""
    def __init__(self):
        Tk.__init__(self)
        global SOURCE
        
        self.title("Muon Classification")
        self.geometry("{}x{}+0+0".format(self.width,self.height))
        self.resizable(width=False,height=False)
        
        self.canvas = Canvas(self)
        self.canvas.config(width=self.width,height=self.height,bg="black")
        self.canvas.grid(column=0,sticky=W,rowspan=60)
               
        #set the source for our images
        self.set_source(SOURCE)
        #setup buttons and such
        self.create_interface()
        #find images in our source
        self.update_image_list()
        #begin displaying images
        self.cycle_images()
        #begin the GUI mainloop
        
        #bind mouse_did_move to click and drag
        self.bind("<Motion>",self.mouse_did_move)
        #bind magnification to left click
        self.bind("<B1-Motion>",self.mouse_did_drag)
        self.bind("<Button-1>",self.magnify)
        
        #bind up and down to cursor resize
        pos = 10
        neg = -pos
        
        self.bind("<Up>",lambda x:self.set_radius(pos))
        self.bind("<Down>",lambda x:self.set_radius(neg))
        
        self.mainloop()
    def create_interface(self):
        #create an outline around where the image will be, image_proportions is the amount of our window that the image will take up
        image_proportions = (0.7,0.875)
        #create a border around image
        border = 10
        
        #limit size of canvas to size of image
        self.canvas.config(width=image_proportions[0]*self.width+border,height=image_proportions[1]*self.height+border)
        
        #create buttons for each type of image
        choices = [
            "Noise",
            "Spot",
            "Worm",
            "Track",
            "Other",
            "Skip"
        ]
        
        for (index,choice) in enumerate(choices):
            #use fn to allow us to call categorize() with arguments in the button callback
            fn = partial(self.categorize,choices[index])
            
            b = Button(self,text=choice,width=10,command=fn)
            #display the button
            b.grid(row=index,column=1,columnspan=2,sticky=W)
            
            
        self.progress_display = Label(text="<> of <>",anchor=E,font=("Menlo","20"))
        self.progress_display.grid(row=60,column=0)
        
        Label().grid(row=len(choices),column=1)
            
        self.previous_image_display = Label(text="Previous:<None>",anchor=W,font=("Menlo","11"),fg='dark gray')
        self.current_image_display = Label(text="Current:<None>",anchor=W,font=("Menlo","11"))
        self.next_image_display = Label(text="Next:<None>",anchor=W,font=("Menlo","11"),fg='dark gray')
        
        self.previous_image_display.grid(row=len(choices)+2,column=1,columnspan=2,sticky=W)
        self.current_image_display.grid(row=len(choices)+4,column=1,columnspan=2,sticky=W)
        self.next_image_display.grid(row=len(choices)+6,column=1,columnspan=2,sticky=W)
        
        Label().grid(row=len(choices)+7,column=1)

        self.cursor_size_label = Label(text="Cursor Size:",anchor=W,font=("Menlo","11"))
        self.cursor_size_display = Label(text=str(self.cursor_radius),anchor='center',font=("Menlo","11"))
        
        self.cursor_size_label.grid(row=len(choices)+8,column=1,sticky=W)
        self.cursor_size_display.grid(row=len(choices)+8,column=2,sticky='nesw')
        
        self.cursor_position_label = Label(text="Cursor Position:",anchor=W,font=("Menlo","11"))
        self.cursor_position_label.grid(row=len(choices)+9,column=1,sticky=W)        
        
        self.cursor_position_display = Label(text=str(self.mouse_position),anchor='center',font=("Menlo","11"))
        self.cursor_position_display.grid(row=len(choices)+9,column=2,sticky='nesw')
        
        self.magnification_display = Label(text=str(self.magnification) + "x magnification",anchor=W,font=("Menlo","11"))
        self.magnification_display.grid(row=len(choices)+10,column=1,columnspan=2)
        
    def display_image(self,filename):
        #show an image, crop first to remove outside white parts
        im = self.crop(filename)
        self.im = im
        self.canvas.create_image(im.width()/2.0,im.height()/2.0,image=im,tags="displayed")
    def update_image_list(self):
        #walk through files in cwd + source to find images and put those images in image_list
        ls = []
        for (dirname,dnames,fnames) in os.walk(os.getcwd()+self.source):
            for f in fnames:
                if f[-4:] == '.png':
                    ls.append(os.getcwd()+self.source+f)
        self.image_list = ls
    def cycle_images(self):
        #cycle through and display images
        #prevent an indexerror when you finish categorizing
        self.current_index += 1 if self.current_index < len(self.image_list) else 0
        self.current_image = self.image_list[self.current_index]
        
        
        try: self.previous_image_display.config(text="Previous:<{}>".format(self.image_list[self.current_index-1].split("/")[-1]))
        except IndexError: pass
        
        self.current_image_display.config(text="Current: <{}>".format(self.current_image.split("/")[-1]))
        
        try: self.next_image_display.config(text="Next:    <{}>".format(self.image_list[self.current_index+1].split("/")[-1]))
        except IndexError: pass
        
        self.progress_display.config(text="<{}> of <{}>".format(self.current_index+1,len(self.image_list)))
        
        self.display_image(self.current_image)
    def categorize(self,kind):        
        if kind == "Skip":
            self.cycle_images()
            return
        #check if a folder exists to put the categorized image into, otherwise make one
        destination = '{}/{}/{}'.format(os.getcwd(),kind,self.current_image.split("/")[-1])
        if not os.path.exists('/'.join(destination.split("/")[:-1])):
            try:
                os.system('mkdir {}'.format('/'.join(destination.split("/")[:-1])))
            except OSError:
                pass
        #move image into folder named 'kind'
        os.system('mv {} {}'.format(self.current_image,destination))
        #show new image
        self.cycle_images()
        
    
        
        
        
    def set_source(self,name):
        #ensure the folder is padded with forward slashes and set it as the image source
        n = name
        #ensure name is valid
        if not os.path.exists(n):
            received = n if len(n) != 0 else "empty string"
            print "Invalid folder name supplied: got {}.".format(received)
            quit()

        if n[0] != "/":
            n = "/" + n
        if n[-1] != "/":
            n = n + "/"
        self.source = n
    def crop(self,image):
        # takes a filename 'image' and crops it by 100,100,100,175. Returns this as a PhotoImage for use with tk canvas .
    
        im = Image.open(image)
        c = (100,100,im.width-100,im.height-175)
        im = im.crop(c)
    
        return ImageTk.PhotoImage(im)
        
            


    def mouse_did_move(self,event):
        if event.x < 0 or event.y < 0 or not self.canvas.winfo_containing(event.x_root,event.y_root):
            return
        self.mouse_position = (event.x-self.cursor_radius*2,event.y-self.cursor_radius*2)
        self.cursor_position_display.config(text=str(self.mouse_position))
        
        self.canvas.delete("selection_circle")
        self.canvas.delete('magnify_rect')
        self.canvas.delete('magnified_image')
        
        #radius of white selection circle
        radius = self.cursor_radius
        c = self.canvas.create_rectangle(event.x-radius*2.5,event.y-radius*2.5,event.x-radius/2,event.y-radius/2,outline="green",tags="selection_circle")
        cc = self.canvas.coords(c)
        l = self.canvas.create_line(cc[2],cc[3],event.x,event.y,fill='green',tags='selection_circle')
   
    def mouse_did_drag(self,event):
        self.mouse_did_move(event)
        self.magnify(event)
    def magnify(self,event):
        circle = self.canvas.find_withtag("selection_circle")
        if not circle or not self.canvas.winfo_containing(event.x_root,event.y_root):
            return
        
        circle = circle[0]
        coords = self.canvas.coords(circle)
        offset = coords[:-2]
        
        width = abs(coords[0]-coords[2])
        height = abs(coords[1]-coords[3])
                
        rect = self.canvas.create_rectangle(offset[0],offset[1],offset[0]+width,offset[1]+height,outline='green',fill='green',tags='magnify_rect')
        
        
        pixel_xrange = (int(offset[0]),int(offset[0]+width-1))
        pixel_yrange = (int(offset[1]),int(offset[1]+height-1))
                
        magnification = self.magnification
        imageObj = Image.open(self.current_image)
        c = (100,100,imageObj.width-100,imageObj.height-175)
        imageObj = imageObj.crop(c)
        imageObj = imageObj.load()
        
        result = []
        center = (offset[0]+width/2,offset[1]+height/2)
        
        try:
            for y in range(*pixel_yrange):
                row = []
                for x in range(*pixel_xrange):
                    for i in range(magnification):
                        value = imageObj[x,y]
                        row.append(value)
                for i in range(magnification):
                    [result.append(x) for x in row]
        except IndexError:
            #TODO: put something here maybe. Or better; prevent it from happening on close
            pass
                
        new = Image.new('RGBA',(int(width)*magnification,int(height)*magnification))
        new.putdata(result)
        self.magnified = ImageTk.PhotoImage(new)
        self.canvas.create_image(event.x-width/2*magnification,event.y-width/2*magnification,image=self.magnified,tags='magnified_image')
        
        self.canvas.coords(rect,event.x-(width * magnification),event.y-(width*magnification),event.x,event.y)
        self.canvas.itemconfig(rect,width=10,fill='green')
                
        
    def distance(self,x0,y0,x1,y1):
        a = x0-x1
        b = y0-y1
        
        return math.sqrt(a**2 + b**2)
    def set_radius(self,amount):
        if self.cursor_radius + amount <= 0:
            return
        self.cursor_radius += amount
        radius = self.cursor_radius
        c = self.canvas.find_withtag('selection_circle')
        x,y = self.mouse_position
        self.canvas.coords(c,x-radius*2.5,y-radius*2.5,x-radius/2,y-radius/2)
        self.cursor_size_display.config(text=str(self.cursor_radius))
        
        
#set this to the folder that has your images;this folder must be *IN* the same folder as the script is *IN*
SOURCE = 'files'

#determine if called from command line with argument and if so replace the SOURCE
if len(sys.argv) == 2: SOURCE = sys.argv[1]

#initialize window
g = GUI()