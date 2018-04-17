# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userhandler', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='testcase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('testcaseid', models.CharField(max_length=10)),
                ('teststeps', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='testsuite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('testsuitename', models.CharField(max_length=128)),
                ('library', models.CharField(max_length=128)),
                ('keyword', models.CharField(max_length=128)),
                ('variable', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='userinfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=128)),
                ('password', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='workspace',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('ip', models.CharField(max_length=128)),
                ('path', models.CharField(max_length=128)),
                ('uname', models.CharField(max_length=128)),
                ('passwd', models.CharField(max_length=128)),
                ('username', models.ForeignKey(related_name='user', to='userhandler.userinfo')),
            ],
        ),
        migrations.DeleteModel(
            name='userhandler',
        ),
        migrations.AddField(
            model_name='testsuite',
            name='username',
            field=models.ForeignKey(related_name='autouser', to='userhandler.userinfo'),
        ),
    ]
