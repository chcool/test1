import pexpect
import re
import sys,os
from exalibs import cleanline,getecrack_py

class RMT_CONN:

	def __init__(self,host,verbose=0,eqptype='EXA',conmode='ssh',userid='root', password='root',timeout=10,port=22,hostname=None):
			from exa_conf import MAX_MORE_LEN
	
			self.eqptype=eqptype
			self.conmode=conmode
			self.host=host
			self.userid=userid
			self.password=password
			self.verbose=verbose
			self.timeout=int(timeout)
			self.port = port
			self.loggedIn = False

			self.ssh_sess = None
			self.serial_sess = None
			self.session = None
		
			#self.PROMPT_REGEX ='([^\r\n]+)([#|>] )$|(\r\n[\w|\W]+[#|>] )'
			self.PROMPT_REGEX ='([^\r\n]+)([#|>] )$'
			self.PROMPT_REGEX2 = '([\r\n|\x08+][\w|\W]+[#|>] )'
			#self.PROMPT_REGEX2 = '\r\n([\w|\W]+[#|>] )'
			self.PROMPT_REGEX3 = '\r\n([^\r\n]+)([#|>] )$' 
			# used for extract prompt,good for calixsupport
			#self.PROMPT_REGEX3 = '\r\n([^\r\n]+[\w]+)([#|>] )$'
			
			self.hostname_REGEX = '\@(.*)\:'
			self.curPrompt=""
			self.hostname=hostname
	
			self.MAX_MORE_LEN=MAX_MORE_LEN
			
			self.expectList1 = [re.escape("""assword:"""),
						  re.escape("""Are you sure you want to continue connecting (yes/no)?"""),
						  re.compile(self.PROMPT_REGEX),
						  pexpect.TIMEOUT,
						  re.escape("ssion denied"),
						  re.compile('(-+More-+)'),
						  pexpect.EOF,
						  re.compile(self.PROMPT_REGEX2),
						  re.escape("""Proceed with reload? [y/N]"""),
						  re.compile('Escape character is ')]

	def set_loginPrompt(self,prompt):
		#self.PROMPT_REGEX = prompt
		self.expectList1[2]=re.compile(prompt)

	def debug_sess(self,sess):
		if int(self.verbose) >= 1:
			print "\r\r======debug-start================\r\r"
			print "\r=== sess.before:",[sess.before]
			print "\r=== sess.after:",[sess.after]
			print "\r\r======debug-end================\r\r"
	
	def set_hostname(self):
		ex=re.compile(self.hostname_REGEX)
		m=re.search(ex,self.curPrompt)
		if m:
			self.hostname = m.groups()[0]
		else:
			self.hostname = self.curPrompt

	def get_hostname(self):
		return self.hostname
			
	def extract_prompt(self,after):
		after =cleanline(after)
		if after:
			ex = re.compile(self.PROMPT_REGEX3)
			m = re.search(ex,after)
			if m:
				print "prompt = " + m.groups()[0]
				self.curPrompt = m.groups()[0]				
			else:
				print "######## START #################"
				print "no prompt found in:\r\n" + after
				print "######### END ################"
	def connect_sess(self):
		loggedIn = False
		exit_status = False
		
		if self.conmode.find('telnet')>=0:
			expectList = self.expectList1		
			print "host="+self.host+",port="+str(self.port)
			self.session = pexpect.spawn('telnet %s %s' % (self.host,self.port))	
	
		if self.session is None:
			print self.conmode+" " + self.host + " " + str(self.port) + " failed, exit"
			return None
	
		if int(self.verbose) >= 2:
			self.session.logfile_read = sys.stdout
			
		while not exit_status:
			i = self.session.expect(expectList)
			if i == 0:
				self.debug_sess(self.session)
				print "\r&&&&&& sent password =", self.password," >>>>>>>>\r"
				sys.stdout.flush()
				self.session.send("%s\r" % self.password)				
				continue
			elif i == 1:
				self.session.send("yes\r")
				continue
			elif i == 2 or i==7:
			#elif i ==2:
				loggedIn = True;
				exit_status = True;
				print "\rgot prompt pattern"
				self.curPrompt = self.session.after
				self.debug_sess(self.session)
			elif i == 3:
				print self.host,"ssh got timeout"
				exit_status = True;
			elif i == 4:
				print "wrong userid/password\r"
				loggedIn = False;
				exit_status = True;
			elif i == 6:
				print "\n===== ssh got pexpect.EOF, might be network issue ====\n"
				exit_status = True;
			elif i == 9:
				print "get IOLAN Escape prompt, send enter"
				self.session.send("\r")
				continue
			else:
				print 'unexpected event during ssh: '
				print "got "+str(i)+","+self.session.before
				exit_status = True;
				continue
				
			if loggedIn:
				#self.ssh_sess.interact()
				print "successfully logged in\n, pexpect.before:\r",self.session.before,"\r-------------\r"
			else:
				print "loggedIn is not True\r"
			
			self.loggedIn = loggedIn
			return self.session
	
	def connect_ssh(self):
		loggedIn = False
		exit_status = False
		self.ssh_sess = None
		port = 22
		
		expectList = self.expectList1		

		self.ssh_sess = pexpect.spawn('ssh -p %s -l%s %s' % (port,self.userid,self.host))	
		self.ssh_sess.maxread=4096
		print "****** maxread = " + str(self.ssh_sess.maxread)
		
		if int(self.verbose) >= 2:
			self.ssh_sess.logfile_read = sys.stdout
		
		while not exit_status:
			i = self.ssh_sess.expect(expectList)
			if i == 0:
				self.debug_sess(self.ssh_sess)
				if self.userid == 'calixsupport' and (self.password == '' or self.password == 'root'):
					pat=re.compile("Calix distro \S*\d\.\d*\.\d*\.\d*\S* (.*)\r\n.*")
					pat=re.compile("Calix distro \S* (.*)\r\n.*")
					m=re.search(pat,self.ssh_sess.before)
					if m:
						print m.groups()
						hn = m.groups()[0].split()[0]	
						if self.hostname != None and hn != self.hostname:
							print "<<<<<<<< WARNING: input hostname %s is not equal to login prompt hostname %s>>>>"% (self.hostname,hn)
							print "<<<<<<<< possible reason: EXA not fully loaded or user provide incorrect hostname>>>>>"
						#self.password=self.getecrack_pl(m.groups()[0])
							newts=' '.join(m.groups()[0].split()[1:])				
							#newts=self.hostname+' '+newts
							#self.hostname
							#newlist[1]=' '.join(m.groups()[0].split()[1:])				
							#self.password=self.getecrack_pl(newts)
							self.password=getecrack_py(hostname=self.hostname,ts=newts)
						#	self.password=getecrack_py(hostname=self.hostname)
						else:
				                        self.password=getecrack_py(host_ts=m.groups()[0])
						print "hostname=%s"%self.hostname
					else:
						print "didn't find crackstr!!!"
				#sys.exit(2)
				else:
					pass
					#print "self.userid is not calixsupport, it is: "+self.userid
				print "\r>>>>>> sent userid/password = %s/%s >>>>>>>>>>>>\r",self.userid, self.password
				sys.stdout.flush()
				self.ssh_sess.send("%s\r" % self.password)				
				continue
			elif i == 1:
				self.ssh_sess.send("yes\r")
				continue
			elif i == 2 or i==7:
			#elif i == 2 :
				loggedIn = True;
				exit_status = True;
				
				self.extract_prompt(self.ssh_sess.after)
				self.set_hostname()
				#self.curPrompt = self.ssh_sess.after
				print "\r>>>>>>got prompt pattern: " + self.curPrompt
				print "\r<<<<<< hostname = " + self.hostname
				self.debug_sess(self.ssh_sess)
			elif i == 3:
				print self.host,"ssh got timeout"
				exit_status = True;
			elif i == 4:
				print "login Denied with userid/password %s/%s!!!\r" % (self.userid,self.password)
				
				
				loggedIn = False;
				exit_status = True;
			elif i == 6:
				print "\n===== ssh got pexpect.EOF, might be network issue ====\n"
				exit_status = True;
			else:
				print 'unexpected event during ssh: '
				print "got "+str(i)+","+self.session.before
				exit_status = True;
			
		if loggedIn:
			#self.ssh_sess.interact()
			print "successfully logged in\n, pexpect.before:\r",self.ssh_sess.before,"\r********************\r"
		else:
			print "loggedIn is not True\r"
		
		self.loggedIn = loggedIn
		return self.ssh_sess

	def getSessLogin(self):
		return self.loggedIn
	
	def getCurPrompt(self):				
		if self.ssh_sess and self.loggedIn:
			self.sendcmd("")
		return self.curPrompt
	
	def entCLI(self):		
		prompt=self.getCurPrompt()
		# if it is currently at linux prompt
		if self.curPrompt.find('@') >= 0:
			self.sendcmd("cli")
			self.sendcmd("en")			
		# if we are in config CLI prompt
		# else:
			# print "curprompt="+self.curPrompt
		
	def entLinux(self):
		prompt=self.getCurPrompt()
		if self.curPrompt.find('@') >= 0:
			return
		elif self.curPrompt.find('config') >=0:
			self.sendcmd("exit")
			self.sendcmd("exit")
		else:
			self.sendcmd("exit")
	
	def addMatch(self,matchstring):
		self.expectList1.append(matchstring)
	
	def sendcmd(self,cmd,sess=None):
		expectList = self.expectList1
		exit_flag = False
		sent_res = False
		sent_ret = ""
		max_retry = 2
		retry = 0
		timeout=self.timeout
		
		if sess is None:
			sess = self.ssh_sess
			
		if sess and self.loggedIn and len(cmd)>1:			
			sess.sendline(cmd)
			while not exit_flag:
				i = sess.expect(expectList,timeout)
				if i == 2 or i == 7:
					#print "<<<< exalib.sendcmd get %d, cmd= %s >>>>>\r" %(i,cmd)
					#exit_flag = True
					sent_res = True
					sent_ret = sent_ret + sess.before
					self.debug_sess(sess)
					self.curPrompt = sess.after
					
					#2014.09.05 - temp test hoch
					retry = max_retry + 1
					sent_ret = sent_ret + sess.after
					timeout=1
					continue
					# if i==7:
						# print "******* get 7, clear out sess.after *****"
						# sent_ret = sent_ret + sess.after
						# sess.expect(expectList,timeout=1)
						
				elif i == 5:
					print "====== get more, send spacebar ==========\r"
					sent_ret = sent_ret + sess.before
					tt_len = str(len(sent_ret))
					#print "~~~~ send_ret length is : " + tt_len +"\n"
					if int(tt_len) > int(self.MAX_MORE_LEN):
						print ">>>>>>> WARNING: tt_len is max_more_len(%d) reached, send q to quit"% self.MAX_MORE_LEN
						self.debug_sess(sess)
						sess.send('q')
					else:
						#sess.send(" ")
						#sess.send('\040')
						self.debug_sess(sess)
						sess.send('\x20')
				# elif i == 7:
					# print "===== get 2nd prompt, exit expect ===="
					# sent_ret = sent_ret + sess.before
					# self.debug_sess(sess)
					# exit_flag = True
				elif i == 3:
					#print " timeout,sess.after="+sess.after+"\r sess.before="+sess.before
					#print " timeout send_ret length is: " + str(len(sent_ret))+"\n" +\
					#	"SESS.AFTER: "+str(sess.after)+ \
					#	";\n SESS.BEFORE: \n"+\
					#	str(sess.before) +\
					#	"\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"					
					sent_ret = sent_ret + sess.before
					#self.debug_sess(sess)
					retry = retry + 1
					if retry > max_retry:
						exit_flag = True
					else:
						sess.send('\n')
				else:
					print "Return, get result = ", expectList[i]
					exit_flag = True
					sent_res = True
					sent_ret=str(expectList[i])
		
		return sent_res, sent_ret

	def getexplist(self):
		return self.expectList1

	# def getecrack_pl(self,crackstr):
		# cmd="perl /home/hochen/prog/perl/ecrack.pl "+crackstr
		# print "in getecrack_pl, cmd = "+cmd
		# str1=os.popen(cmd).read()
		# pat='The password for the default and debug users are: (.*)\n'
		# m=re.search(pat,str1)
		# pw=''
		# if m:
			# pw=m.groups()[0]
		# print "in getecrack_pl, pw = " + pw
		# return pw
