#!/usr/bin/python

import time
import os , sys , os.path
import md5
import logging

class Integraty():
    """
    in:   1.time 2.path 3.
    out:  1.misslist 2.result
    """
    
    def __init__(self , checkTime = time.time(), path = ''):
        self.checkTime = checkTime
        self.path = path
        self.directPath = ''
        print 'time = ' + str(self.checkTime)
        print 'paht = ' + path
    
    def compareMd5(self):
        calStrs = self.calculateFileNameMd5()
        print 'calStr:' + str(calStrs)
        realStr = self.realFileNameMd5()
        print 'realStr:' + str(realStr)

        if realStr in calStrs:
            return True

        #for item in calStrs:
        #    print '### ' + item + '/' + realStr
        #    if item == realStr:
        #        return True
        return False

    def realFileNameMd5(self):
        hourFmt = '%Y%m%d%H'
        timeToHour = self.stamp2time(self.checkTime , hourFmt)
        p = self.path + '/' + timeToHour
        self.directPath = p

        if os.path.exists(p):
            pubStr = ''
            list = os.listdir(p)
            list.sort(self.compare)
            for item in list:
                rItem = p + '/' + item
                if os.path.islink(rItem):
                    #print 'link path ' + rItem
                    #print rItem + ' --> '+  os.readlink(rItem)
                    if os.path.exists(os.readlink(rItem)):
                        pubStr += item
                else:
                    pubStr += item
            #print 'pathPubStr : ' + pubStr
            return self.getStrMd5(pubStr)
        else:
            print p + 'not exists'
            return '-1'

    def calculateFileNameMd5(self):
        hourFmt = '%Y-%m-%d %H'
        timeToHour = self.stamp2time(self.checkTime , hourFmt)
        curHourTimeStamp = self.time2stamp(timeToHour , hourFmt)
        #print str(self.checkTime) + '/' + str(curHourTimeStamp)

        end = int(self.checkTime // 10)
        start = int(curHourTimeStamp // 10)
        #print 'start=' + str(start) + '/ end = ' + str(end)
        

        recentsMd5Strs = []
        for x in [-3, -2, -1 , 0 ,1 , 2]:
            pubStr = ''
            for i in range(start , end + x):
                pubStr += str(i) + '.ts'

            #print 'pubStr ' + pubStr
            md5Str = self.getStrMd5(pubStr)
            recentsMd5Strs.append(md5Str)
        return recentsMd5Strs

    def compare(self , x, y):
        stat_x = os.stat(self.directPath + "/" + x)
        stat_y = os.stat(self.directPath + "/" + y)
        if stat_x.st_ctime < stat_y.st_ctime:
            return -1
        elif stat_x.st_ctime > stat_y.st_ctime:
            return 1
        else:
            return 0

    def getStrMd5(self , str):
        return  md5.new(str).hexdigest()

    def time2stamp(self,timestr, format_type='%Y-%m-%d %H:%M:%S'):
        return time.mktime(time.strptime(timestr, format_type))

    def stamp2time(self,stamp, format_type='%Y-%m-%d %H:%M:%S'):
        return time.strftime(format_type, time.localtime(stamp))


if __name__ == '__main__':
    integraty = Integraty(time.time() , '/var/www/lighttpd/live/hlshddfws/workflow1')
    print str(integraty.compareMd5())


