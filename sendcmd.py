from exalibs import unlock_root,valid_ip
import connect_remote
import sys
from threading import Thread

def unlock_root_by_ip(host1,userid='calixsupport',passwd=''):
	conn1 = connect_remote.RMT_CONN(verbose=1,host=host1,userid=userid,password=passwd,timeout=10,port=22)
	sess1 = conn1.connect_ssh()
	
	if conn1.getSessLogin():
		res,ret=unlock_root(conn1)
		if res and ret.find('password expiry information changed') >=0:
			print "Successfully unlock root for %s !" % host1
		elif res:
			print "unexpected unlock root result = %s " % ret
		else:
			print "unlock_root return failure"
	else:
		print "login to %s failed, abort unlock root for it !" % host1

def sendcmd():
	iplist = sys.argv[1].split(',')
	print iplist
	
	login='calixsupport'
	
	for host_ip in iplist:
		
		if valid_ip(host_ip):
			t=Thread(target=unlock_root_by_ip,args=(host_ip,login))	
			t.start()
		else:
			print "%s is not a valid ip !" % host_ip

if __name__=="__main__":
	optlist= sys.argv
	print optlist
	#sendcmd()
