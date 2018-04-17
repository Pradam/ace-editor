from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from editor import function_inspect
from userhandler.models import workspace
from django.core import serializers
import json
# Create your views here.
def index(request):
    context = {}
    if not request.session.has_key("username"):
        return HttpResponseRedirect('/')
    username = request.session["username"]
    workspace_name = request.POST.get('workspace')
    request.session['workspace'] = workspace_name
    request.session['testsuite'] = request.POST.get('testsuite')
    context_dict = {}
    x = function_inspect.get_functions(['editor.PublicAPIInspec','editor.Builtin'])
    x["StationLib"] = ['Connect Client']
    context.update({'sidebar_functions':x})
    file = open("editor/publicapi_context.txt","r") 
    pubapi_context = json.loads(file.read())
    publicapi_context = json.dumps(pubapi_context["PublicAPI"])
    file.close()
    context.update({"publicapi_context":publicapi_context})
    context_dict["publicapi_context"] = json.dumps(pubapi_context["PublicAPI"])
    ws_obj = workspace.objects.filter(username__username=username, name=workspace_name)
    context['ws_obj'] = ws_obj.values()[0]
    context['username'] = username
    context['testsuite'] = request.POST.get('testsuite')
    with open('context_data.txt', 'w') as fileobj:
        json.dump(context, fileobj)
    return render(request, 'editor.html', context)
