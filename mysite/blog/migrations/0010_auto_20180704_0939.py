# Generated by Django 2.0.6 on 2018-07-04 07:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20180703_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='PostComment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blog.Post'),
        ),
    ]
