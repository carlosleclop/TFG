# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('transitweb', '0015_result'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='adenda',
            field=tinymce.models.HTMLField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='result',
            name='report',
            field=models.CharField(default=datetime.date(2017, 8, 15), max_length=65535),
            preserve_default=False,
        ),
    ]
