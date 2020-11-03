#!/usr/bin/env python3

import requests as rq
import os


DIR = "./downloads/"

try: 
    os.mkdir(DIR)
    print("creating " + DIR + "...")
except FileExistsError:
    pass

DFILE = DIR+"/.dfile"
URL = "google.com"

TYPELIST = ["pdf", "djvu"]


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
#print(candidates)

found_files = [] # list to contain all files found on website
for c in candidates: # check which candidates end in a type in TYPELIST
    if "//" in c:
        continue

    flag = False
    for TYPE in TYPELIST:
        if c.endswith(TYPE):
            flag = True
            break

    if flag:
        found_files += [c]

for f in found_files: # Download and store files
    if f not in dlist:
        print("Downloading " + f + "...")

        r = rq.get(URL + f)

        # At this point, elements in found_files might still contain '/'s. this is bad. 
        fname = f.split("/")[-1] 

        stream = open(DIR+fname, 'wb').write(r.content)
        stream.close()

        dfstream = open(DFILE, 'a+')
        dfstream.write(f + '\n')
        dfstream.close()
    else:
        print(f + " already exists!")


