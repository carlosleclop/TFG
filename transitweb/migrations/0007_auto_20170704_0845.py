# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transitweb', '0006_auto_20170702_2137'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('additionalInfo', models.CharField(max_length=4096, null=True)),
                ('occultation', models.ForeignKey(to='transitweb.Occultation')),
                ('telescope', models.ForeignKey(to='transitweb.Telescope')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='perception',
            name='occultation',
        ),
        migrations.RemoveField(
            model_name='perception',
            name='telescope',
        ),
        migrations.DeleteModel(
            name='Perception',
        ),
        migrations.AlterField(
            model_name='occultation',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
