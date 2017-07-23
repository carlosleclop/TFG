# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transitweb', '0011_remove_occultation_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userobserver',
            name='telescope',
        ),
        migrations.AddField(
            model_name='telescope',
            name='user',
            field=models.ForeignKey(to='transitweb.UserObserver', null=True),
            preserve_default=True,
        ),
    ]
