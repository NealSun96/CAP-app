# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('enrollment', '__first__'),
        ('action_plan', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActionPlanAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answers', models.TextField()),
                ('action_plan', models.ForeignKey(to='action_plan.ActionPlan')),
                ('enrollment', models.ForeignKey(to='enrollment.Enrollment')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
