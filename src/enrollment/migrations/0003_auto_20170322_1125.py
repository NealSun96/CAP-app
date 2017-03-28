# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('enrollment', '0002_enrollment_start_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrollment',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 22, 3, 25, 6, 144998, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
