# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userhandler', '0002_auto_20180319_1253'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testsuite',
            name='username',
        ),
        migrations.AddField(
            model_name='testsuite',
            name='workspace',
            field=models.ForeignKey(related_name='workspace', default=1, to='userhandler.workspace'),
            preserve_default=False,
        ),
    ]
