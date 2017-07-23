# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('transitweb', '0012_auto_20170709_1550'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('birth_date', models.DateField(default=django.utils.timezone.now, null=True)),
                ('public', models.BooleanField(default=True)),
                ('website', models.URLField(null=True, blank=True)),
                ('country', models.CharField(max_length=50, null=True, blank=True)),
                ('phone', models.CharField(max_length=30, null=True, blank=True)),
                ('location', models.ForeignKey(to='transitweb.Location', null=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='userastronomer',
            name='location',
        ),
        migrations.RemoveField(
            model_name='userastronomer',
            name='website',
        ),
        migrations.RemoveField(
            model_name='userobserver',
            name='location',
        ),
        migrations.RemoveField(
            model_name='userobserver',
            name='website',
        ),
    ]
