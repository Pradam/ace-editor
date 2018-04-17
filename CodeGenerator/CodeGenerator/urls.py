"""CodeGenerator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from userhandler import views
from editor import views as edit
#from django.urls import path,include

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',views.login,name="Login"),
    url(r'^logout/$', views.logout, name="Logout"),
    url(r'^verifylogin/',views.verifyLogin,name="verifyLogin"),
    url(r'^register/',views.registerUser,name="registerUser"),
    url(r'^savestep', views.savestep, name="savestep"),
    url(r'^generatefile', views.generatefile, name="generatefile"),
    url(r'^workspace/', views.workspace_page, name="workspace"),
    #url(r'^jenkins/', edit.index, name="Index pages"),
    url(r'^editor/', edit.index, name="Index pages"),
    url(r'^createWorkspace', views.createWS, name="Create Ws"),
    url(r'^createTestsuite', views.createTS, name="Create Ts"),
    url(r'^getwslist/', views.getWSList, name="Get Ws List"),
    url(r'^gettslist/', views.getTSList, name="Get Ts List"),
    url(r'^getExecutionData', views.sendExecutionData, name="Send Execution Data"),
    url(r'^postExecutionData', views.receiveExecutionData, name="Receive Execution Data"),
    url(r'^createjob',views.create_job,name="Create Jenkins Job"),
    url(r'^runjob/',views.run_job,name="Run Jenkins Job"),
    url(r'^execute', views.executeJob, name="Execute Jenkins Job"),
    url(r'^stopjob', views.stop_job, name="Stop Jenkins Job"),
]

