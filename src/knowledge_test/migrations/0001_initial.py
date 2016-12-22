# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='KnowledgeTest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level', models.CharField(max_length=100, choices=[(b'teacher', b'trainer'), (b'manager', b'manager'), (b'non-manager', b'non-manager'), (b'discarded', b'DISCARDED')])),
                ('time_span', models.FloatField()),
                ('course', models.ForeignKey(to='course.Course')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
