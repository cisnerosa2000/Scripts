import os
try:
    import requests
except ImportError:
    print "Requires requests module; can be installed locally with 'pip install requests --user'"
    quit()

FOLDER = ''
def make_folder(name,num=None):
    """
    try to make a folder, otherwise make a folder with that name + some number recursively. Fails after 1000 which should be fine
    takes a folder name input
    """
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
def fetch_from_out(path):
    """takes a single string argument 'path' which is a path to the justtracks.out output file"""
    
    
    webpath = 'https://deco-web.wipac.wisc.edu/deco_plots/'
    ls = {}
    count = 0
    with open(path,'r') as f:
        lines = f.readlines()
        for line in lines:
            d = line.split(",")[-1].replace("path:","").replace("\n","").replace(".jpg","_medium.png").split("/")[-2:]
            
            ls[d[1]] = webpath + d[0] + "/" + d[1]
            count += 1
    
    make_folder('files')
    for link in ls:
        dat = requests.get(ls[link],stream=True)
        print ls[link]
        if dat.status_code == 200:
            os.system("touch {}/{}".format(FOLDER,link))
            with open('{}/{}'.format(FOLDER,link),'w') as image_file:
                for chunk in dat:
                    image_file.write(chunk)
        else:
            print "Failed to locate {}".format(link)
            

#edit the argument to match the path of your .out file
fetch_from_out('justtrackpaths.out')