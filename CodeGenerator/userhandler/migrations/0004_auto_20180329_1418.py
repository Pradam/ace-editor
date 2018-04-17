# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userhandler', '0003_auto_20180329_1334'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testsuite',
            name='workspace',
        ),
        migrations.AddField(
            model_name='testsuite',
            name='ws',
            field=models.ForeignKey(related_name='ws', default=1, to='userhandler.workspace'),
            preserve_default=False,
        ),
    ]
