import argparse
import re,sys
from threading import Thread
from optparser import getHostlist_fromOpt,parseCmd
from util.connect_remote import RMT_CONN
from util.mylog import mylogger

def sendcmd(host,cmd,cmdf,username='calixsupport',password=''):
    #get connection
    conn = RMT_CONN(verbose=0,host=host,userid=username,password=password,timeout=10,port=22)
    sess = conn.connect_ssh()
    #send command
    if conn.getSessLogin() and len(cmd) > 1:
        res,ret = conn.sendcmd(cmd)
        if res:
	    mylogger.debug(ret)
    elif conn.getSessLogin() and len(cmdf) > 0:
        mylogger.info("cmd file = %s" % cmdf
)
        pass
    else:
        mylogger.info("%s is not reachable" % host
)
        return None

    #output result
       

def action():
    mylogger.info( "###### in sendcmd v2 ########")

#    opthash=parseHostlist()
#    if opthash.hlist:

    hostlist = getHostlist_fromOpt()
    if len(hostlist) > 0:
        mylogger.info("hostlist = %s" % ''.join(hostlist))
    else:
        mylogger.error("no hostlist found, abort")
        sys.exit(2)

    #get cmd -m 'one liner', -f 'cmd file'
    opthash=parseCmd()
    command=''
    commandfile=''
    if opthash.cmd:
	mylogger.debug("cmd = %s " % opthash.cmd)
        command = opthash.cmd
    elif opthash.cmdf:
        mylogger.info("cmd file = %s " % opthash.cmdf)
        commandfile = opthash.cmdf
   
    for host_ip in hostlist:
        t=Thread(target=sendcmd,args=(host_ip,command,commandfile))
        t.start() 
#miao
    #sendunlock command"
    pass
    #return result
