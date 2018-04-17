import requests
from requests import packages
import json
from pprint import pprint
#import sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning
packages.urllib3.disable_warnings(InsecureRequestWarning)
packages.urllib3.disable_warnings(InsecurePlatformWarning)

class JsonInterface():
    
    def __init__(self, scg_ip="127.0.0.1", port="7443", pubapi_version="v5_0"):
        
        self.__session =  requests.session()
        self.__session.headers.update({'Content-type':'application/json'})
        self.baseurl="https://{ip}:{port}/api/public/{pubapi_version}/".format(ip=scg_ip, port=port, pubapi_version=pubapi_version)
        
    def get_url(self,url):
        
        print "Get URL %s" % url
        print "API: %s"%(self.baseurl+url)
        return self.baseurl+url
    
    def validate_response(self,response,operation,url):
        
        msg = operation+" operation Failed for URL: "+self.get_url(url)+\
                "\nError Message: "+str(response.reason)+"  "+response._content+"\n"
        #sys.stdout.write(msg)
        #sys.exit(0)

        raise Exception(msg)
        
    def get(self,url):
        
        response = self.__session.get(self.get_url(url),verify=False)  
        assert  response.status_code == 200,self.validate_response(response,self.get.__name__,url)
        data = response.json() 
        return data              
    
    def post(self,_url,data):
  
        #_url = _url.replace("/","")      
        url = self.get_url(_url)
        print "Request Body:\n", 
        pprint(data, indent= 2, width=20)
        response = self.__session.post(url,json.dumps(data),verify=False)
        assert  response.status_code  in (200,201,204),self.validate_response(response,'create',_url)
        data = response.json()
        return  data
    
    def put(self,url,data,status_code=204):
        
        url = self.get_url(url)
        print "Request Body:"
        pprint(data, width= 20)
        response = self.__session.put(url, json.dumps(data),verify=False)
        assert response.status_code == status_code, self.validate_response(response, self.put.__name__, url)
        
    def patch(self,url,data):
        
        url = self.get_url(url)
        print "Request Body:"
        pprint(data, width= 20)
        response = self.__session.patch(url,data = json.dumps(data),verify=False)
        assert  response.status_code == 204,self.validate_response(response,self.patch.__name__,url)
    
    def delete(self,url):
        
        response = self.__session.delete(self.get_url(url),verify=False)
        assert  response.status_code  in (200,204),self.validate_response(response,'delete',url)
        
