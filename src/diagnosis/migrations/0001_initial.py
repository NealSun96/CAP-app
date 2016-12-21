# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('enrollment', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Diagnosis',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('self_diagnosis', models.TextField()),
                ('other_diagnosis', models.TextField()),
                ('completion_date', models.DateTimeField()),
                ('enrollment', models.ForeignKey(to='enrollment.Enrollment')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
