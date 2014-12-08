# EXA Lib

#EXA command used match
import re
import time,datetime
import logging
from util.exa_conf import *
import os
from util.ecrack import ecrack
from socket import inet_aton

def keyboard_exit():
    try:
        sys.stdin.read()
    except KeyboardInterrupt:
        print( "get ctrl-C, exit")
        sys.exit(2)

        
def valid_ip(str):
    try:
        inet_aton(str)
        return True
    except:
        return False

def parse_state(pat_dict,raw):
    res = False
    if type(pat_dict) is not dict:
        print( "pat_dict in not a dictionary, return false")
        return res
    
    ex ='\s*'+'([^\s]+)'+'\s+(.*)'
    pat=re.compile(ex)
    
    list1 = raw.split("\r\n")
    for l in list1:
            m=re.search(pat,l)
            if m:
                x=m.groups()
                if len(x) == 2:
                    pat_dict[x[0]]=x[1]
        
def match_status1(pat_dict,raw):
    
    res = False
    if type(pat_dict) is not dict:
        print( "input a dictionary to match_status1\n")
        return res
    
    for k in pat_dict.keys():
        ex='\s*'+k+'\s+(.*)'
        pat=re.compile(ex)
        m=re.search(pat,raw)
        if m:
            pat_dict[k] = m.groups()[0]
            res = True
            logging.info("%s", k+"is"+str(m.groups()[0]))
        else:
            print( "raw = " + raw)
            print( "ex= " + ex)
    return res

def cleanline(line):    
    l = line
    pat=re.compile(r'\x1b\x5b\x37\x6d|\x1b\x5b\x32\x37\x6d|\x08|\x1b\x5b\x3f\x37\x68')
    m=re.search(pat,line)
    if m:    
        #print( "<<< cleanline = %s " % l)
        l=re.sub(pat,'',line)
    return l
    
# send a 'cmd' to 'conn' and print( the 'cmd')
def sendandprint(conn,cmd):
    res,ret=conn.sendcmd(cmd)
    if res:
        print( "\r\n>>>>>>>>>>>> exalibs.sendandprint START <<<<<<<<<<<<<<<<<<\r\n")
        print( ret)
        print( "\r\n>>>>>>>>>>>> exalibs.sendandprint END <<<<<<<<<<<<<<<<<<\r\n")
    return res,ret

    
# send a cmd from a file without logging
# *** need to add try in file open
def sendfile(conn,cmdfile):    
    f1=open(cmdfile,'r')
    cmds =f1.readlines()
    f1.close()
    
    for cmd in cmds:
        res,cmd=processCmd(conn,cmd)
        if res == 0:
            #res,ret=conn.sendcmd(cmd)
            res,ret=sendandprint(conn,cmd)

def processCmd(conn,cmd):
    res = 0
    cmd1 = cmd.strip().lower()
    commentpat=re.compile('^ *#(.*)')
    m=re.search(commentpat,cmd1)
    if m:
        res = 1
    if cmd1.find('@') <0:
        return res,cmd
    else:        
        res = 1
        if cmd1.find('@exp') >=0:
            explist=cmd.split('\'')
            if len(explist) >=2:
                param = explist[1]
                conn.addMatch(param)
        elif cmd1.find('@wait') >=0:
            explist=cmd.split()
            if len(explist) >=2:
                wait=explist[1]
                time.sleep(int(wait))
        
    return res,cmd
                
def sendfile_wlog(conn,cmdfile,logname):
    if logname != "":
        f=open(logname,'a')
    else:
        f=None
    
    if conn.getSessLogin():

        f1=open(cmdfile,'r')
        cmds =f1.readlines()
        f1.close()
        
        for cmd in cmds:
            res,cmd=processCmd(conn,cmd)
            
            if res == 0:
                print( ">>>>>> about to send cmd %s <<<<<<\n"%cmd)
                res,ret=conn.sendcmd(cmd)
                if f:
                    f.write("\n==========\n%s==========\n"%cmd)
                else:
# print to stdout
                    print(ret)
                    continue 

                if res and f:            
                    f.write(cleanline(ret))    
                    f.write("\n")
                    #print( "<<<<<<<< ret = %s  >>>>>\n"%ret)
                if ret.find('command not found') >=0:
                    print( "*** break!!! ****, got wrong prompt, correct " + cmdfile)
                    break;
    else:
        if f:
            f.write("\n=== %s Login failed ===\n"%host1)
    if f:
        f.close()

        
        
def setStartupxml(conn):
    f = 'setStartup.cmd'
    conn.entLinux()
    sendfile(conn,f)

def cpRunningStartup(conn):
    conn.entCLI()
    res,ret=conn.sendcmd("accept running-config")
    res,ret=conn.sendcmd("copy running-config startup-config")

    
def getBasicConfig(conn,logfile=''):
    conn.entCLI()
    cmd = cmdfile_base+'getbasicConfig.cmd'
    if logfile == '':
        sendfile(conn,cmd)    
    else:
        sendfile_wlog(conn,cmd,logfile)
    
# get upgrade states from 'show upgrade status'
def getupgstate(conn):
    conn.entCLI()
    res,ret=conn.sendcmd("show upgrade status")
    
    if res:
        #print ret
        pat_dict={'state':'','reason':'','curl_error':'',\
        'install_error':'','download_percent_complete':'',\
        'remote-filename':''}
        res=match_status1(pat_dict,ret)
        if not res:
            print( pat_dict)
    else:
        print( "show upgrade status failed")
    return res,pat_dict

def getupgstatus(conn):    
    st = ""
    res,upgstate_dict=getupgstate(conn)
    #print "**** upgstate_dict ****"
    if res:
        st=upgstate_dict['state']                        
    #    print( "st = " + st )
    else:
        print( "exalibs:getupgstatus can't get upgrade status, res is false")
    
    return st
    
def startupg(conn,bldimg):
    conn.entCLI()
    res,ret=conn.sendcmd("upgrade activate filename "+bldimg)    
    if res:
        if ret.find('Error') >= 0:
            print( "send command result contains error !!!")
            res = False
        else:
            print( "debug print upgrade return is: \n" + ret)
            
    return res,ret
    
def upgdownload(conn,bldimg):
    conn.entCLI()
    conn.sendcmd("upgrade download filename "+bldimg)


def unlock_root(conn):
    res,ret=conn.sendcmd("shell")
    res,ret=conn.sendcmd("passwd -u root")
    return res,ret
    
def getecrack_pl(hostname,timestr):
    cmd="perl /home/hochen/prog/perl/ecrack.pl "+hostname+' '+timestr
    print( "in getecrack_pl, cmd = "+cmd)
    str1=os.popen(cmd).read()
    pat='The password for the default and debug users are: (.*)\n'
    m=re.search(pat,str1)
    pw=''
    if m:
        pw=m.groups()[0]
    print( "in getecrack_pl, pw = " + pw)
    return pw

def getecrack_ts():
    ts=time.time()
    day3=datetime.datetime.fromtimestamp(ts).strftime('%A')[:3]
    mon3=datetime.datetime.fromtimestamp(ts).strftime('%B')[:3]
    st_crack = datetime.datetime.fromtimestamp(ts).strftime('%d %H:%M:%S %Y')
    st_crack = "%s %s "+st_crack
    st_crack = st_crack % ( day3, mon3)
    return st_crack

def getecrack_fromhostname(hostname):
    ts=getecrack_ts()
    return getecrack_pl(hostname,ts)


def getecrack_py(hostname=None,ts=None,host_ts=None):

    timestr = time.asctime()
    
    if hostname is not None:
        if ts is not None: # use current time
            timestr = ts
        return ecrack(hostname,timestr)
        
    elif host_ts is not None:
        tmlist = host_ts.split()
        hostname=tmlist[0]    
        timestr=' '.join(tmlist[1:])
        return ecrack(hostname,timestr)
        
    
    pw=ecrack(hostname,timestr)
    print( "pw=%s"%pw)
