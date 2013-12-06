#!/usr/bin/env python
import os
import sys
import commands

f1 = '/var/www/lighttpd'
f1 = '/var/www/lighttpd/tvod/hlshddfws'

print 'os.path.exists ' + f1
print os.path.exists(f1)

print 'os.path.isdir ' + f1
print os.path.isdir(f1)

print 'os.path.isfile ' + f1
print os.path.isfile(f1)

print 'os.path.islink ' + f1
print os.path.islink(f1)
