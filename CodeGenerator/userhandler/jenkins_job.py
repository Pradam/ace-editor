import jenkins
import urllib2
import xml.etree.cElementTree as ET
from time import sleep
import json
import os

class jenkins_job():
    def __init__(self,server_ip,server_port='8080',username='jenkins',password='ruckus'):
        
        self.server_ip = server_ip
        self.server_port = server_port
        self.username = username
        self.password = password
        self.jobs = []
        try:
            complete_server_ip = 'http://' + self.server_ip + ':' + self.server_port
            self.server = jenkins.Jenkins(complete_server_ip,username=self.username,password=self.password,timeout=60)
            self.version = self.server.get_version()
        except:
            print "Failed to connect to jenkins server at %s" % complete_server_ip
        else:
            print "Connected to jenkins Server (version=%s)" % self.version
            self.get_jobs()
            path = os.path.dirname(os.path.realpath(__file__)) + '/' + 'default_job_config.xml'
            self.default_job_config = open(path,'r').read()

    def get_jobs(self):
        '''
		updates the internal jobs list with all the exsisting jobs and returns all the jobs that are present on the jenkins server 
		'''
        
        self.jobs = []
        jobs = self.server.get_jobs()
        for job in jobs:
            self.jobs.append({'name': job['fullname'], 'url': job['url']})
        return self.jobs

    def create_empty_job(self, job_name):
        '''
		create a job with empty config 
		'''
        
        self.server.create_job(job_name, jenkins.EMPTY_CONFIG_XML)
        self.get_jobs()

    def create_job(self,job_name,rwbot_path=None,feature_name=None,project_name=None,rwbot_target=None,robot_filename=None,output_path=None):
        ''' 
		create a job with parameters from xml file
		'''
        
        config = ET.fromstring(self.default_job_config)
        if rwbot_path:
            x = config.find('properties/hudson.model.ParametersDefinitionProperty/parameterDefinitions/hudson.model.StringParameterDefinition[name="RWBOT_PATH"]/defaultValue')
            x.text = rwbot_path
        if feature_name:
            x = config.find('properties/hudson.model.ParametersDefinitionProperty/parameterDefinitions/hudson.model.StringParameterDefinition[name="FEATURE_NAME"]/defaultValue')
            x.text = feature_name
        if project_name:
            x = config.find('properties/hudson.model.ParametersDefinitionProperty/parameterDefinitions/hudson.model.StringParameterDefinition[name="PROJECT_NAME"]/defaultValue')
            x.text = project_name
        if rwbot_target:
            x = config.find('properties/hudson.model.ParametersDefinitionProperty/parameterDefinitions/hudson.model.StringParameterDefinition[name="RWBOT_RUN_TARGET"]/defaultValue')
            x.text = rwbot_target
        if robot_filename:
            x = config.find('properties/hudson.model.ParametersDefinitionProperty/parameterDefinitions/hudson.model.StringParameterDefinition[name="ROBOT_FILE_NAME"]/defaultValue')
            x.text = robot_filename
        if output_path:
            x = config.find('properties/hudson.model.ParametersDefinitionProperty/parameterDefinitions/hudson.model.StringParameterDefinition[name="OUTPUT_PATH"]/defaultValue')
            x.text = output_path
        self.server.create_job(job_name, ET.tostring(config))
        self.get_jobs()

    def delete_job(self, job_name):
        '''
		deletes a selected job
		'''
        
        self.server.delete_job(job_name)
        self.get_jobs()

    def clone_job(self, orginal_job, cloned_job):
        '''
		clone one job with another jobs name
		'''
        
        self.server.copy_job(orginal_job, cloned_job)
        self.get_jobs()

    def execute_job(self, job_name, params={"empty":"empty"}):
        '''
		Executes a job on jenkins server
		if the job is parameterized the an addition dictionary must be passed in the format:
			{'param1': 'test value 1', 'param2': 'test value 2'}
		'''
        
        self.server.build_job(job_name,parameters=params)
        
        #wait until the job is triggered 
        while True:
            jobs = [ x['name'] for x in self.server.get_running_builds()]
            if job_name in jobs: 
                break
            sleep(1)

        #wait until the job is complete 
        while True:
            jobs = [ x['name'] for x in self.server.get_running_builds()]
            #print jobs
            if not job_name in jobs:
                break
            sleep(1)

    def get_running_jobs(self):
        jobs = self.server.get_running_builds()
        jobs = [ j['name'] for j in jobs ] 
        return jobs
    
    def stop_job(self,job_name):
        '''
        Stops the previous build of a job
        '''
        running_builds = self.server.get_running_builds()
        build_number = [ j['number']  for j in running_builds if j['name'] == job_name ][0]
        self.server.stop_build(job_name,build_number)
    

    def get_job_status(self,job_name):
        '''
        Returns the status of the previous build
        '''
        
        last_build_number = self.server.get_job_info(job_name)['lastCompletedBuild']['number']
        build_info = self.server.get_build_info(job_name, last_build_number)
        return build_info['result']
        #print json.dumps(build_info ,indent=2)   
		
    def get_robot_log(self,job_name):
        '''
        Returns The Url of robot log of the most latest build
        '''
        
        last_build_number = str(self.server.get_job_info(job_name)['lastCompletedBuild']['number'])
        url = 'http://' + self.server_ip + ':' + self.server_port + '/job' + '/' + job_name + '/' + last_build_number + '/robot/report/log.html'
        return url

    def get_execution_history(self,job_name):
        '''
        Return the Execution History of a given job
        '''
        job_history = {}
        job_details = self.server.get_job_info(job_name)
        job_history.update({'previous_build': job_details['builds'][:-5]})
        job_history.update({'lastStableBuild':job_details['lastStableBuild']})
        job_history.update({'lastUnstableBuild':job_details['lastUnstableBuild']})
        job_history.update({'lastUnsuccessfulBuild': job_details['lastSuccessfulBuild']})
        job_history.update({'lastSuccessfulBuild' : job_details['lastSuccessfulBuild']})
        job_history.update({'lastCompletedBuild' : job_details['lastCompletedBuild']})


if __name__ == "__main__":
    
    #Creating a jenkins object
    j =jenkins_job('172.19.16.113',username='satheesh.kumar',password='ruckus')
    j.get_execution_history('ARC User Role Mapping')

    #creating a job
    #print "Creating job"
    #j.create_job('new-job',rwbot_path='/var/lib/jenkins/vsz_ap_ws_vignesh/tools/Rwbot',feature_name='test',project_name='vscgap',
    #rwbot_target='vscgap_3.6/scg200_qa_ap_regression',robot_filename='test.robot',output_path='$RWBOT_PATH/targets/vscgap_3.6/targets/scg200_qa_ap_regression/outputs')

    #Executing a job
    #print "Executing job"
    #j.execute_job('new-job')

    #Get Build Status
    #print "Build Status : %s" % j.get_job_status('new-job')

    #Get Job Log
    #print "Log : %s" % j.get_robot_log('new-job')

    #Delete Job
    #print "Deleting job"
    #j.delete_job('new-job')
