#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    import random
    import math
    import linepoints as lp
    import sys
    import os
    from PIL import Image
except ImportError,e:
    print "Failed import: {}".format(e)
    quit()



class Size(object):
    """represents a size, takes integer width and height parameters"""
    def __init__(self,width,height):
        self.width = width
        self.height = height
    def __iter__(self):
        """
        allow unwrapping of values; e.g.
       
        >>> s = Size(100,200)
        >>> width, height = s
        >>> width
        100
        >>> height
        200
        
        """
        yield self.width
        yield self.height
    def area(self):
        return self.width * self.height
    def perimeter(self):
        return self.width * 2 + self.height * 2
    def aspect_ratio(self):
        return self.width/self.height
class Point(object):
    """represents a 2 dimensional point, takes integer x and y parameters"""
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def __iter__(self):
        """
        allow unwrapping; e.g.
        >>> p = Point(33,94)
        >>> x,y = p
        >>> x
        33
        >>> y
        94
        """
        yield self.x
        yield self.y
    def __str__(self):
        """overload print for prettier printing"""
        return "(x: {}, y: {})".format(self.x,self.y)
class Vector(object):
    """represents a 2 dimensional vector in a cartesian coordinate system, takes float or integer dx,dy parameters"""
    def __init__(self,dx,dy):
        self.dx = dx
        self.dy = dy
    def __mul__(self,other):
        """
        override multiplication operator for convenience;
        given a vector pv, 
        
        >>> pv.x = pv.x * speed
        >>> pv.y = pv.y * speed
        
        becomes
        
        >>> pv = pv * speed
        
        and given two vectors, pv0 and pv1,
        
        >>> pv0.x = pv0.x * pv1.x
        >>> pv0.y = pv0.y * pv1.y
        
        becomes
        
        >>> pv0 = pv0 * pv1
        
        """
        t = type(other)
        if t is int or t is float:
            return Vector(self.dx * other,self.dy * other)
        elif t is Vector:
            return Vector(self.dx * other.dx, self.dy * other.dy)
    def __iter__(self):
        """
        allow unwrapping;
        given Vector pv with x 0.75 and y 0.65,
        
        >>> dx,dy = pv
        >>> print dx
        0.8
        >>> print dy
        0.65
        """
        yield self.dx
        yield self.dy
        


class Segment(object):
    """Utility two dimensional line segment class, takes two Point() parameters as the origin and endpoint of the segment"""
    def __init__(self,p1,p2):
        self.origin = p1
        self.endpoint = p2 
    def __str__(self):
        """overload the print operation for readability"""
        return "(x0: {}, y0: {}, x1: {}, y1: {})".format(self.origin.x,self.origin.y,self.endpoint.x,self.endpoint.y)
    def __iter__(self):
        """allow unwrapping of segment coordinates"""
        yield self.origin.x
        yield self.origin.y
        yield self.endpoint.x
        yield self.endpoint.y
    def formula(self):
        """return a lambda that represents the slope intercept form of the line the segment is on f(x) = slope * x + intercept"""
        slope = self.u_vector().dy / self.u_vector().dx
        intercept = self.origin.y - (slope * self.origin.x)
        return lambda x: x * slope + intercept 
    def magnitude(self):
        """return  the length of the segment"""
        return math.sqrt( ((self.origin.x - self.endpoint.x) ** 2) + ((self.origin.y - self.endpoint.y) ** 2) )
    def u_vector(self):
        """returns the unit vector of the segment"""
        m = self.magnitude()
        return Vector(self.origin.x-self.endpoint.x/m,self.origin.y-self.endpoint.y/m)


def polar2cartesian(theta):
    """takes an angle in radians and returns a unit vector point"""
    return Vector(math.cos(theta),math.sin(theta))
def filled_array(size,char=0):
    """returns a square 2d array with the width and height of the 'size' parameter, filled with the 'char' parameter"""
    result = []
    for y in range(size.height):
        row = []
        for x in range(size.width):
            row.append(char)
        result.append(row)
    return result

def display(arr):
    """pretty print a 2d array to stdout"""
    if arr == None:
        return
    print "-" * len(arr)
    for (y,row) in enumerate(arr):
        for (x,char) in enumerate(row):
            sys.stdout.write(str(neighbors(arr,Point(x,y))))
        sys.stdout.write("\n")
def colorize(arr):
    """take a 2d array of 1's and 0's and return a 3d array of rgb values in an image as well as the average brightness of a pixel"""
    if arr is None:
        return None
    array = arr
    
    intensities = []
    for (y,row) in enumerate(array):
        for (x,col) in enumerate(row):
            #0 is empty, 1 is a pixel
            if col == 0:
                array[y][x] = [0,0,0]
            elif col == 1:
                array[y][x] = [1,1,1]
                #find neighboring pixels and use that to determine luminance
                popularity = float(neighbors(array,Point(x,y),8))
                #scale popularity to 0-255
                lum = int(popularity * 255.0)
                intensities.append(lum)
                array[y][x] = [lum,lum,lum]
    avg = 0
    for x in intensities: avg += x
    avg /= len(intensities)
    
    
    return array,avg
def save(image,name,path=None):
    """save an image represented as a 3d array with name to path"""
    if image is None:
        return
    path = path if path is not None else os.getcwd()
    im = Image.new('RGB', (len(image[0]), len(image)))
    im.putdata([tuple(p) for row in image for p in row])
    im.save('{}/{}'.format(path, name))        
def neighbors(array,pos,width=1):
    """Find all neighbors of a 2D point 'pos' in a 2D array within 'width' indices,
        returns a scaled float from 0.0 to 1.0 representing percentage of filled pixels in surroundings
    """
    n = []
    count = 0
    string = "array[pos.y+%s][pos.x+%s]"
    for i in range(-width,width+1):
        for j in range(-width,width+1):
            if i + pos.y < len(array) and j + pos.x < len(array):
                n.append(eval(string % (i,j)))
    for i in n:
        if i != [0,0,0] and i != 0:
            count += 1
    return float(count-1) / house_count(width)
def house_count(size):
    """
    used to find the area of a square with 'size' layers, used in the neighbors() function
    width is the distance from the center to perimeter
    e.g.
    
    square with size 1 that would return 8
    
    v
    000
    010
    000
    
    square with size 2 that would return 24
    
    vv
    00000
    00000
    00100
    00000
    00000
    """
    total = 0
    for i in range(size):
        total += i * 8
    return total
    
    
    
    
def thicken(array):
    """take a 2D array and thicken any shapes drawn"""
    if array is None:
        return None
    array = array
    for (y,row) in enumerate(array):
        for (x,col) in enumerate(row):
            if col != 1:
                continue
            
            chance = 70
            #has a 'chance'% chance of adding random variation to array
            if random.randint(0,100) <= chance:
                for i in range(random.randint(0,3)):
                    xv = random.randint(-1,1)
                    yv = random.randint(-1,1)
                
                    try: array[y+yv][x+xv] = 1
                    except IndexError: pass
            
    return array
            
    
    
    
def generate_track(size = 32,length_threshold = 16):
    """takes optional size and length_threshold integer parameters, width/height of array and minimum length of track"""
    
    #the 'image' array that will be returned
    result = filled_array(Size(size,size))
    
    x0 = random.randint(0,size-1)
    y0 = random.randint(0,size-1)
    
    x1 = int((size-x0) * random.random())
    y1 = int((size-y0) * random.random())
    
    p1 = Point(x0,y0)
    p2 = Point(x1,y1)
    
    line = Segment(p1,p2)
    #ensure a long enough line
    if line.magnitude() < length_threshold:
        generate_track(size,length_threshold)
    #generate a line from segment and write it to result
    for (x,y) in lp.points_on(line,size):
        try:
            result[y][x] = 1
        except IndexError:
            print "-" * size
            print "Failed to write (x: {}, y: {})".format(x,y)
            if Segment(Point(x0,y0),Point(x,y)).magnitude() < length_threshold:
                return generate_track(size,length_threshold)
    return result,line.magnitude()



def area(array):
    """find number of filled pixels in 2d array of integers"""
    count = 0
    for row in array:
        for val in row:
            if val != 0:
                count += 1
    return count


fakes = 100
sample_data = []
for i in range(fakes):
    #128x128 array with minimum 8px length
    t,length = generate_track(size=128,length_threshold=8)
    #thicken lines in array 10 times
    for layer in range(15): t = thicken(t)
    a = area(t)
    #convert array to 3d array of color
    t,lum = colorize(t)
    
    payload = {"area":a,"length":length,"intensity":lum}
    sample_data.append(payload)
    #convert to image and save
    save(image=t,name='fake_{}.png'.format(i),path='/Users/cisnerosa/Desktop/Fake_Samples')
    print "{} of {} ({}%)".format(i+1,fakes,int(float(i+1)/float(fakes) * 100))
    
print sample_data
with open('out.txt','w') as outfile:
    outfile.write(str(sample_data))