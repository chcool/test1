hostmap={}
hostmap['hoch1']='10.243.45.64'
hostmap['hoch2']='10.243.45.63'
hostmap['niagara']='10.243.45.65'
hostmap['niagara-dhcp']='10.243.44.10'
hostmap['havasu']='10.243.45.66'

hostmap['lamborghini']='10.243.46.15'

hostmap['shana1']='10.2.31.151'
hostmap['shana2']='10.2.31.152'
hostmap['shana3']='10.2.31.153'
hostmap['shana4']='10.2.31.154'
hostmap['shana5']='10.2.31.155'
hostmap['shana6']='10.2.31.156'

import json,os
RUN_DIR = os.getcwd()

print( "trying to find exa_conf.json in " + RUN_DIR)
EXA_CONF=RUN_DIR+'/exa_conf.json'
with open(EXA_CONF) as data_file:
	data=json.load(data_file)

cmdfile_base=data["cmdfile_base"]
log_base=data["log_base"]
log_level=int(data["log_level"])

MAX_WAIT=int(data["MAX_WAIT"])
SLEEP_DL=int(data["SLEEP_DL"])
SLEEP_RB=int(data["SLEEP_RB"])

MAX_MORE_LEN=int(data["MAX_MORE_LEN"])
EXPDICT = data['EXPDICT']

from pexpect import EOF as pEOF
from pexpect import TIMEOUT as pTIMEOUT

pexpect_dict = {"timeout":pTIMEOUT,"eof":pEOF}

EXPDICT.update(pexpect_dict)

import time,datetime
ts=time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H%M%S')

import logging

# logging.basicConfig(filename="test.log",level=logging.DEBUG,format="%(asctime)s " \
		# "%(levelname)-5.5s [%(name)s %(module)s:%(funcName)s:%(lineno)d]" \
		# "%(message)s") 

def get_res_fname(prefix):
    global log_base,st
    resultfile = log_base+'/'+prefix+'_'+st+'.log'
    return resultfile


def set_logging(logname):
    global st

#logfile=log_base+logname+st+'.log'
    logging.basicConfig(filename=logname,filemode='w',level=logging.INFO,format="%(asctime)s " \
"%(levelname)-5.5s [%(name)s %(module)s:%(funcName)s:%(lineno)d]" \
"%(message)s") 
    logging.info("in set_logging")
    print(( "<<<<<<<<<<<< in set_logging >>>>> logname = "+logname))

