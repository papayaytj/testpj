#!/usr/bin/python

from integrity import *


def action(argv):
    try:
        basePath = argv[0]
        channelCode = argv[1]
        step = argv[2]

        checkTime = time.time()
        filePre = 'workflow'
        for i in range(1 , step + 1):
            checkPath = basePath
            if not checkPath.endswith('/'):
                checkPath += '/'
            checkPath += channelCode
            if not checkPath.endswith('/'):
                checkPath += '/'
            checkPath += filePre + str(i)
            integraty = Integraty(checkTime , checkPath)
            result =  str(integraty.compareMd5())

            if not result:
                print 'start get miss file '
            #print i
    except Exception , e:
        print e
    return True



if __name__ == '__main__':
    try:
        action(['/var/www/lighttpd/live' , 'hlshddfws' , 3])
        #integraty = Integraty(time.time() , '/var/www/lighttpd/live/hlshddfws/workflow1')
        #print str(integraty.compareMd5())
    except Exception , e :
        print e
