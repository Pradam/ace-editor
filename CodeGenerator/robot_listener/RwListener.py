import requests
import requests
import json

class RwListener():
    ROBOT_LISTENER_API_VERSION = 2
    
    def __init__(self, server_ip='172.19.150.113', server_port='8000', post_url='/postExecutionData'):
        self.url = 'http://' + server_ip + ':' + server_port + post_url
        self.current_suite = ''
        self.current_test = ''
        self.current_keyword = ''
        self.failures = []

    def start_suite(self,name,args):
        self.current_suite = name
        message = {'type':'SUITE_STARTED','suite':name}
        requests.post(self.url,message)

    def end_suite(self,name,args):
        self.current_suite = ''
        message = {'type':'SUITE_ENDED','status':args['status'],'suite':name,'error':args['message'],'statistics':args['statistics']}
        requests.post(self.url,message)

    def start_test(self,name,args):
        self.current_test = name
        message = {'type':'TEST_STARTED','test':name}
        requests.post(self.url,message)

    def end_test(self,name,args):
        self.current_test = ''
        message = {'type':'TEST_ENDED','status':args['status'],'suite': self.current_suite,'test':name,'error':args['message']}
        requests.post(self.url,message)
        self.failures.append(message)

    def start_keyword(self,name,args):
        message = {'type':'KEYWORD_STARTED','keyword':name,'test':self.current_test,'suite':self.current_suite}
        requests.post(self.url,message)
        self.current_keyword = name
    
    def end_keyword(self,name,args):
        self.current_keyword = ''
        message = {'type':'KEYWORD_ENDED','status':args['status'],'suite': self.current_suite,'test':self.current_test,'keyword':name}
        requests.post(self.url,message)
        print " keyword: %s status: %s" %(name,args['status'])
        self.failures.append(message)
            
    def close(self):
        message = {'type':'EXECUTION_COMPLETE'}
        requests.post(self.url,message)
        
'''
class RwListener():
    ROBOT_LISTENER_API_VERSION = 2
    
    def __init__(self, server_ip='172.19.18.94', server_port='8000', post_url='/postExecutionData'):
        self.url = 'http://' + server_ip + ':' + server_port + post_url
        self.current_suite = ''
        self.current_test = ''
        self.current_keyword = ''
        self.failures = []

    def start_suite(self,name,args):
        self.current_suite = name

    def end_suite(self,name,args):
        if args['status'] == 'PASS':
            self.current_suite = ''
        if args['status'] == 'FAIL':
            self.current_suite = ''
            message = {'type':'SUITE_FAILURE','suite':name,'error':args['message'],'statistics':args['statistics']}
            requests.post(self.url,message)
            self.failures.append(message)

    def start_test(self,name,args):
        self.current_test = name

    def end_test(self,name,args):
        if args['status'] == 'PASS':
            self.current_test = ''
        if args['status'] == 'FAIL':
            self.current_test = ''
            message = {'type':'TEST_FAILURE','suite': self.current_suite,'test':name,'error':args['message']}
            requests.post(self.url,message)
            self.failures.append(message)

    def start_keyword(self,name,args):
        self.current_keyword = name
    
    def end_keyword(self,name,args):
        if args['status'] == 'PASS':
            self.current_keyword = ''
        if args['status'] == 'FAIL':
            self.current_keyword = ''
            message = {'type':'KEYWORD_FAILURE','suite': self.current_suite,'test':self.current_test,'keyword':name}
            requests.post(self.url,message)
            self.failures.append(message)
            
    def close(self):
        message = {'type':'EXECUTION_COMPLETE'}
        requests.post(self.url,message)
        
'''
