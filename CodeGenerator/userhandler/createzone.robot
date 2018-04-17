*** Setting ***    

Library           ${ProjectTarget}/libs/python/lib/PublicAPI.py   scg_ip=10.110.219.42  pubapi_version=v5_0
Library            /var/lib/jenkins/perforce/indy_36_jenkins_TE/tools/Rwbot/libs/python/lib/qa/.RWNetgearSwitch.py 
Resource            path.key 
*** Test Case ***
Test Case 1
    session_login   username=admin  password=ruckus1!
    rkszones_create   login_apLoginPassword=ruckus1!  login_apLoginName=admin  name=zone
    ${zone_id}=  get_id_from_name  name=zone
    rkszones_delete  url_id=${zone_id}
