# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('action_plan', '0002_auto_20170105_2232'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='actionplan',
            name='level',
        ),
    ]
