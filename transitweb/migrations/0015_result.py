# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transitweb', '0014_occultation_adenda'),
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('occultation', models.ForeignKey(to='transitweb.Occultation')),
                ('telescope', models.ForeignKey(to='transitweb.Telescope')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
