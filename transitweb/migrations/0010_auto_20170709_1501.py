# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transitweb', '0009_auto_20170709_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='occultation',
            name='id',
            field=models.IntegerField(serialize=False, primary_key=True),
        ),
    ]
