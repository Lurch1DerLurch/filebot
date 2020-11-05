#!/usr/bin/env python3

import requests as rq
import os


# DIR specifies where downloaded files should be stored.
DIR = "./download/"

try: 
    os.mkdir(DIR)
    print("creating " + DIR)
except FileExistsError:
    pass

# DFILE contains the past of .dfile, which keeps track of already-downloaded files.
DFILE = DIR+"/.dfile"

# URL of the website that is to be scraped.
URL = "https://www.math.uni-bonn.de/people/gmartin/AlgebraicGeometryWS2020.html"

# URL for relative paths.
PATHURL = "URL"
if not URL.endswith("/"):
    PATHURL = ""
    sp = URL.split("/")[:-1]
    for s in sp:
        PATHURL += s + "/"

print(PATHURL)


# TYPELIST is the list of desired filetypes.
TYPELIST = ["pdf", "djvu"]



### Algorithm starts here ###

# Check if .dfile exists
if not os.path.exists(DFILE):
    open(DFILE, 'a+').close()
    os.utime(DFILE, None)


# load content of .dfile into dlist
dirfilestream = open(DFILE, 'r')
dlist = dirfilestream.readlines() # .split('\n') 
dlist = [x[:-1] for x in dlist] # remove '\n' from every character in list
dirfilestream.close()


# Scrape URL source
r = rq.get(URL)
source = r.text # source is a string, containing the source code of URL.
source_split = source.split("\"")[1:]
candidates = [sp.split("\"")[0] for sp in source_split] # candidates contains everything within quotes


# found_files will contain all files referenced on by website
found_files = [] 

# filter for canditates with correct file type
for c in candidates: 
    if "//" in c:
        continue

    flag = False  # flag to check filetypes
    for TYPE in TYPELIST:
        if c.endswith(TYPE):
            flag = True
            break

    if flag:
        found_files += [c]

# Download files
for f in found_files: 
    # At this point, elements in found_files might still contain '/'s. this is bad. fname removes those.
    fname = f.split("/")[-1] 

    if fname not in dlist:
        print("Downloading " + fname + "...")

        r = rq.get(PATHURL + f)

        # write content to file
        s = open(DIR+fname, 'wb')
        s.write(r.content)
        s.close()

        # append to .dfile
        dfstream = open(DFILE, 'a+')
        dfstream.write(fname + '\n')
        dfstream.close()

    else:
        print(fname + " already exists!")


