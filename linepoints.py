#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math

class Point(object):
    """Utility two dimensional point class, takes integer x and integer y parameters"""
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def __iter__(self):
        """allow the value to be unwrapped; e.g.
        
            >>> p = Point(10,-5)
            >>> x,y = p
            >>> print x
            10
            >>> print y
            -5
            
        """
        yield self.x
        yield self.y
class Segment(object):
    """Utility two dimensional line segment class, takes two Point() parameters as the origin and endpoint of the segment"""
    def __init__(self,p1,p2):
        self.origin = p1
        self.endpoint = p2 
    def __str__(self):
        """overload the print operation for readability"""
        return "(x0: {}, y0: {}, x1: {}, y1: {})".format(self.origin.x,self.origin.y,self.endpoint.x,self.endpoint.y)
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
class Vector(object):
    """Utility two dimensional vector, takes a dx and dy integer"""
    
    def __init__(self,x,y):
        self.dx = x
        self.dy = y
    def __mul__(self,other):
        """overload multiplication for convenience"""
        t = type(other)
        if t is int or t is float:
            return Vector(self.dx * other,self.dy * other)
        elif t is Vector:
            return Vector(self.dx * other.dx, self.dy * other.dy)
    def __iter__(self):
        """allow value to be unwrapped; e.g.
        
            >>> pv = Vector(0.7,0.6)
            >>> x,y = pv
            >>> print x
            0.7
            >>> print y
            0.6
        """
        yield self.dx
        yield self.dy
    
def corrected(point,size):
    """corrects points outputted by points_on() by adjusting them if they exceed the bounds of the given size"""  
    x = point[0]
    y = point[1]
    
    if x >= size:
        x = size-1
    if y >= size:
        y = size-1
    return (x,y)
    


def points_on(line,size=None):
    """
        Generator function that takes a Segment() line parameter and an optional integer size parameter.
        Yields all points on the segment using Brenham algorithm as long as they are within a square that has the width and height of the size parameter, 
        otherwise they are adjusted to fit. If the size is omitted, all points are yielded with no adjustment.
    
        USAGE:
            for (x,y) in points_on(Segment(Point(x1,y1),Point(x2,y2))):
                #do something with (x,y)
                pass
        Obviously segment and points can and *should* be initialized before being passed to points_on()
    """
    
    # Setup initial conditions
    x1, y1 = line.origin.x,line.origin.y
    x2, y2 = line.endpoint.x,line.endpoint.y
    dx = x2 - x1
    dy = y2 - y1
 
    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)
 
    # Rotate line
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
 
    # Swap start and end points if necessary and store swap state
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True
 
    # Recalculate differentials
    dx = x2 - x1
    dy = y2 - y1
 
    # Calculate error
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1
 
    # Iterate over bounding box generating points between start and end
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx
 
    # Reverse the list if the coordinates were swapped
    if swapped:
        points.reverse()
    #yield points and correct them to ensure that they are within the given array size
    for p in points:
        yield corrected(p,size) if size is not None else p
    