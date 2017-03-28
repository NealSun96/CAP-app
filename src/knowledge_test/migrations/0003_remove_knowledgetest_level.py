# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge_test', '0002_auto_20170105_2232'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='knowledgetest',
            name='level',
        ),
    ]
