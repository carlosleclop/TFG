# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('transitweb', '0013_auto_20170709_1645'),
    ]

    operations = [
        migrations.AddField(
            model_name='occultation',
            name='adenda',
            field=tinymce.models.HTMLField(null=True),
            preserve_default=True,
        ),
    ]
