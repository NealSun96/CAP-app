# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('enrollment', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('assignment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answers', models.TextField()),
                ('time_taken', models.FloatField()),
                ('score', models.IntegerField()),
                ('completion_date', models.DateTimeField()),
                ('assignment', models.ForeignKey(to='assignment.Assignment')),
                ('enrollment', models.ForeignKey(to='enrollment.Enrollment')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
