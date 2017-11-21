# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transitweb', '0002_auto_20171021_0942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='additionalInfo',
            field=models.CharField(max_length=65535, null=True),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='latitude',
            field=models.DecimalField(default=0, max_digits=22, decimal_places=18),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='longitude',
            field=models.DecimalField(default=0, max_digits=22, decimal_places=18),
        ),
    ]
