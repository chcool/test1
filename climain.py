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
    mylogger.info(act_func)

    if len(act_mod) > 0:
        try:
            mod=__import__(act_mod)
        except ImportError as e:
           # type, value, traceback = sys.exc_info()
            mylogger.info("import %s failed"% act_mod)
            mylogger.error("Error details: %s" % str(e))
            sys.exit(2)
    if len(act_func) > 0:
        try:
            func = getattr(mod,act_func)
            func()
        except AttributeError:
            mylogger.info("no function with name = %s in %s" % (act_func,act_mod)) 
            sys.exit(2)
