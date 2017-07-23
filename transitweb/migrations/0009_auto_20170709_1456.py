# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transitweb', '0008_auto_20170709_1455'),
    ]

    operations = [
        migrations.AddField(
            model_name='occultation',
            name='id',
            field=models.AutoField(default=1, serialize=False, primary_key=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='occultation',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
