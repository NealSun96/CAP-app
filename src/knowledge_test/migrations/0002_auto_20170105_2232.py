# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge_test', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='knowledgetest',
            name='level',
            field=models.CharField(max_length=100, choices=[(b'manager', b'manager'), (b'non-manager', b'non-manager'), (b'discarded', b'DISCARDED')]),
            preserve_default=True,
        ),
    ]
