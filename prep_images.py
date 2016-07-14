#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import math
import os

try:
    from PIL import Image
    import numpy as np
    import sys
except ImportError,e:
    print "plotID.py requires PIL for image processing; You can install PIL with 'pip install PIL --user'"
    print e
    quit()

ONE_EIGHTY_OVER_PI = 180.0 / math.pi
PI_OVER_ONE_EIGHTY = math.pi / 180.0
class ImageManipulator(object):
    """
    pull events from processed images, takes an Image() picture, the string name of the image, 
    and a boolean 'replaces' that determines whether or not the new replaces the old (if the directory is the same)
    
    
    """
    image    = None
    pixelObj = None
    def __init__(self,image,name,replaces=False):
        self.name = name
        self.replaces = replaces
        self.image = image.convert('RGB')
        self.pixelObj = self.image.load() #the pixelObj allows for faster access to pixels in the image
    
    def find_illumination(self,samples=300):
        """find an average illumination in the image by sampling samples^2 number of pixels"""
        intensities = []
        for y in range(0,self.image.height-1,int(float(self.image.height)/float(samples)+1)):
            for x in range(0,self.image.width-1,int(float(self.image.width)/float(samples)+1)):
                r,g,b = self.pixelObj[x,y]
                if (r,g,b) != (255,255,255):
                    intensities.append((r+g+b)/3)
                
        avg = 0
        for x in intensities: avg += x
        avg = avg / len(intensities)
        
        return avg
    def draw_above_threshold(self,threshold):
        """put all pixels above the 'threshold' into an array and save it. Crop the image so only these pixels are displayed."""
        
        print "threshold luminance: {}".format(threshold)
        size = self.image.width * self.image.height
        px = []
        py = []
        
        #store a 2d array of pixels
        array_2 = []
        
        #append pixels that are likely part of an event to array_2
        first_px = [self.image.width-1,self.image.height-1]
        last_px = [0,0]
        for y in range(0,self.image.height-1):
            row = []
            for x in range(0,self.image.width-1):
                r,g,b = self.pixelObj[x,y]
                brightness = (r + g + b)/3
                if brightness >= threshold:
                    
                    if x < first_px[0]:
                        first_px[0] = x
                    if y < first_px[1]:
                        first_px[1] = y     
                    
                    if x > last_px[0]:
                        last_px[0] = x
                    if y > last_px[1]:
                        last_px[1] = y
                    
                    self.pixelObj[x,y] = (100,100,100)
                    row.append([brightness,brightness,brightness])
                    px.append(x)
                    py.append(y)
                else:
                    row.append([0,0,0])
            array_2.append(row)
    
        #crop the image so only the selected pixels are visible
        np_array = np.array(array_2)
        crop = (first_px[0],first_px[1],last_px[0],last_px[1])
        
        width, height = (abs(last_px[0]-first_px[0]),abs(last_px[1]-first_px[1]))
        if width <= 3 or height <= 3:
            print "Insufficient area: {} px ({}x{})".format(width * height,width,height)
            return

        
        straight = Image.new('RGB', (len(array_2[0]), len(array_2)))
        straight.putdata([tuple(p) for row in array_2 for p in row])
        straight = straight.crop(crop)
        
        #save image and replace if specified
        straight.save('{}_edited.png'.format(self.name))
        if self.replaces:
            os.system('rm -f {}'.format(self.name))
        new_arr = np.array(straight)
            
    def start(self):
        """find average illumination and use that in the threshold value to find the event"""
        avg = self.find_illumination(100)
        self.draw_above_threshold(avg * 5.0)
#ensure user input
if len(sys.argv) == 2:
    name = sys.argv[1]
    #determine if being called on image or directory
    #TODO://fix this
    if name[-4:] == ".png":
        #apply to one image
        i = ImageManipulator(Image.open(name),name)
        i.start()
    else:
        #apply to many images in a directory
        count = 0
        for (dirname,dnames,fnames) in os.walk(name):
            size = len(fnames)
            print "Editing {} files in {}...".format(size,dirname)
            for f in fnames:
                if f[-4:] != '.png':
                    size -= 1
                    continue             
                i = ImageManipulator(Image.open(os.path.join(dirname,f)),name=f,replaces=True)
                i.start()
                
                count += 1
                print "Finished {}, {} of {} complete".format(f,count,size)
        
