import argparse
import re,sys
from threading import Thread
from optparser import getHostlist_fromOpt,parseCmd
from util.connect_remote import RMT_CONN
from util.exalibs import sendfile_wlog,sendcmdlist_wlog
from util.exa_conf import get_res_fname
from util.mylog import mylogger
from os.path import basename

def sendcmd(host,cmd,cmdf,savef,username='calixsupport',password=''):
    #get connection
    conn = RMT_CONN(verbose=0,host=host,userid=username,password=password,timeout=10,port=22)
    sess = conn.connect_ssh()
    hostname=conn.get_hostname()

    resf = "" 
    

    #send command
    if conn.getSessLogin():
        if savef == "dflt" or savef == "":
            if len(cmdf)>1:
                resf = host + "_" + basename(cmdf)
            else:
                rest = host
            mylogger.info("res file = %s" % resf)
            resf = get_res_fname(resf)
            
        if len(cmd.split(',')) > 1:
            sendcmdlist_wlog(conn,cmd.split(','),resf)
        elif len(cmd) > 1:
            res,ret = conn.sendcmd(cmd)
            if res:
                mylogger.info("===== %s(%s) =======" % (host,hostname))
                mylogger.info(ret)
        if len(cmdf) > 0:
            
            mylogger.info("cmd file = %s" % cmdf)
            mylogger.info("res file = %s" % resf)
            sendfile_wlog(conn,cmdf,resf)
          
    else:
        mylogger.error("%s is not reachable" % host
)
        return None

    #output result
       

def action():
    mylogger.debug( "###### in sendcmd v2 ########")

#    opthash=parseHostlist()
#    if opthash.hlist:

    hostlist = getHostlist_fromOpt()
    if len(hostlist) > 0:
        mylogger.info("hostlist = %s" % ','.join(hostlist))
    else:
        mylogger.error("no hostlist found, abort")
        sys.exit(2)

    #get cmd -m 'one liner', -f 'cmd file'
    opthash=parseCmd()
    command=''
    commandfile=''
    savefile=''

    if opthash.cmd:
        #mylogger.log(7,"cmd = %s " % opthash.cmd)
        mylogger.debug("cmd = %s " % opthash.cmd)
        command = opthash.cmd
    elif opthash.cmdf:
        mylogger.info("cmd file = %s " % opthash.cmdf)
        commandfile = opthash.cmdf
    elif opthash.save:
        mylogger.debug("save to file argument = %s " %opthash.save)
#        if opthash.save == "dflt":
#            savefile = get_res_fname(
   
    for host_ip in hostlist:
        t=Thread(target=sendcmd,args=(host_ip,command,commandfile,opthash.save))
        t.start() 
#miao
    #sendunlock command"
    pass
    #return result
