from django.contrib import admin
from userhandler.models import userinfo, testsuite, workspace

class userinfoAdmin(admin.ModelAdmin):
    model = userinfo
    list_display = ('username', 'password')
    
admin.site.register(userinfo, userinfoAdmin)

class workspaceAdmin(admin.ModelAdmin):
    model = workspace
    list_display = ('username', 'name', 'ip', 'uname', 'passwd', 'path')
    
admin.site.register(workspace, workspaceAdmin)

class testsuiteAdmin(admin.ModelAdmin):
    model = testsuite
    list_display = ('ws', 'testsuitename', 'library', 'keyword', 'variable')
    
admin.site.register(testsuite, testsuiteAdmin)