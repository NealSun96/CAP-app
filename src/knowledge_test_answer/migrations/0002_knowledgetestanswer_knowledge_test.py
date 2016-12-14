# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge_test', '0003_auto_20161214_0151'),
        ('knowledge_test_answer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='knowledgetestanswer',
            name='knowledge_test',
            field=models.ForeignKey(default=1, to='knowledge_test.KnowledgeTest'),
            preserve_default=False,
        ),
    ]
