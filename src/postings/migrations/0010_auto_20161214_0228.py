# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('postings', '0009_auto_20161214_0217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posting',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 14, 2, 28, 11, 574086, tzinfo=utc), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='posting',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 14, 2, 28, 11, 574122, tzinfo=utc), auto_now=True),
            preserve_default=True,
        ),
    ]
