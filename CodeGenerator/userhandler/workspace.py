from log import logging as logg
import copy
import subprocess
from SshClient import SshClient
import os
import re

serverip=os.environ.get("SERVER_IP","172.19.150.113")

class workspace():
    def __init__(self,ip,uname,passwd,path):
        self.ip = ip
        self.uname=uname
        self.passwd=passwd
        self.path=path

    def verify_workspace(self): 
        clnt = SshClient()
        self.prompt = r"%s\S*\s*" % self.uname
        success = clnt.ssh_connect(server=self.ip, username=self.uname, password=self.passwd,
                login_type="interactive", shell_prompt=self.prompt, expect_cmd_list=[[self.prompt, "cd %s" % self.path, 15.0],[self.prompt, "ls", 5.0],["targets", "\n", 5.0]]) 

        if not success:
            logg.warning("Unable to login to workspace %s" % self.ip)
            return False
        return True

    def create_local_user_workspace(self,username,workspace,testsuite):
        self.local_dir = "/tmp/%s/%s/%s/" % (username,workspace,testsuite)
        if not os.path.isfile(self.local_dir): 
            process = subprocess.Popen("mkdir -p %s" % (self.local_dir), shell=True,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True, preexec_fn=os.setsid)

        return True


    def get_file_and_path(self,filepath,rem_dir):

        copycmd = ""
        for libpath in filepath:
            lp=libpath.split("|")
            path=lp[1]
            libr=lp[0]
            copycmd=copycmd + "cp %s %s;" % (path+libr,rem_dir)

        return copycmd

    def create_testsuite(self,testsuite_name,library,keyword,variable):
        clnt = SshClient()
        lifiles=""
        keyfiles=""
        varfiles=""
        scpcmd=""

        release = "scg_3.6"
        rem_dir="/tmp/" + testsuite_name + "/"

        if len(library) > 0 :
            create_lib_dir="mkdir -p %s" % rem_dir + "lib;"
            lifiles=self.get_file_and_path(library,rem_dir+"lib")
            lifiles=create_lib_dir+lifiles
            scpcmd="scp -r %s root@%s:%s" % (rem_dir+"lib",serverip,self.local_dir)  

        if len(keyword) > 0 : 
            create_key_dir="mkdir -p %s" % rem_dir+"key;"
            keyfiles=self.get_file_and_path(keyword,rem_dir+"key")
            keyfiles=create_key_dir+keyfiles
            scpcmd=scpcmd+"scp -r %s root@%s:%s" % (rem_dir+"key",serverip,self.local_dir)  

        if len(variable) > 0 :
            create_var_dir="mkdir -p %s" % rem_dir+"var;"
            varfiles=self.get_file_and_path(variable,rem_dir+"var")
            varfiles=create_var_dir+varfiles
            scpcmd=scpcmd+"scp -r %s root@%s:%s" % (rem_dir+"var",serverip,self.local_dir)  

        logg.warning("Successfully created commands")
        copycmd=lifiles+keyfiles+varfiles
        scpcmd="scp -o StrictHostKeyChecking=no -r %s root@%s:%s." % (rem_dir,serverip,self.local_dir)
        

        self.prompt = r"%s\S*\s*" % self.uname
        success = clnt.ssh_connect(server=self.ip, username=self.uname, password=self.passwd,
                login_type="interactive", shell_prompt=self.prompt, expect_cmd_list=[[self.prompt, "cd %s" % self.path, 15.0],
                    [self.prompt, "./bin/rwbot create-target %s/%s" %(release,"auto_qa_"+testsuite_name), 10.0],["Done to create a new target", "\n", 5.0],
                    [self.prompt, copycmd, 15.0],[self.prompt, scpcmd, 15.0],["Password", "ruckus", 15.0],[self.prompt, "/n", 15.0]]) 

        if not success:
            logg.warning("Unable to login to workspace %s" % self.ip)
            return False

        return True
    
    def copy_testuite_lib_files(self,ws_ip,ws_uname,ws_passwd,path,testsuite_name):

        logg.warning("copy_testuite_lib_files: %s" % ws_ip)
        clnt = SshClient()
        release = "scg_3.6"
        self.prompt = r"%s\S*\s*" % ws_uname

        remote_dir = path + "/targets/" + release + "/targets/" + "auto_qa_"+testsuite_name 
        scpcmd="scp -o StrictHostKeyChecking=no -r root@%s:%s ." % (serverip,"/root/CodeGenerator/userhandler/"+testsuite_name+".robot")
        scpcmd_lib="scp -o StrictHostKeyChecking=no -r root@%s:%s ." % (serverip,"/root/CodeGenerator/editor/PublicAPI.py")
        scpcmd_json_lib="scp -o StrictHostKeyChecking=no -r root@%s:%s ." % (serverip,"/root/CodeGenerator/editor/JsonInterface.py")
        success = clnt.ssh_connect(server=ws_ip, username=ws_uname, password=ws_passwd,
                login_type="interactive", shell_prompt=self.prompt, expect_cmd_list=[[self.prompt, "cd %s" % remote_dir+"/testsuites", 15.0],
                    [self.prompt, scpcmd, 15.0],
                    ["Password", "ruckus", 15.0],[self.prompt, "/n", 15.0],[self.prompt, "/n", 15.0],
                    [self.prompt, "cd ../libs/python/lib/", 15.0],
                    [self.prompt, scpcmd_lib, 15.0],
                    ["Password", "ruckus", 15.0],[self.prompt, "/n", 15.0],[self.prompt, "/n", 15.0],
                    [self.prompt, scpcmd_json_lib, 15.0],
                    ["Password", "ruckus", 15.0],[self.prompt, "/n", 15.0],[self.prompt, "/n", 15.0]])

if __name__ == '__main__':
    
    ws = workspace(ip="172.19.16.90",uname="jenkins",passwd="ruckus",path="/var/lib/jenkins/perforce/indy_36_jenkins_TE/tools/Rwbot/")
    #ws.create_local_user_workspace(workspace="indy",testsuite="sample")
    #ws.create_testsuite(testsuite_name="sample",library=["RWNetgearSwitch.py | /var/lib/jenkins/perforce/indy_36_jenkins_TE/tools/Rwbot/libs/python/lib/qa/"],keyword=[],variable=[])
    ws.copy_testuite_lib_files(ws_ip="172.19.16.90",ws_uname="jenkins",ws_passwd="ruckus",path="/var/lib/jenkins/perforce/indy_36_jenkins_TE/tools/Rwbot/",testsuite_name="Testsuite")
