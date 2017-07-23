# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('transitweb', '0005_remove_telescope_unnecesaryid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Perception',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('latitude', models.DecimalField(default=0, max_digits=13, decimal_places=10)),
                ('longitude', models.DecimalField(default=0, max_digits=13, decimal_places=10)),
                ('attitude', models.DecimalField(default=0, max_digits=13, decimal_places=10)),
                ('datePrediction', models.DateField(default=django.utils.timezone.now, null=True)),
                ('timePrediction', models.TimeField(default=django.utils.timezone.now, null=True)),
                ('additionalInfo', models.CharField(max_length=4096, null=True)),
                ('occultation', models.ForeignKey(to='transitweb.Occultation')),
                ('telescope', models.ForeignKey(to='transitweb.Telescope')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='occultation',
            name='location',
        ),
        migrations.AddField(
            model_name='occultation',
            name='slug',
            field=models.SlugField(default='a'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userastronomer',
            name='location',
            field=models.ForeignKey(to='transitweb.Location', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userastronomer',
            name='website',
            field=models.URLField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='telescope',
            name='additionalInfo',
            field=models.CharField(max_length=128, null=True),
        ),
    ]
