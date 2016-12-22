# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge_test', '0001_initial'),
        ('question', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionOrdered',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ordering', models.IntegerField()),
                ('score', models.IntegerField()),
                ('question', models.ForeignKey(to='question.Question')),
                ('test', models.ForeignKey(to='knowledge_test.KnowledgeTest')),
            ],
            options={
                'ordering': ['ordering'],
            },
            bases=(models.Model,),
        ),
    ]
