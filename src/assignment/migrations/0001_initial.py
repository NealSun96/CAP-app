# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ordering', models.IntegerField()),
                ('level', models.CharField(max_length=100, choices=[(b'teacher', b'trainer'), (b'manager', b'manager'), (b'non-manager', b'non-manager')])),
                ('title', models.CharField(max_length=100)),
                ('time_span', models.FloatField()),
                ('total_score', models.IntegerField()),
                ('course', models.ForeignKey(to='course.Course')),
            ],
            options={
                'ordering': ['ordering'],
            },
            bases=(models.Model,),
        ),
    ]
