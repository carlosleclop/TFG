# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('latitude', models.DecimalField(default=0, max_digits=13, decimal_places=10)),
                ('longitude', models.DecimalField(default=0, max_digits=13, decimal_places=10)),
                ('attitude', models.DecimalField(default=0, max_digits=13, decimal_places=10)),
                ('country', models.CharField(max_length=128)),
                ('additionalInfo', models.CharField(max_length=128)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Occultation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datePrediction', models.DateField(default=django.utils.timezone.now)),
                ('timePrediction', models.TimeField(default=django.utils.timezone.now)),
                ('additionalInfo', models.CharField(max_length=128, null=True)),
                ('location', models.ForeignKey(to='transitweb.Location')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Telescope',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mobile', models.BooleanField(default=False)),
                ('unnecesaryID', models.CharField(unique=True, max_length=128)),
                ('additionalInfo', models.CharField(max_length=128)),
                ('location', models.ForeignKey(to='transitweb.Location')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserAstronomer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserObserver',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('website', models.URLField(blank=True)),
                ('location', models.ForeignKey(to='transitweb.Location')),
                ('telescope', models.ForeignKey(to='transitweb.Telescope', null=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='occultation',
            name='usersGo',
            field=models.ManyToManyField(to='transitweb.UserObserver', null=True),
            preserve_default=True,
        ),
    ]
