#!/bin/python3

#You can change this code if you like.  
#It does show you that the program needs to be invoked with either "clean" or
#or a url.  The clean is added as a simple way to delete the cache directory
#and the files referenced by it.
#
#My implementation used two classes: 
#cacheDir - managed the cache directory and the files containing objects
#proxyClient - returns the requested object 

import sys
from proxyClient import *
from cacheDir import *

if (len(sys.argv) < 2):
    print("usage: proxy.py <url>")
    print("       Retrieves and displays the object at the given url.")
    print("usage: proxy.py clean")
    print("       Deletes the cache directory and the object files named in the directory.")
else:
    if sys.argv[1] == "clean":
       cachedir = cacheDir()
       cachedir.clean()
    else:
       cachedir = cacheDir()
       client = proxyClient(sys.argv[1], cachedir)
       client.getObject()


