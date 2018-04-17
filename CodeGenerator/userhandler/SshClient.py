import paramiko
import select
import subprocess
import os
import re
import socket
import time

class SshClient:
    """
    Provides SSH Login to Remote Node or SCG and starts or stops the tcpdump capture process.
    """
    def __init__(self,**kwargs):
        self.ssh = paramiko.SSHClient()
        self.transport = None
        self.channel = None
        self.sftp = None
        self.server = None
        self.login_type = None
        self.shell_prompt = None
        self.channel_recvbufsize = 1024
        self.channel_select_tout = 5.0
        self.channel_select_max_tout = 1800.0
        self.recvbuf = None
        self.is_pcapclient = False
        self.is_closed = False

    def set_pcap_download_localdir(self,  ldir='/tmp/', filename='tmp.pcap'):
        """
        ldir: Capture file local directory
        """
        #capture file local name
        self.capture_lfile = ldir + '/' + filename
        self.capture_lfile_reset_cmd = '>' + self.capture_lfile

    def capture_pcap_init(self, ldir='/tmp/', rdir='/tmp/', 
            filename='tmp.pcap', intf='lo', capture_filter=None, **kwargs):
        """
        Initializes the parameters to support start and stop of capture process on remote server.
        This method must be called if SshClient needs to be used as PcapClient.

        rdir: Capture file remote directory
        filename: Capture file name without any dir path appended to it
        intf: Capture network interface name on remote server
        capture_filter: filter name for capture process - for e.g., "port 80" to filter http for tcpdump

        Returns:
            None
        """
        self.is_pcapclient = True
        #capture file remote directory
        self.capture_rdir = rdir
        #capture file remote name
        self.capture_rfile = rdir + '/' + filename
        #capture interface name on remote server
        self.capture_intf = intf
        #capture process name
        self.capture_process = r'tcpdump'
        #Build file reset commands
        self.capture_rfile_reset_cmd = '>' + self.capture_rfile
        
        if self.capture_intf != 'any':
            if capture_filter:
                print "Actual capture_filter: %s is replaced with None. Using capture_filter is deprecated" % capture_filter
                capture_filter = None
        else:
            print "Actual capture_filter is being used"

        self.capture_pgrep_cmd = 'sudo pgrep %s' % (self.capture_process)

        if not capture_filter:
            #Build start and stop commands
            #Start command - capture process will run in the background
            self.capture_start_cmd = 'sudo nohup' + ' ' +  self.capture_process +' ' + '-nn' + ' ' + '-i' + ' ' + self.capture_intf + ' ' + '-s0' + ' ' + \
                 '-w' + ' ' + self.capture_rfile + ' ' + '-U -B 8192' + ' ' + '>/dev/null 2>&1' + ' ' + '&'
            self.capture_pkill_regex = r'[ \t]' + '-nn' + r'[ \t]' + '-i' + r'[ \t]' + self.capture_intf +  r'[ \t]' + '-s0' + \
                 r'[ \t]' + '-w' + r'[ \t]' + self.capture_rfile + r".*"
            self.capture_pkill_spattern =  self.capture_process + self.capture_pkill_regex
            self.capture_stop_cmd = 'sudo pkill -SIGINT' + ' ' + '-f' + ' ' + '\"' + self.capture_pkill_spattern + '\"'
            self.capture_force_stop_cmd = 'sudo pkill -SIGKILL' + ' ' + '-f' + ' ' + '\"' + self.capture_pkill_spattern + '\"'
        else:
            #Build start and stop commands
            #Start command - capture process will run in the background
            self.capture_start_cmd = 'sudo nohup' + ' ' + self.capture_process +' ' + '\"' + capture_filter + '\"' + ' ' + \
                 '-nn' + ' ' + '-i' + ' ' + self.capture_intf + ' ' + '-s0' + ' ' + \
                 '-w' + ' ' + self.capture_rfile + ' ' + '-U -B 8192' + ' ' + '>/dev/null 2>&1' + ' ' + '&'
            self.capture_pkill_regex = r'[ \t]' + capture_filter + r'[ \t]' + \
                 '-nn' + r'[ \t]' + '-i' + r'[ \t]' + self.capture_intf +  r'[ \t]' + '-s0' + \
                 r'[ \t]' + '-w' + r'[ \t]' + self.capture_rfile + r".*"
            self.capture_pkill_spattern =  self.capture_process + self.capture_pkill_regex
            self.capture_stop_cmd = 'sudo pkill -SIGINT' + ' ' + '-f' + ' ' + '\"' + self.capture_pkill_spattern + '\"'
            self.capture_force_stop_cmd = 'sudo pkill -SIGKILL' + ' ' + '-f' + ' ' + '\"' + self.capture_pkill_spattern + '\"'

    def _capture_set_cmds(self, login_type=None):
        """
        Builds the command format for capture start and stop commands
        """
        if login_type == "interactive":
            #For interactive mode, append new line to commands
            self.capture_rfile_reset_cmd = self.capture_rfile_reset_cmd + '\n'
            self.capture_start_cmd = self.capture_start_cmd + '\n'
            self.capture_stop_cmd = self.capture_stop_cmd + '\n'
            self.capture_force_stop_cmd = self.capture_force_stop_cmd + '\n'
            self.capture_pgrep_cmd = self.capture_pgrep_cmd + '\n'

    def _start_proc(self, cmd, expected=None, ret_recv_buf=None):
        """
        Starts the process on remote server
        """
        print "SshClient:: Command: %s" % cmd
        try:
            if self.login_type == "interactive":
                shell_prompt = None
                if not expected:
                    shell_prompt = self.shell_prompt
                else:
                    shell_prompt = expected
                #print "SshClient:: send data: %s to channel" % cmd
                self.channel.sendall(cmd)
                print "SshClient:: Tx: %s" % cmd
                is_match = False
                while True:
                    r, w, e = select.select([self.channel], [], [], self.channel_select_tout)
                    if self.channel in r:
                        #print "SshClient:: channel ready to receive data"
                        try:
                            recvbuf = self.channel.recv(self.channel_recvbufsize)
                            #print "SshClient:: Rx: %s" % recvbuf
                            if len(recvbuf) == 0:
                                print "SshClient:: Error: EOF recvd on channel"
                                return False
                            else:
                                self.recvbuf = recvbuf
                                #print "SshClient:: recvd data: %s on channel" % self.recvbuf
                                if not re.search(shell_prompt, self.recvbuf, re.I|re.M):
                                    is_match = False
                                else:
                                    #print """SshClient:: expected shell prompt: %s matches the rcvd data: %s""" % (
                                            #shell_prompt, self.recvbuf)
                                    is_match = True
                                    break
                        except socket.timeout:
                            print "SshClient:: Error: socket recv timeout"
                            return False
                    else:
                        print "SshClient:: _start_proc - select() timedout on read channel"
                        break
                #if not is_match:
                #    print """SshClient:: Error: expected shell prompt: %s did not match 
                #    the rcvd data: %s""" % (shell_prompt, self.recvbuf)
                #    return False
            else:
                stdin, stdout, stderr = self.ssh.exec_command(cmd)
                print "SshClient:: exec_command: stdout: %s   stderr: %s" % (stdout, stderr)
                if expected is not None:
                    for l in stdout :
                        if expected in l.strip():
                            return True
                    return False
     
            if ret_recv_buf:
                return self.recvbuf
            return True
        except Exception, err:
            print "SshClient:: Error: exception - %s" % str(err)
            return False

    def _capture_pkill_process(self):
        """
        Kill capture process using pkill cmd
        
        """
        return self._start_proc(self.capture_stop_cmd)

    def _capture_force_pkill_process(self):
        """
        Kill capture process using pkill cmd
        
        """
        return self._start_proc(self.capture_force_stop_cmd)

    def _capture_pgrep(self):
        """
        pgrep capture process
        
        """
        return self._start_proc(self.capture_pgrep_cmd)

    def _capture_reset_remote_file(self):
        """
        reset the remote capture file
        """
        print "SshClient:: Reset Capture file on server. Cmd: %s" % self.capture_rfile_reset_cmd
        return self._start_proc(self.capture_rfile_reset_cmd)

    def _capture_reset_local_file(self):
        """
        reset the local capture file
        """
        """
        try:
            print "SshClient:: Reset Capture file on localhost. Cmd: %s" % self.capture_lfile_reset_cmd
            process = subprocess.Popen(self.capture_lfile_reset_cmd, shell=True,
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                        close_fds=True, preexec_fn=os.setsid)
            stdout, stderr = process.communicate()
            return True
        except Exception, err:
            print "SshClient:: Error: subprocess exception - %s" % str(err)
            return False
        """
        print "SshClient:: Reset Capture file on localhost. Cmd: %s" % self.capture_lfile_reset_cmd
        os.system(self.capture_lfile_reset_cmd)
        time.sleep(1)
        return True

    def ssh_connect(self, server='127.0.0.1', username='root', password='ruckus', 
             login_type=None, shell_prompt=r"root@\S*#", 
             expect_cmd_list=[[r"root@\S*#", None, 30.0]], 
             expect_regex_opts = re.I|re.M, **kwargs):
        """
        Establishes SSH connection to remote server.
        server: Remote Server IP
        username: Remote username
        password: password for this username
        login_type: None or Interactive. If interactive, then 
            following arguments given by user are considered to make sure that the session enters shell mode.
        expect_cmd_list: It is of format - [expected_prompt, cmd_to_execute, expect_prompt_timeout]
            expected_prompt - This prompt will be compared against the received data from server on ssh channel.
            cmd_to_execute - If a prompt is found, then this command will be sent on channel to server
            expect_prompt_timeout - This is timeout if no data received on ssh channel when waiting for prompt
        expect_regex_opts: regex options to match the expected prompt

        Returns:
            True, if the ssh connection is successful
            False, if the ssh connection is not successful or an exception occurred or a prompt is not found
        """
        try:
            if (not server) or (not username) or (not password):
                print "SshClient:: Error: Invalid param"
                return False
            self.server = server
            self.login_type = login_type
            if self.is_pcapclient:
                self._capture_set_cmds(login_type=login_type)

            print "SshClient:: SSH user login type: %s" % login_type
            print "SshClient:: SSH connecting to server: %s..." % server
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            #self.ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
            self.ssh.connect(server, username=username, password=password)
            print "SshClient:: SSH connection successful to server: %s" % server

            if self.login_type == "interactive":
                if len(expect_cmd_list) <= 0:
                    print "SshClient:: Error: expect_cmd_list is empty"
                    return False
                if not shell_prompt:
                    print "SshClient:: Error: shell_prompt is empty for interactive mode"
                    return False
                self.shell_prompt = shell_prompt #default shell prompt
                self.transport = self.ssh.get_transport()
                self.channel = self.transport.open_session()
                self.channel.get_pty()
                self.channel.invoke_shell()
                #blocking socket for send/recv
                self.channel.setblocking(1) 

                for expect_cmd in expect_cmd_list:
                    if len(expect_cmd) != 3:
                        print "SshClient:: Error: expect or cmd or timeout value is missing"
                        return False

                    self.recvbuf = None
                    is_match = False
                    while True:
                        r, w, e = select.select([self.channel], [], [], float(expect_cmd[2]))
                        if self.channel in r:
                            #print "SshClient:: channel ready to receive data"
                            try:
                                recvbuf = self.channel.recv(self.channel_recvbufsize)
                                if len(recvbuf) == 0:
                                    print "SshClient:: Error: EOF recvd on channel"
                                    return False
                                else:
                                    self.recvbuf = recvbuf
                                    #print "SshClient:: recvd data: %s on channel" % self.recvbuf
                                    if not re.search(expect_cmd[0], self.recvbuf, expect_regex_opts):
                                        is_match = False
                                    else:
                                        is_match = True
                                        print """SshClient:: Expected Data: %s matches 
                                            the rcvd data: %s""" % (expect_cmd[0], self.recvbuf)
                                        if expect_cmd[1]:
                                            print "SshClient:: send data: %s to channel" % (expect_cmd[1]+'\n')
                                            self.channel.sendall(expect_cmd[1] + '\n')
                                        break
                            except socket.timeout:
                                print "SshClient:: Error: socket recv timeout"
                                return False
                        else:
                            print "SshClient:: connect - select() timedout on read channel"
                            break

                    if not is_match:
                        print """SshClient:: Error: Expected Data: %s did not match the rcvd data: %s""" % (
                                expect_cmd[0], self.recvbuf)
                        return False

            return True
        except Exception, err:
            print "SshClient:: Error: exception - %s" % str(err)
            return False

    def ssh_close(self):
        """
        Closes SSH connection to remote
        """
        try:
            if self.login_type == "interactive":
                print "SshClient:: Shutdown ssh channel to server: %s..." % self.server
                self.channel.shutdown(2)
            print "SshClient:: Closing ssh to server: %s..." % self.server
            self.ssh.close()
            #update closed connection state to True
            self.is_closed = True
            return True
        except Exception, err:
            print "SshClient:: Error: exception - %s" % str(err)
            return False

    def capture_start(self):
        """
        Resets remote capture file and starts the capture process on remote server
        """
        try:
            print "SshClient:: Stopping existing capture process on server (if any)..."
            if not self.capture_stop():
                return False
            if not self._capture_reset_remote_file():
                return False
            time.sleep(1)
            if not self._start_proc(self.capture_start_cmd):
                return False
            time.sleep(2)
            return True
        except Exception, err:
            print "SshClient:: Error: exception - %s" % str(err)
            return False

    def capture_stop(self):
        """
        Stops the capture process on remote server
        """
        try:
            ret = self._capture_pkill_process()
            if ret:
                print "Sleep 2 secs after kill process..."
                time.sleep(2)
                ret = self._capture_pgrep()
                ret = self._capture_force_pkill_process()
                print "Sleep 1 secs after force kill process..."
                time.sleep(1)
            return ret
        except Exception, err:
            print "SshClient:: Error: exception - %s" % str(err)
            return False

    def remote_exec_command(self, cmd,expected=None):
        """
        For non-interactive shells, cmd will be executed on remote server
        """
        try:
            return self._start_proc(cmd,expected=expected)
        except Exception, err:
            print "SshClient:: Error: exception - %s" % str(err)
            return False

    def sftp_connect(self):
        """
        sftp connect to remoteA
        Returns:
            True, if the sftp connection is successful
            False, if the sftp connection is not successful
        """
        try:
            if not self.login_type:
                print "SshClient:: Opening sftp to server: %s..." % self.server
                self.sftp = self.ssh.open_sftp()
                return True
            else:
                print "SshClient:: Error: Invalid method for login_type: %s" % self.login_type
                return False
        except Exception, err:
            print "SshClient:: Error: exception - %s" % str(err)
            return False

    def sftp_close(self):
        """
        Closes sftp connection
        """
        try:
            if not self.login_type:
                print "SshClient:: Closing sftp to server: %s..." % self.server
                self.sftp.close()
                return True
            else:
                print "SshClient:: Error: Invalid method for login_type: %s" % self.login_type
                return False
        except Exception, err:
            print "SshClient:: Error: exception - %s" % str(err)
            return False

    def sftp_download(self):
        """
        Downloads the remote capture file to local node using sftp
        """
        try:
            if not self.login_type:
                if not self._capture_reset_local_file():
                    return False
                print """SshClient:: sftp download of remotefile: %s on server: %s 
                    to localfile: %s""" % (self.capture_rfile, self.server, self.capture_lfile)
                self.sftp.get(self.capture_rfile, self.capture_lfile)
                return True
            else:
                print "SshClient:: Error: Invalid method for login_type: %s" % self.login_type
                return False
        except Exception, err:
            print "SshClient:: Error: exception - %s" % str(err)
            return False

    def scp_download(self, toaddr=None, username='root', password='ruckus', expected=None):
        """
        Downloads the remote capture file to local node using scp.
        The scp command will be executed on remote server.

        toaddr: scp to Destination address. i.e., local IP address reachable to remote server
        username: local host username
        password: local host password for this username
        """
        try:
            if (not toaddr) or (not username) or (not password):
                print "SshClient:: Error: Invalid param" 
                return False

            if self.login_type == "interactive":
                if not self._capture_reset_local_file():
                    return False
                shell_prompt = None
                if not expected:
                    shell_prompt = self.shell_prompt
                else:
                    shell_prompt = expected
                #expect following prompts from scp command on remote
                scp_expect = [r"\(yes/no\)\?\s*", r"Password:\s*"]
                scp_cmd = 'scp' + ' ' + self.capture_rfile + ' ' + username + '@' + toaddr + ':' + \
                        self.capture_lfile + '\n'
                print "SshClient:: scp download operation to " + toaddr + " start..."
                print "SshClient:: send data: %s to channel" % scp_cmd
                self.channel.sendall(scp_cmd)

                is_match = False
                is_scp = False
                is_error = False
                self.recvbuf = None
                while True:
                    r, w, e = select.select([self.channel], [], [], self.channel_select_max_tout)
                    if self.channel in r:
                        #print "SshClient:: channel ready to receive data"
                        try:
                            recvbuf = self.channel.recv(self.channel_recvbufsize)
                            if len(recvbuf) == 0:
                                print "SshClient:: Error: EOF recvd on channel"
                                return False
                            else:
                                print "Rx: ", recvbuf
                                self.recvbuf = recvbuf
                                if not re.search(scp_expect[0], self.recvbuf, re.I|re.M):
                                    is_match = False
                                else:
                                    is_match = False
                                    print """SshClient:: Expected Data: %s matches 
                                        the rcvd data: %s""" % (scp_expect[0], self.recvbuf)
                                    print "SshClient:: send data: %s to channel" % ('yes' + '\n')
                                    self.channel.sendall('yes' + '\n')

                                if not re.search(scp_expect[1], self.recvbuf, re.I|re.M):
                                    is_match = False
                                else:
                                    is_match = False
                                    is_scp = True
                                    print """SshClient:: Expected Data: %s matches 
                                    the rcvd data: %s""" % (scp_expect[1], self.recvbuf)
                                    print "SshClient:: send data: %s to channel" % (password + '\n')
                                    self.channel.sendall(password + '\n')
                                if is_scp:
                                    if re.search(shell_prompt, self.recvbuf, re.I|re.M):
                                        print """SshClient:: Expected Data: %s matches 
                                        the rcvd data: %s""" % (shell_prompt, self.recvbuf)
                                        print "SshClient:: scp operation completed"
                                        is_match = True
                                        break
                                    else:
                                        is_match = False
                                        if re.search("Permission denied", self.recvbuf, re.I|re.M):
                                            is_error = True
                                else:
                                    if re.search(shell_prompt, self.recvbuf, re.I|re.M):
                                        break

                        except socket.timeout:
                            print "SshClient:: Error: socket recv timeout"
                            return False
                    else:
                        print "SshClient:: select() timedout on read channel"
                        break
                    
                if not is_match:
                    if is_scp:
                        print """SshClient:: Error: Expected post_scp_prompt: %s did not match 
                        the rcvd data: %s""" % (shell_prompt, self.recvbuf)
                    else:
                        print """SshClient:: Error: Expected Data: %s did not match 
                        the rcvd data: %s""" % (scp_expect[1], self.recvbuf)
                    return False
                else:
                    if is_error:
                        print """SshClient:: Error: Permission denied!"""
                        return False
                    else:
                        return True
            else:
                print "SshClient:: Error: Invalid method for login_type: %s" % self.login_type
                return False
        except Exception, err:
            print "SshClient:: Error: exception - %s" % str(err)
            return False

    #def __del__(self):
    #    if not self.is_closed:
    #        self.ssh_close()

"""
if __name__ == '__main__':
    
    clnt = SshClient()
    clnt.capture_pcap_init(intf='br0', capture_filter='tcp') 
    clnt.set_pcap_download_localdir(ldir='/tmp/'):
    if not clnt.ssh_connect(server="10.1.20.2", username="admin", password="RUCKUS1!",
        login_type="interactive",
        shell_prompt=r"bash\S*#\s*",
        expect_cmd_list=[[r"ruckus>\s*", "en", 15.0], [r"Password:\s*", "RUCKUS1!", 5.0],
            [r"ruckus#\s*", "!v54!", 5.0], [r"bash\S*#\s*", None, 5.0]]): 
            print "ERROR: connect failed"
            quit()

    if not clnt.capture_start():
        print "ERROR: capture_start() failed"
        quit()

    time.sleep(10.0)

    if not clnt.capture_stop():
        print "ERROR: capture_stop() failed"
        quit()

    if not clnt.scp_download(toaddr="172.19.7.85"):
        print "ERROR: scp_download() failed"
        quit()

    #clnt.sftp_connect()
    #clnt.sftp_download()
    #clnt.sftp_close()

    clnt.ssh_close()

if __name__ == '__main__':
        main()
"""
