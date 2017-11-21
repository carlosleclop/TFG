# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transitweb', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='latitude',
            field=models.DecimalField(default=0, max_digits=20, decimal_places=16),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='longitude',
            field=models.DecimalField(default=0, max_digits=20, decimal_places=16),
        ),
    ]
