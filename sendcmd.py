import argparse
import re,sys
from threading import Thread
from optparser import getHostlist_fromOpt,parseCmd
from util.connect_remote import RMT_CONN
from util.exalibs import sendfile_wlog,sendcmdlist_wlog
from util.exa_conf import get_res_fname
from util.mylog import mylogger
from os.path import basename

def sendcmd(host,cmd,cmdf,savef,prt,username='calixsupport',password=''):
    #get connection
    conn = RMT_CONN(verbose=0,host=host,userid=username,password=password,timeout=10,port=22)
    sess = conn.connect_node()
    hostname=conn.get_hostname()

    resf = "" 
   
   # print(prt) 

    #send command
    if conn.getSessLogin():
        if savef == "dflt" or savef is None:
            if len(cmdf)>1:
                resf = host + "_" + basename(cmdf)
            else:
                rest = host
            mylogger.info("res file = %s" % resf)
            resf = get_res_fname(resf)
        else:
            resf = savef
            
        if len(cmd.split(',')) > 1:
            sendcmdlist_wlog(conn,cmd.split(','),resf,prt)
        elif len(cmd) > 1:
            #res,ret = conn.sendcmd(cmd)
            res,ret=sendcmdlist_wlog(conn,[cmd],resf,prt)
            if res:
                mylogger.info("===== %s(%s) =======" % (host,hostname))
                mylogger.info(ret)
        if len(cmdf) > 0:
            
            mylogger.info("cmd file = %s" % cmdf)
            mylogger.info("res file = %s" % resf)
            sendfile_wlog(conn,cmdf,resf,prt)
          
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
    savefile=None

    print(opthash)
    #sys.exit(2)

    if opthash.cmd:
        #mylogger.log(7,"cmd = %s " % opthash.cmd)
        mylogger.debug("cmd = %s " % opthash.cmd)
        command = opthash.cmd
        
    if opthash.cmdf:
        mylogger.info("cmd file = %s " % opthash.cmdf)
        commandfile = opthash.cmdf
    if opthash.save:
       savefile=opthash.savef
       mylogger.info("save to file argument = %s " %opthash.save)
#        if opthash.save == "dflt":
#            savefile = get_res_fname(
   
    for host_ip in hostlist:
        t=Thread(target=sendcmd,args=(host_ip,command,commandfile,savefile,opthash.prt))
        t.start() 
#miao
    #sendunlock command"
    pass
    #return result
