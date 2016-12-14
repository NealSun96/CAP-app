# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('action_plan', '0002_remove_actionplan_open_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actionplan',
            name='level',
            field=models.CharField(max_length=100, choices=[(b'teacher', b'trainer'), (b'manager', b'manager'), (b'non-manager', b'non-manager'), (b'discarded', b'DISCARDED')]),
            preserve_default=True,
        ),
    ]
