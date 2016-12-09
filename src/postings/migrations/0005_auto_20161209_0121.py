# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('postings', '0004_auto_20161206_0201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posting',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 9, 1, 21, 52, 91632, tzinfo=utc), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='posting',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 9, 1, 21, 52, 91668, tzinfo=utc), auto_now=True),
            preserve_default=True,
        ),
    ]
