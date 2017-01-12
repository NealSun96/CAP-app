# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('enrollment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='enrollment',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 12, 3, 10, 18, 18097, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
