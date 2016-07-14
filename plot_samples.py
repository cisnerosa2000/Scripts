#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    import random
    import math
    import matplotlib.pyplot as plt
    from matplotlib.colors import colorConverter
except ImportError,e:
    print "plot_samples.py requires matplotlib"
    print e
    quit()
def find_space(taken,bbox,buf=30):
    x = random.randint(bbox[0],bbox[2]);
    y = random.randint(bbox[1],bbox[3]);
    
    for point in taken:
        if abs(point[0]-x) < buf and abs(point[1]-y) < buf:
            return find_space(taken=taken,bbox=bbox,buf=buf)
            
    return (x,y)
def main(filename):
    infile = None
    with open(filename) as f:
        infile = f.readlines()
    if infile is None:
        print "Failed to read {}".format(filename)
        return
    
    
    
    data = eval(str(infile))
    if type(data) is not list:
        print "{} read; expected dict; got {}".format(filename,type(data))
        return

   # plt.subplot('111',axisbg='black')
    

    limit = 100
    for (index,piece) in enumerate(eval(data[0])):
        if index > limit:
            break
        a = piece['area']
        l = piece['length']
        i = piece['intensity']
        color = float(index)/float(limit)*100-1
                
        fig = plt.gcf()
        size = fig.get_size_inches()*fig.dpi
        
        theta = float(index)/float(limit)
        
        
        plt.plot(a,l,'bo',markersize=10
        )
        
        #plt.annotate(
          #  str(index), 
          #  xy = (a, l), xytext = (-20, 20),
         #   textcoords = 'offset points', ha = 'right', va = 'bottom',
          #  arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0')
     #   )
        
        
        
        
    
    plt.grid(True)
    plt.xkcd()
    
    plt.savefig('outgraph.png')
    plt.show()

if __name__ == "__main__":
    main('out.txt')