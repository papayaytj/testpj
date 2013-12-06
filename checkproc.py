#!/usr/bin/env python
import os
import sys
import commands

def test():
	global channelName
	print str(channelName)
	channelName = channelName + 2
	print str(channelName)

channelName=1

print 'out1' + str(channelName)
test()
print 'out2' + str(channelName)


