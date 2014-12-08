import argparse
from socket import inet_aton
import json
from util.mylog import mylogger

def valid_ip(str):
    try:
        inet_aton(str)
        return True
    except:
        return False

def getjsonData(fname):
    data = None
    try:
        jdata = open(fname)
        data = json.load(jdata)
    except IOError:
        mylogger.error( ("open %s failed" % fname))
    except (ValueError, TypeError) as e:
        mylogger.error( "%s is not a valid json file !!!" % fname)
    return data

def gethostList_fromjson(fname):
    
    mylogger.info("gethostList_fromjson, fname="+fname)
    jdata = getjsonData(fname)
    if not jdata:
        mylogger.error("jdata is empty, return None")
        return None
    hosts =[]
    try:
        tmphosts=jdata['hosts']
        if type(tmphosts) is list:
            hosts = tmphosts
            #mylogger.log(15,':'.join(hosts))
            #print(len(hosts))
        elif type(tmphosts) is dict:
            hosts = tmphosts.values()

        elif type(tmphosts) is unicode:
            hosts = tmphosts.split(',')
        else:
            mylogger.error( "type of 'host' is %s, not list nor dict" % type(tmphosts))
    except KeyError:
        print( "no 'hosts' in -l file")
        return hosts
    return hosts

def getHostlist_fromOpt():
    opthash = parseHostlist()
    hostlist=[]
    mylogger.info(opthash)
    if opthash.hlist:
       
       for elem in opthash.hlist.split(','):
           #mylogger.info(elem)
           if valid_ip(elem):
               hostlist.append(elem) 
           else:
               tmplist = gethostList_fromjson(elem)
               if tmplist:
                    mylogger.debug( tmplist )
                    hostlist = hostlist + tmplist
    return hostlist

def parseHostlist():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l","--hlist",help="host list, a comma separated host IP list, or host list file")
    args,unknown = parser.parse_known_args()
    return args

#called by sendcmd.py
def parseCmd():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m","--cmd",help="command to be sent")
    parser.add_argument("-f","--cmdf",help="command file to be sent")
    parser.add_argument("-s","--save",help="wether result of send command should be saved to file, dflt means default")
    args,unknown = parser.parse_known_args()
    return args

#2014.11.25 - not called 
def parseCfg():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c","--cfg",help="json config file,not implemented ")
    args,unknown = parser.parse_known_args()
    return args

