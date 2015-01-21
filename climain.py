import argparse
import sys,re
from util.mylog import mylogger,cfg_logging

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a","--act",help="upgrade,sendcmd,unlock")
    
    args,unknown = parser.parse_known_args()
    return args


def parseActionStr(actstr):
    actlist=[]
    act_mod = ''
    act_func = ''

    actlist=actstr.split('.')
    if len(actlist) >= 1:
        act_mod=re.sub(' ','',actlist[0])
    if len(actlist) ==2:
        act_func=re.sub(' ','',actlist[1])

    else:
        pass

    ##print act_func
    return act_mod,act_func

if __name__ == "__main__":
    cfg_logging()
# check action string
    opthash=parseArgs()
    if opthash.act:
        mylogger.info("action string = %s" % opthash.act)
    else:
        mylogger.info("please use -a <action string> or --act=<action string>")
        sys.exit(0)
# call the right package with parameter list
   

    act_mod,act_func=parseActionStr(opthash.act)
    mylogger.debug("module=%s, action=%s"%(act_mod,act_func))

    if len(act_mod) > 0:
        try:
            mod=__import__(act_mod)
        except ImportError as e:
            import traceback
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print("*** print_tb:")
            traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
            print( "*** print_exception:")
            traceback.print_exception(exc_type, exc_value, exc_traceback,
                              limit=2, file=sys.stdout)
            print( "*** print_exc:")
            traceback.print_exc()
            
            mylogger.info("import %s failed"% act_mod)
            mylogger.error("Error details: %s" % str(e))
            sys.exit(2)
    if len(act_func) > 0:
        try:
            func = getattr(mod,act_func)
            func()
        except AttributeError as e:
            mylogger.info("no function with name = %s in %s" % (act_func,act_mod)) 
            import traceback
            traceback.print_exc()
            sys.exit(2)
