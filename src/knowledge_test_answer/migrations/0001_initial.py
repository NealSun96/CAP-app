# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge_test', '0001_initial'),
        ('enrollment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='KnowledgeTestAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answers', models.TextField()),
                ('time_taken', models.FloatField()),
                ('first_score', models.IntegerField()),
                ('final_score', models.IntegerField()),
                ('completion_date', models.DateTimeField()),
                ('enrollment', models.ForeignKey(to='enrollment.Enrollment')),
                ('knowledge_test', models.ForeignKey(to='knowledge_test.KnowledgeTest')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
