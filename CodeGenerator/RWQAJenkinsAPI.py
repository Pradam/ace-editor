import sys
from jenkinsapi.jenkins import Jenkins
import optparse
import logging
import time

class RWQAJenkinsAPI:
    
    def __init__(self,jenkins_ip="172.19.16.225", jenkins_port="8080", username="", password=""):
        """Create object for jenkins,
        using IP, port, username and password"""
        
        self.jen_url = 'http://%s:%s' % (jenkins_ip,jenkins_port)
        try:
            self.jen_obj = Jenkins(self.jen_url, username=username, password=password)
        except Exception, e:
            print e
            sys.exit(1)
        
    def run_job(self, job_name=None, build_params=None):
        """Start job execution using job name"""
        
        if not self.jen_obj.has_job(job_name):
            raise Exception("job:\"%s\" does not exist" % (job_name))
        
        job = self.jen_obj[job_name]
        
        if build_params:
            self.run_job_obj = job.invoke(build_params=build_params)
        else:
            self.run_job_obj = job.invoke()

        self.queue_id = self.run_job_obj.queue_id
        return True
    
    def check_job_queued_or_running(self, job_name=None, timeout=10):
        """Wait and check job completion status"""
        
        i = 0
        try:
            self.run_job_obj.block_until_building()
        except TypeError:
            cancelled_data = self.run_job_obj.poll("cancelled")
            if cancelled_data.get("cancelled",False):
                print "Queued job aborted"
                sys.exit(1)
        except Exception,e:
            print e
            sys.exit(1)
            
        self.build_no = self.run_job_obj.get_build_number()
        while i != timeout:
            log.warn("Querying jenkins url: %s  job: %s  Build: %s ..." %(self.jen_url, job_name, self.build_no))
            if self.run_job_obj.is_running():
                log.warn("Jenkins url: %s  job: %s  Build: %s is running" %(self.jen_url, job_name, self.build_no))
            else:
                return True
            
            time.sleep(timeout)
        return False
                    
    def log_build_details(self, job_name=None):
        """Display job details once job completed"""
        
        job = self.jen_obj[job_name]
        timeout = 20
        status = self.check_job_queued_or_running(job_name=job_name, timeout=timeout)
        if status == False:
            raise Exception("timeout [%s] exceeted still job queued or running" % (timeout))
       
        if is_console:
            print "***************************Console Logs***************************************"
            print job.get_build(self.build_no).get_console()
            print "**************************Build Details******************************************"
            
        log.warn("Build Number is %s" % self.build_no)
        
        self.build_status = job.get_build(self.build_no).get_status()
        if self.build_status == "SUCCESS":
            log.warn("Job completed successfully...")  
        else:
            log.error("Job is %s ..."% self.build_status)
            sys.exit(1)
                               
if (__name__ == "__main__"):
                      
    # Define the Options
    parser = optparse.OptionParser()
    parser.add_option("-i", "--jenkins_ip", dest="jenkins_ip_address",
                  help="jenkins server ip address")
    parser.add_option("-p", "--jenkins-port", dest="jenkins_port",
                  help="jenkins server port")
    parser.add_option("-u", "--jenkins-username", dest="jenkins_username",
                  help="jenkins user name")
    parser.add_option("-w", "--jenkins-pssword", dest="jenkins_pass",
                  help="jenkins password")
    parser.add_option("-j", "--jenkins-job", dest="jenkins_job_name",
                  help="jenkins server existing job name")
    parser.add_option("-a", "--build-params", dest="build_params", action="append",
                  help="jenkins job build params, pass multiple key value [-a \"key1=val1\" -a \"key2=val2\"]")
    parser.add_option("-c", "--job-console", dest="job_console", default=False,
                  help="dont display job console details")
    # Parse the Arguments
    (options, args) = parser.parse_args()
    # Exit with Error message, when the required options are missing
    if not options.jenkins_ip_address:
        parser.error("'-i' is required.")
    if not options.jenkins_port:
        parser.error("'-p' is required.")
    if not options.jenkins_job_name:
        parser.error("'-j' is required.")
    if not options.jenkins_username:
        username = ""
    else:
        username = options.jenkins_username
    if not options.jenkins_pass:
        password = ""
    else:
        password = options.jenkins_pass
    if not options.build_params:
        param = None
    else:
        build_params = options.build_params
        param_dict = {}
        for bparam in build_params:
            param_dict.update({bparam.split("=")[0]: bparam.split("=")[1]})
        param = param_dict
              
    jenkins_ip_addr = options.jenkins_ip_address
    jenkins_port = options.jenkins_port
    jenkins_job_name = options.jenkins_job_name
    is_console = options.job_console
    
    #log_filename = jenkins_job_name + '.log'
    log = logging.getLogger("jenking_log")
    handler = logging.StreamHandler()
    handler.setLevel(logging.WARN)
    # create formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    # add formatter to ch
    handler.setFormatter(formatter)
    # add ch to logger
    log.addHandler(handler)
    #fh = logging.FileHandler(log_filename, mode="w")
    #formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')
    #fh.setFormatter(formatter)
    #log.addHandler(fh)
    #log.setLevel(logging.WARN)
            
    log.warn("Jenkins IP Address is [%s]" % jenkins_ip_addr)
    log.warn("Username is [%s]" % username)
    log.warn("Password is [%s]" % password)
    log.warn("Job name to trigger [%s]" % jenkins_job_name)
    
    
        
    jen = RWQAJenkinsAPI(jenkins_ip=jenkins_ip_addr,jenkins_port=jenkins_port,username=username,password=password)
    jen.run_job(job_name=jenkins_job_name, build_params=param)
    jen.log_build_details(job_name=jenkins_job_name)
    sys.exit(0)
        
