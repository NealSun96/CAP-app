# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('postings', '0008_auto_20161214_0214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posting',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 14, 2, 17, 6, 184012, tzinfo=utc), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='posting',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 14, 2, 17, 6, 184066, tzinfo=utc), auto_now=True),
            preserve_default=True,
        ),
    ]
