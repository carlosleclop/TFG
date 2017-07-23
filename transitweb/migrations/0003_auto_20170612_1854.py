# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transitweb', '0002_auto_20170608_1101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='occultation',
            name='location',
            field=models.ForeignKey(to='transitweb.Location', null=True),
        ),
    ]
