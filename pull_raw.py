#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import os
import sys

#unfortunately necessary due to the recursive nature of the make_folder() function
FOLDER = ""
#the remote dir
SOURCE = "/net/deco/deco_data/"

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
returns a dict containing entries "count" and "items". "Count" is the number of images, "items" is the actual array of images
"""
def fetch_links(f,limit,index=-1):
    with open(f,"r") as csvfile:
        
        r = csv.reader(csvfile)
        result = []
        count = 0
        
        for (i,row) in enumerate(r):
            if i == 0: continue #ignores the defining row
            if count > limit: break
        
            date = row[index]
            date = date.replace("_zoom","").replace("_medium","")
            if '.png' in date:
                result.append("{}.jpg".format(date.replace(".png","")))
                count += 1
        return {"items":result,"count":count}
"""
Takes inputs 'files', 'user', and 'host' and retrieves the given files from 'user'@'host' and stores them in a new folder in the cwd
"""
def download_raw(files,user,host):
    make_folder("raw_deco_data")
    print "Copying files to %s... " % FOLDER
    cmd = ("scp %s@%s:\"%s\" \"%s\"" % (user,host,[os.path.join(SOURCE,x) for x in files],FOLDER)).replace(",","")
    
    for char in ["'","]","["]:
        if char in cmd:
            cmd = cmd.replace(char,"")
    os.system(cmd)
if len(sys.argv) >= 4:
    download_raw(files=fetch_links(sys.argv[1],limit=int(sys.argv[4]) if len(sys.argv)>=5 else 20)["items"],user=sys.argv[2],host=sys.argv[3])
else:
    print """
    Missing last %s argument(s), pull_raw takes minimum 3 args, max 4:
        file: the .csv to pull raw images from
        user: the username of your remote account
        server: the server you wish to use
        limit: the max number of files to retrieve (optional; defaults to 20)
    """ % (5-len(sys.argv))
"""
EXAMPLE USAGE:
    python pull_raw.py deco.csv acisneros cobalt 400
"""       