# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('postings', '0005_auto_20161209_0121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posting',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 14, 1, 49, 52, 883789, tzinfo=utc), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='posting',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 14, 1, 49, 52, 883826, tzinfo=utc), auto_now=True),
            preserve_default=True,
        ),
    ]
