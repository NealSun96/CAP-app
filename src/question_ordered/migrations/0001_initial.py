# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0001_initial'),
        ('assignment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionOrdered',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ordering', models.IntegerField()),
                ('score', models.IntegerField()),
                ('assignment', models.ForeignKey(to='assignment.Assignment')),
                ('question', models.ForeignKey(to='question.Question')),
            ],
            options={
                'ordering': ['ordering'],
            },
            bases=(models.Model,),
        ),
    ]
