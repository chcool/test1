import argparse
import re,sys
from optparser import parseHostlist
from util.mylog import mylogger

def action():
    mylogger.info( "###### in unlock.action v2 ########")
    opthash=parseHostlist()
    if opthash.hlist:
        mylogger.info( "hostlist = %s" % opthash.hlist)
    else:
        mylogger.info( "unlock:action:use -l or --hlist to give a list of host IPs")
        sys.exit(2)
    
#miao
    #sendunlock command"
    pass
    #return result
