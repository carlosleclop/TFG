# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transitweb', '0003_auto_20170612_1854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userobserver',
            name='location',
            field=models.ForeignKey(to='transitweb.Location', null=True),
        ),
        migrations.AlterField(
            model_name='userobserver',
            name='website',
            field=models.URLField(null=True, blank=True),
        ),
    ]
