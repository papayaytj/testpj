#!/usr/bin/python  
# -*- coding: utf-8 -*-  
   
""" 
define common switch operation method, like : 
    telnet(ip,usr,pwd,enable_pwd) 
    ssh(ip,usr,pwd,enable_pwd) 
    remote_telnet_nf(ip,usr,pwd,enable_pwd) 
    send_cmd(cmd,sleep_time) 
    send_event_cmd(cmd, event_interval) 
    event_test(cmd,event_interval, stop_time) 
""" 
   
__author__ =  'Godlaughing' 
   
   
import os  
import re  
import sys  
import time  
import pexpect  
   
   
known_dut = {  
    '1.1.1.1':{'usr':'root','pwd':'abc'},  
    '2.2.2.2':{'usr':'root','pwd':'123'},  
   
}  
   
   
   
def telnet(ip='127.0.0.1', usr='root', pwd='123', enable_pwd=''):  

   
    global session  
    if usr is 'root' and ip in known_dut:  
    usr = known_dut[ip]['usr']  
    if pwd is "123" and ip in known_dut:  
    pwd = known_dut[ip]['pwd']  
   
    session = pexpect.spawn('telnet %s' % ip, maxread=10000)  
    session.logfile_read = sys.stdout  
    #session.logfile_read = file('/var/log/switch_log/%s_%s' % ('icos', time.strftime("%Y%m%d")), 'a+')  
    index = session.expect(['ser:','>','word:','pexpect.TIMEOUT','pexpect.EOF'])  
    if index == 0:  
        session.sendline(usr)  
        session.expect('word:')  
        session.sendline(pwd)  
        index = session.expect(['>',':','#'])  
    if index == 1:  
        raise Exception('your username %s or password %s is wrong!' % (usr,pwd))  
        elif index == 2:  
        index = 10 
           
    elif index == 1:  
        pass 
   
    # telnet use line password  
    elif index == 2:  
        session.sendline(pwd)  
        index = session.expect(['>',':','#'])  
        if index == 1 :  
            raise Exception('your password is wrong!')  
        elif index == 2:  
        index = 10 
    elif index == 3 or index == 4:  
        raise Exception('can not telnet to %s' % ip)  
   
    if index != 10:  
        session.sendline('enable')  
        index = session.expect([':','#'])  
        if index == 0:  
            session.sendline(enable_pwd)  
            session.expect(['#','>'])  
            if index == 1 :  
                    raise Exception('your password is wrong!')  
       
    _config_pre_cmd()  
      
   
def ssh(ip,usr="root", pwd="123", enable_pwd=""):  
    """ssh to device. 
 
    args: 
        ip: the switch ip you want to ssh. no default value. 
        usr: login username, default: root 
        pwd: login password, default: 123 
        enable_pwd: enable password, default: '' 
 
    """ 
   
    global session  
    if usr is 'root' and ip in known_dut:  
        usr = known_dut[ip]['usr']  
    if pwd is "123" and ip in known_dut:  
        pwd = known_dut[ip]['pwd']  
   
    session = pexpect.spawn('ssh %s@%s' % (usr,ip), maxread=10000)  
    session.logfile_read = sys.stdout  
    index = session.expect(['yes/no','word:','pexpect.TIMEOUT','pexpect.EOF'])  
    if index == 0:  
        session.sendline('yes')  
        session.expect('word:')  
        index = 1 
   
    if index == 1:  
        session.sendline(pwd)  
        index = session.expect(['>','word:','#'])  
        if index == 1 :  
            raise Exception('your username %s or password %s is wrong!' % (usr,pwd))  
        if index == 2 :   
        index = 100 
    if index == 2 or index == 3:  
        raise Exception('can not ssh to %s' % ip)  
   
    if index != 100:  
        session.sendline('enable')  
        index = session.expect([':','#'])  
        if index == 0:  
        session.sendline(enable_pwd)  
        session.expect(['#','>'])  
        if index == 1 :  
            raise Exception('your password is wrong!')  
       
    _config_pre_cmd()  
   
def send_cmd(cmd,sleep_time=0.01):  
    '''''send commands to switch that telnet/ssh before. 
      
    args: 
        cmd: command, use ';' or line feed like the output of 'show run' or both to seperate commands. 
        sleep_time: sleep for x second after send a command, default: 0.1. 
 
    returns: 
        the output of the commands. 
 
    raises: 
        Exception: the session is dead or not exists. 
    ''' 
   
    cmd = cmd.replace(';','\n')  
    cmd_list = cmd.split('\n')  
    output = ''  
    for command in cmd_list:  
        command = command.strip()  
        # python function  
        if command.find('(') > 0 and command.endswith(')') is True:  
            exec(command)  
        else:      
            session.sendline(command)  
            time.sleep(sleep_time)  
            index = session.expect(['y/n','yes/no','#','>','pexpect.TIMEOUT','pexpect.EOF'])  
            if index == 0 or index == 1:  
                output += session.before  
                session.send('y')  
                session.expect(['#','pexpect.TIMEOUT','pexpect.EOF'])  
            output += session.before  
        time.sleep(sleep_time)  
    return output  
   
def send_event_cmd(cmd, event_interval=30):  
    """send commands to switch that telnet/ssh before in event testing. 
 
    args: 
        cmd: command, use ';' or line feed like the output of 'show run' or both to seperate commands; 
            leave empty after triple quote, and never put ';' in the end of line; 
            blank line, will sleep event_interval; 
            you can also add 'sleep x' in cmd for sleep x seconds. 
        event_interval: sleep for x second after send a event test, default: 30. 
 
    returns: 
        the output of the commands. 
 
    raises: 
        Exception: the session is dead or not exists. 
    """ 
   
    cmd = cmd.replace(';','\n')  
    cmd_list = cmd.split('\n')  
    output = ''  
    for command in cmd_list:  
        command = command.strip()  
        if command == '':  
            time.sleep(event_interval)  
        elif command.find('sleep') == 0:  
            interval = command.split()[1]  
            time.sleep(float(interval))  
        else:  
            output += send_cmd(command)  
    return output  
   
def event_test(cmd,event_interval=30, stop_time='1d8',run_times=0):  
    """send cmd repeatedly in event testing. 
 
    args: 
        cmd: command, use ';' or line feed like the output of 'show run' or both to seperate commands; 
            leave empty after triple quote, and never put ';' in the end of line; 
            blank line, will sleep event_interval; 
            you can also add 'sleep x' in cmd for sleep x seconds. 
        event_interval: sleep for x second after send a event test, default: 30. 
        stop_time: the time to stop run this script. default '1d8' means tomorrow 8:00. 
            '1d' means after the 24:00, not 24 hours,8 means at 8:00. 
            it will not just stop at stop_time, it depends on the total time for run once. 
        run_times: the num of running times. default 0 means ignore this arg. 
 
    returns: 
        the output of the commands. 
 
    raises: 
        Exception: the session is dead or not exists. 
    """ 
    begin_day = time.localtime()[2]  
    (stop_day,stop_hour) = stop_time.split('d')  
    i = 1 
    while 1:  
        print " \n## ==== %s, the %s time begin ====\n" % (time.strftime("%Y-%m-%d %X"), i)  
        send_event_cmd(cmd,event_interval)  
        today = time.localtime()[2]  
        hour = time.localtime()[3]  
        if run_times > 0:  
            if i >= run_times:  
                print " \n## ==== %s, the %s time end, test done! ====\n" % (time.strftime("%Y-%m-%d %X"), i)  
                return "ok" 
        else:  
            if today - begin_day == int(stop_day) and hour >= int(stop_hour):  
                print " \n## ==== %s, the %s time end, test done! ====\n" % (time.strftime("%Y-%m-%d %X"), i)  
                return "ok" 
         
        i += 1 
def exit_session():  
    """exit from telnet/ssh session. 
 
    args: 
        name: session name, default is global var 'sessoin'. 
      
    returns: 
        None 
      
    raises: 
        default exception 
    """ 
    global session  
   
   
def log_with_date(msg):  
    print "\n", time.strftime("%Y-%m-%d %X"), "INFO:", msg, "\n" 
   
def debug_log(name, msg):  
    """ print the value of 'name' 
     args: 
        name: the string of msg 
    """ 
    print "--------- debug %s --------" % name  
    print msg  
    print "-----------------------------" 
    session.close()  
   
   
def _config_pre_cmd():  
    """ config some pre command """ 
   
    output = send_cmd("")  
    if output.find("~") > 0:  
        return 
        
    session.sendline("show version")  
    index = session.expect(['#','--More--'])  
    output = session.before  
    if index == 1:  
        session.sendline("q")  
    
    if output.find('xxx') > 0 :  
        send_cmd("yyy")  
    elif output.find('Broadcom') > 0 :  
        send_cmd("terminal length 0")  