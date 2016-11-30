# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('postings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posting',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 30, 2, 14, 40, 428193, tzinfo=utc), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='posting',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 30, 2, 14, 40, 428225, tzinfo=utc), auto_now=True),
            preserve_default=True,
        ),
    ]
