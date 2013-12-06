#!/usr/bin/python
import os
import sys
import time
import datetime
import string
import threading

listSize = 12

def generateSubIndex(keySeq , tsDir , idxTmpFile , idxTargetFile):
    global listSize

    os.system('echo \"#EXTM3U\" > ' + idxTmpFile)
    os.system('echo \"#EXT-X-VERSION:3\" >> ' + idxTmpFile)
    os.system('echo \"#EXT-X-TARGETDURATION:10\" >> ' + idxTmpFile)
    os.system('echo \"#EXT-X-MEDIA-SEQUENCE:' + str(keySeq) + '\" >> ' + idxTmpFile)
    
    for k in range(0 , listSize):
        #pF = time.strftime('%Y%m%d%H',time.localtime(keySeq * 10))
        relatePath = '20131112T123456-6-' + str(keySeq) + '.ts'
        absolutePath = tsDir + '/' + relatePath 
        if not os.path.exists(absolutePath):
            os.system('touch ' + absolutePath)

        os.system('echo \"#EXTINF:10,\" >> ' + idxTmpFile)
        os.system('echo \"' + relatePath + '\" >> ' + idxTmpFile)
        keySeq += 1
        
    os.system('cat ' + idxTmpFile  + ' > ' + idxTargetFile)

if __name__ == "__main__":
    # main(sys.argv[1:])
    s = 1
    dir = '/dev/shm/ftp/live/testhar/workflow06'
    tmpF = dir + '/my.m3u8'
    F = dir + '/workflow06-mnf.m3u8'
    os.system('mkdir -p ' + dir)
    while(True):
        generateSubIndex( s ,dir , tmpF , F)
        print 'current sequence  = ' + str(s)
        s += 1
        time.sleep(10)
