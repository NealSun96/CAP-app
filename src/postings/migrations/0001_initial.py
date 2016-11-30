# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Posting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b'Title', max_length=200)),
                ('url', models.URLField(default=b'http://youtube.com/', max_length=400)),
                ('timestamp', models.DateTimeField(default=datetime.datetime(2016, 11, 30, 2, 14, 26, 679949, tzinfo=utc), auto_now_add=True)),
                ('updated', models.DateTimeField(default=datetime.datetime(2016, 11, 30, 2, 14, 26, 680004, tzinfo=utc), auto_now=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-updated', '-timestamp'],
            },
            bases=(models.Model,),
        ),
    ]
