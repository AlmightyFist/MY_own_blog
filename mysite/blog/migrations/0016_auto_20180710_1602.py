# Generated by Django 2.0.6 on 2018-07-10 14:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_postcategory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postcategory',
            name='Post',
        ),
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='blog.PostCategory'),
        ),
    ]
