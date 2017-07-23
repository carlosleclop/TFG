# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transitweb', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='telescope',
            name='location',
        ),
        migrations.AddField(
            model_name='telescope',
            name='country',
            field=models.CharField(max_length=128, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='telescope',
            name='latitude',
            field=models.DecimalField(default=0, max_digits=13, decimal_places=10),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='telescope',
            name='longitude',
            field=models.DecimalField(default=0, max_digits=13, decimal_places=10),
            preserve_default=True,
        ),
    ]
