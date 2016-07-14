#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import os
import sys
try:
    import requests
except ImportError:
    print "pull_links.py requires requests for fetching the images from the server\nYou can download requests using 'pip install requests --user'"
    sys.exit(0)



#unfortunately necessary due to the recursive nature of the make_folder() function
FOLDER = ""

"""
try to make a folder, otherwise make a folder with that name + some number recursively. Fails after 1000 which should be fine
takes a folder name input
"""
def make_folder(name,num=None):
    global FOLDER
    try:
        if num is None:
            os.mkdir(name)
            FOLDER = name
        else:
            os.mkdir("{}_{}".format(name,num))
            FOLDER = "{}_{}".format(name,num)
    except OSError:
        make_folder(name,0 if num is None else num + 1)
"""
takes an input csv file 'f' and an optional row index 'index' and returns a dict containing the number of items 
'count' and the resulting items 'items'. By default index is -1, which will return the links of a deco.csv
also has an input 'type'. there are 2 variations of each image, medium and zoom, zoom is the default.
returns a dict containing entries "count" and "items". "Count" is the number of images, "items" is the actual array of images
"""
def fetch_links(f,typeof="zoom",index=-1):
    with open(f,'r') as csvfile:
        
        r = csv.reader(csvfile)
        result = []
        count = 0
        
        for (i,row) in enumerate(r):
            if i == 0: continue #ignores the defining row
        
            date = row[index]
            date = date.replace("_zoom","").replace("_medium","")
            if ".png" in date: 
                result.append("{}_{}.png".format(date.replace(".png",""),typeof))
            
            count += 1
        return {"items":result,"count":count}
"""
takes a list of filenames 'files', and optional inputs 'folder_name' and 'max_files' and downloads files and places into cwd/'folder_name' until it reaches 'max_files' number of files
"""
def download(files,folder_name="deco_data_images",max_files=200):
    prefix = "https://deco-web.wipac.wisc.edu/deco_plots/"
    
    #create folder to hold images
    make_folder(folder_name)
    successes = 0
    for (index,f) in enumerate(files):   
             
        link = prefix + f        
        f = f[f.index("/"):] #remove the directory included in the name; we can get the event name from the id anyways
        
        dat = requests.get(link,stream=True)
                
        if dat.status_code == 200:
            os.system("touch {}/{}".format(FOLDER,f))
            with open('{}/{}'.format(FOLDER,f),'w') as image_file:
                for chunk in dat:
                    image_file.write(chunk)
            print "Successfully downloaded {} to {}. File #{} of {} ({} failed)".format(f,FOLDER,successes,max_files,index-successes)
            successes += 1
        else:
            print "Failed to locate {}".format(link)
        if successes > max_files:
            break
"""
For ordinary use, call fetch_links() on some csv file downloaded from https://wipac.wisc.edu/deco/data and store the result,
            and then call download() on the "items" of that result
            
            e.g.:
                links = fetch_links("deco.csv")
                download(links["items"])
            
            will download up to 200 images found in data.csv to a new folder in the cwd named "deco_data_images"

Can be called from command line with the following syntax (uses default arguments):
         python pull_links.py /path/to/file.csv
"""
#if len(sys.argv) == 2 and __name__ == "__main__":      
    #links = fetch_links(sys.argv[1],typeof='medium')
    
