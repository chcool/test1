import logging
import sys

mylogger = logging.getLogger()

mylogger.setLevel(logging.DEBUG)

def cfg_logging(tostd=1,logname=''):
    stdpri = logging.StreamHandler(sys.stdout)
    stdpri.setLevel(logging.DEBUG)
    #formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')
    formatter = logging.Formatter('%(asctime)s-[%(module)s:%(funcName)s:%(lineno)d] %(message)s')
    stdpri.setFormatter(formatter)
    mylogger.addHandler(stdpri)

