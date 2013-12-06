#!/usr/bin/python
import sys
import time
import os
print sys.version

os.system('echo \"' + str(time.time()) + '\" >> /opt/gg')



print 'test end'
