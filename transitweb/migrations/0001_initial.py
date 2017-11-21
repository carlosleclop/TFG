# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mobile', models.BooleanField(default=False)),
                ('country', models.CharField(max_length=128, null=True)),
                ('latitude', models.DecimalField(default=0, max_digits=13, decimal_places=10)),
                ('longitude', models.DecimalField(default=0, max_digits=13, decimal_places=10)),
                ('additionalInfo', models.CharField(max_length=128, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
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
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.CharField(max_length=255)),
                ('message', models.CharField(max_length=65535, null=True)),
                ('read', models.BooleanField(default=False)),
                ('datetime', models.DateTimeField(auto_now=True)),
                ('receiver', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
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
                ('adenda', tinymce.models.HTMLField(null=True)),
                ('attachedFile', models.FileField(null=True, upload_to=b'')),
                ('attachedImage', models.ImageField(null=True, upload_to=b'')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
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
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('report', models.CharField(max_length=65535)),
                ('adenda', tinymce.models.HTMLField(null=True)),
                ('equipment', models.ForeignKey(to='transitweb.Equipment')),
                ('occultation', models.ForeignKey(to='transitweb.Occultation')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('additionalInfo', models.CharField(max_length=4096, null=True)),
                ('equipment', models.ForeignKey(to='transitweb.Equipment')),
                ('occultation', models.ForeignKey(to='transitweb.Occultation')),
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
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='occultation',
            name='reporter',
            field=models.ForeignKey(to='transitweb.UserAstronomer', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='occultation',
            name='usersGo',
            field=models.ManyToManyField(to='transitweb.UserObserver', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='equipment',
            name='user',
            field=models.ForeignKey(to='transitweb.UserObserver', null=True),
            preserve_default=True,
        ),
    ]
