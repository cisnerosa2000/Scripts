from skimage import measure
import os
from PIL import Image
import numpy as np
#import matplotlib.pyplot as plt
from itertools import izip
import math

def pairwise(iterable):
    a = iter(iterable)
    return izip(a, a)
def crop(fname):
    # takes a filename 'image' and crops it by 100,100,100,175. Returns this as a PhotoImage for use with tk canvas .

    image = Image.open(fname)
    c = (100,100,image.width-100,image.height-175)
    image = image.crop(c)
    return image
def to_array(image,size):
    result = []
    avg = 0
    m = 0
    for y in range(size[1]):
        row = []
        for x in range(size[0]):
            r,g,b,a = image[x,y]
            av = (r+g+b)/3.0/255.0
            row.append(av)
            avg += av
            if av > m and av != 1.0:
                m = av
        result.append(row)
        
    avg /= float(size[0] * size[1])
    return result,avg,m
def magnitude(p0,p1):
    a = p0[0] - p1[0]
    b = p0[1] - p1[0]
    return math.sqrt()
def process(name,target_size):
    global FAILURES
    im = Image.open(name)
    w,h = im.size
    
    px = im.load()
    im_arr,avg,max_intensity = to_array(px,(w,h))
    print max_intensity
    npim = np.array(im_arr,dtype=float)
    
    intensity_threshold = 10.0
    cc = measure.find_contours(npim,10.0)#avg*intensity_threshold)
    
    #display in pyplot
   # pyim = plt.imread(name)
    #plt.imshow(pyim)
    # plt.plot(cc[0][:, 1], cc[0][:, 0], linewidth=2)
        
    
    #find largest and smallest point in order to create bbox
    largest = [0,0]
    smallest = [w,h]
    changed = False
    
    try:
        for i in range(len(cc[0][:,1])):
            x = cc[0][:,1][i]
            y = cc[0][:,0][i]
        
            if x < smallest[0]:
                smallest[0] = x
            if y < smallest[1]:
                smallest[1] = y
            if x > largest[0]:
                largest[0] = x
            if y > largest[1]:
                largest[1] = y
    except:
        if not changed:
            FAILURES += 1
            changed = True
            
    
    #crop image so only event is visible and save
    try:
        im.crop((smallest[0],smallest[1],largest[0],largest[1])).save('/users/cisnerosa/desktop/results/{}'.format(name.split("/")[-1]))
    except:
        if not changed:
            FAILURES += 1
            changed = True
    
pth = '/Users/cisnerosa/Desktop/classification/Track/'
count = 0
FAILURES = 0
for (dname,dnames,fnames) in os.walk(pth):
    total = len(fnames)
    for fname in fnames:
        count += 1
        print "{}/{}({}%)".format(count,total,int(float(count)/float(total)*100))
        if fname [-4:] != '.png':
            continue
        process(pth+fname,(32,32))
    print "{} completed, {} failed. {}% success rate (best case)".format(total,FAILURES,int(float(total-FAILURES)/float(total)*100))
        
        
        
        
        
        
        
        
                