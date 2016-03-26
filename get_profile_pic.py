#! /usr/bin/python
import sys
import avatar

if len(sys.argv) == 1:
    print "Feed me a Github username"
    quit(-1)

avatar.show(str(sys.argv[1]))
