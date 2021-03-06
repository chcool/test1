import pexpect
import re
import sys,os
from time import sleep
from util.exalibs import cleanline,getecrack_py
from util.mylog import mylogger

class RMT_CONN:

    def __init__(self,host,verbose=0,eqptype='EXA',conmode='ssh',userid='root', password='root',timeout=10,port='0',hostname=None,connectstr=None):
            from util.exa_conf import MAX_MORE_LEN, EXPDICT
    
            self.eqptype=eqptype
            self.conmode=conmode
            self.host=host
            self.userid=userid
            self.password=password
            self.verbose=verbose
            self.timeout=int(timeout)
            self.port = port
            self.loggedIn = False
            
            if connectstr is not None:
                self.connectstr=connectstr
            else:
                #self.connectstr = '%s -p %s -l%s %s' % (conmode,port,self.userid,self.host)
                if port == '0':
                    self.connectstr="%s -l %s %s" % (conmode,self.userid,self.host)
                else:
                    self.connectstr="%s -l %s %s %s" % (conmode,self.userid,self.host,port)
            
            
            self.ssh_sess = None
            self.serial_sess = None
            self.session = None
        
            #self.PROMPT_REGEX ='([^\r\n]+)([#|>] )$|(\r\n[\w|\W]+[#|>] )'
            self.PROMPT_REGEX ='([^\r\n]+)([#|>] )$'
            # \0x08 is good so far - 2014.11.24 \0x08 = \b
            #self.PROMPT_REGEX2 = '([\r\n|\x08+][\w|\W]+[#|>] )'
            self.PROMPT_REGEX2 = '([\r\n|\b+][\w|\W]+[#|>] )'
            #self.PROMPT_REGEX2 = '\r\n([\\w|\\W]+[#|>] )'
            self.PROMPT_REGEX3 = '\r\n([^\r\n]+)([#|>] )$' 
            # used for extract prompt,good for calixsupport
            #self.PROMPT_REGEX3 = '\r\n([^\r\n]+[\w]+)([#|>] )$'
            
            self.hostname_REGEX = '\@(.*)\:'
            self.curPrompt=""
            self.hostname=hostname
            self.crackarr=[]
    
            self.MAX_MORE_LEN=MAX_MORE_LEN
            
            
            self.expectList1 = list(EXPDICT.values())
            self.expectKeys = list(EXPDICT.keys())
            self.expectActions = {}
            
            self.reload = 0
            
    def set_loginPrompt(self,prompt):
        #self.PROMPT_REGEX = prompt
        self.expectList1[2]=re.compile(prompt)

    def debug_sess(self,sess):
        #if int(self.verbose) >= 0:
        if 1==1:
            mylogger.debug( "======debug-start================")
            mylogger.debug("sess.maxread = %d" % sess.maxread)
            try:
                mylogger.debug("sess.match =  " + str(sess.match.group(0)))
            except AttributeError as e:
                mylogger.debug("debug_sess except:%s "%str(e))
            mylogger.debug( "=== sess.before:"+str([sess.before]))
            mylogger.debug( "=== sess.after:"+str([sess.after]))
            mylogger.debug( "======debug-end===================")
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
                mylogger.debug( "prompt = " + m.groups()[0])
                self.curPrompt = m.groups()[0]                
            else:
                print( "######## START #################")
                print( "no prompt found in:\r\n" + after)
                print( "######### END ################")
    # def connect_sess(self):
        # loggedIn = False
        # exit_status = False
        
        # if self.conmode.find('telnet')>=0:
            # expectList = self.expectList1        
            # print( "host="+self.host+",port="+str(self.port))
            # self.session = pexpect.spawn('telnet %s %s' % (self.host,self.port))    
    
        # if self.session is None:
            # print( self.conmode+" " + self.host + " " + str(self.port) + " failed, exit")
            # return None
    
        # if int(self.verbose) >= 2:
            # self.session.logfile_read = sys.stdout
            
        # while not exit_status:
            # i = self.session.expect(expectList)
            # if i == 0:
                # self.debug_sess(self.session)
                # print( "\r&&&&&& sent password =", self.password," >>>>>>>>\r")
                # sys.stdout.flush()
                # self.session.send("%s\r" % self.password)                
                # continue
            # elif i == 1:
                # self.session.send("yes\r")
                # continue
            # elif i == 2 or i==7:
            # #elif i ==2:
                # loggedIn = True;
                # exit_status = True;
                # print( "\rgot prompt pattern")
                # self.curPrompt = self.session.after
                # self.debug_sess(self.session)
            # elif i == 3:
                # print( self.host,"ssh got timeout")
                # exit_status = True;
            # elif i == 4:
                # print( "wrong userid/password\r")
                # loggedIn = False;
                # exit_status = True;
            # elif i == 6:
                # print( "\n===== ssh got pexpect.EOF, might be network issue ====\n")
                # exit_status = True;
            # elif i == 9:
                # print( "get IOLAN Escape prompt, send enter")
                # self.session.send("\r")
                # continue
            # else:
                # print( 'unexpected event during ssh: ')
                # print( "got "+str(i)+","+self.session.before)
                # exit_status = True;
                # continue
                
            # if loggedIn:
                # #self.ssh_sess.interact()
                # mylogger.debug( "successfully logged in\n, pexpect.before:\r",self.session.before,"\r-------------\r")
            # else:
                # print( "loggedIn is not True\r")
            
            # self.loggedIn = loggedIn
            # return self.session
       
    def setcrackarr(self,matchstr,pat):
        print(matchstr)
        m=re.match(pat,matchstr)
        if m:
            self.crackarr = m.groups()[0].split()
            if len(self.crackarr) >= 6:
                self.crackarr = self.crackarr[-6:]
            else:
                mylogger.error("crackarr = [%s] length < 6, not right, abort" % ' '.join(self.crackarr))
                return False
            
            
            hn = self.crackarr[0]    
            if self.hostname != None and hn != self.hostname:
                newts=' '.join(self.crackarr[1:])                
                self.password=getecrack_py(hostname=self.hostname,ts=newts)
            else:
                self.password=getecrack_py(host_ts=' '.join(self.crackarr))
            
            return True
        else:
            mylogger.error(" === extract ecrack string seriously wrong, abort !!! ===")
            #exist_status = True
            return False
        #sys.exit(2)
                
    def connect_node(self):
        loggedIn = False
        exit_status = False
        self.ssh_sess = None
        port = 22
        
        expectList = self.expectList1    
        expectKeys = self.expectKeys

        #self.ssh_sess = pexpect.spawn('ssh -p %s -l%s %s' % (port,self.userid,self.host),maxread=4096)   
        mylogger.info("connectstr=%s,userid=%s,password=%s"%(self.connectstr,self.userid,self.password))
        self.ssh_sess = pexpect.spawn(self.connectstr,maxread=4096)    
        #self.ssh_sess.maxread=5120
        
        if int(self.verbose) >= 2:
            self.ssh_sess.logfile_read = sys.stdout
        
        while not exit_status:
            mylogger.debug("============= expect started =============")
            i = self.ssh_sess.expect(expectList)
            mylogger.debug("======== expected key = %s =============" % expectKeys[i])
            
            
            if expectKeys[i].find('crackstr') >=0:
                if self.userid == 'calixsupport':
                    mylogger.debug("key=%s,pat=%s"%(expectKeys[i],expectList[i]))
                    pat=re.compile(expectList[i])
                    #res = self.setcrackarr((self.ssh_sess.after).decode("utf-8"),pat)
                    res = self.setcrackarr((self.ssh_sess.after).decode("utf-8"),pat)
                    if  res is not True:
                        self.exit_status = True
                    else:
                        continue
                continue 
                
            if expectKeys[i] == 'password':
                self.debug_sess(self.ssh_sess)
                
                #the following need to be cleaned later
                if self.userid == 'calixsupport' and (self.password == '' or self.password == 'root'):
                    '''#pat=re.compile("Calix distro \S*\d\.\d*\.\d*\.\d*\S* (.*)\r\n.*")
                    # 2015.1.15 this works with ssh
                    pat=re.compile("Calix distro \S* (.*)\r\n.*")
                    #pat_console=re.compile("Calix [^ ]+ (.*)\r\n.*")
                    
                    
                    m=re.search(pat,(self.ssh_sess.before).decode("utf-8"))
                    if m:
                        mylogger.debug(m.groups())
                        hn = m.groups()[0].split()[0]    
                        if self.hostname != None and hn != self.hostname:
                            print( "<<<<<<<< WARNING: input hostname %s is not equal to login prompt hostname %s>>>>"% (self.hostname,hn))
                            print( "<<<<<<<< possible reason: EXA not fully loaded or user provide incorrect hostname>>>>>")
                        #self.password=self.getecrack_pl(m.groups()[0])
                            newts=' '.join(m.groups()[0].split()[1:])                
                            #newts=self.hostname+' '+newts
                            #self.hostname
                            #newlist[1]=' '.join(m.groups()[0].split()[1:])                
                            #self.password=self.getecrack_pl(newts)
                            self.password=getecrack_py(hostname=self.hostname,ts=newts)
                        #    self.password=getecrack_py(hostname=self.hostname)
                        else:
                                        self.password=getecrack_py(host_ts=m.groups()[0])
                        mylogger.debug( "hostname=%s"%self.hostname)
                    else:
                        mylogger.error( "didn't find crackstr!!!")
                        exit_status = True
                #sys.exit(2)
                else:
                    pass
                    print "self.userid is not calixsupport, it is: "+self.userid
                '''
                mylogger.info( "<<< v4 - sent userid/password = %s/%s >>>" %(self.userid, self.password))
                #sys.stdout.flush()
                #self.ssh_sess.send("%s\r" % self.password.decode("utf-8"))                
                self.ssh_sess.sendline(self.password)
                continue
            
            elif expectKeys[i] == 'login':
                self.debug_sess(self.ssh_sess)
                mylogger.debug("<<<< get login prompt >>")
                self.ssh_sess.sendline(self.userid)
                continue
            elif expectKeys[i] == 'continue':
                self.ssh_sess.send("yes\r")
                continue
            elif expectKeys[i] == 'escape':
                self.ssh_sess.send('\n')
                continue
            elif expectKeys[i] == 'cliprompt' or expectKeys[i] == 'cliprompt2':
            
                loggedIn = True;
                exit_status = True;
                
                self.extract_prompt((self.ssh_sess.after).decode("utf-8"))
                self.set_hostname()
                #self.curPrompt = self.ssh_sess.after
                mylogger.debug( ">> i = %s >>>>got prompt pattern: " % str(i) + self.curPrompt)
                mylogger.debug( "<<<<<< hostname = " + self.hostname)
                self.debug_sess(self.ssh_sess)
                
            
            elif expectKeys[i] == 'timeout':
                print( self.host,"ssh got timeout")
                self.debug_sess(self.ssh_sess)
                exit_status = True;
            
            elif expectKeys[i] == 'logindenied':
                print( "login Denied with userid/password %s/%s!!!\r" % (self.userid,self.password))
                loggedIn = False;
                exit_status = True;
            elif expectKeys[i] == 'portbusy':
                mylogger.error( "=== iolan port busy, please release it, abort !!! ====\n")
                loggedIn = False;
                exit_status = True;
            elif expectKeys[i] == 'eof':
            
                mylogger.error( "\n===== ssh got pexpect.EOF, might be network issue ====\n")
                
                exit_status = True;
            else:
                print( 'unexpected event during ssh: ')
                print( "got "+expectKeys[i]+"="+str(self.ssh_sess.before))
                exit_status = True;
            
        if loggedIn:
            #self.ssh_sess.interact()
            mylogger.debug( "successfully logged in\n, pexpect.before:\r"+str(self.ssh_sess.before)+"\r********************\r")
        else:
            print( "loggedIn is not True\r")
        
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
            # print( "curprompt="+self.curPrompt)
        
    def entLinux(self):
        prompt=self.getCurPrompt()
        if self.curPrompt.find('@') >= 0:
            return
        elif self.curPrompt.find('config') >=0:
            self.sendcmd("exit")
            self.sendcmd("exit")
        else:
            self.sendcmd("exit")
    
    # usd with @exp, to handle unexpected prompt
    # see cmd/HOCH2-ntp-snmp.cmd
    def addMatch(self,matchstring):
        mylogger.debug("~~~~~~ add match pattern %s ~~~~~~~~" % matchstring)
        params=matchstring.split('|')
        
        
        if len(params) >= 1:
            self.expectList1.append(params[0].decode("utf-8"))
            keyidx = len(self.expectList1)
            self.expectKeys.append("tmpkey"+str(keyidx))
            if len(params) >=2:
                
                self.expectActions['tmpkey'+str(keyidx)]=params[1]
        
    # need to add more logic later to sendcmd. 2014.12.8
    
    def sendaction(self,action,sess):
        res = True
        if action.find('ctrl-') >= 0:
                cmdlist=action.strip().split('-')
                if len(cmdlist) > 1:
                    #sess.sendcontrol(cmdlist[1])    
                    sess.send('\x03')
                else:
                    mylogger.error("%s is not a valid command,exit sendcmd" % cmd)
                    res = False
        elif action.find('<return>'):
            sess.sendline()
        else:
            sess.sendline(action)
        return res
        
    def sendcmd(self,cmd,sess=None):
        
        expectList = self.expectList1    
        expectKeys = self.expectKeys
        exit_flag = False
        sent_res = False
        sent_ret = ""
        max_retry = 2
        retry = 0
        timeout=self.timeout
        
        mylogger.debug(expectList)
        mylogger.debug(expectKeys)
        mylogger.debug(str(self.expectActions))
        
        if sess is None:
            sess = self.ssh_sess
            
        if sess and self.loggedIn and len(cmd)>=1:      
            if cmd.find('ctrl-') >= 0:
                cmdlist=cmd.strip().split('-')
                if len(cmdlist) > 1:
                    sess.sendcontrol(cmdlist[1])    
                else:
                    mylogger.error("%s is not a valid command,exit sendcmd" % cmd)
                    exit_flag = True
            else:      
                sess.sendline(cmd)
            while not exit_flag:
                i = sess.expect(expectList,timeout)
                
                if expectKeys[i].find('tmpkey') >= 0:
                    mylogger.debug(" ~~~~~ get tmpkey:%s ~~~~~~~"% (expectKeys[i])) 
                    try:
                        action = self.expectActions[expectKeys[i]]
                        exit_flag = not self.sendaction(action,sess)
                        
                    except (NameError, KeyError) as e:
                        mylogger.debug("no action for %s" % (expectKeys[i])) 
                        mylogger.debug(str(e))
                        exit_flag = True
                    send_res = True
                    sent_ret = sent_ret + (sess.before).decode("utf-8") + (sess.after).decode("utf-8")
                    self.debug_sess(sess)
                    continue
                
                elif expectKeys[i] == 'cliprompt' or expectKeys[i] == 'cliprompt2':
                    mylogger.debug( "<<<< getprompt:%s, retry = %d, cmd= %s >>>>>" %(expectKeys[i],retry,cmd))
                    #exit_flag = True
                    sent_res = True
                    sent_ret = sent_ret + (sess.before).decode("utf-8")
                    self.debug_sess(sess)
                    self.curPrompt = sess.after
                    
					
                    #let it timeout immediately
                    retry = max_retry + 1
                    timeout=1
                    sent_ret = sent_ret + (sess.after).decode("utf-8")
                    
                    #2014.12.03 - figure out why need to always return twice here, in linux prompt, sometimes need to do more expect 
					#otherwise the result want to captured.so always let timeout to exit the loop
                    #exit_flag = Tru
                    continue
                   
                        
                #elif i == 5:
                
                elif expectKeys[i] == 'more':
                    mylogger.debug( "====== get more, send spacebar ==========\r")
                    sent_ret = sent_ret + (sess.before).decode("utf-8")
                    tt_len = str(len(sent_ret))
                    #print "~~~~ send_ret length is : " + tt_len +"\n"
                    if int(tt_len) > int(self.MAX_MORE_LEN):
                        mylogger.warning( ">>>>>>> WARNING: tt_len is max_more_len(%d) reached, send q to quit"% self.MAX_MORE_LEN)
                        self.debug_sess(sess)
                        sess.send('q')
                    else:
                        #sess.send(" ")
                        #sess.send('\040')
                        self.debug_sess(sess)
                        sess.send('\x20')
                elif expectKeys[i] == 'reloadprompt':
                    mylogger.warning("get reload prompt, answer Y will reload the node")
                    sent_res = True
                    exit_flag = True
                    
                    self.debug_sess(sess)
                    sent_ret = sent_ret + (sess.before).decode("utf-8")+(sess.after).decode("utf-8")
                    if self.reload == 1:
                        sess.send('y')
                        exit_flag = False
                        continue
                
                elif expectKeys[i] == 'eof':
                    self.loggedIn = False
                    exit_flag = True
                    send_res = False
                
                #elif i == 3:
                elif expectKeys[i] == 'timeout':
                    mylogger.debug(" timeout,retry = %d " % retry)
                    self.debug_sess(sess)
                    #print " timeout send_ret length is: " + str(len(sent_ret))+"\n" +\
                    #    "SESS.AFTER: "+str(sess.after)+ \
                    #    ";\n SESS.BEFORE: \n"+\
                    #    str(sess.before) +\
                    #    "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"                    
                    sent_ret = sent_ret + (sess.before).decode("utf-8")
                    #self.debug_sess(sess)
                    retry = retry + 1
                    if retry > max_retry:
                        exit_flag = True
                    else:
                        sess.send('\n')
                elif expectKeys[i] == 'escape':
                    mylogger.error( "get Escape in sendcommand, wierd, continue !!!!")
                    pass 
                else:
                    mylogger.error( "get unexpected result = "+ expectKeys[i])
                    self.debug_sess(sess)
                    exit_flag = True
                    sent_res = True
                    sent_ret=str(expectList[i])
        
        return sent_res, sent_ret

    def reconnect(self,wait=30,maxtry=50):
        self.loggedIn = False
        for i in range(0,maxtry):
            mylogger.info("reconnect retry %d"%i)
            self.connect_node()
            if self.loggedIn:
                break
            else:
                sleep(wait)
    
    
    def restart(self):
        mylogger.warning("about to reload the node !!!")
        self.reload = 1
        if self.loggedIn:
            self.sendcmd('reload')
        else:
            mylogger.warning("node is not logged in, abort restart attempt")
    
    def getexplist(self):
        return self.expectList1

    
