#!/usr/bin/python

import pexpect

def fscpl2r(src , login , passwd , host , target):
    ssh_newkey = 'Are you sure you want to continue connecting'
        
    p = pexpect.spawn('scp -P 9999 %s %s@%s:%s' % (src , login , host , target))
    try:
        i = p.expect([ssh_newkey , 'password:'] , timeout = 5)
        if i == 0:
            p.sendline('yes')
            p.expect('password:')
            p.sendline(passwd)
        elif i == 1 :
            p.sendline(passwd)
    except pexpect.EOF:
        print 'EOF'
        p.close()
        return 'eof'
    except pexpect.TIMEOUT:
        print 'time out'
        p.close()
        return 'timeout'
    else:
        print 'ok'

    r = p.read()
    p.close()
    return r
    

if __name__ == '__main__':
    ret = fscpl2r('/opt/gg' , 'wanghao' , 'bestv' , '10.50.134.209' , '/home/wanghao')
    print ret

