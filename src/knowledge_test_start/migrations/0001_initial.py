# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('enrollment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='KnowledgeTestStart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.DateTimeField(null=True, blank=True)),
                ('enrollment', models.ForeignKey(to='enrollment.Enrollment')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
