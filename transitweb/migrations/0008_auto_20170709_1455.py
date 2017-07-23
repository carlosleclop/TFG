# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transitweb', '0007_auto_20170704_0845'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='occultation',
            name='id',
        ),
        migrations.AlterField(
            model_name='occultation',
            name='slug',
            field=models.SlugField(unique=True, serialize=False, primary_key=True),
        ),
    ]
