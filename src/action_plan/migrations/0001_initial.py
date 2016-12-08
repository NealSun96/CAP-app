# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('course', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActionPlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level', models.CharField(max_length=100, choices=[(b'teacher', b'trainer'), (b'manager', b'manager'), (b'non-manager', b'non-manager')])),
                ('open_date', models.DateTimeField(default=datetime.datetime(2016, 12, 6, 2, 1, 28, 974851))),
                ('action_points', models.TextField()),
                ('course', models.ForeignKey(to='course.Course')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
