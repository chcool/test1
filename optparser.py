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
        print "open %s failed" % fname
    except (ValueError, TypeError), e:
        print "%s is not a valid json file" % fname
    return data

def gethostList_fromjson(fname):
    jdata = getjsonData(fname)
    hosts =[]
    try:
        tmphosts=jdata['hosts']
        if type(tmphosts) is list:
            hosts = tmphosts
        elif type(tmphosts) is dict:
            hosts = tmphosts.values()

        else:
            print "type of 'host' is not list nor dict"
    except KeyError:
        print "no 'hosts' in -l file"
        return hosts
    return hosts

def getHostlist_fromOpt():
    opthash = parseHostlist()
    hostlist=[]

    if opthash.hlist:
       for elem in opthash.hlist.split(','):
           if valid_ip(elem):
               hostlist.append(elem) 
	   else:
               tmplist = gethostList_fromjson(elem)
               print tmplist 
               hostlist = hostlist + tmplist
    return hostlist

def parseHostlist():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l","--hlist",help="host list, a comma separated host IP list, or host list file")
    args,unknown = parser.parse_known_args()
    return args

def parseCmd():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m","--cmd",help="command to be sent")
    parser.add_argument("-f","--cmdf",help="command file to be sent")
    args,unknown = parser.parse_known_args()
    return args

def parseCfg():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c","--cfg",help="json config file,not implemented ")
    args,unknown = parser.parse_known_args()
    return args

