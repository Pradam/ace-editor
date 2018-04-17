from django.db import models

# Create your models here.

class userinfo(models.Model):
    username = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    def __unicode__(self):
        return "Username: %s"%(self.username) 

class workspace(models.Model):
    username = models.ForeignKey(userinfo,related_name='user')
    name = models.CharField(max_length=128)
    ip = models.CharField(max_length=128)
    path = models.CharField(max_length=128)
    uname = models.CharField(max_length=128)
    passwd = models.CharField(max_length=128)
    def __unicode__(self):
        return "%s, workspace name: %s"%(self.username, self.name)

class testsuite(models.Model):
    ws = models.ForeignKey(workspace,related_name='ws')
    testsuitename = models.CharField(max_length=128)
    library = models.CharField(max_length=128)
    keyword = models.CharField(max_length=128)
    variable = models.CharField(max_length=128)

class testcase(models.Model):
    testcaseid = models.CharField(max_length=10)
    teststeps =  models.CharField(max_length=255)

