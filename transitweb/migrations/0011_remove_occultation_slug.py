# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transitweb', '0010_auto_20170709_1501'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='occultation',
            name='slug',
        ),
    ]
