# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=250)),
                ('slug', models.SlugField(max_length=250, unique_for_date='publish')),
                ('body_text', models.TextField()),
                ('publish_date', models.DateTimeField(blank=True, null=True)),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(max_length=20, choices=[('draft', 'Roboczy'), ('published', 'Opublikowany')])),
                ('author', models.ForeignKey(related_name='blog_posts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
