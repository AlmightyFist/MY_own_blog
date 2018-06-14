# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20180613_1211'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='create_date',
            new_name='created',
        ),
        migrations.RemoveField(
            model_name='post',
            name='publish_date',
        ),
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.CharField(max_length=20, default='draft', choices=[('draft', 'Roboczy'), ('published', 'Opublikowany')]),
        ),
    ]
