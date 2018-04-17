from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect 
from .models import userinfo, testsuite, testcase, workspace
import genfile as gen
import workspace as wks
from log import logging as logg
import json
from jenkins_job import jenkins_job as jenkins


# Create your views here.

def login(request):
    if request.session.has_key("username"):
        return HttpResponseRedirect('/workspace/')
    return render(request,"login.html")

def verifyLogin(request):
    username = request.POST.get('uname','')
    password = request.POST.get('psw','')
    un = userinfo.objects.filter(username=username)
    request.session['username'] = username
    #all_entries = userinfo.objects.all()
    #logg.warning("%s"% all_entries.values_list())
    logg.warning("Username %s" % username)
    return HttpResponseRedirect("/workspace/")
    #return render(request,"dashboard.html")

def logout(request):
   try:
      del request.session['username']
   except:
      pass
   return HttpResponseRedirect('/')

def registerUser(request):
    username = request.POST.get('uname','')
    password = request.POST.get('psw','')
    user = userinfo(username=username, password=password)
    user.save()
    return render(request,"login.html")

def workspace_page(request):
    context = {}
    if not request.session.has_key("username"):
        return HttpResponseRedirect('/')
    username = request.session["username"]
    uid = userinfo.objects.filter(username=username).values_list('id',flat=True)[0]
    #uid = 
    workspace_list = workspace.objects.filter(username__id=uid) 
    context['uid']=uid
    context['workspaces']= workspace_list
    context['username']=request.session["username"]
    return render(request,"workspace.html", context)


def createWS(request):
    context={}
    username = request.session["username"]
    logg.warning("NAME  %s" % request.POST.get('ws_name',''))
    name = request.POST.get('ws_name','')
    path = request.POST.get('ws_path','')
    ip = request.POST.get('ws_ip','')
    uname = request.POST.get('ws_uname','')
    passwd = request.POST.get('ws_passwd','')
    un=userinfo.objects.get(username=username)
    if workspace.objects.filter(name=name).exists():
        logg.warning("Workspace %s exists" % name)
    else:
        logg.warning("Verify login")
        _ws = wks.workspace(ip=ip,uname=uname,passwd=passwd,path=path)
        login_success = _ws.verify_workspace()
        logg.warning("Login  %s" % login_success)
        if login_success:
            wsinfo = workspace(username=un, name=name, ip=ip, path=path, uname=uname, passwd=passwd)
            logg.warning("Username %s" % username)
            wsinfo.save()
    """
    instance = workspace.objects.get(name=name)
    instance.delete()
    """
    context['username']=request.session["username"]
    return JsonResponse(context)

def createTS(request):
    context={}
    username = request.session["username"]
    name = request.POST.get('ts_name','')
    library = request.POST.get('ts_lib','')
    keyword = request.POST.get('ts_key','')
    variable = request.POST.get('ts_var','')
    ws=workspace.objects.get(name=request.GET.get('workspacename'))
    ws_list = workspace.objects.filter(name=request.GET.get('workspacename'))
    path = ws_list.values()[0]["path"]
    ip = ws_list.values()[0]["ip"]
    uname = ws_list.values()[0]["uname"]
    passwd = ws_list.values()[0]["passwd"]
    _ws = wks.workspace(ip=ip,uname=uname,passwd=passwd,path=path)
    if testsuite.objects.filter(testsuitename=name).exists():
        logg.warning("Testsuite %s exists" % name)
    else:
        local_created = _ws.create_local_user_workspace(username=username,workspace=request.GET.get('workspacename'),testsuite=name)
        if local_created: 
            suite_created = _ws.create_testsuite(testsuite_name=name,library=[library],keyword=[keyword],variable=[variable])
        if suite_created: 
            tsinfo = testsuite(ws=ws, testsuitename=name, library=library, keyword=keyword, variable=variable)
            tsinfo.save()
    """
    instance = workspace.objects.get(name=name)
    instance.delete()
    """
    context['username']=request.session["username"]
    return JsonResponse(context)

def getWSList(request):
    context={}
    ws_list = workspace.objects.filter(username__username = request.session["username"]).values_list('name',flat=True)
    context['username']=request.session["username"]
    context.update({'ws_list': list(ws_list)})
    return JsonResponse(context)

def getTSList(request):
    context={}
    ts_list = testsuite.objects.filter(ws__name = request.GET.get('workspacename')).values_list('testsuitename',flat=True)
    context['username']=request.session["username"]
    context.update({'ts_list': list(ts_list)})
    return JsonResponse(context)

#def jenkins(request):
#    return render(request,"jenkins.html")

def generatefile(request):
    context = {}
    logg.warning("Editor %s" % request.POST.get('tc'))
    workspace_name=request.session["workspace"]
    testsuitename=request.session["testsuite"]
    ws_list = workspace.objects.filter(name=workspace_name)
    ts_list = testsuite.objects.filter(testsuitename=testsuitename)
    ws_name = ws_list.values()[0]["name"]
    ws_path = ws_list.values()[0]["path"]
    ws_ip = ws_list.values()[0]["ip"]
    ws_uname = ws_list.values()[0]["uname"]
    ws_passwd = ws_list.values()[0]["passwd"]
    ts_name = ts_list.values()[0]["testsuitename"]
    library = ts_list.values()[0]["library"]
    keyword = ts_list.values()[0]["keyword"]
    variable = ts_list.values()[0]["variable"]
    logg.warning("************* Editor %s" % ts_list.values())
    fil = gen.generate_test_suite_file(teststeps=request.POST.get('tc'),
            ws_name=ws_name,ws_ip=ws_ip,ws_uname=ws_uname,ws_passwd=ws_passwd,
            ts_name=ts_name,library=[library],keyword=[keyword],variable=[variable])

    logg.warning("************* Editor %s" % fil)

    _ws = wks.workspace(ip=ws_ip,uname=ws_uname,passwd=ws_passwd,path=ws_path)
    _ws.copy_testuite_lib_files(ws_ip=ws_ip,ws_uname=ws_uname,
            ws_passwd=ws_passwd,path=ws_path,testsuite_name=ts_name)

    context.update({'object':fil,'status':"success"})
    return JsonResponse(context)
    
def savestep(request):
    context = {}
    logg.warning("Editor %s" % request.POST.get('tstep'))
    context.update({'object':"success",'status':"success"})
    return JsonResponse(context)

execution_data = []
def receiveExecutionData(request):
    context = {}
    data = request.POST.dict()
    execution_data.append(data)
    #logg.warning(execution_data)
    return JsonResponse(context)

def sendExecutionData(request):
    context = {}
    context['status'] = 'fail'
    if len(execution_data) > 0:
        context['execution_data'] = json.dumps(execution_data)
        context['status'] = 'pass'
        del execution_data[:]
    return JsonResponse(context)

def create_job(request):
    context = {}
    jenkins_ip = request.POST.get('jen_ip')
    jenkins_username = request.POST.get('jen_uname')
    jenkins_password = request.POST.get('jen_passwd')
    rwbot_path = request.POST.get('rwbot_path')
    rwbot_target = request.POST.get('rwbot_target')
    feature_name = request.POST.get('feature_name')
    project_name = request.POST.get('project_name')
    
    job_name = project_name + '-' + feature_name
    robot_filename = '$FEATURE_NAME.robot'
    output_path = '$RWBOT_PATH/targets/' + rwbot_target.split('/')[0] + '/targets/' + rwbot_target.split('/')[1] + '/outputs'
    jenkins_handler = jenkins(jenkins_ip,username =jenkins_username,password=jenkins_password)
    jenkins_handler.create_job(job_name,rwbot_path=rwbot_path,feature_name=feature_name,project_name=project_name,rwbot_target=rwbot_target,robot_filename=robot_filename,output_path=output_path)
    jobs = jenkins_handler.get_jobs();
    context['job_name'] = job_name;
    context['status'] = 'PASS' if job_name in [ j['name'] for j in jobs ] else 'FAIL'
    return JsonResponse(context)

def run_job(request):
    context = {}
    
    f = open('userhandler/createzone.robot','r').read()

    context['job_name'] = request.GET.get('job_name')
    context['suite_content'] = f
    return render(request,"execution.html",context)

def executeJob(request):
    context = {}
    execution_data = []
    job_name = request.POST.get('name')

    workspace_name=request.session["workspace"]
    ws_list = workspace.objects.filter(name=workspace_name)
    jenkins_ip = ws_list.values()[0]["ip"]
    jenkins_username = 'jenkins'
    jenkins_password = 'ruckus'

    jenkins_handler = jenkins(jenkins_ip,username =jenkins_username,password=jenkins_password)
    running_jobs = jenkins_handler.get_running_jobs()
    if job_name in running_jobs:
        context['status'] = 'Job Already Running'
    else:
        jenkins_handler.execute_job(job_name)
        status = jenkins_handler.get_job_status(job_name)
        if status != 'ABORTED':
            job_log = jenkins_handler.get_robot_log(job_name)
            context['job_log'] = job_log
        context['status'] = status
    return JsonResponse(context)

def stop_job(request):
    context = {}
    job_name = request.POST.get('name')
 
    workspace_name=request.session["workspace"]
    ws_list = workspace.objects.filter(name=workspace_name)
    jenkins_ip = ws_list.values()[0]["ip"]
    jenkins_username = 'jenkins'
    jenkins_password = 'ruckus'

    jenkins_handler = jenkins(jenkins_ip,username =jenkins_username,password=jenkins_password)
    jenkins_handler.stop_job(job_name)
    return JsonResponse(context)
