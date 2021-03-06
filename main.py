#!/usr/bin/env python3

import requests as rq
from http.client import responses
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

# URL of the website.
URL = "http://www.math.uni-bonn.de/people/mihatsch/ant/"

# URL for relative paths.
PATHURL = URL
if not URL.endswith("/"):
    PATHURL = ""
    sp = URL.split("/")[:-1]
    for s in sp:
        PATHURL += s + "/"



# TYPELIST is the list of desired filetypes.
TYPELIST = ["pdf", "djvu"]

# follow links to extern URLs:
FOLLOW_EXTERN = False


### Algorithm starts here ###

# load URL
print("Looking for files on " + PATHURL, end="... ")
try:
    r = rq.get(URL)
    print("Status code {}".format(r.status_code))
except:
    print("Connection failed!")

# Check if .dfile exists
if not os.path.exists(DFILE):
    open(DFILE, 'a+').close()
    os.utime(DFILE, None)


# load content of .dfile into dlist
dirfilestream = open(DFILE, 'r')
dlist = dirfilestream.readlines() # .split('\n') 
dlist = [x[:-1] for x in dlist] # remove '\n' from every the end of every entry
dirfilestream.close()



# Scrape URL source
source = r.text # source is a string, containing the source code of URL.
source_split = source.split("\"")[1:]
candidates = [sp.split("\"")[0] for sp in source_split] # candidates contains everything within quotes


# found_files will contain all files referenced on by website source, with fitting endings
found_files = [] 

# filter for canditates with correct file type
for c in candidates: 
    if "//" in c and not FOLLOW_EXTERN:
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
    # At this point, elements in found_files might still contain '/'s. This causes conflicts. In fname, these are removed.
    fname = f.split("/")[-1] 

    if fname not in dlist:
        print("Trying to download " + fname + "...", end=" ", flush=True)

        if "//" in f:
            PURL = f
        else:
            PURL = PATHURL + f

        r = rq.get(PURL)

        if r.status_code != 200:
            print("failed! Message: \"" + str(r.status_code) + ": " + responses[r.status_code] + "\"")
            continue

        # write content to file
        s = open(DIR+fname, 'wb')
        s.write(r.content)
        s.close()

        # append to .dfile
        dfstream = open(DFILE, 'a+')
        dfstream.write(PURL + '\n')
        dfstream.close()

        print("complete!")

    else:
        print(fname + " already exists!")


