import argparse
import re,sys
from threading import Thread
from optparser import getHostlist_fromOpt,parseCmd
from util.connect_remote import RMT_CONN
from util.exalibs import sendfile_wlog,sendcmdlist_wlog
from util.exa_conf import get_res_fname
from util.mylog import mylogger
from os.path import basename

def sendcmd(host,cmd,cmdf,savef,prt,username,password,connectstr):
    #get connection
    #conn = RMT_CONN(verbose=0,host=host,userid=username,password=password,timeout=10)
    ## host,verbose=0,eqptype='EXA',conmode='ssh',userid='root', password='root',timeout=10,port=22,hostname=None
    #connectstr="telnet %s %s" % (host,'10022')
    #connectstr="telnet %s" % (host)
    mylogger.info("connect str = %s" % connectstr)
    conn = RMT_CONN(verbose=0,host=host,userid=username,password=password,timeout=10,connectstr=connectstr)
    sess = conn.connect_node()
    hostname=conn.get_hostname()

    resf = "" 
   
   # print(prt) 

    #send command
    if conn.getSessLogin():
        if savef == "dflt":
            if len(cmdf)>1:
                resf = host + "_" + basename(cmdf)
            else:
                resf = host            
            resf = get_res_fname(resf)
            mylogger.info("res file = %s" % resf)
            
        elif savef is not None:
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
    mylogger.debug( "###### in sendcmd v3 ########")

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
    prt=True

    print(opthash)
    #sys.exit(2)

    if opthash.cmd:
        #mylogger.log(7,"cmd = %s " % opthash.cmd)
        mylogger.debug("cmd = %s " % opthash.cmd)
        command = opthash.cmd
        
    if opthash.cmdf:
        mylogger.info("cmd file = %s " % opthash.cmdf)
        commandfile = opthash.cmdf
    if opthash.savef:
       savefile=opthash.savef
       mylogger.info("save to file argument = %s " %opthash.save)
    elif opthash.save:
        savefile="dflt"
#   
    if opthash.noprt is True:
        prt = False

    userid='calixsupport'
    password=''

    if opthash.user:
        mylogger.info("user Userid = %s" % opthash.user)
        userid=opthash.user

    if opthash.pw:
        mylogger.info("login pw = %s" % opthash.pw)
        password=opthash.pw

    constr='ssh -l '+userid
    port=None

    if opthash.constr:
        constr=opthash.constr 

    if opthash.port:
        port = opthash.port 

    for host_ip in hostlist:
        constr = constr + ' ' + host_ip

        if port:
            constr = constr + ' ' + port 
        
        t=Thread(target=sendcmd,args=(host_ip,command,commandfile,savefile,prt,userid,password,constr))
        t.start() 
#miao
    #sendunlock command"
    pass
    #return result
